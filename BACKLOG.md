# Sonraya Bırakılanlar

> Proje kapsamı dışında kalan fikirler buraya yazılır.
> Kural: temel sistem bitmeden buradan hiçbir madde alınıp yapılmaz.
> Bir fikir aklına geldiğinde silinmesin diye buraya not düşülür, sonra karar verilir.

## Bekleyen fikirler

| Fikir | Neden şimdi değil |
|---|---|
| Otomatik kayıtların seyreltilmesi | G9 EK'ten çıkan not. Sistem her turda kontrol geçmişine yeni bir satır eklediği için veritabanı her seferinde değişiyor; dolayısıyla "değişiklik yoksa kayıt atlanır" mantığı hiç devreye girmiyor ve her tur depoya bir kayıt bırakıyor. Depo zamanla bu kayıtlarla dolacak. Çözüm seçenekleri: kayıtları günde bir toplu atmak, kontrol geçmişini ayrı bir yerde tutmak veya eski kayıtları belirli aralıklarla temizlemek. Şu an çalışmayı engellemiyor, o yüzden bekliyor. |
| Zamanlayıcının güvenilirliği | G9 EK'ten çıkan not. GitHub ücretsiz hesaplarda zamanlanmış işleri seyreltiyor: yaklaşık 24 saatte 24 tur beklenirken 3 tur gerçekleşti. Bu projenin kontrolü dışında bir kısıt. Gerçekten saatlik çalışma şart olursa dışarıdan bir tetikleyici servis gerekir; izleme amacı için mevcut sıklık kabul edilebilir bulundu. |
| Adres gizlemede öneksiz sunucu adının da yakalanması | G8 denetiminden çıkan not. Hata metninde bir sunucu adı hiçbir önek olmadan tek başına geçerse ve API adresi bilinmiyorsa, o ad gizlenmeden kalabilir. Denetim acil görmedi: gerçek akışta ana akış hata metnini temizlerken API adresini her zaman veriyor, adres verildiğinde sunucu adı kesin olarak çıkarılıyor. Yani bu boşluk şu an gerçek bir turda oluşmuyor. |

## Bilinçli olarak kapsam dışı bırakılanlar

| Fikir | Neden şimdi değil |
|---|---|
| Streamlit paneli (tarayıcıda görsel ekran) | Yol haritasında opsiyonel; sadece zaman kalırsa |
| E-posta / Slack bildirimi | Telegram yeterli; ikinci kanal karmaşıklık ekler |
| Kimlik doğrulama gerektiren API'ler | Önce herkese açık adreslerle temel sistem oturmalı |

## Tamamlananlar

| Fikir | Ne zaman yapıldı |
|---|---|
| `slow_response` tespiti | **G8'de yapıldı** (Hafta 3, Gün 3-4). `checks` tablosu dolduruldu, son 10 başarılı kontrolün ortalaması referans alınıyor, 3 katı aşılırsa bulgu üretiliyor. Yanlış alarmı önlemek için en az 3 geçmiş kayıt şartı var. |
