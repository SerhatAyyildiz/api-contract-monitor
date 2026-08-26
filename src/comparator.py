"""
GÖREVİ: Kayıtlı referans şema ile yeni gelen şemayı karşılaştırıp farkları bulmak.

*** PROJENİN KALBİ BU DOSYADIR. ***
Sistemin var oluş sebebi burada çalışan karşılaştırmadır.

Bu dosya, iki şema (schema.py'nin ürettiği alan->tip haritası) arasındaki
şu farkları bulur:
- Alan silinmiş        (eskiden vardı, artık yok)         -> field_removed, KRİTİK
- Alan eklenmiş         (yeni ortaya çıkmış)               -> field_added, bilgi amaçlı
- Tip değişmiş          (sayıydı, metne dönmüş)            -> type_changed, KRİTİK
İç içe (nested) bir alanın içinde bir şey değişirse, bulgu kendi gerçek
tipini (field_removed/type_changed/field_added) korur; sadece "field"
yolu "plan.space" gibi genişler. Ayrı bir "nested_changed" etiketi
üretilmez (bkz. PROJE_YOL_HARITASI.md Bölüm 11, G6 kaydı - bu, proje
sahibiyle netleştirilmiş bilinçli bir tasarım kararıdır).

Bu dosya ne YAPMIYOR:
- Bildirim göndermez, Telegram'ı hiç tanımaz
- Veritabanına dokunmaz
- API'ye istek atmaz, fetcher'ın durum bilgisiyle (timeout/response_error/
  invalid_json) hiç ilgilenmez - bunlar şema karşılaştırması değildir,
  main.py'nin (Hafta 3) işidir
- slow_response tespiti yapmaz - referans yanıt süresi henüz hiçbir yerde
  saklanmıyor (bkz. BACKLOG.md)
- Sadece farkı bulur ve listeyi geri verir; ne yapılacağına main.py karar verir
"""

# Her değişiklik tipinin ne kadar önemli olduğu (PROJE_YOL_HARITASI.md Bölüm 6).
# nested_changed bu turda hiç üretilmiyor ama tablo eksiksiz kalsın diye burada.
ONEM_DERECELERI = {
    "field_removed": "critical",
    "type_changed": "critical",
    "nested_changed": "critical",
    "field_added": "info",
}


def semalari_karsilastir(eski_sema, yeni_sema, yol=""):
    """İki şemayı karşılaştırıp bulunan tüm farkları tek bir liste olarak döndürür."""
    bulgular = []
    bulgular += _silinen_alanlari_bul(eski_sema, yeni_sema, yol)
    bulgular += _eklenen_alanlari_bul(eski_sema, yeni_sema, yol)
    bulgular += _ortak_alanlari_karsilastir(eski_sema, yeni_sema, yol)
    return bulgular


def _silinen_alanlari_bul(eski_sema, yeni_sema, yol):
    """Eski şemada olup yeni şemada olmayan alanları field_removed olarak raporlar."""
    bulgular = []
    for alan_adi in eski_sema.keys() - yeni_sema.keys():
        tam_yol = yol + alan_adi
        tip = eski_sema[alan_adi]
        details = f"{tam_yol} alanı ({_tip_etiketi(tip)}) artık yanıtta yok."
        bulgular.append(_bulgu_olustur("field_removed", tam_yol, details))
    return bulgular


def _eklenen_alanlari_bul(eski_sema, yeni_sema, yol):
    """Yeni şemada olup eski şemada olmayan alanları field_added olarak raporlar."""
    bulgular = []
    for alan_adi in yeni_sema.keys() - eski_sema.keys():
        tam_yol = yol + alan_adi
        tip = yeni_sema[alan_adi]
        details = f"{tam_yol} alanı ({_tip_etiketi(tip)}) yeni eklendi."
        bulgular.append(_bulgu_olustur("field_added", tam_yol, details))
    return bulgular


def _ortak_alanlari_karsilastir(eski_sema, yeni_sema, yol):
    """İki şemada da bulunan alanları gezip her biri için tip/iç yapı karşılaştırması yapar."""
    bulgular = []
    for alan_adi in eski_sema.keys() & yeni_sema.keys():
        bulgular += _alan_semasini_karsilastir(
            alan_adi, eski_sema[alan_adi], yeni_sema[alan_adi], yol
        )
    return bulgular


def _alan_semasini_karsilastir(alan_adi, eski_parca, yeni_parca, yol):
    """Tek bir alanın eski/yeni şema parçasını türüne göre (düz obje/dizi/temel tip) karşılaştırır."""
    tam_yol = yol + alan_adi

    if _duz_obje_mi(eski_parca) and _duz_obje_mi(yeni_parca):
        return semalari_karsilastir(eski_parca, yeni_parca, tam_yol + ".")

    if _dizi_mi(eski_parca) and _dizi_mi(yeni_parca):
        return _dizi_elemanlarini_karsilastir(tam_yol, eski_parca, yeni_parca)

    if _tip_etiketi(eski_parca) != _tip_etiketi(yeni_parca):
        details = (
            f"{tam_yol} alanının tipi '{_tip_etiketi(eski_parca)}' iken "
            f"'{_tip_etiketi(yeni_parca)}' oldu."
        )
        return [_bulgu_olustur("type_changed", tam_yol, details)]

    return []


def _dizi_elemanlarini_karsilastir(tam_yol, eski_dizi, yeni_dizi):
    """İki array-wrapper'ın ('items' alanlarının) kendi aralarında karşılaştırılmasını yapar."""
    eski_items = eski_dizi.get("items")
    yeni_items = yeni_dizi.get("items")

    if _duz_obje_mi(eski_items) and _duz_obje_mi(yeni_items):
        return semalari_karsilastir(eski_items, yeni_items, tam_yol + "[].")

    if _tip_etiketi(eski_items) != _tip_etiketi(yeni_items):
        details = (
            f"{tam_yol} dizisinin eleman tipi '{_tip_etiketi(eski_items)}' iken "
            f"'{_tip_etiketi(yeni_items)}' oldu."
        )
        return [_bulgu_olustur("type_changed", tam_yol, details)]

    return []


def _duz_obje_mi(sema_parcasi):
    """Bir şema parçasının (array-wrapper OLMAYAN) düz iç içe obje olup olmadığını söyler."""
    return isinstance(sema_parcasi, dict) and not _dizi_mi(sema_parcasi)


def _dizi_mi(sema_parcasi):
    """Bir şema parçasının schema.py'nin ürettiği array-wrapper biçiminde olup olmadığını söyler."""
    return isinstance(sema_parcasi, dict) and sema_parcasi.get("type") == "array"


def _tip_etiketi(sema_parcasi):
    """Karşılaştırma ve mesaj yazımı için bir şema parçasının okunabilir tip adını döndürür."""
    if _dizi_mi(sema_parcasi):
        return "array"
    if isinstance(sema_parcasi, dict):
        return "object"
    return sema_parcasi


def _bulgu_olustur(change_type, field, details):
    """Her bulgunun aynı yapıda (change_type, field, details, severity) üretilmesini sağlar."""
    return {
        "change_type": change_type,
        "field": field,
        "details": details,
        "severity": ONEM_DERECELERI[change_type],
    }
