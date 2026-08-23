# API Contract Monitor — Proje Yol Haritası ve Ajan Kuralları

> Bu dosya projenin tek referans kaynağıdır. Her yeni ajan oturumunda bu dosya okutulmalıdır.
> Ajan bu dosyadaki kurallara uymak zorundadır. Kurallarla çelişen bir talep gelirse ajan önce uyarmalıdır.

---

## 1. Proje Özeti

**Ne yapıyor:** Belirlenen dış API'leri periyodik olarak kontrol eden, dönen yanıtın yapısını (şemasını) daha önce kaydedilmiş referansla karşılaştıran, bir sapma tespit ettiğinde bunu yorumlayıp kullanıcıya bildirim gönderen otomatik izleme sistemi.

**Çözdüğü problem:** Dış API'ler haber vermeden değişir (alan silinir, tip değişir, endpoint bozulur). Bu değişiklikler genelde ancak son kullanıcı şikayet ettiğinde fark edilir. Bu sistem, sorunu kullanıcıdan önce yakalar.

**Kullanıcı profili:** Dış API'lere bağımlı yazılım ekipleri, mikroservis mimarileri, entegrasyon ağırlıklı projeler.

**Proje sahibinin durumu (ajan bunu bilmeli):**
- Yazılım öğrencisi, ilk otomasyon projesi
- Python'a derinlemesine hakim değil, akış seviyesinde takip etmek istiyor
- Kod okumadan ne olup bittiğini anlayabilmek için, her aşamada **kod içermeyen, düz Türkçe bir açıklama yazısı** istiyor (bkz. Bölüm 2.10)
- Süre: 4 hafta
- Bütçe: 0 TL — sadece ücretsiz servisler kullanılacak

---

## 2. Ajan Çalışma Kuralları

Bu bölüm ajanın uyması gereken kurallardır. İstisnasız geçerlidir.

### 2.1 Açıklama zorunluluğu
- Her kod üretiminden sonra, teknik terim kullanmadan, en fazla 5 madde halinde ne yapıldığını açıkla.
- Kod içine Türkçe yorum satırları ekle. Her fonksiyonun başında ne işe yaradığını 1 cümleyle yaz.
- Proje sahibi Python'a hakim değil. "Nasıl olsa anlar" varsayımıyla açıklama atlanmaz.

### 2.2 Kapsam kontrolü
- **MVP bitmeden yeni özellik eklenmez.** Sırayla ilerlenir.
- Proje sahibi kapsam dışı bir özellik isterse: ajan bunu `BACKLOG.md` dosyasına ekler ve "bunu şimdi mi yapalım yoksa v1 bitince mi" diye sorar.
- Büyük bir görevde ajan kodlamaya başlamadan önce ne yapacağını özetler; görevi bölmek gerekiyorsa gerekçesini açıklar.

### 2.3 Adım büyüklüğü
- Adım büyüklüğü için sabit bir sınır yoktur. Bir görev kaç fonksiyon veya kaç dosya gerektiriyorsa o kadarı tek adımda yapılır.
- Görev tek adımda halledilemeyecek kadar karmaşık veya uzunsa parçalara bölünebilir. Bu durumda ajan bölme gerekçesini ve parçaların sırasını önceden açıklar.
- Ölçüt dosya sayısı değil, **görev bütünlüğüdür**: adım sonunda anlamlı ve test edilebilir bir iş tamamlanmış olmalıdır.
- Her adımdan sonra kod çalıştırılabilir durumda olmalıdır. "Yarım bırakılmış, sonra tamamlanacak" kod bırakılmaz.
- Komutları ajan kendisi çalıştırır. Proje sahibinden terminal komutu çalıştırması istenmez.
- Ajan komutu çalıştırdıktan sonra sonucu düz Türkçe özetler: "Çalıştırdım, sistem şu yanıtı verdi, bu şu anlama geliyor."
- **İstisna — kritik komutlar:** Geri alınamaz veya riskli bir komut gerekiyorsa (veri silme, force push, geçmişi değiştirme, dosya üzerine yazma) ajan komutu çalıştırmadan önce durur ve 2-3 cümleyle ne olacağını, neyi etkileyeceğini açıklar, onay alır.
- Proje sahibi isterse kendisi de çalıştırabilir, ama bu bir zorunluluk değildir.

### 2.4 Onay kapıları (test ve commit)

Ajan **kesintisiz** ilerler. Sadece iki noktada durur ve proje sahibinden onay alır:

**KAPI 1 — Test onayı**
- Bir görevin kodu bittiğinde ajan testi kendisi çalıştırır ve durur.
- Sunacağı rapor:
  - Ne test edildi (düz Türkçe, kod yok)
  - Sonuç: geçti / geçmedi
  - Beklenen davranış ne, gerçekleşen ne
  - Bozarak test yapıldıysa: neyi bozdu, sistem doğru tepki verdi mi
- **Denetçi ajan raporu (zorunlu ek adım):**
  - Ana akış ajanı test raporunu sunduktan sonra durur. Proje sahibi bu aşamada ayrı bir oturumda çalışan denetçi ajandan bir rapor getirir.
  - Ana akış ajanı denetçi ajanı çalıştırmaz, yönlendirmez, görevini tanımlamaz. Sadece gelen raporu bekler.
  - Rapor geldiğinde ana akış ajanı raporu okur ve içindeki bulgulara göre hareket eder.
- Ardından şunu sorar: **"Bu adım tamamlandı sayılsın mı?"**
- **Çatışma durumu:** Denetçi raporu olumsuz veya şartlı ise, ana akış ajanı kendi başına karar veremez. Bulguları düz Türkçe özetler, kararı proje sahibi verir: düzeltme yapılsın mı, yoksa gerekçeyle geçilsin mi.
- Onay gelmeden commit'e geçilmez.

**KAPI 2 — Commit onayı**
- Test onayı alındıktan sonra ajan durur ve şunları sunar:
  - Hangi dosyalar değişti (liste)
  - Önerilen commit mesajı
  - Bu commit'ten sonra sistemin kazandığı yeni yetenek (1 cümle)
- Ardından şunu sorar: **"Commit atayım mı?"**
- Onay gelmeden commit atılmaz ve bir sonraki göreve geçilmez.

**Kapılar arası kural**
- Bu iki kapı dışında ajan onay için durmaz — kod yazarken, dosya oluştururken, komut çalıştırırken akışı kesmez.
- Tek istisna Bölüm 2.3'teki kritik komutlardır; onlar her zaman ayrıca onay gerektirir.
- Ajan bir görevi "tamamlandı" diye işaretlemek için her iki kapıdan da onay almış olmalıdır.
- Test geçmezse ajan commit kapısına gitmez; sorunu düzeltir ve test kapısına geri döner.
- Denetçi raporu gelmeden Kapı 1 tamamlanmış sayılmaz. Ana akış ajanı "denetçi raporunu atlayalım" öneremez.

### 2.5 Güvenlik kuralları
- API anahtarları, token'lar, şifreler **asla** kod içine yazılmaz.
- Tüm sırlar `.env` dosyasında tutulur, `python-dotenv` ile okunur.
- `.env` dosyası **mutlaka** `.gitignore` içinde olmalıdır.
- GitHub Actions için sırlar repository Secrets bölümünde tutulur.
- Ajan, sır içeren bir dosyayı commit etmeye çalışırsa kendini durdurur ve uyarır.

### 2.6 Hata yönetimi kuralı
- Ajan her yeni modülde şu soruyu kendisi sorar ve cevaplar: "Bu adımda ne ters gidebilir?"
- Cevabı liste halinde proje sahibine sunar, onay alır, sonra kodlar.
- Proje sahibinden "hangi hataları ele alalım" diye beklemez — öneriyi kendisi getirir.

### 2.7 Git kuralları
- Her çalışan aşamadan sonra commit atılır.
- Commit mesajları Türkçe ve açıklayıcı olur: `API şema karşılaştırma fonksiyonu eklendi`
- Riskli/deneysel işler için ayrı branch açılır.
- Ajan asla `git push --force`, `git reset --hard` gibi yıkıcı komutları onay almadan çalıştırmaz.

### 2.8 Bağımlılık kuralı
- Yeni bir kütüphane eklenmeden önce gerekçesi açıklanır ve onay alınır.
- Standart kütüphane ile çözülebilecek bir şey için dış kütüphane kurulmaz.
- Tüm bağımlılıklar `requirements.txt` içinde tutulur.

### 2.9 Kod düzeni — spagetti kod yasağı

Spagetti kod yazılmaz. Bu bir tercih değil, kuraldır. Ajan aşağıdaki sinyallerden herhangi birini üretiyorsa durur ve yapıyı düzeltir:

- **Tek sorumluluk ihlali:** Bir fonksiyon birden fazla iş yapıyor (hem veri çekip hem kaydedip hem bildirim gönderiyor gibi). Her fonksiyon tek bir iş yapar.
- **Kod tekrarı:** Aynı kod bloğu birden fazla yerde tekrarlanıyor. Tekrarlanan mantık ayrı bir fonksiyona çıkarılır.
- **Aşırı uzun fonksiyon:** Yaklaşık 50 satırı geçen fonksiyonlar. Bu sert bir sınır değil, "bu fonksiyon çok iş yapıyor olabilir" sinyalidir.
- **Modül karışması:** Bir modül başka bir modülün işine giriyor (örnek: `comparator.py` içinden doğrudan Telegram çağrılması). Modüller Bölüm 4'teki sorumluluk dağılımına sadık kalır.
- **Derin iç içe bloklar:** Üç kattan fazla iç içe geçmiş `if`/`for` blokları. Erken çıkış (early return) veya ayrı fonksiyon ile sadeleştirilir.
- **Dosya yığılması:** Bölüm 4'teki klasör yapısına uyulmaması, her şeyin tek dosyaya yığılması.
- **Anlamsız isimlendirme:** `data`, `temp`, `x`, `islem2` gibi ne yaptığı anlaşılmayan isimler. İsimler ne yaptığını söylemelidir.

**Neden bu kural var:** Proje sahibi kodu satır satır okumuyor, akış seviyesinde takip ediyor. Kod dağınıklaşırsa hem proje sahibi kontrolü kaybeder hem de sonraki haftalarda üzerine ekleme yapmak zorlaşır. Ayrıca bu proje bir CV çalışmasıdır; kod kalitesi doğrudan değerlendirilecektir.

**Uygulama:** Ajan bir görevi bitirmeden önce kendi ürettiği koda bu listeyle bakar. İhlal varsa düzeltir, sonra Kapı 1'e geçer.

### 2.10 Kod içermeyen ilerleme günlüğü (zorunlu)
- Her tamamlanan görevden sonra ajan, `ILERLEME.md` dosyasına yeni bir kayıt ekler.
- Bu kayıt **hiç kod içermez**. Değişken adı, fonksiyon adı, komut, dosya yolu geçmez.
- Amaç: proje sahibinin kodu hiç açmadan sistemin ne durumda olduğunu anlaması.
- Her kayıt şu 4 başlığı içerir:
  1. **Ne yaptık:** Günlük konuşma diliyle, 2-3 cümle
  2. **Sistem şimdi ne yapabiliyor:** Önceki duruma göre kazanılan yeni yetenek
  3. **Neden böyle yaptık:** Alınan kararın gerekçesi, varsa alternatifi
  4. **Sırada ne var:** Bir sonraki adım
- Yazım kuralı: teknik terim kullanılacaksa parantez içinde günlük dilde karşılığı verilir.
  Örnek: "şema (API'nin döndürdüğü verinin yapısı)"
- Ajan bu dosyayı yazmadan görevi "tamamlandı" olarak işaretlemez.

### 2.11 Model ve mod kullanımı
- Mimari/tasarım kararları → **Plan modu**, `opusplan`
- Kod yazımı, düzeltme, test → **Default mod**, Sonnet
- Küçük düzeltmeler için plan modu kullanılmaz (gereksiz maliyet)

---

## 3. Teknik Stack

| Amaç | Araç | Not |
|---|---|---|
| Dil | Python 3.11+ | |
| IDE | Antigravity (Claude Code ajanı ile) | |
| Versiyon kontrol | Git + GitHub | |
| HTTP istekleri | `requests` | |
| Ortam değişkenleri | `python-dotenv` | |
| Veri saklama | SQLite (`sqlite3`, standart kütüphane) | Ek kurulum gerektirmez |
| Zamanlama | GitHub Actions (cron) | Ücretsiz |
| Bildirim | Telegram Bot API | Ücretsiz, kurulumu kolay |
| LLM yorumlama | Google AI Studio (Gemini free tier) veya Groq | Ücretsiz kota |
| Dashboard (opsiyonel) | Streamlit | Sadece zaman kalırsa |
| Test edilecek API'ler | JSONPlaceholder, GitHub API, CoinGecko, arXiv | Hepsi ücretsiz/public |

**Kural:** Bu listede olmayan bir araç, gerekçesi açıklanıp onaylanmadan projeye girmez.

---

## 4. Klasör Yapısı

```
api-contract-monitor/
├── .github/
│   └── workflows/
│       └── monitor.yml          # GitHub Actions zamanlayıcı
├── src/
│   ├── __init__.py
│   ├── fetcher.py               # API'ye istek atar, yanıtı döndürür
│   ├── schema.py                # JSON'dan şema çıkarır
│   ├── comparator.py            # İki şemayı karşılaştırır  [PROJENİN KALBİ]
│   ├── storage.py               # SQLite okuma/yazma
│   ├── notifier.py              # Telegram bildirimi gönderir
│   ├── analyzer.py              # LLM ile değişikliği yorumlar (Hafta 4)
│   └── main.py                  # Hepsini sırayla çalıştırır
├── config/
│   └── apis.json                # İzlenecek API listesi
├── data/
│   └── monitor.db               # SQLite veritabanı (gitignore'da)
├── tests/
│   └── test_comparator.py       # Karşılaştırma testleri
├── .env                         # Sırlar (gitignore'da)
├── .env.example                 # Örnek sır dosyası (commit edilir)
├── .gitignore
├── requirements.txt
├── README.md
├── ILERLEME.md                  # Ajanın yazdığı, kod içermeyen ilerleme günlüğü
├── TODO.md                      # Proje sahibinin haftalık notları
├── BACKLOG.md                   # Sonraya bırakılan fikirler
└── PROJE_YOL_HARITASI.md        # Bu dosya
```

---

## 5. Veri Modeli

### 5.1 `config/apis.json` formatı
```json
{
  "apis": [
    {
      "id": "github-user",
      "name": "GitHub Kullanıcı API",
      "url": "https://api.github.com/users/octocat",
      "method": "GET",
      "headers": {},
      "timeout": 10,
      "enabled": true
    }
  ]
}
```

### 5.2 SQLite tabloları

**`schemas`** — Her API için kayıtlı referans şema
| Sütun | Tip | Açıklama |
|---|---|---|
| id | INTEGER | Otomatik artan |
| api_id | TEXT | apis.json'daki id |
| schema_json | TEXT | Çıkarılan şema (JSON metni) |
| created_at | TIMESTAMP | Kayıt zamanı |

**`checks`** — Her kontrol turunun kaydı
| Sütun | Tip | Açıklama |
|---|---|---|
| id | INTEGER | Otomatik artan |
| api_id | TEXT | Hangi API |
| status | TEXT | ok / changed / error |
| response_time_ms | INTEGER | Yanıt süresi |
| checked_at | TIMESTAMP | Kontrol zamanı |

**`changes`** — Tespit edilen değişiklikler
| Sütun | Tip | Açıklama |
|---|---|---|
| id | INTEGER | Otomatik artan |
| api_id | TEXT | Hangi API |
| change_type | TEXT | field_removed / type_changed / field_added |
| details | TEXT | Değişikliğin açıklaması |
| llm_comment | TEXT | LLM yorumu (Hafta 4) |
| detected_at | TIMESTAMP | Tespit zamanı |

### 5.3 Şema formatı (comparator'ın karşılaştıracağı yapı)
```json
{
  "login": "string",
  "id": "integer",
  "public_repos": "integer",
  "created_at": "string",
  "plan": {
    "name": "string",
    "space": "integer"
  }
}
```
İç içe yapılar (nested) desteklenmeli. Diziler için ilk elemanın tipi baz alınır.

---

## 6. Tespit Edilecek Değişiklik Tipleri

Ajan `comparator.py` yazarken bu listenin hepsini kapsamalıdır:

| Tip | Açıklama | Önem |
|---|---|---|
| `field_removed` | Referansta olan alan artık yok | **Kritik** — uygulamayı kırar |
| `type_changed` | Alanın tipi değişti (int → string) | **Kritik** |
| `field_added` | Yeni alan eklendi | Bilgi amaçlı |
| `nested_changed` | İç içe objede değişiklik | Kritik |
| `response_error` | API hata kodu döndürdü (4xx/5xx) | **Kritik** |
| `timeout` | Yanıt gelmedi | Kritik |
| `invalid_json` | Yanıt JSON olarak parse edilemedi | Kritik |
| `slow_response` | Yanıt süresi referansın 3 katından fazla | Uyarı |

---

## 7. Haftalık Yol Haritası

### HAFTA 1 — Temel ve İlk Çalışan Sistem

**Hedef:** Bir API'ye istek atıp yanıtını görebilen, versiyon kontrolü kurulmuş bir proje.

#### Gün 1-2: Ortam kurulumu
- [ ] Python 3.11+ kurulumu, `python --version` ile doğrula
- [ ] Antigravity kurulumu ve Claude Code ajanı bağlantısı
- [ ] GitHub'da `api-contract-monitor` reposu oluştur (public)
- [ ] Yerelde `git clone`, `python -m venv venv`, sanal ortamı aktifleştir
- [ ] `.gitignore` oluştur (venv, .env, data/, __pycache__ içermeli)
- [ ] İlk commit: "Proje iskeleti oluşturuldu"

**Ajan modu:** Default / Sonnet

#### Gün 3-4: Mimari planlama
- [ ] **Plan modunda** (`opusplan`) ajana bu dosyayı okut ve mimari planı çıkarttır
- [ ] Klasör yapısını oluştur (Bölüm 4'teki gibi)
- [ ] `requirements.txt` oluştur, `requests` ve `python-dotenv` ekle, kur
- [ ] Ajanın ürettiği implementation plan artifact'ini oku, anlamadığın yere yorum bırak

**Ajan modu:** Plan modu / `opusplan`

#### Gün 5-7: İlk çalışan script
- [ ] `config/apis.json` dosyasını oluştur, içine 1 test API'si koy (JSONPlaceholder önerilir)
- [ ] `src/fetcher.py` yaz: config'i okur, API'ye istek atar, yanıtı ve süreyi döndürür
- [ ] Ajan scripti çalıştırır, dönen JSON yanıtını sana özetler
- [ ] `print()` ekleyerek her adımda ne olduğunu izle
- [ ] Commit: "API istek modülü eklendi"

**Ajan modu:** Default / Sonnet

**Hafta 1 bitiş kriteri (Definition of Done):**
> Terminalde `python src/fetcher.py` çalıştırdığında bir API'nin JSON yanıtı ekrana yazılıyor, kod GitHub'a push edilmiş durumda.

---

### HAFTA 2 — Şema Çıkarma ve Karşılaştırma (Projenin Kalbi)

**Hedef:** Sistemin bir değişikliği tespit edebilmesi. Bu haftanın çıktısı projenin en kritik parçası.

#### Gün 1-2: Şema çıkarma tasarımı
- [ ] **Plan modunda** şema çıkarma yaklaşımını tasarlat (iç içe objeler, diziler, null değerler nasıl ele alınacak)
- [ ] Planı oku, kabul et
- [ ] `src/schema.py` yaz: JSON alır, şema (alan → tip haritası) döndürür
- [ ] Elle test: farklı JSON'lar ver, doğru şema çıkıyor mu bak

**Ajan modu:** Plan modu → Default

#### Gün 3-4: Depolama katmanı
- [ ] `src/storage.py` yaz: SQLite tablolarını oluşturur (Bölüm 5.2), şema kaydeder/okur
- [ ] İlk çalıştırmada referans şema kaydedilmeli, sonraki çalıştırmalarda okunmalı
- [ ] `data/monitor.db` dosyasının oluştuğunu doğrula
- [ ] Commit: "SQLite depolama katmanı eklendi"

**Ajan modu:** Default / Sonnet

#### Gün 5-7: Karşılaştırma mantığı
- [ ] **Plan modunda** karşılaştırma algoritmasını tasarlat
- [ ] `src/comparator.py` yaz: Bölüm 6'daki **tüm** değişiklik tiplerini tespit etmeli
- [ ] `tests/test_comparator.py` yaz: her değişiklik tipi için en az 1 test
- [ ] **Manuel test:** `data/monitor.db` içindeki referans şemayı elle değiştir, sistem yakalıyor mu bak
- [ ] Commit: "Şema karşılaştırma mantığı eklendi"

**Ajan modu:** Plan modu → Default

**Hafta 2 bitiş kriteri:**
> Referans şemayı kasıtlı bozduğunda sistem terminalde "field_removed: age" gibi doğru bir tespit yazdırıyor. Testler geçiyor.

**⚠️ Kritik uyarı:** Bu hafta gecikirse Hafta 4'teki LLM katmanı iptal edilir. Temel sistem her zaman önceliklidir.

---

### HAFTA 3 — Bildirim, Hata Yönetimi ve Otomatik Çalışma

**Hedef:** Sistemin gerçekten otomatik çalışması ve seni bilgilendirmesi.

#### Gün 1-2: Telegram bildirimi
- [ ] Telegram'da `@BotFather` ile bot oluştur, token al
- [ ] Kendi chat ID'ni öğren (`@userinfobot` kullanabilirsin)
- [ ] `.env` dosyasına `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` ekle
- [ ] `.env.example` oluştur (değerler boş, sadece anahtar isimleri)
- [ ] `src/notifier.py` yaz: mesaj gönderir, mesajı okunabilir biçimde formatlar
- [ ] Test mesajı gönder, telefonuna geldiğini doğrula
- [ ] Commit: "Telegram bildirim modülü eklendi"

**Ajan modu:** Default / Sonnet

#### Gün 3-4: Hata yönetimi ve ana akış
- [ ] Ajandan "bu sistemde ne ters gidebilir" listesi iste, onayla
- [ ] Tüm modüllere hata yakalama ekle:
  - Ağ hatası / timeout
  - Geçersiz JSON
  - HTTP 4xx/5xx yanıtlar
  - Veritabanı hatası
  - Telegram gönderim hatası (bildirim gitmezse sistem çökmemeli)
  - Config dosyası eksik/bozuk
- [ ] `src/main.py` yaz: tüm modülleri sırayla çalıştıran ana akış
- [ ] Loglama ekle (`logging` modülü, standart kütüphane)
- [ ] **Bozarak test:** Ajandan config'e yanlış URL yazıp çalıştırmasını iste, sistemin düzgün hata verdiğini sana raporlamasını iste
- [ ] Commit: "Hata yönetimi ve ana akış eklendi"

**Ajan modu:** Default / Sonnet

#### Gün 5-7: GitHub Actions ile otomatikleştirme
- [ ] `.github/workflows/monitor.yml` oluştur
- [ ] Cron ayarı: saatte bir çalışacak şekilde (`0 * * * *`)
- [ ] GitHub repo Settings → Secrets bölümüne token'ları ekle
- [ ] Veritabanı kalıcılığı için çözüm: ya Actions cache ya da sonuçları repo'ya commit etme (ajan öneri sunmalı)
- [ ] Workflow'u manuel tetikle (`workflow_dispatch`), log'ları kontrol et
- [ ] Bildirimin gerçekten geldiğini doğrula
- [ ] Commit: "GitHub Actions otomasyonu eklendi"

**Ajan modu:** Default / Sonnet

**Hafta 3 bitiş kriteri:**
> Sisteme hiç dokunmadan, saatlik olarak otomatik çalışıyor ve bir değişiklik olduğunda Telegram'a bildirim düşüyor. Bu noktada proje **tamamlanmış** sayılır — sonraki hafta bonus.

---

### HAFTA 4 — LLM Katmanı ve Sunum

**Hedef:** Projeyi CV'de güçlü kılan katmanı eklemek ve düzgün paketlemek.

#### Gün 1-3: LLM yorumlama katmanı
- [ ] Google AI Studio'dan ücretsiz API anahtarı al, `.env`'e ekle
- [ ] **Plan modunda** prompt tasarımını yaptır: LLM'e ne gönderilecek, ne dönmesi bekleniyor
- [ ] `src/analyzer.py` yaz: tespit edilen değişikliği LLM'e gönderir, "breaking change mi, etkisi ne, ne yapılmalı" yorumu alır
- [ ] LLM yanıtını bildirime ekle
- [ ] **Hata yönetimi:** LLM API'si çökerse sistem çalışmaya devam etmeli, sadece yorum olmadan bildirim gitmeli
- [ ] Kota aşımına karşı önlem: sadece kritik değişikliklerde LLM çağrılmalı
- [ ] Commit: "LLM analiz katmanı eklendi"

**Ajan modu:** Plan modu → Default

#### Gün 4-5: Dokümantasyon
- [ ] `README.md` yaz. İçermesi gerekenler:
  - Problem tanımı (neden bu proje var)
  - Çözüm özeti
  - Mimari diyagramı (basit bir akış şeması)
  - Kullanılan teknolojiler
  - Kurulum adımları (adım adım, çalıştırılabilir komutlarla)
  - Örnek çıktı (Telegram bildiriminin ekran görüntüsü)
  - Konfigürasyon açıklaması
- [ ] `.env.example` güncel mi kontrol et
- [ ] Kod içindeki gereksiz `print()` ve yorumları temizle

**Ajan modu:** Default / Sonnet

#### Gün 6-7: Cila ve sunum
- [ ] Kod gözden geçirme: ölü kod var mı, isimlendirmeler anlamlı mı
- [ ] Demo hazırlığı: sistemin bir değişikliği yakalayıp bildirim gönderdiği kısa video/GIF
- [ ] CV satırını yaz (Bölüm 9'daki şablon)
- [ ] LinkedIn/portföy paylaşımı (opsiyonel)
- [ ] Son commit ve push

**Ajan modu:** Default / Sonnet

**Hafta 4 bitiş kriteri:**
> Repo'ya giren biri README'yi okuyup projenin ne yaptığını 30 saniyede anlıyor ve kurulum adımlarını takip ederek çalıştırabiliyor.

---

## 8. Proje Sahibinin Haftalık Takip Rutini

Toplam ~1 saat/hafta. Kod okumak zorunda değilsin.

| Ne zaman | Ne yapacaksın | Süre |
|---|---|---|
| Her adım sonrası | Ajanın çalıştırma sonucu özetini oku, beklenen sonuç mu diye bak | 5 dk |
| Haftada 1 | Ajandan girdiyi bozarak test etmesini iste (yanlış URL, bozuk şema), sonucu oku | 10 dk |
| Her adım sonrası | `ILERLEME.md`'ye eklenen yeni kaydı oku (kod içermez) | 5 dk |
| Haftada 1 | Ajanın walkthrough artifact'lerini oku | 15 dk |
| Haftada 1 | `TODO.md`'ye kendi cümlelerinle "sistem şu an ne yapabiliyor" yaz | 10 dk |
| Haftada 1 | Ana dosyaların fonksiyon isimlerini oku, akışı takip et | 15 dk |

**Güvenlik ağı:** Her çalışan aşamada commit at. Bir şey bozulursa `git checkout .` veya `git reset --hard HEAD` ile geri dön. Deneysel işler için `git branch deneme` ile ayrı dal aç.

---

## 9. Çıktı Kriterleri ve CV Sunumu

### Proje "bitti" sayılması için gerekenler
- [ ] En az 3 farklı API izleniyor
- [ ] Tüm değişiklik tipleri (Bölüm 6) tespit edilebiliyor
- [ ] Hata durumlarında sistem çökmüyor
- [ ] GitHub Actions ile otomatik çalışıyor
- [ ] Bildirimler geliyor
- [ ] README eksiksiz
- [ ] Sırlar repo'da açıkta değil
- [ ] Testler yazılmış ve geçiyor

### CV satırı şablonu
> **API Contract Monitor** — Python, GitHub Actions, SQLite, LLM API, Telegram Bot API
> Dış servislerdeki şema değişikliklerini otomatik tespit edip breaking change analizi yapan izleme sistemi. Saatlik cron ile birden fazla endpoint izleniyor; tespit edilen değişiklikler LLM ile yorumlanıp anlık bildirim olarak iletiliyor.

### Mülakatta gelebilecek sorular (hazırlıklı ol)
1. "Postman, Pact gibi araçlar varken neden bunu yazdın?" → Öğrenme amaçlı + kendi ihtiyacıma göre özelleştirilmiş
2. "Şema karşılaştırmayı nasıl yaptın?" → `comparator.py`'yi anlayabilecek kadar oku
3. "Hangi hata durumlarını ele aldın?" → Bölüm 6 ve Hafta 3 listesi
4. "Sırları nasıl yönettin?" → .env + GitHub Secrets
5. "Nasıl ölçeklendirirdin?" → Config bazlı yapı sayesinde yeni API eklemek sadece JSON'a satır eklemek

---

## 10. Risk Yönetimi ve Öncelik Sırası

Zaman yetmezse **bu sırayla** feda edilir:

1. ❌ Streamlit dashboard (zaten opsiyonel)
2. ❌ LLM yorumlama katmanı (Hafta 4a)
3. ❌ `slow_response` tespiti
4. ❌ Test dosyaları (ama tercihen kalsın)
5. ⚠️ Buradan sonrası feda edilemez

**Asla feda edilmeyecekler:** fetcher, schema, comparator, storage, notifier, main, hata yönetimi, GitHub Actions, README.

**Kırmızı çizgi:** Hafta 2 sonunda karşılaştırma mantığı çalışmıyorsa, kapsam derhal daraltılır (tek API, sadece field_removed ve type_changed tespiti) ve kalan zaman temel sistemi bitirmeye harcanır.

---

## 11. YAPILANLAR — Tamamlanan Görevler Kaydı

> Bu bölüm, denetçi ajanın "neyi denetleyeceğim" sorusuna tek bakışta cevap bulması içindir.
> Kısa ve kuru tutulur. Anlatı ve gerekçe `ILERLEME.md` dosyasına yazılır, buraya değil.
> Ana akış ajanı, Kapı 2 (commit) onayı alındıktan sonra bu tabloya satır ekler.

| # | Görev | Etkilenen dosyalar | Test durumu | Denetçi kararı | Commit | Tarih |
|---|---|---|---|---|---|---|
| 1 | *(örnek) API istek modülü* | *src/fetcher.py, config/apis.json* | *Geçti* | *Onaylandı* | *abc1234* | *—* |

**Sütun açıklamaları:**
- **Görev:** Yol haritasındaki hangi adım tamamlandı
- **Etkilenen dosyalar:** Oluşturulan veya değiştirilen dosyalar
- **Test durumu:** Geçti / Geçmedi / Kısmen
- **Denetçi kararı:** Onaylandı / Şartlı onaylandı / Onaylanmadı — şartlı veya onaylanmadıysa yanına tek cümlelik gerekçe
- **Commit:** Commit hash'inin ilk 7 karakteri
- **Tarih:** Görev tamamlanma tarihi

**Bekleyen düzeltmeler** (denetçi şartlı onay verdiyse buraya yazılır):
- *(henüz yok)*

---

## 12. Ajan Oturumu Başlangıç Şablonu

Her yeni oturumda ajana şunu ver:

```
Bu dosyayı oku: PROJE_YOL_HARITASI.md

Ben Python'a hakim değilim, akış seviyesinde takip ediyorum.
Şu an Hafta [X], Gün [Y] aşamasındayım.
Tamamlanan görevler: Bölüm 11'deki YAPILANLAR tablosuna bak

Bugünkü hedef: [görev]

Kurallar:
- Bölüm 2'deki ajan kurallarına uy
- Kod yazmadan önce ne yapacağını 5 maddede anlat
- Kod yazdıktan sonra teknik terim kullanmadan açıkla
- Komutları sen çalıştır, bana sadece sonucu düz Türkçe özetle
- Sadece iki noktada dur ve onayımı al: (1) testi çalıştırıp sonucu sunduğunda, (2) commit atmadan önce. Bunlar dışında akışı kesme.
- Test raporundan sonra dur, sana bir denetçi raporu ileteceğim. O rapor gelmeden commit'e geçme. Rapor olumsuzsa kendi başına karar verme, bana sor.
- Test geçmeden commit önerme; onay almadan bir sonraki göreve geçme
- Kritik/geri alınamaz bir komut gerekiyorsa önce dur, ne olacağını kısaca açıkla ve onayımı al
- Görev bitince ILERLEME.md'ye kod içermeyen bir kayıt ekle (Bölüm 2.10 formatında)
- Commit onayı aldıktan sonra Bölüm 11'deki YAPILANLAR tablosuna satır ekle
- Spagetti kod yazma (Bölüm 2.9) — kodu bitirmeden önce o listeyle kendini kontrol et
- Kapsam dışına çıkma, yeni fikirleri BACKLOG.md'ye yaz
```
