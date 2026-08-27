"""
GÖREVİ: Ana akışın (orkestra şefi) doğru kararlar verdiğini otomatik doğrulamak.

Test şu demek: bilinen bir girdi veriyoruz, çıkması gereken sonucu önceden
söylüyoruz, bilgisayar ikisini karşılaştırıp "tuttu / tutmadı" diyor.

ÖNEMLİ - burada GERÇEK hiçbir şey yapılmaz:
- Gerçek bir API'ye istek atılmaz
- Gerçek bir Telegram mesajı gönderilmez
- Gerçek data/monitor.db dosyasına yazılmaz

Bunların hepsinin yerine "sahte" (taklit) sürümler konur. Böylece testler
internetsiz de çalışır, hızlıdır ve yanlışlıkla telefona mesaj göndermez.
Bu taklit etme işi pytest'in monkeypatch aracıyla yapılır.
"""

import pytest

from src import main
from src.storage import DepolamaHatasi


def _bulgu(change_type, severity="critical"):
    """Testlerde kullanılmak üzere tek bir örnek bulgu üretir."""
    return {
        "change_type": change_type,
        "field": "ornek_alan",
        "details": "örnek açıklama",
        "severity": severity,
    }


# ---------------------------------------------------------------------------
# durumu_bulguya_cevir - G6'dan devredilen iş:
# veri çekme katmanının hata durumlarını bulguya çevirmek
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "fetcher_durumu, beklenen_change_type",
    [
        ("timeout", "timeout"),
        ("response_error", "response_error"),
        ("invalid_json", "invalid_json"),
        # network_error ayrı bir Bölüm 6 tipi değil; response_error'a eşleniyor.
        ("network_error", "response_error"),
    ],
)
def test_hata_durumlari_dogru_bulguya_cevriliyor(fetcher_durumu, beklenen_change_type):
    """Yanıt alınamayan her durum, comparator'ınkiyle aynı biçimde kritik bir bulguya dönüşmeli."""
    cekme_sonucu = {
        "api_id": "test-api",
        "durum": fetcher_durumu,
        "hata": "bir şeyler ters gitti",
    }

    bulgular = main.durumu_bulguya_cevir(cekme_sonucu)

    assert len(bulgular) == 1
    assert bulgular[0]["change_type"] == beklenen_change_type
    assert bulgular[0]["severity"] == "critical"
    assert "bir şeyler ters gitti" in bulgular[0]["details"]


def test_basarili_durumda_hata_bulgusu_uretilmez():
    """Yanıt sorunsuz geldiyse hata bulgusu listesi boş olmalı."""
    cekme_sonucu = {"api_id": "test-api", "durum": "ok", "hata": None}

    assert main.durumu_bulguya_cevir(cekme_sonucu) == []


# ---------------------------------------------------------------------------
# GÜVENLİK: adres gizleme
# Hata metinleri hem loga hem Telegram mesajına hem veritabanına gidiyor;
# adres bir erişim anahtarı taşıyabilir.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "gizlenmesi_gereken",
    [
        "https://api.ornek.com/veri?apikey=GIZLI_ANAHTAR_123",
        "http://kullanici:parola@ornek.com/yol",
        "host='api.ornek.com'",
        "url=/gizli/yol?token=ABC123",
    ],
)
def test_hata_metnindeki_adres_gizleniyor(gizlenmesi_gereken):
    """Hata metninde geçen tam adres, dışarı çıkmadan önce gizlenmeli."""
    temiz = main.hata_metnini_temizle(f"Adrese ulaşılamadı: {gizlenmesi_gereken}")

    assert gizlenmesi_gereken not in temiz
    assert "<adres gizlendi>" in temiz


def test_gercek_requests_hata_metnindeki_adres_gizleniyor():
    """requests'in ürettiği gerçek biçimdeki hata metninde hiçbir adres parçası kalmamalı."""
    ham = (
        "Adrese ulaşılamadı: HTTPSConnectionPool("
        "host='gizli-api.ornek.com', port=443): Max retries exceeded with "
        "url: /veri?apikey=SIR (Caused by NameResolutionError(...))"
    )

    temiz = main.hata_metnini_temizle(ham)

    assert "gizli-api.ornek.com" not in temiz
    assert "SIR" not in temiz


def test_sunucu_adi_tirnak_icinde_serbest_gecse_bile_gizlenir():
    """requests sunucu adını 'host=' öneki olmadan da yazabiliyor; bu durumda da gizlenmeli.

    Bu, bozarak testte gerçekten karşılaşılan bir durumdur: NameResolutionError
    metninde sunucu adı "Failed to resolve 'ad'" biçiminde tek başına geçiyordu.
    """
    ham = (
        "Adrese ulaşılamadı: HTTPSConnectionPool(host='gizli-api.ornek.com', "
        "port=443): Failed to resolve 'gizli-api.ornek.com' "
        "([Errno 11001] getaddrinfo failed)"
    )

    temiz = main.hata_metnini_temizle(ham, "https://gizli-api.ornek.com/veri")

    assert "gizli-api.ornek.com" not in temiz


def test_config_adresi_hata_metninden_tamamen_cikarilir():
    """Config'de yazılı adres, hata metninde nasıl geçerse geçsin çıkarılmalı."""
    adres = "https://api.ornek.com/v1/veri?apikey=COK_GIZLI"
    ham = f"Adrese ulaşılamadı: {adres} bağlantı kurulamadı"

    temiz = main.hata_metnini_temizle(ham, adres)

    assert "COK_GIZLI" not in temiz
    assert "api.ornek.com" not in temiz


def test_adres_bilinmeden_de_temizlik_yapilir():
    """API adresi verilmese bile genel desen adres benzeri parçaları temizlemeli."""
    temiz = main.hata_metnini_temizle("Hata: https://baska.ornek.com/yol?key=SIR")

    assert "SIR" not in temiz


def test_adres_gizleme_bulguya_da_uygulaniyor():
    """Gizleme sadece logda değil, veritabanına ve bildirime giden bulguda da olmalı."""
    cekme_sonucu = {
        "api_id": "test-api",
        "durum": "network_error",
        "hata": "Adrese ulaşılamadı: https://api.ornek.com/v1?key=SIR",
    }

    bulgu = main.durumu_bulguya_cevir(cekme_sonucu)[0]

    assert "SIR" not in bulgu["details"]
    assert "api.ornek.com" not in bulgu["details"]


def test_bos_hata_metni_cokme_yaratmaz():
    """Hata metni boş veya yoksa temizleyici çökmemeli."""
    assert main.hata_metnini_temizle(None) is None
    assert main.hata_metnini_temizle("") == ""


def test_adres_icermeyen_hata_metni_bozulmadan_gecer():
    """İçinde adres olmayan bir hata mesajı olduğu gibi korunmalı (okunabilirlik)."""
    metin = "Yanıt beklenen sürede gelmedi."

    assert main.hata_metnini_temizle(metin) == metin


# ---------------------------------------------------------------------------
# kontrol_durumunu_belirle - turun sonucunu tek kelimeye indirgeme
# ---------------------------------------------------------------------------

def test_hata_bulgusu_varsa_durum_error_olur():
    """Yanıt alınamadıysa tur 'error' olarak kaydedilmeli."""
    assert main.kontrol_durumunu_belirle([_bulgu("timeout")], ilk_kez_mi=False) == "error"


def test_sadece_sema_bulgusu_varsa_durum_changed_olur():
    """API yanıt verdiyse ama şeması değiştiyse tur 'changed' olarak kaydedilmeli."""
    assert main.kontrol_durumunu_belirle([_bulgu("field_removed")], ilk_kez_mi=False) == "changed"


def test_bulgu_yoksa_durum_ok_olur():
    """Hiçbir fark yoksa tur 'ok' olarak kaydedilmeli."""
    assert main.kontrol_durumunu_belirle([], ilk_kez_mi=False) == "ok"


def test_ilk_kez_gorulen_api_ok_sayilir():
    """İlk kez görülen API bir sorun değildir; referans kaydı 'ok' olmalı."""
    assert main.kontrol_durumunu_belirle([], ilk_kez_mi=True) == "ok"


def test_hata_ve_sema_bulgusu_bir_aradayken_error_baskin_gelir():
    """Karışık bulgu varsa daha ciddi olan (error) kazanmalı."""
    bulgular = [_bulgu("field_added", severity="info"), _bulgu("response_error")]

    assert main.kontrol_durumunu_belirle(bulgular, ilk_kez_mi=False) == "error"


def test_yavas_yanit_bulgusu_turu_changed_yapar():
    """Yavaş yanıt bir hata değil, bir değişikliktir; tur 'changed' sayılmalı."""
    bulgular = [_bulgu("slow_response", severity="info")]

    assert main.kontrol_durumunu_belirle(bulgular, ilk_kez_mi=False) == "changed"


# ---------------------------------------------------------------------------
# Kusur 1 doğrulaması:
# referans şema yalnızca gerektiğinde kaydedilmeli
# ---------------------------------------------------------------------------

def test_fark_yokken_sema_yeniden_kaydedilmez(monkeypatch):
    """Şema değişmediyse veritabanına yeni bir referans satırı yazılmamalı."""
    kaydedilenler = []
    sema = {"id": "integer"}

    monkeypatch.setattr(main.schema, "sema_cikar", lambda veri: sema)
    monkeypatch.setattr(main.storage, "son_semayi_oku", lambda api_id: sema)
    monkeypatch.setattr(
        main.storage, "sema_kaydet",
        lambda api_id, yeni_sema: kaydedilenler.append(yeni_sema),
    )

    bulgular, ilk_kez_mi = main.sema_farklarini_bul("test-api", {"id": 1})

    assert bulgular == []
    assert ilk_kez_mi is False
    assert kaydedilenler == []


def test_fark_varken_sema_yeniden_kaydedilir(monkeypatch):
    """Gerçek bir değişiklik bulunduysa yeni şema referans olarak kaydedilmeli."""
    kaydedilenler = []
    eski_sema = {"id": "integer", "age": "integer"}
    yeni_sema = {"id": "integer"}

    monkeypatch.setattr(main.schema, "sema_cikar", lambda veri: yeni_sema)
    monkeypatch.setattr(main.storage, "son_semayi_oku", lambda api_id: eski_sema)
    monkeypatch.setattr(
        main.storage, "sema_kaydet",
        lambda api_id, sema: kaydedilenler.append(sema),
    )

    bulgular, ilk_kez_mi = main.sema_farklarini_bul("test-api", {"id": 1})

    assert [b["change_type"] for b in bulgular] == ["field_removed"]
    assert ilk_kez_mi is False
    assert kaydedilenler == [yeni_sema]


def test_ilk_kez_gorulen_api_icin_sema_kaydedilir(monkeypatch):
    """Daha önce kaydı olmayan bir API'nin şeması referans olarak kaydedilmeli."""
    kaydedilenler = []
    yeni_sema = {"id": "integer"}

    monkeypatch.setattr(main.schema, "sema_cikar", lambda veri: yeni_sema)
    monkeypatch.setattr(main.storage, "son_semayi_oku", lambda api_id: None)
    monkeypatch.setattr(
        main.storage, "sema_kaydet",
        lambda api_id, sema: kaydedilenler.append(sema),
    )

    bulgular, ilk_kez_mi = main.sema_farklarini_bul("test-api", {"id": 1})

    assert bulgular == []
    assert ilk_kez_mi is True
    assert kaydedilenler == [yeni_sema]


# ---------------------------------------------------------------------------
# Kusur 2 doğrulaması:
# veritabanı yazılamasa bile bildirim gitmeli
# ---------------------------------------------------------------------------

def test_veritabani_hatasinda_bile_bildirim_denenir(monkeypatch):
    """Kayıt başarısız olsa bile tespit edilen değişiklik bildirilmeli."""
    gonderilenler = []

    def patlayan_kayit(api_id, status, response_time_ms):
        raise DepolamaHatasi("disk dolu")

    monkeypatch.setattr(main.storage, "kontrol_kaydet", patlayan_kayit)
    monkeypatch.setattr(main.storage, "degisiklikleri_kaydet", lambda api_id, bulgular: None)
    monkeypatch.setattr(
        main.notifier, "bildirim_gonder",
        lambda api_id, bulgular: gonderilenler.append(api_id) or {"gonderildi": True, "durum": "ok"},
    )

    main.bulgulari_kaydet_ve_bildir("test-api", [_bulgu("field_removed")], 100, ilk_kez_mi=False)

    assert gonderilenler == ["test-api"]


def test_bildirim_gonderilemezse_sistem_cokmez(monkeypatch):
    """Telegram'a ulaşılamasa bile tur normal şekilde tamamlanmalı."""
    monkeypatch.setattr(main.storage, "kontrol_kaydet", lambda *args: None)
    monkeypatch.setattr(main.storage, "degisiklikleri_kaydet", lambda *args: None)
    monkeypatch.setattr(
        main.notifier, "bildirim_gonder",
        lambda api_id, bulgular: {"gonderildi": False, "durum": "network_error"},
    )

    # İstisna fırlatmadan tamamlanması yeterli.
    main.bulgulari_kaydet_ve_bildir("test-api", [_bulgu("field_removed")], 100, ilk_kez_mi=False)


def test_bulgu_yokken_bildirim_gonderilmez(monkeypatch):
    """Değişiklik yoksa boşuna bildirim gönderilmemeli."""
    gonderilenler = []

    monkeypatch.setattr(main.storage, "kontrol_kaydet", lambda *args: None)
    monkeypatch.setattr(main.storage, "degisiklikleri_kaydet", lambda *args: None)
    monkeypatch.setattr(
        main.notifier, "bildirim_gonder",
        lambda api_id, bulgular: gonderilenler.append(api_id),
    )

    main.bulgulari_kaydet_ve_bildir("test-api", [], 100, ilk_kez_mi=False)

    assert gonderilenler == []


# ---------------------------------------------------------------------------
# Turun dayanıklılığı: bir API çökse bile diğerleri işlenmeli
# ---------------------------------------------------------------------------

def test_bir_api_cokse_bile_tur_devam_eder(monkeypatch):
    """Beklenmedik bir hata alan API atlanmalı, kalan API'ler işlenmeye devam etmeli."""
    islenenler = []

    def bazen_patlayan(api_tanimi):
        if api_tanimi["id"] == "patlayan":
            raise ValueError("hiç beklenmeyen bir sorun")
        islenenler.append(api_tanimi["id"])

    monkeypatch.setattr(main, "tek_api_isle", bazen_patlayan)

    ozet = main.tum_apileri_isle([
        {"id": "birinci"},
        {"id": "patlayan"},
        {"id": "ucuncu"},
    ])

    assert islenenler == ["birinci", "ucuncu"]
    assert ozet == {"toplam": 3, "basarili": 2, "hatali": 1}


def test_veritabani_hatasi_alan_api_atlanir_digerleri_isler(monkeypatch):
    """Bir API'nin veritabanı hatası tüm turu düşürmemeli."""
    islenenler = []

    def bazen_patlayan(api_tanimi):
        if api_tanimi["id"] == "patlayan":
            raise DepolamaHatasi("veritabanı kilitli")
        islenenler.append(api_tanimi["id"])

    monkeypatch.setattr(main, "tek_api_isle", bazen_patlayan)

    ozet = main.tum_apileri_isle([{"id": "patlayan"}, {"id": "saglam"}])

    assert islenenler == ["saglam"]
    assert ozet == {"toplam": 2, "basarili": 1, "hatali": 1}


# ---------------------------------------------------------------------------
# main() giriş noktası: hangi durumda hangi çıkış kodu
# ---------------------------------------------------------------------------

def test_etkin_api_yoksa_tur_hatasiz_biter(monkeypatch):
    """Tüm API'ler kapalıysa bu bir hata değildir; çıkış kodu 0 olmalı."""
    monkeypatch.setattr(main.storage, "veritabanini_hazirla", lambda: None)
    monkeypatch.setattr(main, "api_listesini_oku", lambda: [{"id": "kapali", "enabled": False}])

    assert main.main() == 0


def test_config_okunamazsa_cikis_kodu_1_olur(monkeypatch):
    """Config bozuksa tur hiç başlamamalı ve hata çıkış kodu dönmeli."""
    def patlayan_okuma():
        raise main.YapilandirmaHatasi("config bulunamadı")

    monkeypatch.setattr(main.storage, "veritabanini_hazirla", lambda: None)
    monkeypatch.setattr(main, "api_listesini_oku", patlayan_okuma)

    assert main.main() == 1


def test_veritabani_hazirlanamazsa_cikis_kodu_1_olur(monkeypatch):
    """Veritabanı açılamıyorsa tur hiç başlamamalı ve hata çıkış kodu dönmeli."""
    def patlayan_hazirlik():
        raise DepolamaHatasi("veritabanına bağlanılamadı")

    monkeypatch.setattr(main.storage, "veritabanini_hazirla", patlayan_hazirlik)

    assert main.main() == 1
