"""
GÖREVİ: Diğer tüm dosyaları doğru sırayla çağıran ana akış. Sistemin giriş kapısı.

*** ORKESTRA ŞEFİ BU DOSYADIR. ***
Diğer modüller birbirini tanımaz ve birbirini çağırmaz.
Hepsini buradan çağırıyoruz. Bu sayede tüm akış tek dosyaya bakarak anlaşılır.

İZLENECEK AKIŞ (her API için sırayla):

  1. Listeyi oku          -> config/apis.json
  2. İstek at             -> fetcher
  3. Yapıyı çıkar         -> schema
  4. Kayıtlı hali getir   -> storage
       * İlk kez görülüyorsa: referans olarak kaydet ve dur
  5. Karşılaştır          -> comparator
       * Fark yoksa: "sorun yok" kaydı at, tur biter
  6. Yorumlat             -> analyzer   (Hafta 4 - henüz yok, çağrılmıyor)
  7. Haber ver            -> notifier
  8. Kaydet               -> storage

GÜVENLİK: Hiçbir log satırı bir API'nin tam adresini (url) veya başlıklarını
(headers) yazdırmaz - bunlar ileride erişim anahtarı taşıyabilir. Sadece
api_id loglanır. Bildirim sonucu loglanırken de yalnızca "durum" alanı
yazılır; notifier'ın ham hata metni asla loglanmaz (notifier zaten token'ı
temizliyor, bu ikinci bir güvenlik kapısıdır).

Ne zaman yazılacak: Hafta 3, Gün 3-4
"""

import logging
import re
from urllib.parse import urlparse

from src import comparator, notifier, schema, storage
from src.fetcher import YapilandirmaHatasi, api_listesini_oku, etkin_apileri_sec, veri_cek
from src.storage import DepolamaHatasi

# fetcher'ın "durum" alanını, comparator'ın ürettiğiyle AYNI BİÇİMDE bir
# bulguya çevirmek için kullanılan eşleme. network_error ayrı bir Bölüm 6
# tipi değil; response_error'a eşleniyor çünkü ikisi de "API şu an
# kullanılamıyor" demek - gerçek sebep zaten details metninde kalıyor.
HATA_DURUMU_ESLEMESI = {
    "timeout": "timeout",
    "response_error": "response_error",
    "invalid_json": "invalid_json",
    "network_error": "response_error",
}

# Hata metinlerinde geçen adres parçalarını yakalayan desen. requests bunları
# birkaç ayrı biçimde yazıyor: tam adres (https://...), bağlantı havuzu
# bilgisi (host='...') ve istenen yol (url: /... veya url=/...). Hepsi
# erişim anahtarı taşıyabildiği için loga ve bildirime çıkmadan önce
# gizlenir - bkz. hata_metnini_temizle.
ADRES_DESENI = re.compile(
    r"https?://\S+"
    r"|host='[^']*'"
    r"|url[:=]\s*\S+"
)

GIZLENDI_ISARETI = "<adres gizlendi>"


def main():
    """Logu ve veritabanını hazırlar, config'i okur, tüm etkin API'leri işletir, çıkış kodu üretir."""
    loglamayi_hazirla()

    try:
        storage.veritabanini_hazirla()
        api_listesi = api_listesini_oku()
    except (YapilandirmaHatasi, DepolamaHatasi) as hata:
        logging.error("Tur başlatılamadı: %s", hata)
        return 1

    etkin_apiler = etkin_apileri_sec(api_listesi)
    if not etkin_apiler:
        logging.warning("İzlenecek etkin API bulunamadı, tur atlanıyor.")
        return 0

    ozet = tum_apileri_isle(etkin_apiler)
    _tur_ozetini_logla(ozet)
    return 0


def loglamayi_hazirla():
    """Konsola zaman damgalı ve seviyeli log yazılmasını tek bir yerden ayarlar."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def tum_apileri_isle(etkin_apiler):
    """Her API'yi kendi hata koruması içinde sırayla işler; biri çökse bile diğerlerine devam eder."""
    ozet = {"toplam": len(etkin_apiler), "basarili": 0, "hatali": 0}

    for api_tanimi in etkin_apiler:
        try:
            tek_api_isle(api_tanimi)
            ozet["basarili"] += 1
        except DepolamaHatasi as hata:
            logging.error("%s: veritabanı hatası, bu API atlanıyor: %s", api_tanimi["id"], hata)
            ozet["hatali"] += 1
        except Exception:
            # Bir API'nin beklenmedik bir sorunu diğer API'lerin kontrolünü
            # engellemesin diye burada yakalanıyor - hata yutulmuyor, tam
            # izi (traceback) loglanıyor.
            logging.exception("%s: beklenmedik hata, bu API atlanıyor.", api_tanimi["id"])
            ozet["hatali"] += 1

    return ozet


def tek_api_isle(api_tanimi):
    """Bir API için 8 adımlık kontrol akışının tamamını (istek, karşılaştırma, kayıt, bildirim) yürütür."""
    cekme_sonucu = veri_cek(api_tanimi)

    if cekme_sonucu["durum"] != "ok":
        hatali_sonucu_isle(api_tanimi, cekme_sonucu)
        return

    basarili_sonucu_isle(api_tanimi, cekme_sonucu)


def durumu_bulguya_cevir(cekme_sonucu, api_adresi=None):
    """Fetcher'ın 'ok' olmayan durumunu, comparator'ınkiyle aynı biçimde bir bulguya çevirir."""
    if cekme_sonucu["durum"] == "ok":
        return []

    change_type = HATA_DURUMU_ESLEMESI[cekme_sonucu["durum"]]
    temiz_hata = hata_metnini_temizle(cekme_sonucu["hata"], api_adresi)
    details = f"{cekme_sonucu['api_id']}: {temiz_hata}"
    return [{"change_type": change_type, "field": None, "details": details, "severity": "critical"}]


def hata_metnini_temizle(hata_metni, api_adresi=None):
    """Bir hata metnindeki adresleri gizler; adres bir erişim anahtarı taşıyabilir.

    requests kütüphanesi ağ hatalarında istenen adresi hata metnine koyar. O
    metin buradan hem loga hem Telegram mesajına hem veritabanına gidiyor.
    Adreste anahtar taşıyan bir API eklendiğinde (config'de bu mümkün)
    anahtar üç yere birden sızardı.

    İki kat koruma var: önce API'nin config'deki gerçek adresi ve sunucu adı
    metinden çıkarılır (kesin çözüm), sonra genel bir desen kalan adres
    benzeri parçaları da temizler (requests'in ileride biçim değiştirmesine
    karşı ikinci savunma hattı).
    """
    if not hata_metni:
        return hata_metni

    temiz = _bilinen_adresi_gizle(hata_metni, api_adresi)
    return ADRES_DESENI.sub(GIZLENDI_ISARETI, temiz)


def _bilinen_adresi_gizle(hata_metni, api_adresi):
    """Config'de yazılı olan adresi ve onun sunucu adını hata metninden çıkarır."""
    if not api_adresi:
        return hata_metni

    temiz = hata_metni.replace(api_adresi, GIZLENDI_ISARETI)

    sunucu_adi = urlparse(api_adresi).hostname
    if sunucu_adi:
        temiz = temiz.replace(sunucu_adi, GIZLENDI_ISARETI)

    return temiz


def hatali_sonucu_isle(api_tanimi, cekme_sonucu):
    """Yanıt alınamayan bir API için hata bulgusunu üretir, kaydeder ve bildirir."""
    api_id = api_tanimi["id"]
    api_adresi = api_tanimi.get("url")
    bulgular = durumu_bulguya_cevir(cekme_sonucu, api_adresi)

    logging.error("%s: %s", api_id, hata_metnini_temizle(cekme_sonucu["hata"], api_adresi))
    bulgulari_kaydet_ve_bildir(api_id, bulgular, cekme_sonucu["sure_ms"], ilk_kez_mi=False)


def basarili_sonucu_isle(api_tanimi, cekme_sonucu):
    """Yanıt alınan bir API için şema ve yanıt süresi bulgularını toplayıp kaydeder, gerekirse bildirir."""
    api_id = api_tanimi["id"]
    sure_ms = cekme_sonucu["sure_ms"]

    sema_bulgulari, ilk_kez_mi = sema_farklarini_bul(api_id, cekme_sonucu["veri"])

    if ilk_kez_mi:
        logging.warning("%s: ilk kez görülüyor, referans olarak kaydedildi.", api_id)
        bulgulari_kaydet_ve_bildir(api_id, [], sure_ms, ilk_kez_mi=True)
        return

    yavas_bulgular = yavas_yanit_bulgusunu_al(api_id, sure_ms)
    bulgular = sema_bulgulari + yavas_bulgular

    if not bulgular:
        logging.info("%s: değişiklik yok (%s ms).", api_id, sure_ms)
    else:
        logging.info("%s: %s bulgu tespit edildi (%s ms).", api_id, len(bulgular), sure_ms)

    bulgulari_kaydet_ve_bildir(api_id, bulgular, sure_ms, ilk_kez_mi=False)


def sema_farklarini_bul(api_id, veri):
    """Yeni şemayı çıkarır, kayıtlı referansla karşılaştırır; API'nin ilk kez görülüp görülmediğini de bildirir.

    Şema SADECE iki durumda kaydedilir: API ilk kez görülüyorsa veya gerçekten
    bir fark bulunduysa. Fark yokken de kaydetseydik veritabanı her turda bir
    satır büyürdü; dahası bir alan bir tur kaybolup sonra geri geldiğinde
    referans bu arada bozuk şemayla güncellenmiş olacağı için sistem aynı
    değişikliği ikinci kez bildirirdi.
    """
    yeni_sema = schema.sema_cikar(veri)
    eski_sema = storage.son_semayi_oku(api_id)

    if eski_sema is None:
        storage.sema_kaydet(api_id, yeni_sema)
        return [], True

    bulgular = comparator.semalari_karsilastir(eski_sema, yeni_sema)
    if bulgular:
        storage.sema_kaydet(api_id, yeni_sema)

    return bulgular, False


def yavas_yanit_bulgusunu_al(api_id, sure_ms):
    """Geçmiş yanıt sürelerini okuyup comparator'a kıyaslatır; yeterli veri yoksa boş liste döndürür."""
    referans_sure_ms = storage.ortalama_yanit_suresini_oku(api_id)
    return comparator.yanit_suresini_degerlendir(sure_ms, referans_sure_ms)


def kontrol_durumunu_belirle(bulgular, ilk_kez_mi):
    """Bir turun sonucunu checks tablosuna yazılacak tek kelimeye (ok/changed/error) indirger."""
    if ilk_kez_mi:
        return "ok"

    hata_tipleri = set(HATA_DURUMU_ESLEMESI.values())
    if any(bulgu["change_type"] in hata_tipleri for bulgu in bulgular):
        return "error"

    if bulgular:
        return "changed"

    return "ok"


def bulgulari_kaydet_ve_bildir(api_id, bulgular, sure_ms, ilk_kez_mi):
    """Sonucu veritabanına yazar, sonra bulgu varsa bildirir; kayıt başarısız olsa bile bildirim denenir."""
    sonuclari_kaydet(api_id, bulgular, sure_ms, ilk_kez_mi)

    if bulgular:
        # Hafta 4: LLM yorumu burada bulgulara eklenecek.
        bildirimi_gonder_ve_logla(api_id, bulgular)


def sonuclari_kaydet(api_id, bulgular, sure_ms, ilk_kez_mi):
    """Kontrol kaydını ve bulguları veritabanına yazar; yazamazsa loglar ama akışı kesmez.

    Veritabanına yazamamak, tespit edilen bir değişikliği bildirmemek için
    yeterli sebep değildir - bildirim bu sistemin asıl çıktısıdır. Bu yüzden
    hata burada yutulmuyor, loglanıyor ve akış devam ediyor.
    """
    status = kontrol_durumunu_belirle(bulgular, ilk_kez_mi)

    try:
        storage.kontrol_kaydet(api_id, status, sure_ms)
        storage.degisiklikleri_kaydet(api_id, bulgular)
    except DepolamaHatasi as hata:
        logging.error("%s: sonuçlar kaydedilemedi, bildirime devam ediliyor: %s", api_id, hata)


def bildirimi_gonder_ve_logla(api_id, bulgular):
    """Bildirimi gönderir ve sonucunu, gizli anahtar sızmayacak biçimde (sadece durum kelimesiyle) loglar."""
    sonuc = notifier.bildirim_gonder(api_id, bulgular)

    if sonuc["gonderildi"]:
        logging.info("%s: bildirim gönderildi.", api_id)
    else:
        logging.warning("%s: bildirim gönderilemedi (durum: %s).", api_id, sonuc["durum"])


def _tur_ozetini_logla(ozet):
    """Tur sonunda kaç API'nin sorunsuz, kaçının hatalı bittiğini tek satırda özetler."""
    logging.info(
        "Tur bitti: %s API, %s başarılı, %s hatalı.",
        ozet["toplam"], ozet["basarili"], ozet["hatali"],
    )


if __name__ == "__main__":
    raise SystemExit(main())
