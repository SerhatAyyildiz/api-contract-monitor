"""
GÖREVİ: Kayıtlı referans şema ile yeni gelen şemayı karşılaştırıp farkları bulmak.

*** PROJENİN KALBİ BU DOSYADIR. ***
Sistemin var oluş sebebi burada çalışan karşılaştırmadır.

Bu dosya ne yapacak - yakalaması gereken değişiklik tipleri:
- Alan silinmiş        (eskiden vardı, artık yok)         -> KRİTİK
- Tip değişmiş         (sayıydı, metne dönmüş)            -> KRİTİK
- İç içe yapı değişmiş (alanın içindeki alanlar değişmiş) -> KRİTİK
- Yeni alan eklenmiş                                      -> bilgi amaçlı
- Yanıt hata kodu döndürmüş                               -> KRİTİK
- Yanıt hiç gelmemiş (zaman aşımı)                        -> KRİTİK
- Yanıt okunamamış (bozuk veri)                           -> KRİTİK
- Yanıt normalden 3 kat yavaş gelmiş                      -> uyarı

Bu dosya ne YAPMAYACAK:
- Bildirim göndermez, Telegram'ı hiç tanımaz
- Veritabanına dokunmaz
- Sadece farkı bulur ve listeyi geri verir; ne yapılacağına main.py karar verir

Ne zaman yazılacak: Hafta 2, Gün 5-7
"""

# Henüz kod yazılmadı - bu dosya şu an sadece bir yer tutucudur.
