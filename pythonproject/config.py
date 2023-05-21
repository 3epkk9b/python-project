import os

class Config:
   SECRET_KEY = '98541236587541256985475695425987'
   SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
   MAIL_SERVER ='smtp.gmail.com'
   MAIL_PORT = 587
   MAIL_USE_TLS = True
   MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
   MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')