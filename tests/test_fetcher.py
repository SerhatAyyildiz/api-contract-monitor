"""
GÖREVİ: Config dosyasının okunmasıyla ilgili dayanıklılığı otomatik doğrulamak.

Bu dosya SADECE config okuma tarafını test eder; gerçek bir API'ye istek
atılmaz (o kısım G3'te elle test edilmişti).

Buradaki BOM testi gerçek bir bozarak testinden doğdu: Windows'ta config
dosyası Not Defteri veya PowerShell ile kaydedildiğinde dosyanın başına
görünmez bir işaret (BOM) ekleniyor ve sistem dosyayı okuyamıyordu.
"""

import pytest

from src.fetcher import YapilandirmaHatasi, api_listesini_oku, etkin_apileri_sec

GECERLI_CONFIG = """{
  "apis": [
    {"id": "test-api", "name": "Test", "url": "https://ornek.com",
     "method": "GET", "headers": {}, "timeout": 10, "enabled": true}
  ]
}"""


def test_bom_iceren_config_okunabiliyor(tmp_path):
    """Başında görünmez BOM işareti olan config dosyası sorunsuz okunmalı."""
    config_yolu = tmp_path / "apis.json"
    # utf-8-sig ile yazmak dosyanin basina BOM koyar - Not Defteri'nin yaptigi sey.
    config_yolu.write_text(GECERLI_CONFIG, encoding="utf-8-sig")

    api_listesi = api_listesini_oku(config_yolu)

    assert len(api_listesi) == 1
    assert api_listesi[0]["id"] == "test-api"


def test_bom_icermeyen_config_de_okunabiliyor(tmp_path):
    """BOM'suz normal bir config dosyası da aynı şekilde okunabilmeli."""
    config_yolu = tmp_path / "apis.json"
    config_yolu.write_text(GECERLI_CONFIG, encoding="utf-8")

    api_listesi = api_listesini_oku(config_yolu)

    assert len(api_listesi) == 1


def test_turkce_karakterli_config_bozulmadan_okunuyor(tmp_path):
    """API adında Türkçe karakter geçse bile içerik bozulmamalı."""
    config_yolu = tmp_path / "apis.json"
    config_yolu.write_text(
        '{"apis": [{"id": "t", "name": "Şığüöç Testi", "url": "https://a.com", '
        '"method": "GET", "headers": {}, "timeout": 10, "enabled": true}]}',
        encoding="utf-8",
    )

    api_listesi = api_listesini_oku(config_yolu)

    assert api_listesi[0]["name"] == "Şığüöç Testi"


def test_olmayan_config_anlasilir_hata_verir(tmp_path):
    """Config dosyası yoksa çökmek yerine anlaşılır bir hata verilmeli."""
    with pytest.raises(YapilandirmaHatasi, match="bulunamadı"):
        api_listesini_oku(tmp_path / "yok.json")


def test_bozuk_json_anlasilir_hata_verir(tmp_path):
    """Config geçerli JSON değilse anlaşılır bir hata verilmeli."""
    config_yolu = tmp_path / "apis.json"
    config_yolu.write_text("{ bu gecerli json degil", encoding="utf-8")

    with pytest.raises(YapilandirmaHatasi, match="JSON"):
        api_listesini_oku(config_yolu)


def test_kapali_apiler_secilmez():
    """enabled alanı kapalı olan API'ler izleme listesine alınmamalı."""
    liste = [
        {"id": "acik", "enabled": True},
        {"id": "kapali", "enabled": False},
        {"id": "belirtilmemis"},
    ]

    secilenler = [api["id"] for api in etkin_apileri_sec(liste)]

    # enabled belirtilmemisse varsayilan olarak acik sayilir.
    assert secilenler == ["acik", "belirtilmemis"]
