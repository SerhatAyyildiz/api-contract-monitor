"""
GÖREVİ: Depolama katmanının bu turda eklenen kısmını otomatik doğrulamak.

Test şu demek: bilinen bir girdi veriyoruz, çıkması gereken sonucu önceden
söylüyoruz, bilgisayar ikisini karşılaştırıp "tuttu / tutmadı" diyor.

Bu dosya SADECE bu turda eklenen üç işi test eder:
- kontrol_kaydet         : her kontrol turunun sonucunu checks tablosuna yazma
- degisiklikleri_kaydet  : bulunan sapmaları changes tablosuna yazma
- ortalama_yanit_suresini_oku : yavaş yanıt tespiti için geçmiş süre ortalaması

ÖNEMLİ: Testler gerçek data/monitor.db dosyasına HİÇ dokunmaz. pytest'in
tmp_path özelliği her test için geçici bir klasör verir, veritabanı orada
kurulur ve test bitince kendiliğinden silinir.
"""

import sqlite3

import pytest

from src.storage import (
    DepolamaHatasi,
    SLOW_RESPONSE_ICIN_ASGARI_KAYIT,
    degisiklikleri_kaydet,
    kontrol_kaydet,
    ortalama_yanit_suresini_oku,
    veritabanini_hazirla,
)


@pytest.fixture
def gecici_db(tmp_path):
    """Her teste, tabloları kurulmuş boş ve geçici bir veritabanı yolu verir."""
    db_yolu = tmp_path / "test_monitor.db"
    veritabanini_hazirla(db_yolu)
    return db_yolu


def _satirlari_oku(db_yolu, sorgu):
    """Test doğrulaması için veritabanından ham satırları okur."""
    baglanti = sqlite3.connect(db_yolu)
    try:
        return baglanti.execute(sorgu).fetchall()
    finally:
        baglanti.close()


# ---------------------------------------------------------------------------
# checks tablosu
# ---------------------------------------------------------------------------

def test_kontrol_kaydi_yaziliyor_ve_geri_okunuyor(gecici_db):
    """Yazılan kontrol kaydı, verilen api_id/durum/süre değerleriyle geri okunmalı."""
    kontrol_kaydet("test-api", "ok", 250, db_yolu=gecici_db)

    satirlar = _satirlari_oku(
        gecici_db, "SELECT api_id, status, response_time_ms FROM checks"
    )
    assert satirlar == [("test-api", "ok", 250)]


def test_kontrol_kaydi_her_cagrida_yeni_satir_ekler(gecici_db):
    """Aynı API için üst üste kaydedilen turlar birbirinin üzerine yazmamalı (geçmiş korunur)."""
    kontrol_kaydet("test-api", "ok", 100, db_yolu=gecici_db)
    kontrol_kaydet("test-api", "changed", 200, db_yolu=gecici_db)

    satirlar = _satirlari_oku(gecici_db, "SELECT status FROM checks ORDER BY id")
    assert satirlar == [("ok",), ("changed",)]


# ---------------------------------------------------------------------------
# changes tablosu
# ---------------------------------------------------------------------------

def test_bulgular_changes_tablosuna_satir_satir_yaziliyor(gecici_db):
    """Bulgu listesindeki her bulgu ayrı bir satır olarak kaydedilmeli."""
    bulgular = [
        {"change_type": "field_removed", "field": "age",
         "details": "age alanı artık yok.", "severity": "critical"},
        {"change_type": "field_added", "field": "email",
         "details": "email alanı eklendi.", "severity": "info"},
    ]
    degisiklikleri_kaydet("test-api", bulgular, db_yolu=gecici_db)

    satirlar = _satirlari_oku(
        gecici_db, "SELECT api_id, change_type, details FROM changes ORDER BY id"
    )
    assert satirlar == [
        ("test-api", "field_removed", "age alanı artık yok."),
        ("test-api", "field_added", "email alanı eklendi."),
    ]


def test_bos_bulgu_listesi_hic_satir_yazmaz(gecici_db):
    """Hiç bulgu yoksa changes tablosuna dokunulmamalı ve hata verilmemeli."""
    degisiklikleri_kaydet("test-api", [], db_yolu=gecici_db)

    assert _satirlari_oku(gecici_db, "SELECT COUNT(*) FROM changes") == [(0,)]


# ---------------------------------------------------------------------------
# Yavaş yanıt için geçmiş ortalama
# ---------------------------------------------------------------------------

def test_yetersiz_gecmis_varken_ortalama_none_doner(gecici_db):
    """Asgari kayıt sayısına ulaşılmadan ortalama verilmemeli (erken/yanlış alarm koruması)."""
    for _ in range(SLOW_RESPONSE_ICIN_ASGARI_KAYIT - 1):
        kontrol_kaydet("test-api", "ok", 100, db_yolu=gecici_db)

    assert ortalama_yanit_suresini_oku("test-api", db_yolu=gecici_db) is None


def test_hic_kaydi_olmayan_api_icin_ortalama_none_doner(gecici_db):
    """Daha önce hiç görülmemiş bir API için ortalama sorulunca çökmeden None dönmeli."""
    assert ortalama_yanit_suresini_oku("hic-yok", db_yolu=gecici_db) is None


def test_yeterli_gecmis_varken_dogru_ortalama_doner(gecici_db):
    """Yeterli kayıt varsa süreler toplanıp sayıya bölünmüş hali dönmeli."""
    for sure in (100, 200, 300):
        kontrol_kaydet("test-api", "ok", sure, db_yolu=gecici_db)

    assert ortalama_yanit_suresini_oku("test-api", db_yolu=gecici_db) == 200


def test_ortalama_sadece_basarili_turlari_sayar(gecici_db):
    """Hatalı turların süreleri ortalamayı bozmamalı; sadece 'ok' kayıtları sayılmalı."""
    for sure in (100, 200, 300):
        kontrol_kaydet("test-api", "ok", sure, db_yolu=gecici_db)
    # Zaman aşımına uğrayan bir tur, sınıra dayanmış çok yüksek bir süre bırakır.
    kontrol_kaydet("test-api", "error", 10000, db_yolu=gecici_db)

    assert ortalama_yanit_suresini_oku("test-api", db_yolu=gecici_db) == 200


def test_ortalama_baska_apinin_kayitlarini_karistirmaz(gecici_db):
    """Bir API'nin ortalaması hesaplanırken başka API'lerin süreleri hesaba katılmamalı."""
    for sure in (100, 200, 300):
        kontrol_kaydet("test-api", "ok", sure, db_yolu=gecici_db)
    for sure in (9000, 9000, 9000):
        kontrol_kaydet("baska-api", "ok", sure, db_yolu=gecici_db)

    assert ortalama_yanit_suresini_oku("test-api", db_yolu=gecici_db) == 200


def test_ortalama_sadece_son_n_kaydi_dikkate_alir(gecici_db):
    """Belirtilen adetten eski kayıtlar ortalamaya karışmamalı."""
    kontrol_kaydet("test-api", "ok", 9000, db_yolu=gecici_db)
    for sure in (100, 200, 300):
        kontrol_kaydet("test-api", "ok", sure, db_yolu=gecici_db)

    # Son 3 kayıt: 100, 200, 300 -> eski 9000 dışarıda kalmalı.
    assert ortalama_yanit_suresini_oku("test-api", adet=3, db_yolu=gecici_db) == 200


# ---------------------------------------------------------------------------
# Bozarak test
# ---------------------------------------------------------------------------

def test_gecersiz_veritabani_yolunda_depolama_hatasi_verir(tmp_path):
    """Veritabanı olarak bir klasör verilirse sistem çökmemeli, anlaşılır hata vermeli."""
    klasor_yolu = tmp_path / "bu_bir_klasor"
    klasor_yolu.mkdir()

    with pytest.raises(DepolamaHatasi):
        kontrol_kaydet("test-api", "ok", 100, db_yolu=klasor_yolu)
