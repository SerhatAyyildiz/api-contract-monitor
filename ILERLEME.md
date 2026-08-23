# İlerleme Günlüğü

> Bu dosya kod içermez. Amacı, projeyi hiç açmadan sistemin ne durumda olduğunu anlayabilmektir.
> En yeni kayıt en üsttedir.

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
