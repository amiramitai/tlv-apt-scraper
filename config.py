import os

GMAIL_EMAIL = 'sender@gmail.com'
# get your password at:
# https://myaccount.google.com/apppasswords
GMAIL_PASSWORD = ''

MSG_FROM = GMAIL_EMAIL
MSG_TO = "receiver@gmail.com"
MSG_SUBJECT = 'New Apartments!'

PRICE_MIN = 6500
PRICE_MAX = 8500

if os.name == 'nt':
    home = f"{os.environ['homedrive']}{os.environ['homepath']}"
    DATA_DIR = os.path.join(home, 'AppData\\Local\\Google\\Chrome\\User Data\\Default')
else:
    DATA_DIR = os.path.join(os.environ['HOME'],'Library/Application Support/Google/Chrome/')

SKIP_MISSING_IMG = True

REDIS_SETTINGS = {
    'host': u'localhost', 
    'port': 6379, 
    'db': 0,
    'username': None,
    'password': None
}

YAD2_AREA_URLS = [
    # Lev Haair
    f'https://www.yad2.co.il/realestate/rent/map?city=5000&neighborhood=1520&propertyGroup=apartments&price={PRICE_MIN}-{PRICE_MAX}&z=14',
    # Kerem
    f'https://www.yad2.co.il/realestate/rent/map?city=5000&neighborhood=1521&propertyGroup=apartments&price={PRICE_MIN}-{PRICE_MAX}&z=15',
    # Zafon Yashan
    f'https://www.yad2.co.il/realestate/rent/map?city=5000&neighborhood=1461&propertyGroup=apartments&price={PRICE_MIN}-{PRICE_MAX}&z=13',
    # Karlibach
    f'https://www.yad2.co.il/realestate/rent/map?city=5000&neighborhood=1462&propertyGroup=apartments&price={PRICE_MIN}-{PRICE_MAX}&z=15',
]

TO_FILTER_OUT = [
    'סאבלט'
]