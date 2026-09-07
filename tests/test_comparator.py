"""
GÖREVİ: Karşılaştırma mantığının gerçekten doğru çalıştığını otomatik doğrulamak.

Test şu demek: bilinen bir girdi veriyoruz, çıkması gereken sonucu önceden
söylüyoruz, bilgisayar ikisini karşılaştırıp "tuttu / tutmadı" diyor.
Böylece ileride bir şeyi bozduğumuzda anında haberimiz olur.

Bu dosya, comparator.py'nin bu turda gerçekten kapsadığı 4 değişiklik tipini
test eder: field_removed, field_added, type_changed ve (ayrı bir etiket
olarak DEĞİL, gerçek tipini koruyarak) iç içe alanlardaki karşılıkları.

NOT: response_error, timeout, invalid_json için burada TEST YOK. Bu üç
tip fetcher.py'nin durum bilgisiyle ilgili ve kapsam dışı bırakıldı (bkz.
BACKLOG.md, PROJE_YOL_HARITASI.md Bölüm 11 G6 kaydı). slow_response ise
alttaki bölümde ayrıca test ediliyor (bkz. Bölüm 11 G12 kaydı).
"""

from src.comparator import semalari_karsilastir


def test_field_removed_tespit_edilir():
    """Eski şemada olup yeni şemada olmayan alan field_removed olarak bulunmalı."""
    eski = {"id": "integer", "age": "integer"}
    yeni = {"id": "integer"}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "field_removed", "field": "age",
         "details": "age alanı (integer) artık yanıtta yok.", "severity": "critical"}
    ]


def test_field_removed_yoksa_bos_liste():
    """İki şema aynı alanlara sahipse field_removed üretilmemeli."""
    sema = {"id": "integer", "name": "string"}
    assert semalari_karsilastir(sema, dict(sema)) == []


def test_type_changed_tespit_edilir():
    """Aynı alanın tipi değişirse type_changed olarak bulunmalı."""
    eski = {"id": "integer"}
    yeni = {"id": "string"}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "type_changed", "field": "id",
         "details": "id alanının tipi 'integer' iken 'string' oldu.", "severity": "critical"}
    ]


def test_type_changed_yoksa_bos_liste():
    """Tipler aynıysa type_changed üretilmemeli."""
    sema = {"id": "integer", "name": "string"}
    assert semalari_karsilastir(sema, dict(sema)) == []


def test_field_added_tespit_edilir():
    """Yeni şemada olup eski şemada olmayan alan field_added olarak bulunmalı, severity info olmalı."""
    eski = {"id": "integer"}
    yeni = {"id": "integer", "email": "string"}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "field_added", "field": "email",
         "details": "email alanı (string) yeni eklendi.", "severity": "info"}
    ]


def test_field_added_yoksa_bos_liste():
    """İki şema aynı alanlara sahipse field_added üretilmemeli."""
    sema = {"id": "integer"}
    assert semalari_karsilastir(sema, dict(sema)) == []


def test_nested_icinde_field_removed_path_ile_raporlanir():
    """İç içe bir objenin içinde alan silinirse, field yolu 'plan.space' gibi genişlemeli."""
    eski = {"id": "integer", "plan": {"name": "string", "space": "integer"}}
    yeni = {"id": "integer", "plan": {"name": "string"}}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "field_removed", "field": "plan.space",
         "details": "plan.space alanı (integer) artık yanıtta yok.", "severity": "critical"}
    ]


def test_nested_icinde_type_changed_path_ile_raporlanir():
    """İç içe bir objenin içinde tip değişirse, field yolu genişlemiş halde type_changed dönmeli."""
    eski = {"plan": {"space": "integer"}}
    yeni = {"plan": {"space": "string"}}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "type_changed", "field": "plan.space",
         "details": "plan.space alanının tipi 'integer' iken 'string' oldu.", "severity": "critical"}
    ]


def test_nested_obje_birebir_ayniyken_bulgu_yok():
    """İç içe obje her iki tarafta da birebir aynıysa hiçbir bulgu üretilmemeli."""
    sema = {"id": "integer", "plan": {"name": "string", "space": "integer"}}
    assert semalari_karsilastir(sema, dict(sema)) == []


def test_array_items_tipi_degisince_type_changed_raporlanir():
    """Dizi elemanının tipi değişirse type_changed olarak, dizi adının yolu ile raporlanmalı."""
    eski = {"scores": {"type": "array", "items": "integer"}}
    yeni = {"scores": {"type": "array", "items": "string"}}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "type_changed", "field": "scores",
         "details": "scores dizisinin eleman tipi 'integer' iken 'string' oldu.",
         "severity": "critical"}
    ]


def test_array_icindeki_obje_alani_silinirse_path_ile_raporlanir():
    """Dizi elemanı bir obje ise, o objenin içindeki alan silinmesi [] yol gösterimiyle raporlanmalı."""
    eski = {"tags": {"type": "array", "items": {"id": "integer", "name": "string"}}}
    yeni = {"tags": {"type": "array", "items": {"id": "integer"}}}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "field_removed", "field": "tags[].name",
         "details": "tags[].name alanı (string) artık yanıtta yok.", "severity": "critical"}
    ]


def test_array_iken_duz_alana_donusmus_type_changed_sayilir():
    """Bir alan eskiden dizi iken şimdi düz bir tipe dönüşmüşse bu type_changed sayılmalı."""
    eski = {"tags": {"type": "array", "items": "string"}}
    yeni = {"tags": "string"}
    bulgular = semalari_karsilastir(eski, yeni)
    assert bulgular == [
        {"change_type": "type_changed", "field": "tags",
         "details": "tags alanının tipi 'array' iken 'string' oldu.", "severity": "critical"}
    ]


def test_iki_sema_tamamen_ayni_bos_liste_doner():
    """Karmaşık, iç içe geçmiş bir şema bile birebir aynıysa boş liste dönmeli (genel smoke test)."""
    sema = {
        "id": "integer", "login": "string",
        "plan": {"name": "string", "space": "integer"},
        "tags": {"type": "array", "items": {"id": "integer", "name": "string"}},
    }
    assert semalari_karsilastir(sema, dict(sema)) == []


def test_birden_fazla_degisiklik_ayni_anda_tespit_edilir():
    """field_removed, field_added ve type_changed aynı anda oluşursa hepsi listede olmalı, hiçbiri kaybolmamalı."""
    eski = {"id": "integer", "age": "integer", "name": "string"}
    yeni = {"id": "string", "name": "string", "email": "string"}
    bulgular = semalari_karsilastir(eski, yeni)

    tipler = {(b["change_type"], b["field"]) for b in bulgular}
    assert tipler == {
        ("field_removed", "age"),
        ("field_added", "email"),
        ("type_changed", "id"),
    }
    assert len(bulgular) == 3


def test_bos_semalar_ile_cagrilinca_hata_vermez():
    """İki boş şema ile çağrıldığında hata fırlatmadan boş liste dönmeli (kenar durum)."""
    assert semalari_karsilastir({}, {}) == []


# ---------------------------------------------------------------------------
# yanit_suresini_degerlendir - yavaş yanıt tespiti
#
# G11'de gerçek kullanımda üç yanlış alarm bulundu: hızlı bir API'nin
# ortalaması düşükken (örn. 17 ms) referansın 3 katı eşiği de düşük
# kalıyor ve sıradan bir ağ dalgalanması "yavaş" sanılıyordu. Düzeltme
# olarak mutlak bir alt sınır (ASGARI_YAVAS_SURE_MS) eklendi: bir yanıt
# artık hem oranı hem mutlak sınırı aşmadıkça bulgu üretilmiyor.
# ---------------------------------------------------------------------------

from src.comparator import ASGARI_YAVAS_SURE_MS, yanit_suresini_degerlendir


def test_referans_yokken_bulgu_uretilmez():
    """Geçmiş kaydı olmayan (referans_sure_ms None) bir API için değerlendirme yapılamaz."""
    assert yanit_suresini_degerlendir(5000, None) == []


def test_referans_sifirken_bulgu_uretilmez():
    """referans_sure_ms 0 gelirse (teorik olarak) çökmeden boş liste dönmeli."""
    assert yanit_suresini_degerlendir(5000, 0) == []


def test_mutlak_sinirin_altinda_oran_asilsa_bile_bulgu_uretilmez():
    """Yanıt mutlak sınırın altındaysa, referansın kaç katı olursa olsun yavaş sayılmamalı.

    Bu, G11'de bulunan gerçek yanlış alarmların birebir simülasyonudur:
    ortalaması çok düşük bir API'de ufak bir dalgalanma bile eskiden
    'yavaş' sayılıyordu.
    """
    assert yanit_suresini_degerlendir(75, 17) == []      # gerçek olay: pypi-paket
    assert yanit_suresini_degerlendir(299, 91) == []      # gerçek olay: jsonplaceholder
    assert yanit_suresini_degerlendir(326, 105) == []     # gerçek olay: jsonplaceholder


def test_mutlak_siniri_asip_orani_asmayan_yanit_bulgu_uretmez():
    """Mutlak sınırın üzerinde olsa bile referansın 3 katını aşmıyorsa yavaş sayılmamalı."""
    # Referans zaten yüksek (1000 ms); 2500 ms bunun sadece 2.5 katı.
    assert yanit_suresini_degerlendir(2500, 1000) == []


def test_hem_mutlak_hem_oran_siniri_asilinca_bulgu_uretilir():
    """Yanıt hem 1000 ms'yi hem referansın 3 katını aşıyorsa gerçek bir yavaşlama sayılmalı."""
    bulgular = yanit_suresini_degerlendir(1500, 100)

    assert len(bulgular) == 1
    assert bulgular[0]["change_type"] == "slow_response"
    assert bulgular[0]["severity"] == "info"
    assert "1500" in bulgular[0]["details"]
    assert "100" in bulgular[0]["details"]


def test_mutlak_sinirin_bir_altindaki_yanit_asla_yavas_sayilmaz():
    """Sınırın tam 1 ms altındaki bir süre, oran ne kadar aşılırsa aşılsın yavaş sayılmamalı."""
    assert yanit_suresini_degerlendir(ASGARI_YAVAS_SURE_MS - 1, 1) == []


def test_mutlak_sinira_tam_esit_yanit_oran_da_asiliyorsa_yakalanir():
    """Sınıra tam eşit bir süre, oran şartı da sağlanıyorsa yavaş sayılmalı (sınır dahildir)."""
    bulgular = yanit_suresini_degerlendir(ASGARI_YAVAS_SURE_MS, 1)

    assert len(bulgular) == 1
    assert bulgular[0]["change_type"] == "slow_response"


def test_gercekten_yavas_bir_yanit_hala_yakalaniyor():
    """Düzeltme sonrası bile gerçek bir yavaşlama (referansın kat kat üzerinde, saniyeler süren) kaçmamalı."""
    # pypi-paket gibi normalde ~13 ms süren bir API aniden 3 saniye sürerse.
    bulgular = yanit_suresini_degerlendir(3000, 13)

    assert len(bulgular) == 1
    assert bulgular[0]["change_type"] == "slow_response"
