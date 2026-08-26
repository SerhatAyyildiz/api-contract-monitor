# İlerleme Günlüğü

> Bu dosya kod içermez. Amacı, projeyi hiç açmadan sistemin ne durumda olduğunu anlayabilmektir.
> En yeni kayıt en üsttedir.

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
