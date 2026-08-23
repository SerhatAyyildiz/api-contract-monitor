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
  6. Yorumlat             -> analyzer   (sadece kritik farklarda)
  7. Haber ver            -> notifier
  8. Kaydet               -> storage

Ne zaman yazılacak: Hafta 3, Gün 3-4
"""

# Henüz kod yazılmadı - bu dosya şu an sadece bir yer tutucudur.
