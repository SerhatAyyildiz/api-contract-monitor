# İlerleme Günlüğü

> Bu dosya kod içermez. Amacı, projeyi hiç açmadan sistemin ne durumda olduğunu anlayabilmektir.
> En yeni kayıt en üsttedir.

---

## Kayıt 8 — Sistem artık tek başına baştan sona çalışıyor

**Tarih:** 27 Ağustos 2026
**Aşama:** Hafta 3, Gün 3-4

### Ne yaptık

Şimdiye kadar sistemin parçaları vardı ama birbirinden bağımsızdı — biri adrese istek atıyor, biri yapıyı karşılaştırıyor, biri haber veriyordu, ama hiçbiri bir araya gelip tek bir bütün oluşturmuyordu. Bu adımda hepsini birbirine bağlayan bir "orkestra şefi" yazıldı: artık tek bir komutla sistem baştan sona kendi kendine çalışıyor.

Bunun yanında sisteme bir sağlamlık katmanı eklendi. Daha önce "acaba bir şey ters giderse ne olur" sorusunun cevabı belirsizdi. Bu turda dokuz farklı aksilik ihtimali tek tek düşünüldü (bağlantı kopması, adresin cevap vermemesi, bozuk cevap, veri saklama sorunu, haber verme sorunu gibi) ve her biri kasıtlı olarak tetiklenip sistemin gerçekten çökmediği kanıtlandı.

Ayrıca bir önceki oturumdan yarım kalmış bir çalışma devralındı. O çalışma çöpe atılmadı; satır satır incelendi, gerçekten üç yanlış davranış bulundu ve düzeltildi. En önemlisi: sistem "referans" olarak sakladığı bilgiyi her kontrolde gereksiz yere baştan yazıyordu — bu hem yer israfıydı hem de bir alan kaybolup sonra geri gelirse aynı haberin ikinci kez gönderilmesine yol açabilirdi. Artık bu bilgi yalnızca gerçekten bir değişiklik olduğunda güncelleniyor.

### Sistem şimdi ne yapabiliyor

- Tek bir komutla, hiç elle müdahale gerekmeden, baştan sona bir kontrol turu tamamlayabiliyor.
- Bir adrese ulaşılamasa, cevap bozuk gelse, saklama alanı sorun çıkarsa veya haber verme kanalı çalışmasa bile sistem çökmüyor; sorunu not edip diğer işlerine devam ediyor.
- Birden fazla adres izlendiğinde, birindeki sorun diğerlerinin kontrol edilmesini engellemiyor.
- Bir adresin normalden çok daha yavaş cevap verdiği durumları da artık fark edebiliyor (geçmiş cevap sürelerini biriktirip kıyaslıyor).
- Hata mesajlarının içinde yanlışlıkla bir adresin tam bilgisinin görünmesi engellendi — bu bilgi ileride bir erişim şifresi taşıyabileceği için özellikle önemliydi ve test sırasında fark edilip kapatıldı.
- Windows'ta bazı programlarla (örneğin Not Defteri) düzenlenen ayar dosyalarının görünmez bir işaret yüzünden okunamaması sorunu da bu turda giderildi.

### Neden böyle yaptık

**Neden devralınan yarım işi silip baştan yazmadık:** İncelendiğinde çalışır durumda olduğu görüldü, sadece hiç sınanmamıştı. Silmek hem gereksiz emek kaybı olurdu hem de riski azaltmazdı — asıl güvence sınamaktan geliyor, yeniden yazmaktan değil. Bu yüzden koru-ve-denetle yolu seçildi.

**Neden "referans bilginin gereksiz güncellenmesi" bu kadar önemliydi:** Bu sistemin bütün amacı, bir şey değiştiğinde bunu fark edip haber vermek. Eğer referans bilgi kendini sürekli tazelerse, sistem zamanla neyin "normal" olduğunu unutabilir ve aynı sorunu tekrar tekrar yeni bir şeymiş gibi bildirebilir. Bu, güvenilirliği doğrudan zedeleyen bir sorundu.

**Neden dokuz aksilik ihtimalini tek tek kasıtlı olarak tetikledik:** "Muhtemelen çalışır" ile "denedim, çalıştığını gördüm" arasında büyük fark var. Bu sistem gözetimsiz, saatlik olarak kendi kendine çalışacak; kimse başında durup "şimdi ne oldu" diye bakmayacak. Bu yüzden aksilik durumlarının gerçekten güvenli bir şekilde ele alındığından emin olmak, gelecekte fark edilmeyen bir sessiz çökmeden çok daha değerliydi.

**Neden adres bilgisinin gizlenmesi bir öncelik oldu:** Şu an izlenen adresler herkese açık, ama ileride bir erişim şifresi gerektiren bir adres eklenmesi mümkün. Böyle bir adres bir hata mesajının içinde görünürse, o şifre farkında olmadan hem ekrana hem haber kanalına hem saklama alanına sızabilirdi. Bu, küçük bir ayrıntı gibi görünse de geri dönüşü zor bir güvenlik sorunudur; bu yüzden fark edilir edilmez düzeltildi.

### Sırada ne var

Sistem artık elle çalıştırıldığında baştan sona doğru işliyor. Bir sonraki adım, bunu insan müdahalesinden tamamen bağımsız hale getirmek: sistemin belirli aralıklarla (saatte bir) kendiliğinden çalışmasını sağlayacak bir zamanlayıcı kurulacak. Bu kurulduğunda proje, yol haritasının üçüncü haftasının bitiş çizgisine ulaşmış olacak.

## Kayıt 7 — Sistem artık haber verebiliyor

**Tarih:** 26 Ağustos 2026
**Aşama:** Hafta 3, Gün 1-2

### Ne yaptık

Şimdiye kadar sistem bir değişikliği tespit edebiliyordu ama bunu kimseye söylemiyordu — bulgular yalnızca ekranda kalıyordu. Bu adımda sisteme, bulduğu değişikliği telefona haber verme yeteneği kazandırdık.

Önce sizin tarafınızda birkaç adım tamamlandı: Telegram üzerinde bir bot oluşturuldu, sizin hesabınızın kimliği öğrenildi, bu bilgiler gizli ayar dosyasına yazıldı. Ardından bu bilgileri kullanıp gerçekten mesaj gönderen parçayı yazdık.

Kodlamadan önce mesajın nasıl görüneceğine dair bir tasarım kararı aldık: ciddi olan değişiklikler ile sadece bilgilendirme amaçlı olanlar ayrı gruplarda, renkli bir işaretle gösterilecekti. Böylece telefona bakıldığında bir saniyede "acil bir şey var mı" sorusu cevaplanabilecek.

### Sistem şimdi ne yapabiliyor

- Bir değişiklik tespit ettiğinde artık bunu telefona bildirebiliyor.
- Bildirimde ciddi olan değişiklikler ile sadece bilgi amaçlı olanlar birbirinden ayrılıyor; hangisinin acil olduğu ilk bakışta anlaşılıyor.
- Bildirim çok fazla değişiklik içeriyorsa mesajı olması gerekenden uzun tutmuyor, "bunun dışında şu kadar değişiklik daha var" diye özetliyor.
- Bildirim gönderiminde herhangi bir aksilik olursa (bağlantı sorunu, ayarların eksik olması, Telegram'ın hata vermesi) sistem çökmüyor; sadece gönderemediğini not edip devam ediyor.
- **Bunu gerçekten sınadık:** örnek bir bildirim gönderildi ve telefona ulaştığı gözle görülerek doğrulandı.

### Neden böyle yaptık

**Neden bildirim gönderen parça, bir aksilik olduğunda sistemi durdurmuyor:** Bir bildirimin gidip gitmemesi, sistemin asıl işini (değişiklik takibini) etkilememeli. Telefon kapalıysa ya da internet o an kesilmişse bile, sistem kontrolüne devam etmeli ve bir sonraki turda yine denemeli. Durması, tek bir aksak bildirim yüzünden bütün takibi durdurmak anlamına gelirdi.

**Neden mesajları ciddi/bilgi diye ikiye ayırdık:** Her değişiklik aynı önemde değil. Bir alanın tamamen kaybolması ile yeni bir alanın eklenmesi çok farklı şeyler — biri uygulamanızı bozabilir, diğeri sadece bilgi niteliğinde. İkisini aynı kefeye koyup tek bir liste halinde göndermek, telefonda bakan kişiyi (sizi) her seferinde bütün listeyi okumaya zorlardı. Ayırınca gerçekten önemli olan öne çıkıyor.

**Neden erişim anahtarının hata mesajlarına karışmamasına özellikle dikkat ettik:** Telefonunuza mesaj göndermek için kullanılan adresin içinde, o adrese özel bir erişim anahtarı geçiyor. Bir hata oluştuğunda, o hatayı açıklayan mesaj genellikle adresin tamamını da içeriyor. Bu mesaj olduğu gibi ekrana yazılsaydı, anahtar da yanlışlıkla görünür olurdu. Bunu fark edip özellikle temizledik ve bunun gerçekten çalıştığını ayrı bir sınamayla kanıtladık — bu proje için gizli bilgi sızıntısı hep en ciddi risk olarak görülüyor.

**Neden mesajı zenginleştirilmiş biçim yerine düz metin olarak gönderdik:** Bazı platformlar mesaj içinde kalın yazı, madde işareti gibi biçimlendirmelere izin verir, ama bunun için mesajın belirli karakterlere (alt çizgi, köşeli parantez gibi) özel anlam yüklemesi gerekir. Bizim değişiklik bulgularımızda bu karakterler zaten doğal olarak geçebiliyor (örneğin bir liste içindeki bir alanın adı). Zenginleştirilmiş biçim kullansaydık, bu karakterler mesajı bozabilir hatta gönderimi tamamen başarısız kılabilirdi. Düz metin bu riski baştan ortadan kaldırdı.

**Bağımsız denetim ne dedi:** Denetim, bildirimin gerçekten çalıştığını ve aksilik durumlarında sistemin çökmediğini doğruladı. İki küçük konuyu (gerçek bir hata koduyla hiç denenmemiş olması, art arda çok sayıda bildirim gönderilmesi durumu) not etti ama bunların acil olmadığını, şimdilik bekletilebileceğini söyledi.

### Sırada ne var

Hafta 3'ün devamı:

1. Şimdiye kadar yazılan tüm parçaları (veri çekme, yapı çıkarma, karşılaştırma, bildirim) sırayla çalıştıran bir ana akış yazılacak. Bu, sistemin tek bir komutla uçtan uca çalışmasını sağlayacak.
2. Bu adımda, bir önceki bölümde bilerek ertelenmiş birkaç durumun (adresin hata vermesi, yanıtın hiç gelmemesi gibi) nasıl ele alınacağı da netleşecek.
3. Ardından sistem, insana hiç dokunmadan kendi kendine, düzenli aralıklarla çalışır hale getirilecek.

---

## Kayıt 6 — Sistem artık değişikliği görebiliyor (Hafta 2 tamamlandı)

**Tarih:** 26 Ağustos 2026
**Aşama:** Hafta 2, Gün 5-7 — **Hafta 2 burada bitti**

### Ne yaptık

Şimdiye kadar sistem bir adrese bağlanıp veri getirebiliyor, getirdiğinin yapısını okuyabiliyor ve bunu hafızasına alabiliyordu. Ama hâlâ yapamadığı tek şey vardı: **iki hali karşılaştırıp "ne değişmiş" diyebilmek.** Bu adımda onu yaptık — projenin var oluş sebebi olan parça.

Kodlamaya başlamadan önce bir tasarım turu yaptık, çünkü burada gerçek bir karar vardı: sistemin yakalaması gereken sekiz durum var, ama bunların yalnızca dördü gerçekten "iki yapıyı karşılaştırmakla" bulunuyor. Diğer dördü (adres hata verdi, yanıt gelmedi, yanıt okunamadı, yanıt yavaştı) aslında bambaşka bir konu — onlar veri getirme aşamasında zaten belli oluyor. Bu ayrımı netleştirip sadece karşılaştırmaya odaklandık.

### Sistem şimdi ne yapabiliyor

Sistem artık bir adresin yapısındaki değişiklikleri **görebiliyor**:

- Bir bilgi alanı kaybolmuşsa fark ediyor ve bunu ciddi bir sorun olarak işaretliyor.
- Bir alanın türü değişmişse (sayıydı, yazıya dönmüş gibi) yakalıyor, bunu da ciddi sayıyor.
- Yeni bir alan eklenmişse haber veriyor ama bunu ciddi değil, sadece bilgilendirme olarak işaretliyor.
- İç içe geçmiş bilgi bloklarının **içindeki** değişiklikleri de aynı netlikte buluyor. "Bir yerlerde bir şey değişti" demiyor; tam olarak hangi alt-alanın değiştiğini adıyla söylüyor.
- Liste halindeki bilgilerde, listenin içindeki yapı değişse bile fark ediyor.
- Hiçbir değişiklik yoksa bunu da net biçimde söylüyor — sessiz kalmıyor.

Ayrıca bu mantığın doğruluğunu sürekli kontrol eden 15 otomatik sınama yazıldı. Bundan sonra biri yanlışlıkla bir şeyi bozarsa, anında haberimiz olacak.

### Neden böyle yaptık

**Neden bu parçayı sadece karşılaştırmaya odakladık, sekiz durumun hepsini buraya sıkıştırmadık:** "Adres hata verdi" veya "yanıt gelmedi" bir *karşılaştırma sonucu* değil — bunlar veri getirme aşamasında zaten anlaşılıyor, ortada karşılaştırılacak iki yapı bile yok. Bunları da bu parçaya yüklemek, parçanın iki farklı işi birden yapması demekti. Ayrı tuttuk ki ileride bir sorun çıktığında "karşılaştırma mı yanlış, yoksa veri mi gelmedi" sorusu net cevaplanabilsin.

**Neden iç içe bir alanın içindeki değişikliği "orada bir şey değişti" diye değil, tam adıyla raporluyoruz:** Bir bildirim aldığınızda "plan bilgisinde bir değişiklik var" demek işe yaramaz — hangi alan, ne olmuş, bilmeniz gerekir. Sistem bu yüzden değişikliğin tam yerini adıyla söylüyor. Zaten haftanın hedefi de tam olarak bu netlikteydi.

**Neden yavaş yanıt tespitini şimdilik yapmadık:** Bir yanıtın "yavaş" olduğunu söyleyebilmek için normalde ne kadar sürdüğünü bilmek gerekir. Ama sistem şu an geçmiş yanıt sürelerini hiçbir yerde saklamıyor — karşılaştıracak bir referans yok. Olmayan bir veriyle çalışacak kod yazmak yerine bunu açıkça not düşüp erteledik.

**Bağımsız denetim ne dedi:** Denetim, karşılaştırma mantığının gerçekten çalıştığını ve testlerin gerçek olduğunu (yapay, boş test olmadığını) doğruladı. Bir de haklı bir uyarı bıraktı: ertelenen o dört durumun ileride *gerçekten* yapıldığından emin olunmalı, unutulup gitmemeli. Bunu ciddiye alıp yol haritasının Hafta 3 bölümüne, üzeri çizilmeyi bekleyen iki somut madde olarak ekledik — böylece takip edilmeden geçilmesi mümkün değil.

### Sırada ne var

**Hafta 2 tamamlandı.** Projenin en kritik ve en riskli bölümü artık geride — yol haritası bu haftanın gecikmesi durumunda son haftanın iptal edileceğini söylüyordu, o risk kalktı.

Hafta 3, sistemi gerçekten "canlı" hale getiriyor:

1. Telefona bildirim gönderme yeteneği eklenecek.
2. Tüm parçaları sırayla çalıştıran bir ana akış yazılacak — bu adımda, yukarıda bahsedilen ertelenmiş dört durum da ele alınacak.
3. Sistem kendi kendine, saat başı otomatik çalışır hale getirilecek.

Bu hafta bittiğinde proje aslında **tamamlanmış** sayılıyor; son hafta bonus.

---

## Kayıt 5 — Hafızası olan bir sistem

**Tarih:** 25 Ağustos 2026
**Aşama:** Hafta 2, Gün 3-4

### Ne yaptık

Bir önceki adımda sistem gelen verinin yapısını okuyabiliyordu ama bu bilgiyi hemen unutuyordu — her çalıştırmada sıfırdan başlıyordu. Bu adımda sisteme bir hafıza kazandırdık: okuduğu yapıyı kalıcı olarak saklayabiliyor ve daha sonra geri çağırabiliyor.

Bunun için üç ayrı kayıt defteri hazırladık: biri "her adresin normal hali ne" bilgisini tutacak, diğer ikisi ("her kontrolde ne oldu" ve "hangi değişiklikler yakalandı") bir sonraki adımda dolacak. Şimdilik sadece ilkini kullanıma aldık.

Test ederken beklenmedik bir şey bulduk ve hemen düzelttik — aşağıda anlatıyoruz.

### Sistem şimdi ne yapabiliyor

- Bir adresin yapısını öğrendiğinde bunu kalıcı olarak saklayabiliyor; bilgisayar kapatılıp açılsa bile bu bilgi kaybolmuyor.
- Aynı adres için daha önce kaydedilmiş bir bilgi varsa onu geri çağırabiliyor.
- Bir adresin yapısı zamanla değiştiğinde, eski kayıtları silmiyor — üzerine yenisini ekliyor. Böylece ileride "bu adres geçmişte nasıl değişti" sorusu da cevaplanabilecek.
- Daha önce hiç görmediği bir adres sorulduğunda çökmüyor, düzgünce "bu konuda bir kaydım yok" diyebiliyor.
- Artık üç parça (adrese bağlanma, yapıyı okuma, hafızaya alma) birlikte, gerçek bir adresle uçtan uca çalışıyor.

### Neden böyle yaptık

**Neden üç kayıt defterinin hepsini şimdiden hazırladık ama ikisini boş bıraktık:** Bir kayıt defterinin yapısını sonradan değiştirmek, baştan doğru kurmaktan çok daha zahmetli. Bu yüzden hepsini şimdiden doğru biçimde hazırladık, ama henüz ihtiyaç duymadığımız ikisine dokunmadık — onlar bir sonraki adımda, karşılaştırma mantığı yazılırken doğal olarak dolacak.

**Neden eski kayıtları silmek yerine üzerine ekliyoruz:** Bir adresin zaman içinde nasıl değiştiğini görebilmek, bu projenin değerli bir yan faydası olabilir. Üstüne yazmak yerine geçmişi biriktirmek, ileride bu soruyu cevaplama imkanını açık tutuyor — ve bunun bedeli neredeyse hiç yok.

**Test sırasında ne bulduk, neden önemliydi:** Sistemin kayıt defterine her bağlandığında bağlantıyı düzgün kapattığını varsaymıştık, ama kasıtlı olarak bozuk bir durum yaratıp denediğimizde, bağlantının tam kapanmadığını fark ettik. Normal kullanımda bu görünmezdi, ama bir sorun anında (örneğin kayıt defteri dosyası bir şekilde bozulursa) sistemin o dosyayı bırakmadan elinde tutmaya devam etmesine yol açabilirdi — bu da üst üste binen ek sorunlara kapı aralardı. Bunu erkenden, gerçek bir soruna dönüşmeden yakaladık ve kaynağında düzelttik. Sonra aynı bozarak testi tekrarlayıp düzeltmenin işe yaradığını ayrıca kanıtladık.

**Neden kayıt defterini bilgisayarın geneline değil, projenin kendi klasörüne koyduk:** Bu proje silinirse geride hiçbir iz kalmaması, kurulduğu ilk günden beri takip ettiğimiz bir ilke. Kayıt defteri dosyası ayrıca dışarı gönderilecek listeye asla girmeyecek şekilde korunuyor — bu üç ayrı yöntemle test edilip doğrulandı, çünkü içinde ileride hassas olabilecek bilgiler birikebilir.

### Sırada ne var

Hafta 2'nin son ve en kritik bölümü:

1. İki yapıyı (eski ve yeni) karşılaştırıp "şu bilgi silinmiş", "şu bilginin türü değişmiş" gibi somut tespitler yapan mantık yazılacak. Bu, projenin asıl var oluş sebebi.
2. Bu adımda otomatik testler de yazılacak — her tespit türü için en az bir tane.
3. Bu bölüm bittiğinde Hafta 2 tamamlanmış olacak.

---

## Kayıt 4 — Yanıtın yapısını okuyabilen bir sistem

**Tarih:** 24 Ağustos 2026
**Aşama:** Hafta 2, Gün 1-2

### Ne yaptık

Şimdiye kadar sistem bir adrese bağlanıp veri getirebiliyordu ama getirdiği veriyi anlamıyordu — sadece ham haliyle ekrana yazıyordu. Bu adımda sisteme, gelen verinin **yapısını okuma** yeteneğini kazandırdık: hangi bilgi alanları var, her birinin türü ne.

Kodlamaya başlamadan önce bir tasarım turu yaptık, çünkü burada birkaç zor karar vardı: bir bilgi boşsa ne yapılacak, liste halinde gelen veriler nasıl ele alınacak, iç içe geçmiş bilgi blokları nasıl korunacak. Bu kararları birlikte netleştirdik, sonra kodladık.

### Sistem şimdi ne yapabiliyor

- Gelen bir yanıta bakıp "burada şu bilgiler var, her biri şu türden" diyebiliyor.
- İç içe geçmiş bilgi bloklarını (bir bilginin içinde başka bilgiler olması) kaybetmeden aynen koruyor.
- Liste halinde gelen bilgilerde, listenin içindekilerin de ne türden olduğunu anlıyor — liste bir bilgi bloğu içeriyorsa, o bloğun içini de okuyor.
- Beklenmedik durumlarla karşılaşınca (boş liste, boş blok, hiç veri gelmemesi) çökmüyor, anlamlı bir şekilde "bunu görmedim" diyebiliyor.
- Bunu gerçek bir adresten alınan canlı veriyle de kanıtladık — önceki haftanın veri çekme parçasıyla sorunsuz birlikte çalıştı.

### Neden böyle yaptık

**Neden bir bilginin doğru/yanlış (evet/hayır) olup olmadığını sayı ile karıştırmamaya özellikle dikkat ettik:** Kullandığımız programlama dilinde doğru/yanlış değerleri, arka planda sayılarla aynı aileden sayılıyor. Bu yüzden dikkatsiz yazılırsa "aktif mi" gibi bir bilgi yanlışlıkla "sayı" olarak etiketlenebilir. Bunu bilerek kontrol ettik ve doğru ayrımın yapıldığını ayrıca kanıtladık.

**Neden liste içindeki bilgi bloklarının da içini okuduk, sadece "burası bir liste" demekle yetinmedik:** Eğer sadece "liste" deseydik, bu listenin içindeki bir bilginin silinmesi veya değişmesi hiç fark edilemezdi — sistemin asıl amacı bu tür değişiklikleri yakalamak olduğu için, bu bilgiyi görmezden gelmek sistemi işlevsiz kılardı.

**Neden bu parçayı, veriyi saklayan veya karşılaştıran parçalardan ayrı tuttuk:** Bu parçanın tek işi "şu an ne görüyorum" sorusuna cevap vermek. "Bu bir değişiklik mi" sorusunu bir sonraki parça soracak. İkisini karıştırsaydık, ileride bir sorun çıktığında hangi parçanın hatalı olduğunu ayırt etmek zorlaşırdı.

**Neden karışık bilgi barındıran bir listede ilk elemanı esas aldık:** Basitlik tercih edildi. Bir listenin içindeki her elemanın farklı türden olması nadir bir durum; bunu ayrıca özel olarak ele almak şu aşamada gereksiz karmaşıklık katardı. İleride ihtiyaç olursa bu genişletilebilir.

### Sırada ne var

Hafta 2'nin devamı:

1. Çıkarılan bu yapı bir yerde saklanmalı — çünkü bir değişikliği fark edebilmek için "önceki hali" elde bulunmalı. Bu, veritabanı katmanının işi.
2. Ardından projenin kalbi: iki yapıyı karşılaştırıp "şu bilgi silinmiş", "şu bilginin türü değişmiş" gibi tespitler yapan mantık yazılacak.

---

## Kayıt 3 — Sistemin ilk gerçek işi: dışarıdan veri çekme

**Tarih:** 24 Ağustos 2026
**Aşama:** Hafta 1, Gün 5-7

### Ne yaptık

Bugüne kadar proje bir iskeletti; hiçbir parçanın içinde çalışan bir şey yoktu. Bu adımda sistemin ilk gerçek işini yazdık: bir internet adresine bağlanıp oradan veri çekmek.

Önce izlenecek ilk adresi belirledik — herkese açık, şifre istemeyen bir deneme servisi seçtik. Sonra bu adrese bağlanan, gelen yanıtı, sunucunun verdiği durum bilgisini ve yanıtın kaç milisaniyede geldiğini geri veren parçayı yazdık.

Kod yazmadan önce "burada ne ters gidebilir" diye bir liste çıkardık ve yedi ayrı aksilik belirledik. Yazarken bu yedi durumun hepsini tek tek karşıladık, sonra da hepsini gerçekten yaşatarak sınadık.

### Sistem şimdi ne yapabiliyor

İlk kez çalıştırılabilir bir program var. Öncekine göre kazanılanlar:

- Belirlenen adrese bağlanıp gerçek veri getirebiliyor ve getirdiğini ekranda okunabilir biçimde gösteriyor.
- Yanıtın ne kadar sürede geldiğini ölçüyor. Bu ölçüm ileride "bu servis yavaşlamış mı" sorusunu cevaplamak için kullanılacak.
- Aksilik çıktığında çökmüyor. Bağlantı kurulamazsa, yanıt zamanında gelmezse, sunucu hata verirse, gelen yanıt beklenen biçimde değilse, ayar dosyası bozuksa ya da hiç yoksa — her durumda ne olduğunu anlaşılır biçimde söyleyip düzgünce duruyor.
- Yeni bir adresi izlemeye almak için koda dokunmak gerekmiyor; ayar dosyasına bir satır eklemek yetiyor.

### Neden böyle yaptık

**Neden veri çeken parça başka hiçbir iş yapmıyor:** Bu parça yalnızca veri getiriyor — getirdiğini yorumlamıyor, saklamıyor, kimseye haber vermiyor. Bunların her biri ayrı parçaların işi olacak. Böyle ayırmasaydık, ileride bir sorun çıktığında "yanıt mı gelmedi, gelen yanıt mı anlaşılmadı, yoksa kaydedilemedi mi" sorusunu ayırt etmek zorlaşırdı.

**Neden her aksilik için ayrı bir karşılama yolu yazdık:** Bu sistemin varlık sebebi zaten aksilikleri fark etmek. Kendisi ilk aksilikte çöken bir izleme sistemi işe yaramaz. Ayrıca aksilikleri birbirinden ayırmak önemli: "bağlanamadım" ile "sunucu hata verdi" farklı şeyler ve ileride farklı tepkiler gerektirecekler.

**Neden aksilikleri gerçekten yaşatarak denedik:** Hata karşılama kodunun yazılmış olması, çalıştığı anlamına gelmiyor. Bu yüzden sırayla var olmayan bir adres verdik, tanınan süreyi kasten yetersiz bıraktık, olmayan bir kaynak istedik, beklenen biçimde olmayan bir yanıt ürettik, ayar dosyasını bozduk ve sildik. Her seferinde sistemin çökmediğini ve doğru şeyi söylediğini gözümüzle gördük.

**Neden bozmadan önce yedek aldık:** Bozarak sınamak faydalı ama ayar dosyasını gerçekten bozmayı gerektiriyordu. Yedek alıp sonunda geri yükledik ve dosyanın ilk haliyle birebir aynı olduğunu ayrıca kanıtladık. Böyle yapmasaydık, testlerden arta kalan bozuk bir ayarın fark edilmeden kalması riski olurdu.

**Bir sınamada beklenmedik bir şey oldu:** Yanıt için tanınan süreyi aşırı kısa tuttuğumuzda — bağlantının kurulmasına bile yetmeyecek kadar — sistem durumu "süre doldu" yerine "bağlanamadım" diye etiketledi. İkisi de bir bakıma doğru, ama biz "süre doldu" bekliyorduk. Gerçekçi bir süreyle tekrar denediğimizde doğru etiketi verdi. Denetim de bunun engelleyici olmadığını, acil olmadığını söyledi. Bu yüzden şimdilik olduğu gibi bıraktık ve kayıt altına aldık.

**Neden şimdilik tek adres izleniyor:** Yol haritası bu aşama için tek adres öngörüyor. Sistem baştan birden fazla adresle çalışacak biçimde yazıldı, ama önce tek adresle her şeyin doğru işlediğinden emin olmak istedik. Adres çoğaltmak sonraki haftalarda sadece ayar dosyasına satır eklemek olacak.

### Sırada ne var

Hafta 1 burada tamamlanıyor. Hafta 2 projenin en kritik bölümü:

1. Gelen yanıtın yapısını çıkaran parça tasarlanacak. Yani "bu yanıtta hangi bilgiler var ve her biri ne türden" sorusunun cevabı. İç içe geçmiş yapılar ve listeler burada özen isteyecek.
2. Çıkarılan bu yapının saklanması gerekecek, çünkü karşılaştırma ancak "önceki hali" elde varsa mümkün olur.
3. Ardından projenin kalbi gelecek: iki yapıyı karşılaştırıp neyin değiştiğini bulan parça.

Bu bölüm tasarım kararı gerektirdiği için önce plan çıkarılacak, sonra yazılacak.

---

## Kayıt 2 — Çalışmanın internete yedeklenmesi

**Tarih:** 23 Ağustos 2026
**Aşama:** Hafta 1, Gün 3-4 sonu

### Ne yaptık

Şimdiye kadar yapılan her şey yalnızca bu bilgisayarda duruyordu. Bunu değiştirdik: proje için açılan internet üzerindeki depoya bağlantı kurduk ve tüm çalışmayı oraya gönderdik. Göndermeden önce ana dalın adını, karşı tarafın beklediği isimle aynı olacak şekilde düzelttik; aksi halde dosyalar orada beklenen yerde görünmeyecekti.

Gönderimden önce gizli bilgi kontrolünü üç ayrı katmanda tekrarladık. Sadece "şu an ne gidiyor" diye bakmakla yetinmedik, geçmişin tamamını da taradık.

### Sistem şimdi ne yapabiliyor

Sistem hâlâ bir iş yapmıyor, ama önemli bir güvence kazanıldı:

- Çalışmanın tamamı artık ikinci bir yerde duruyor. Bu bilgisayara bir şey olsa bile proje kaybolmaz.
- Yapılan işin geçmişi dışarıdan görülebilir durumda — bu proje bir özgeçmiş çalışması olduğu için, düzenli ilerlemenin kaydı da değerli.
- Gizli bilgi koruması, dışarı açılmadan hemen önce bağımsız olarak yeniden kanıtlandı.

### Neden böyle yaptık

**Neden ilk gönderimden önce dal adını değiştirdik:** Yerel çalışmanın ana kolu ile karşı tarafın varsayılan ana kolu farklı adlar taşıyordu. Bu haliyle gönderilseydi depoda birbirinden habersiz iki ayrı kol oluşurdu; dosyalar açılışta görünmez, sonradan toparlaması can sıkıcı olurdu. Tek bir düzeltmeyle baştan önlendi.

**Neden üç ayrı kontrol yaptık:** Bir erişim anahtarının herkese açık ortama sızması bu projenin en gerçek riski ve geri dönüşü çok zor. Önce hangi dosyaların gittiğine baktık; sonra bu dosyaların içinde şifre görünümlü bir metin var mı diye taradık; son olarak geçmişte herhangi bir anda böyle bir dosyanın girip girmediğini kontrol ettik. Üçü de temiz çıktı. Tek bir kontrolle yetinmek, "dosya listesi temiz ama birinin içine anahtar yapıştırılmış" durumunu kaçırabilirdi.

**Neden şimdi gönderdik, daha sonra değil:** Bir haftalık iş biriktikten sonra ilk yedeği almak gereksiz risk olurdu. Zemin hazırken almak daha ucuz.

### Sırada ne var

Hafta 1'in son bölümü:

1. İzlenecek ilk adres tanımlanacak — herkese açık, kimlik doğrulaması istemeyen bir test adresi.
2. Sistemin ilk gerçek işi yazılacak: dışarıdan veri çekme. Bu parça bir adrese istek atacak, dönen yanıtı ve yanıtın kaç milisaniyede geldiğini geri verecek.
3. O adımın sonunda ekranda ilk kez gerçek bir yanıt görülecek. Hafta 1'in bitiş ölçütü budur.

---

## Kayıt 1 — Proje iskeleti, çalışma ortamı ve güvenlik kalkanı

**Tarih:** 23 Ağustos 2026
**Aşama:** Hafta 1, Gün 3-4 (mimari planlama)

### Ne yaptık

Projenin oturacağı iskeleti kurduk. Yol haritasında tasarlanmış olan klasör ve dosya düzenini gerçek hale getirdik: her parçanın duracağı yer artık hazır ve boş bekliyor. Her dosyanın en üstüne, o dosyanın ilerleyen haftalarda ne işe yarayacağını anlatan Türkçe bir açıklama koyduk.

Ardından projenin çalışacağı ortamı hazırladık: dil kuruldu, projeye özel yalıtılmış bir çalışma alanı açıldı ve iki yardımcı paket bu alana kuruldu. Projeyi versiyon kontrolü altına aldık, yani bundan sonra yapılan her değişikliğin kaydı tutulacak ve gerektiğinde geriye dönülebilecek.

Bu adımda bilerek hiç çalışan kod yazılmadı. Amaç, evin duvarlarını örmeden önce oda planını yerleştirmek ve zemini dökmekti.

### Sistem şimdi ne yapabiliyor

Sistem henüz hiçbir iş yapmıyor — çalıştırılacak bir program yok. Kazanılan şey işlevsellik değil, **düzen, zemin ve koruma**:

- Projenin her parçasının nereye yazılacağı belli. Bundan sonra "bu kod nereye gitmeli" sorusu sorulmayacak.
- Çalışma ortamı hazır ve sınandı. Yarın kod yazmaya başlandığında kurulumla uğraşılmayacak.
- Yardımcı paketler yalıtılmış alana kuruldu, bilgisayarın geneline bulaşmadı. Bu proje silinse bilgisayarda iz kalmaz.
- Gizli bilgiler için bir koruma kalkanı kuruldu ve **çalıştığı kanıtlandı**. Şifre ve erişim anahtarlarının yanlışlıkla herkese açık ortama gitmesi artık engelleniyor.
- Yapılan her değişiklik kayıt altına alınabilir durumda; bir şey bozulursa önceki hale dönmek mümkün.

### Neden böyle yaptık

**Neden ayrı ayrı boş dosyalar açtık, hepsini tek dosyada toplamadık:** Her parçanın tek bir işi olsun istedik. Veri çeken kısım sadece veri çeker, karşılaştıran kısım sadece karşılaştırır, haber veren kısım sadece haber verir. Bu ayrım sayesinde bir sorun çıktığında hangi parçaya bakılacağı belli olur, ve ileride bir parçayı değiştirmek diğerlerini bozmaz. Her şeyi tek dosyaya yığmak başta hızlı görünür ama üçüncü haftada içinden çıkılmaz hale gelir.

**Neden dosyaların içine şimdiden kod yazmadık:** Yarım kalmış, çalışmayan kod bırakmak istemedik. Her aşama sonunda proje çalışır durumda olmalı. Boş bir dosya dürüsttür; yarım bir dosya ise ilerideki bir sürprizdir.

**Neden yalıtılmış bir çalışma alanı kurduk:** Yardımcı paketler doğrudan bilgisayara kurulsaydı, başka projelerle sürüm çakışması yaşanabilirdi. Yalıtılmış alan sayesinde bu projenin ihtiyaçları kendi kutusunda duruyor.

**Neden koruma kalkanını kasıtlı olarak sınadık:** Bu projenin en gerçek riski, bir erişim anahtarının yanlışlıkla herkese açık ortama sızması. Böyle bir şey bir kez olduğunda geri almak neredeyse imkânsızdır. Bu yüzden ilk kayıt alınmadan önce, kasıtlı olarak sahte gizli dosyalar oluşturup sistemin bunları gerçekten engellediğini kanıtladık. Sonra o sahte dosyalar silindi. Kalkan ayrıca binden fazla dosyadan oluşan gerçek çalışma alanı üzerinde de sınandı ve tamamını gizlediği doğrulandı.

**Alternatif neydi:** Doğrudan çalışan bir program yazıp sonra düzene sokmak da mümkündü. Onu seçmedik, çünkü sonradan düzene sokmak pratikte hiç yapılmaz.

### Sırada ne var

Bu adımın onayı ve kaydı alındıktan sonra Hafta 1'in son bölümüne geçilecek:

1. İzlenecek ilk adres tanımlanacak — başlangıç için herkese açık, kimlik doğrulaması istemeyen bir test adresi seçilecek.
2. Sistemin ilk gerçek işi yazılacak: dışarıdan veri çekme. Bu parça bir adrese istek atacak, dönen yanıtı ve yanıtın kaç milisaniyede geldiğini geri verecek.
3. O adımın sonunda ekranda ilk kez gerçek bir yanıt görülecek. Hafta 1'in bitiş ölçütü tam olarak budur.

Ayrıca çözülmeyi bekleyen bir konu var: proje için internet üzerinde bir depo açıldı, ancak buradaki çalışma henüz oraya bağlanmadı. Bu bağlantı, ilk kayıt alındıktan sonra ayrıca konuşulacak.
