"""
GÖREVİ: Verileri kalıcı olarak kaydetmek ve geri okumak.

Kayıtlar data/monitor.db dosyasında tutulacak. Bu dosya bir veritabanıdır
(düzenli kayıt tutan, içinde tablolar bulunan tek bir dosya).

Bu dosya üç tablo yönetiyor:
- schemas : her API için kaydedilen şema geçmişi
- checks  : her kontrol turunun kaydı (durum + yanıt süresi)
- changes : tespit edilen sapmalar

Üçü de dolu; hepsini main.py çağırıyor (Hafta 3, Gün 3-4).

Bu dosya ne YAPMIYOR:
- Veriyi yorumlamaz, sadece saklar ve geri verir
- Şema çıkarmaz (o schema.py'nin işi), API'ye istek atmaz (o fetcher.py'nin işi)

ÖNEMLİ KURAL: Veritabanına dokunan TEK dosya budur.
Başka hiçbir modül doğrudan veritabanına yazmaz veya okumaz.
"""

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Bu dosya src/ klasörünün içinde durduğu için proje kökü bir üst seviyededir.
PROJE_KOKU = Path(__file__).resolve().parent.parent
VARSAYILAN_DB_YOLU = PROJE_KOKU / "data" / "monitor.db"

# Yavaş yanıt tespiti için kaç geçmiş kontrole bakılacağı ve
# kıyas yapılabilmesi için gereken en az kayıt sayısı.
VARSAYILAN_GECMIS_ADEDI = 10
SLOW_RESPONSE_ICIN_ASGARI_KAYIT = 3

# Üç tablo da burada kuruluyor (Bölüm 5.2'deki yapı).
TABLOLARI_OLUSTUR_SORGUSU = """
CREATE TABLE IF NOT EXISTS schemas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id TEXT NOT NULL,
    schema_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id TEXT NOT NULL,
    status TEXT NOT NULL,
    response_time_ms INTEGER,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_id TEXT NOT NULL,
    change_type TEXT NOT NULL,
    details TEXT,
    llm_comment TEXT,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


class DepolamaHatasi(Exception):
    """Veritabanına erişilemediğinde veya bir sorgu başarısız olduğunda kullanılır."""


@contextmanager
def _baglanti_ac(db_yolu):
    """Veritabanı klasörünü hazırlar, bağlantıyı açar ve iş bitince MUTLAKA kapatır.

    NOT: sqlite3.Connection'ın kendi "with" desteği bağlantıyı kapatmaz, yalnızca
    işlemi onaylar/geri alır. Bu yüzden kapatma işi burada elle, finally ile yapılıyor.
    """
    try:
        Path(db_yolu).parent.mkdir(parents=True, exist_ok=True)
        baglanti = sqlite3.connect(db_yolu)
    except (OSError, sqlite3.Error) as hata:
        raise DepolamaHatasi(f"Veritabanına bağlanılamadı ({db_yolu}): {hata}")

    try:
        yield baglanti
        baglanti.commit()
    finally:
        baglanti.close()


def veritabanini_hazirla(db_yolu=VARSAYILAN_DB_YOLU):
    """Üç tabloyu da (schemas, checks, changes) yoksa oluşturur; varsa dokunmaz."""
    with _baglanti_ac(db_yolu) as baglanti:
        try:
            baglanti.executescript(TABLOLARI_OLUSTUR_SORGUSU)
        except sqlite3.Error as hata:
            raise DepolamaHatasi(f"Tablolar oluşturulamadı: {hata}")


def sema_kaydet(api_id, sema, db_yolu=VARSAYILAN_DB_YOLU):
    """Bir API'nin şemasını yeni bir satır olarak ekler; eski kayıtlara dokunmaz (geçmiş korunur)."""
    sema_metni = json.dumps(sema, ensure_ascii=False)
    with _baglanti_ac(db_yolu) as baglanti:
        try:
            baglanti.execute(
                "INSERT INTO schemas (api_id, schema_json) VALUES (?, ?)",
                (api_id, sema_metni),
            )
        except sqlite3.Error as hata:
            raise DepolamaHatasi(f"Şema kaydedilemedi (api_id={api_id}): {hata}")


def son_semayi_oku(api_id, db_yolu=VARSAYILAN_DB_YOLU):
    """O API için en son kaydedilen şemayı döndürür; hiç kayıt yoksa None döndürür (hata değildir)."""
    with _baglanti_ac(db_yolu) as baglanti:
        try:
            satir = baglanti.execute(
                "SELECT schema_json FROM schemas WHERE api_id = ? "
                "ORDER BY id DESC LIMIT 1",
                (api_id,),
            ).fetchone()
        except sqlite3.Error as hata:
            raise DepolamaHatasi(f"Şema okunamadı (api_id={api_id}): {hata}")

    if satir is None:
        return None
    return json.loads(satir[0])


def kontrol_kaydet(api_id, status, response_time_ms, db_yolu=VARSAYILAN_DB_YOLU):
    """Bir kontrol turunun sonucunu (durum + yanıt süresi) checks tablosuna yeni satır olarak ekler."""
    with _baglanti_ac(db_yolu) as baglanti:
        try:
            baglanti.execute(
                "INSERT INTO checks (api_id, status, response_time_ms) VALUES (?, ?, ?)",
                (api_id, status, response_time_ms),
            )
        except sqlite3.Error as hata:
            raise DepolamaHatasi(f"Kontrol kaydedilemedi (api_id={api_id}): {hata}")


def degisiklikleri_kaydet(api_id, bulgular, db_yolu=VARSAYILAN_DB_YOLU):
    """Bulgu listesindeki her değişikliği changes tablosuna, tek bağlantıda, ayrı satır olarak ekler."""
    if not bulgular:
        return

    with _baglanti_ac(db_yolu) as baglanti:
        try:
            baglanti.executemany(
                "INSERT INTO changes (api_id, change_type, details) VALUES (?, ?, ?)",
                [(api_id, bulgu["change_type"], bulgu["details"]) for bulgu in bulgular],
            )
        except sqlite3.Error as hata:
            raise DepolamaHatasi(f"Değişiklikler kaydedilemedi (api_id={api_id}): {hata}")


def ortalama_yanit_suresini_oku(api_id, adet=VARSAYILAN_GECMIS_ADEDI, db_yolu=VARSAYILAN_DB_YOLU):
    """Son N başarılı kontrolün ortalama yanıt süresini döndürür; yeterli geçmiş yoksa None döndürür."""
    with _baglanti_ac(db_yolu) as baglanti:
        try:
            sureler = _gecmis_yanit_surelerini_getir(baglanti, api_id, adet)
        except sqlite3.Error as hata:
            raise DepolamaHatasi(f"Geçmiş yanıt süreleri okunamadı (api_id={api_id}): {hata}")

    if len(sureler) < SLOW_RESPONSE_ICIN_ASGARI_KAYIT:
        return None
    return int(sum(sureler) / len(sureler))


def _gecmis_yanit_surelerini_getir(baglanti, api_id, adet):
    """Yalnızca başarılı (status='ok') kontrollerin son N yanıt süresini veritabanından çeker."""
    satirlar = baglanti.execute(
        "SELECT response_time_ms FROM checks WHERE api_id = ? AND status = 'ok' "
        "AND response_time_ms IS NOT NULL ORDER BY id DESC LIMIT ?",
        (api_id, adet),
    ).fetchall()
    return [satir[0] for satir in satirlar]


# ---------------------------------------------------------------------------
# GEÇİCİ ELLE-TEST GÖSTERİM BÖLÜMÜ
#
# Aşağısı yalnızca bu dosya doğrudan çalıştırıldığında devreye girer. Amacı,
# Hafta 2 Gün 3-4'ün depolama katmanını elle doğrulamak. Otomatik testler
# Hafta 2 Gün 5-7'de comparator ile birlikte yazılacak.
# ---------------------------------------------------------------------------

def _gosterim():
    """Veritabanını hazırlar, örnek bir şema kaydedip geri okur, sonucu ekrana yazar."""
    veritabanini_hazirla()
    print(f"Veritabanı hazır: {VARSAYILAN_DB_YOLU}")

    ornek_sema = {"id": "integer", "login": "string", "plan": {"space": "integer"}}
    sema_kaydet("gosterim-ornegi", ornek_sema)
    print("Örnek şema kaydedildi.")

    okunan = son_semayi_oku("gosterim-ornegi")
    print("Geri okunan şema:", json.dumps(okunan, ensure_ascii=False))

    bos_sonuc = son_semayi_oku("hic-kaydi-olmayan-api")
    print("Kaydı olmayan API için sonuç:", bos_sonuc)
    return 0


if __name__ == "__main__":
    raise SystemExit(_gosterim())
