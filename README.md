# API Contract Monitor

Dış API'lerdeki sessiz yapı değişikliklerini, son kullanıcı fark etmeden önce yakalayan otomatik izleme sistemi.

> **Durum:** Yapım aşamasında (Hafta 1 / 4). Bu dosya Hafta 4'te tam içerikle doldurulacak.

## Problem

Bağımlı olduğumuz dış servisler haber vermeden değişir: bir alan kaldırılır, bir tip değişir, bir adres bozulur. Bu değişiklikler genelde ancak bir kullanıcı şikayet ettiğinde fark edilir.

## Çözüm

Sistem izlenen servisleri saat başı kontrol eder, dönen yanıtın yapısını daha önce kaydettiği referansla karşılaştırır, bir sapma bulursa yorumlayıp anlık bildirim gönderir.

## Kullanılan teknolojiler

Python · SQLite · GitHub Actions · Telegram Bot API · LLM API

## Hafta 4'te eklenecek bölümler

- Mimari akış şeması
- Adım adım kurulum talimatları
- Örnek bildirim ekran görüntüsü
- Yapılandırma açıklaması
