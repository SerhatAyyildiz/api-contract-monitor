"""
GÖREVİ: Bildirim modülünün mesaj oluşturma ve hata yönetimi mantığını
GERÇEK TELEGRAM ÇAĞRISI YAPMADAN otomatik doğrulamak.

Bu dosya iki grup test içerir:
- Mesaj biçimlendirme testleri: bildirim_mesaji_olustur() ağa hiç çıkmayan
  saf bir fonksiyon olduğu için doğrudan test edilebiliyor.
- Ayar/hata yönetimi testleri: ortam değişkenleri monkeypatch ile geçici
  olarak değiştirilip ayar_eksik durumunun çökmeden yakalandığı doğrulanıyor.
  Gerçek bir Telegram sunucusuna hiçbir istek atılmıyor.
"""

from src.notifier import bildirim_mesaji_olustur, bildirim_gonder, _hatayi_temizle


def test_kritik_ve_bilgi_karisik_iki_grup_da_gorunur():
    """Kritik ve bilgi amaçlı bulgular varsa her iki başlık da mesajda olmalı."""
    bulgular = [
        {"details": "age alanı (integer) artık yanıtta yok.", "severity": "critical"},
        {"details": "email alanı (string) yeni eklendi.", "severity": "info"},
    ]
    mesaj = bildirim_mesaji_olustur("demo-api", bulgular)
    assert "KRİTİK (1)" in mesaj
    assert "BİLGİ (1)" in mesaj


def test_sadece_kritik_varsa_bilgi_basligi_yok():
    """Yalnızca kritik bulgu varsa BİLGİ başlığı mesajda hiç görünmemeli."""
    bulgular = [{"details": "age alanı (integer) artık yanıtta yok.", "severity": "critical"}]
    mesaj = bildirim_mesaji_olustur("demo-api", bulgular)
    assert "KRİTİK" in mesaj
    assert "BİLGİ" not in mesaj


def test_sadece_bilgi_varsa_baslik_emojisi_sari():
    """Yalnızca bilgi amaçlı bulgu varsa başlık emojisi 🟡 olmalı, 🔴 değil."""
    bulgular = [{"details": "email alanı (string) yeni eklendi.", "severity": "info"}]
    mesaj = bildirim_mesaji_olustur("demo-api", bulgular)
    assert mesaj.startswith("🟡")
    assert "🔴" not in mesaj


def test_api_id_mesajda_geciyor():
    """Fonksiyona verilen api_id, bulgu sözlüklerinde olmasa bile mesajda görünmeli."""
    mesaj = bildirim_mesaji_olustur("github-user", [])
    assert "github-user" in mesaj


def test_her_bulgunun_details_metni_aynen_var():
    """Her bulgunun details metni, değiştirilmeden mesajın içinde bulunmalı."""
    bulgular = [
        {"details": "id alanının tipi 'integer' iken 'string' oldu.", "severity": "critical"},
    ]
    mesaj = bildirim_mesaji_olustur("demo-api", bulgular)
    assert "id alanının tipi 'integer' iken 'string' oldu." in mesaj


def test_bos_bulgu_listesi_cokmeden_mesaj_uretir():
    """Boş bulgu listesiyle çağrıldığında hata fırlatmadan bir mesaj üretilmeli."""
    mesaj = bildirim_mesaji_olustur("demo-api", [])
    assert "demo-api" in mesaj
    assert "KRİTİK" not in mesaj
    assert "BİLGİ" not in mesaj


def test_cok_fazla_bulgu_uzunluk_sinirini_asmaz():
    """Çok sayıda bulgu mesajı 4096 karakteri aşacaksa, kırpılıp not düşülmeli."""
    bulgular = [
        {"details": f"alan_{i} alanı (integer) artık yanıtta yok.", "severity": "critical"}
        for i in range(500)
    ]
    mesaj = bildirim_mesaji_olustur("demo-api", bulgular)
    assert len(mesaj) <= 4096
    assert "daha fazlası" in mesaj
    assert "500" in mesaj


def test_ozel_karakterli_alan_adi_bozulmadan_gecer():
    """Alan adında alt çizgi ve köşeli parantez geçen bulgular (dizi içi alan) bozulmadan mesaja girmeli."""
    bulgular = [
        {"details": "tags[].name alanı (string) artık yanıtta yok.", "severity": "critical"},
    ]
    mesaj = bildirim_mesaji_olustur("demo-api", bulgular)
    assert "tags[].name alanı (string) artık yanıtta yok." in mesaj


def test_token_eksikse_ayar_eksik_doner(monkeypatch):
    """TELEGRAM_BOT_TOKEN tanımlı değilse istisna fırlamadan ayar_eksik dönmeli."""
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")
    sonuc = bildirim_gonder("demo-api", [])
    assert sonuc["gonderildi"] is False
    assert sonuc["durum"] == "ayar_eksik"
    assert sonuc["hata"] is not None


def test_chat_id_eksikse_ayar_eksik_doner(monkeypatch):
    """TELEGRAM_CHAT_ID tanımlı değilse istisna fırlamadan ayar_eksik dönmeli."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "sahte-token")
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    sonuc = bildirim_gonder("demo-api", [])
    assert sonuc["gonderildi"] is False
    assert sonuc["durum"] == "ayar_eksik"


def test_token_bos_metinse_ayar_eksik_doner(monkeypatch):
    """TELEGRAM_BOT_TOKEN boş bir metinse de eksik sayılıp ayar_eksik dönmeli."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")
    sonuc = bildirim_gonder("demo-api", [])
    assert sonuc["gonderildi"] is False
    assert sonuc["durum"] == "ayar_eksik"


def test_hata_metninde_token_gizlenir():
    """Bir hata metninde token geçiyorsa, temizlenmiş metinde token görünmemeli."""
    sahte_token = "123456789:ABCdefGHIjklMNOpqrSTUvwxYZ"
    ham_hata = f"https://api.telegram.org/bot{sahte_token}/sendMessage adresine ulaşılamadı"

    temiz_hata = _hatayi_temizle(ham_hata, sahte_token)

    assert sahte_token not in temiz_hata
    assert "<gizlendi>" in temiz_hata
