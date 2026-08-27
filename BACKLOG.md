# Sonraya Bırakılanlar

> Proje kapsamı dışında kalan fikirler buraya yazılır.
> Kural: temel sistem bitmeden buradan hiçbir madde alınıp yapılmaz.
> Bir fikir aklına geldiğinde silinmesin diye buraya not düşülür, sonra karar verilir.

## Bekleyen fikirler

| Fikir | Neden şimdi değil |
|---|---|
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
