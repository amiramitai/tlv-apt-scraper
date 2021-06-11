import re
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bidi.algorithm import get_display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import redis

from config import *

options = webdriver.ChromeOptions() 
options.add_argument(f"user-data-dir={DATA_DIR}")
added = []

rclient = redis.StrictRedis(**REDIS_SETTINGS)
browser = webdriver.Chrome(options=options)

def should_filter_out(html):
    for f in TO_FILTER_OUT:
        if f in html:
            print('filtering..', get_display(f))
            return True
    return False

def scrape(url):
    global browser
    global added
    browser.get(url)
    els = browser.find_elements_by_css_selector('.feeditem.table')

    for e in els:
        html = e.get_attribute('innerHTML')
        text = e.text
        item_id = re.findall('item-id="(.*?)"', html)
        if not item_id:
            print('[!] item id was not found')
            continue
        item_id = item_id[0]
        img = re.findall('img\.yad2.*?(?:png|jpg|jpeg|bmp|gif)', html, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        if not img and SKIP_MISSING_IMG:
            print('[!] skipping missing image..')
            continue
        
        img = img[0]
        if rclient.hexists('results', item_id):
            print('[!] already cached', item_id)
            continue
        
        if should_filter_out(html):
            continue
        
        
        print('new result:', get_display(text))
        style = 'style="display: flex;"'
        html = html.replace('item-id', style + ' item-id')
        url = f'https://www.yad2.co.il/item/{item_id}'
        html = f'<a href={url} target="_blank">{html}</a>'

        added.append(html)
        rclient.hset('results', item_id, 1)        

def send_email(html):
    print('[+] sending email to:', MSG_TO)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = MSG_SUBJECT
    msg['From'] = MSG_FROM
    msg['To'] = MSG_TO
    part = MIMEText(html, 'html')
    msg.attach(part)
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(GMAIL_EMAIL, GMAIL_PASSWORD)
    mail.sendmail(MSG_FROM, MSG_TO, msg.as_string())

def main():
    global added
    while True:
        added = []
        for url in YAD2_AREA_URLS:
            print('[+] scraping:', url)
            scrape(url)
        if not added:
            print('[+] sleeping...')
            time.sleep(10 * 60)
            continue
        html = '<html><body>'
        for a in added:
            html += a
        html == '</body></html>'
        send_email(html)
        print('[+] sleeping...')
        time.sleep(10 * 60)

if __name__ == '__main__':
    main()
