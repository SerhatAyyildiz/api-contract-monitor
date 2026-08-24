"""
GÖREVİ: Gelen yanıta bakıp "hangi alan var, tipi ne" haritasını çıkarmak.

Bu haritaya şema deniyor (API'nin döndürdüğü verinin yapısı).
Örnek: gelen veride "yas" diye bir alan varsa ve içinde sayı yazıyorsa,
şemaya "yas -> sayı" olarak kaydedilir. Değerin kendisi değil, TİPİ önemlidir.

Bu dosya ne yapıyor:
- Ham yanıtı alır, alan adı ve tip eşleşmelerini çıkarır
- İç içe geçmiş yapıları da (bir alanın içinde başka alanlar olması) işler
- Diziler için ilk elemanın tipini baz alır; elemanı obje ise iç şemasını da çıkarır

Bu dosya ne YAPMIYOR:
- İki şemayı karşılaştırmaz (o comparator.py'nin işi)
- API'ye istek atmaz (o fetcher.py'nin işi)
- Hiçbir şeyi veritabanına kaydetmez (o storage.py'nin işi)
"""

# Bir dizinin içi boşsa eleman tipi bilinmediği için bu etiket kullanılır.
BILINMEYEN_TIP = "unknown"


def sema_cikar(veri):
    """Ham bir JSON değerini alır, alan adı -> tip haritası biçiminde şemasını döndürür."""
    if isinstance(veri, dict):
        return _obje_semasi(veri)
    if isinstance(veri, list):
        return _dizi_semasi(veri)
    return {"type": _temel_tip_adi(veri)}


def _deger_semasi(deger):
    """Tek bir değeri tipine göre sınıflandırır; dict/list ise ilgili yardımcıya yönlendirir."""
    if isinstance(deger, dict):
        return _obje_semasi(deger)
    if isinstance(deger, list):
        return _dizi_semasi(deger)
    return _temel_tip_adi(deger)


def _obje_semasi(obje):
    """Bir sözlüğün her alanını gezip alan adı -> şema haritası üretir."""
    return {alan_adi: _deger_semasi(alan_degeri) for alan_adi, alan_degeri in obje.items()}


def _dizi_semasi(dizi):
    """Bir listenin ilk elemanına bakıp {'type': 'array', 'items': ...} biçiminde şema döndürür."""
    if not dizi:
        return {"type": "array", "items": BILINMEYEN_TIP}
    return {"type": "array", "items": _deger_semasi(dizi[0])}


def _temel_tip_adi(deger):
    """Dizi/sözlük olmayan tek bir değerin proje etiketini döndürür."""
    # bool, Python'da int'in alt sınıfıdır; bu yüzden bool kontrolü int'ten ÖNCE yapılmalı.
    # Aksi halde True/False değerleri yanlışlıkla "integer" olarak etiketlenir.
    if isinstance(deger, bool):
        return "boolean"
    if deger is None:
        return "null"
    if isinstance(deger, str):
        return "string"
    if isinstance(deger, int):
        return "integer"
    if isinstance(deger, float):
        return "float"
    return BILINMEYEN_TIP


# ---------------------------------------------------------------------------
# GEÇİCİ ELLE-TEST GÖSTERİM BÖLÜMÜ
#
# Aşağısı yalnızca bu dosya doğrudan çalıştırıldığında devreye girer. Amacı,
# Hafta 2 Gün 1-2'nin "elle test: farklı JSON'lar ver, doğru şema çıkıyor mu
# bak" isteğini karşılamak. Otomatik testler Hafta 2 Gün 5-7'de yazılacak.
# ---------------------------------------------------------------------------

import json

ORNEK_GIRDILER = {
    "1) Duz obje (karisik tipler)": {
        "login": "octocat", "id": 1, "public_repos": 8,
        "active": True, "avatar_url": None,
    },
    "2) Ic ice obje": {
        "login": "octocat", "id": 1,
        "plan": {"name": "free", "space": 976562499, "private_repos": 0},
    },
    "3) Diziler (basit + obje elemanli + bos)": {
        "id": 1,
        "scores": [10, 20, 30],
        "tags": [{"id": 5, "name": "vip"}, {"id": 9, "name": "beta"}],
        "empty_list": [],
    },
    "4) Kok seviyede liste": [
        {"id": 1, "title": "a"}, {"id": 2, "title": "b"},
    ],
    "5) Kok seviyede None ve tek bir temel deger": None,
    "5b) Kok seviyede tek sayi": 42,
}


def _gosterim():
    """Örnek girdileri sırayla şemaya çevirip ekrana okunabilir biçimde yazar."""
    for baslik, girdi in ORNEK_GIRDILER.items():
        print(f"\n--- {baslik} ---")
        print("girdi :", json.dumps(girdi, ensure_ascii=False))
        print("sema  :", json.dumps(sema_cikar(girdi), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(_gosterim())
