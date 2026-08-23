"""
GÖREVİ: Verileri kalıcı olarak kaydetmek ve geri okumak.

Kayıtlar data/monitor.db dosyasında tutulacak. Bu dosya bir veritabanıdır
(düzenli kayıt tutan, içinde tablolar bulunan tek bir dosya).

Bu dosya ne yapacak - üç tablo yönetecek:
- Referans şemalar : her API için "normal hali bu" kaydı
- Kontrol geçmişi  : her turda ne oldu, ne kadar sürdü
- Değişiklikler    : tespit edilen sapmalar ve yorumları

Bu dosya ne YAPMAYACAK:
- Veriyi yorumlamaz, sadece saklar ve geri verir

ÖNEMLİ KURAL: Veritabanına dokunan TEK dosya budur.
Başka hiçbir modül doğrudan veritabanına yazmaz veya okumaz.

Ne zaman yazılacak: Hafta 2, Gün 3-4
"""

# Henüz kod yazılmadı - bu dosya şu an sadece bir yer tutucudur.
