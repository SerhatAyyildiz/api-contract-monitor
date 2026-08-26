"""
GÖREVİ: Tespit edilen değişikliği okunabilir bir mesaja çevirip telefona göndermek.

Bildirim Telegram üzerinden gidiyor.

Bu dosya ne yapıyor:
- Fark listesini insanın anlayacağı bir mesaja dönüştürür (kritik/bilgi
  amaçlı bulgular ayrı gruplanır, emoji ile işaretlenir)
- Mesajı Telegram'a gönderir
- Gönderim başarısız olursa sistemin çökmesine izin vermez;
  bildirim gitmese bile kontrol turu tamamlanmış sayılır

Bu dosya ne YAPMIYOR:
- Değişikliği kendisi tespit etmez, hazır listeyi alır (comparator.py'nin işi)
- Neyin bildirime değer olduğuna karar vermez; o kararı main.py verir
- Veritabanına dokunmaz

GÜVENLİK: Telegram anahtarı bu dosyanın içine YAZILMAZ, .env dosyasından
okunur. Ayrıca Telegram'ın adresi anahtarı İÇİNDE taşıdığı için (bkz.
_mesaji_telegram_e_yolla), hiçbir hata mesajı ham haliyle döndürülmez;
_hatayi_temizle() anahtarı gizler.
"""

import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_ADRESI = "https://api.telegram.org/bot{token}/sendMessage"
MESAJ_UZUNLUK_SINIRI = 4096
ISTEK_ZAMAN_ASIMI = 10


def bildirim_mesaji_olustur(api_id, bulgular):
    """Bulgu listesini, kritik/bilgi olarak gruplanmış okunabilir bir Telegram mesajına çevirir."""
    kritikler, bilgiler = _bulgulari_grupla(bulgular)
    emoji = "🔴" if kritikler else "🟡"

    satirlar = [f"{emoji} API Değişikliği: {api_id}", ""]

    if kritikler:
        satirlar.append(f"KRİTİK ({len(kritikler)})")
        satirlar += [f"• {bulgu['details']}" for bulgu in kritikler]
        satirlar.append("")

    if bilgiler:
        satirlar.append(f"BİLGİ ({len(bilgiler)})")
        satirlar += [f"• {bulgu['details']}" for bulgu in bilgiler]
        satirlar.append("")

    satirlar.append(datetime.now().strftime("%d.%m.%Y %H:%M"))

    mesaj = "\n".join(satirlar)
    return _mesaji_kirp(mesaj, len(bulgular))


def bildirim_gonder(api_id, bulgular):
    """Bulgu listesini mesaja çevirip Telegram'a gönderir; hiçbir hatada çökmez."""
    token, chat_id = _ayarlari_oku()
    if not token or not chat_id:
        return _sonuc_olustur(False, "ayar_eksik", "TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik.")

    mesaj = bildirim_mesaji_olustur(api_id, bulgular)
    return _mesaji_telegram_e_yolla(token, chat_id, mesaj)


def _ayarlari_oku():
    """Telegram ayarlarını .env üzerinden okur; eksikse (None, None) döndürür."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return None, None
    return token, chat_id


def _mesaji_telegram_e_yolla(token, chat_id, mesaj):
    """Hazırlanmış mesajı Telegram Bot API'sine gönderir; ağ/API hatalarını yakalar."""
    adres = TELEGRAM_ADRESI.format(token=token)

    try:
        yanit = requests.post(
            adres,
            data={"chat_id": chat_id, "text": mesaj},
            timeout=ISTEK_ZAMAN_ASIMI,
        )
    except requests.exceptions.Timeout:
        return _sonuc_olustur(False, "timeout", "Telegram'dan yanıt beklenen sürede gelmedi.")
    except requests.exceptions.RequestException as hata:
        return _sonuc_olustur(False, "network_error", _hatayi_temizle(str(hata), token))

    if yanit.status_code >= 400:
        hata_metni = _hatayi_temizle(yanit.text, token)
        return _sonuc_olustur(False, "api_error", f"Telegram {yanit.status_code} döndürdü: {hata_metni}")

    return _sonuc_olustur(True, "ok")


def _bulgulari_grupla(bulgular):
    """Bulgu listesini severity alanına göre (kritik, bilgi) iki listeye ayırır."""
    kritikler = [b for b in bulgular if b.get("severity") == "critical"]
    bilgiler = [b for b in bulgular if b.get("severity") == "info"]
    return kritikler, bilgiler


def _mesaji_kirp(mesaj, bulgu_sayisi):
    """Mesaj Telegram'ın uzunluk sınırını aşarsa kırpar, kaç bulgunun gizlendiğini not düşer."""
    if len(mesaj) <= MESAJ_UZUNLUK_SINIRI:
        return mesaj

    not_metni = f"\n\n... ve daha fazlası (toplam {bulgu_sayisi} bulgu)"
    kesme_noktasi = MESAJ_UZUNLUK_SINIRI - len(not_metni)
    return mesaj[:kesme_noktasi] + not_metni


def _hatayi_temizle(metin, token):
    """Bir hata metninde Telegram token'ı geçiyorsa onu '<gizlendi>' ile değiştirir."""
    if token and token in metin:
        return metin.replace(token, "<gizlendi>")
    return metin


def _sonuc_olustur(gonderildi, durum, hata=None):
    """Her gönderim sonucunun aynı yapıda (gonderildi, durum, hata) üretilmesini sağlar."""
    return {"gonderildi": gonderildi, "durum": durum, "hata": hata}


# ---------------------------------------------------------------------------
# GEÇİCİ ELLE-TEST GÖSTERİM BÖLÜMÜ
#
# DİKKAT: Bu bölüm çalıştırılırsa GERÇEKTEN Telegram mesajı gider.
#
# Aşağısı yalnızca bu dosya doğrudan çalıştırıldığında devreye girer. Amacı,
# Hafta 3 Gün 1-2'nin "test mesajı gönder, telefonuna geldiğini doğrula"
# isteğini karşılamak.
# ---------------------------------------------------------------------------

def _gosterim():
    """Örnek bulgularla gerçek bir test mesajı gönderir, sonucu ekrana yazar."""
    ornek_bulgular = [
        {"change_type": "field_removed", "field": "age",
         "details": "age alanı (integer) artık yanıtta yok.", "severity": "critical"},
        {"change_type": "field_added", "field": "email",
         "details": "email alanı (string) yeni eklendi.", "severity": "info"},
    ]

    print("Test mesajı hazırlanıyor ve Telegram'a gönderiliyor...")
    sonuc = bildirim_gonder("gosterim-ornegi", ornek_bulgular)
    print("Sonuç:", sonuc)
    return 0 if sonuc["gonderildi"] else 1


if __name__ == "__main__":
    raise SystemExit(_gosterim())
