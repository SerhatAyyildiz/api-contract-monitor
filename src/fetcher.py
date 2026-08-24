"""
GÖREVİ: İzlenecek API'ye internet üzerinden istek atmak.

Bu dosya ne yapıyor:
- config/apis.json içindeki adrese bir istek gönderir
- Dönen yanıtı ve yanıtın kaç milisaniyede geldiğini geri verir
- İnternet kopması, zaman aşımı, hata kodu gibi durumları yakalar

Bu dosya ne YAPMIYOR:
- Yanıtın içeriğini yorumlamaz (o schema.py'nin işi)
- Hiçbir şeyi veritabanına kaydetmez (o storage.py'nin işi)
- Bildirim göndermez (o notifier.py'nin işi)
"""

import json
import time
from pathlib import Path

import requests


# Bu dosya src/ klasörünün içinde durduğu için proje kökü bir üst seviyededir.
# Böylece hangi klasörden çalıştırılırsa çalıştırılsın config dosyası bulunur.
PROJE_KOKU = Path(__file__).resolve().parent.parent
VARSAYILAN_CONFIG_YOLU = PROJE_KOKU / "config" / "apis.json"

# Bir API tanımında mutlaka dolu olması gereken alanlar.
ZORUNLU_ALANLAR = ("id", "url", "method")

# Config'de belirtilmemişse kullanılacak varsayılan değerler.
VARSAYILAN_METHOD = "GET"
VARSAYILAN_TIMEOUT = 10


class YapilandirmaHatasi(Exception):
    """Config dosyası okunamadığında veya içeriği geçersiz olduğunda kullanılır."""


def api_listesini_oku(config_yolu=VARSAYILAN_CONFIG_YOLU):
    """Config dosyasını okur, doğrular ve içindeki API tanımlarının listesini döndürür."""
    icerik = _config_dosyasini_oku(config_yolu)
    veri = _json_ayristir(icerik, config_yolu)

    api_listesi = veri.get("apis")
    if not isinstance(api_listesi, list):
        raise YapilandirmaHatasi(
            f"Yapılandırma dosyasında 'apis' adlı bir liste bulunamadı: {config_yolu}"
        )

    for api_tanimi in api_listesi:
        _api_tanimini_dogrula(api_tanimi)

    return api_listesi


def _config_dosyasini_oku(config_yolu):
    """Config dosyasının ham metnini okur; dosya yoksa veya açılamıyorsa anlaşılır hata verir."""
    try:
        return Path(config_yolu).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise YapilandirmaHatasi(f"Yapılandırma dosyası bulunamadı: {config_yolu}")
    except OSError as hata:
        raise YapilandirmaHatasi(f"Yapılandırma dosyası okunamadı: {hata}")


def _json_ayristir(icerik, config_yolu):
    """Config metnini JSON olarak çözer; bozuksa hangi dosyanın bozuk olduğunu söyler."""
    try:
        return json.loads(icerik)
    except json.JSONDecodeError as hata:
        raise YapilandirmaHatasi(
            f"Yapılandırma dosyası geçerli bir JSON değil ({config_yolu}): {hata}"
        )


def _api_tanimini_dogrula(api_tanimi):
    """Tek bir API tanımında zorunlu alanların dolu olduğunu kontrol eder."""
    if not isinstance(api_tanimi, dict):
        raise YapilandirmaHatasi("Her API tanımı bir nesne (süslü parantezli blok) olmalıdır.")

    eksik_alanlar = [alan for alan in ZORUNLU_ALANLAR if not api_tanimi.get(alan)]
    if eksik_alanlar:
        raise YapilandirmaHatasi(
            f"API tanımında eksik alan var: {', '.join(eksik_alanlar)} -> {api_tanimi}"
        )


def etkin_apileri_sec(api_listesi):
    """Listedeki API'lerden yalnızca izlenmesi açık olanları döndürür."""
    return [api_tanimi for api_tanimi in api_listesi if api_tanimi.get("enabled", True)]


def veri_cek(api_tanimi):
    """Verilen API'ye istek atar; yanıtı, durum kodunu ve geçen süreyi tek bir sonuçta döndürür."""
    baslangic = time.perf_counter()

    try:
        yanit = requests.request(
            method=api_tanimi.get("method", VARSAYILAN_METHOD),
            url=api_tanimi["url"],
            headers=api_tanimi.get("headers") or {},
            timeout=api_tanimi.get("timeout", VARSAYILAN_TIMEOUT),
        )
    except requests.exceptions.Timeout:
        return _sonuc_olustur(
            api_tanimi, "timeout", _gecen_sure_ms(baslangic),
            hata="Yanıt beklenen sürede gelmedi.",
        )
    except requests.exceptions.RequestException as hata:
        return _sonuc_olustur(
            api_tanimi, "network_error", _gecen_sure_ms(baslangic),
            hata=f"Adrese ulaşılamadı: {hata}",
        )

    sure_ms = _gecen_sure_ms(baslangic)

    if yanit.status_code >= 400:
        return _sonuc_olustur(
            api_tanimi, "response_error", sure_ms, http_kodu=yanit.status_code,
            hata=f"Sunucu {yanit.status_code} hata kodu döndürdü.",
        )

    try:
        veri = yanit.json()
    except ValueError:
        return _sonuc_olustur(
            api_tanimi, "invalid_json", sure_ms, http_kodu=yanit.status_code,
            hata="Yanıt JSON olarak ayrıştırılamadı.",
        )

    return _sonuc_olustur(api_tanimi, "ok", sure_ms, http_kodu=yanit.status_code, veri=veri)


def _gecen_sure_ms(baslangic):
    """Başlangıç anından bu yana geçen süreyi milisaniye cinsinden tam sayı olarak verir."""
    return int((time.perf_counter() - baslangic) * 1000)


def _sonuc_olustur(api_tanimi, durum, sure_ms, http_kodu=None, veri=None, hata=None):
    """Başarılı da olsa hatalı da olsa her çekme sonucunu aynı yapıda toplar."""
    return {
        "api_id": api_tanimi.get("id"),
        "durum": durum,
        "http_kodu": http_kodu,
        "sure_ms": sure_ms,
        "veri": veri,
        "hata": hata,
    }


# ---------------------------------------------------------------------------
# GEÇİCİ GÖSTERİM BÖLÜMÜ
#
# Aşağısı yalnızca bu dosya doğrudan çalıştırıldığında devreye girer; başka bir
# dosya bu modülü kullandığında çalışmaz. Amacı, Hafta 1 bitiş ölçütü gereği
# ekranda ilk gerçek yanıtın görülebilmesidir.
#
# Hafta 3'te src/main.py yazıldığında ana akış oraya taşınacak; bu bölüm o
# noktada sadeleştirilebilir veya tamamen kaldırılabilir.
# ---------------------------------------------------------------------------

def _sonucu_yazdir(sonuc):
    """Tek bir çekme sonucunu terminalde okunabilir biçimde ekrana yazar."""
    print(
        f"\n[{sonuc['api_id']}] durum: {sonuc['durum']} | "
        f"HTTP: {sonuc['http_kodu']} | süre: {sonuc['sure_ms']} ms"
    )
    if sonuc["hata"]:
        print(f"  hata: {sonuc['hata']}")
    if sonuc["veri"] is not None:
        print("  yanıt:")
        print(json.dumps(sonuc["veri"], indent=2, ensure_ascii=False))


def _gosterim():
    """Config'deki etkin API'leri sırayla çeker ve sonuçlarını ekrana yazar."""
    try:
        api_listesi = api_listesini_oku()
    except YapilandirmaHatasi as hata:
        print(f"Yapılandırma hatası: {hata}")
        return 1

    etkin_apiler = etkin_apileri_sec(api_listesi)
    if not etkin_apiler:
        print("İzlenecek etkin API bulunamadı.")
        return 0

    print(f"{len(etkin_apiler)} adet etkin API çekilecek.")
    for api_tanimi in etkin_apiler:
        _sonucu_yazdir(veri_cek(api_tanimi))
    return 0


if __name__ == "__main__":
    raise SystemExit(_gosterim())
