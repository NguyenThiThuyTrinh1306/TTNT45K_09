import os
import playsound
import speech_recognition as sr
import datetime
import wikipedia as wk
import requests
import sys
import ctypes
import re
import json
import audioop
from json import encoder
from logging import fatal
from datetime import date, time
from time import strftime 
from gtts import gTTS
from requests.models import Response 
import webbrowser as wr
from wikipedia.wikipedia import WikipediaPage, languages, search
from  youtube_search  import YoutubeSearch
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


wk.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install() 

def bot_speak(text):
    tts = gTTS(text=text, lang='vi')
    filename = 'Cuties.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def bot_audio():
    print("\nCuties: tôi đang nghe đây, bạn nói đi ")
    a = sr.Recognizer()
    with sr.Microphone() as Micro:
        print("\nngười sử dụng: ", end = '')
        audio = a.record(Micro, duration=7)
        try:
            brain = a.recognize_google(audio, language="vi-VN")
            print(brain)
            return brain
        except:
            print("\nCuties: >....<")
            return 0

def stop_bot():
    bot_speak("Tạm biệt, hãy gọi tôi nếu bạn cần nhé")

def content():
    for i in range(3):
        you = bot_audio()
        if you:
            return you.lower()
        elif i<2:
            bot_speak("Tớ không nghe rõ, cậu nói lại một lần nữa nhé")
    stop_bot()
    return 0

def bot_chao(name):
    ngay_gio = int(strftime("%H"))
    if 0 <= ngay_gio < 11:
        bot_speak(f"Chào {name}. Buổi sáng vui vẻ nha.")
    elif 11 <= ngay_gio < 13:
        bot_speak(f"Chào  {name}. Chúc bạn buổi trưa vui vẻ.")
    elif 13 <= ngay_gio < 18:
        bot_speak(f"Chào  {name}. Chúc bạn buổi chiều vui vẻ")
    elif 18 <= ngay_gio < 22:
        bot_speak(f"Chào  {name}. Chúc bạn buổi tối vui vẻ")
    else:
        bot_speak(f"Chào {name}. Ngủ sớm kẻo bệnh nào.")
    
def bot_time(you):
    now = datetime.datetime.now()
    if "ngày" in you:
        bot_speak ("Hôm nay là ngày %d tháng %d năm %d" %(now.day, now.month, now.year))
    elif "giờ" in you:
        bot_speak ("Bây giờ là giờ %d phút %d giây %d" %(now.hour, now.minute, now.second))
    else:
        bot_speak ("Bạn nhắc lại được không, tớ không nghe rõ")
  

def open_app(you):
    if "google" in you:
        bot_speak("Google Chrome của bạn đây")
        
        os.system('C:\\Users\\Public\\Desktop\\Google Chrome.lnk')
    elif "word" in you:
        bot_speak("Microsoft Word của bạn đây")
            
        os.system('C:\\Users\\W\\Desktop\\Word.lnk')
    elif "excel" in you:
        bot_speak(" Microsoft Excel của bạn đây")
       
        os.system('C:\\Users\\W\\Desktop\\Excel.lnk')
    else:
        bot_speak("Không tìm thấy ứng dụng bạn muốn, thử lại nào")
        

def web_bot(text):
    b = re.search('mở (.+)', text)
    if b :
        domain = b.group(1)
        url = "https://www." + domain
        wr.open(url)
        bot_speak("tớ mở cho cậu ngay đây")
        if input("Cậu muốn tiếp tục thì nhấn w:") =="w" :
           pass 
        return True
    else:
        return False

def open_gg(you):
    search_for = you.split("kiếm", 1)[1]
    bot_speak('Okay!')
    driver = webdriver.Chrome(path)
    driver.get("http://www.google.com")
    que = driver.find_element_by_xpath("//input[@name='q']")
    que.send_keys(str(search_for))
    que.send_keys(Keys.RETURN)

def thoi_tiet():
    bot_speak("Bạn muốn biết thời tiết ở đâu")
    thoitiet_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = content() 
    if not city:
        pass
    api_key = "4e8088e6873108e3f0838348de757f57"
    c_url = thoitiet_url + "appid=" + api_key +"&q=" + city + "&units=metric" 
    Response = requests.get(c_url)
    data = Response.json()
    if data["cod"]!="404":
        city_res = data["main"]
        temperature = city_res["temp"]
        humidity = city_res["humidity"]
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        Ct = f""" 
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        nhiệt độ trung bình là {temperature} độ C,độ ẩm là{humidity}% """
        bot_speak(Ct)
    else:
        bot_speak("địa chỉ bạn tìm không tồn tại")


def open_youtube():
    bot_speak("Bạn muốn tôi mở video nào")
    search = content()
    while True:
         result = YoutubeSearch(search, max_results= 10 ).to_dict()
         if result:
             break
    link =  f"https://www.youtube.com" + result[0]['url_suffix']
    wr.get().open(link)
    bot_speak("video bạn tìm đây")
  
def thongtin():
    try:
        bot_speak("bạn muốn biết gì nào")
        cts = content()
        infor = wk.summary(cts).split('\n')
        bot_speak(infor[0])
        dem = 0
        for ct in infor[1:]:
            if dem < 2:
                bot_speak("bạn muốn tìm gì nữa ?")
                onl = content()
                if 'tiếp tục' not in onl:
                    break
            dem += 1
            bot_speak(ct, sentences = 1)
        bot_speak("thông tin của bạn đây")
    except:
        bot_speak(" tớ không nghe rõ !!!")
def giup():
    
    bot_speak(f"""
    xin chào tớ có thể giúp bạn thực hiện các việc sau đây:
    1. chào hỏi
    2. Hiển thị giờ
    3. Mở website, ứng dụng desktop
    4. Tìm kiếm với google
    5. Dự báo thời tiết
    6. Tìm kiếm video với youtube
    7. Định nghĩa với từ điển bách khoa toàn thư ( Wikipedia )
    """)

def main_brain():
    bot_speak("Xin chào. Bạn tên gì?")
    global robot_name
    robot_name = "Chin Chin"
    global name
    name = content()
    if name:
        bot_speak(f'Xin chào bạn {name}.')
        bot_speak(f'Bạn cần Chin Chin giúp gì không ?')
        while True:
            you = content()

            if not you:
                break
            elif ('tạm biệt' in you) or ('hẹn gặp lại' in you):
                stop_bot()
                break
            elif "chào" in you:
                bot_chao(name)
            elif "bây giờ" in you or "hôm nay" in you:
                bot_time(you)

            elif "mở" in you:
                if '.' in you:
                    web_bot(you)
                else:
                    open_app(you)
                    
            elif "tìm kiếm" in you:
                open_gg(you)
            elif "thời tiết" in you:
                thoi_tiet()
            elif 'youtube' in you:
                bot_speak("Bạn muốn tìm cơ bản hay nâng cao")
                yc = content()
                if "cơ bản" in yc:
                    open_youtube()
                    if input():
                        pass
                elif "nâng cao" in yc:
                    open_youtube()
                    if input("Tiếp tục y\n: ") == "y":
                        pass
            elif "tìm hiểu" in you:
                thongtin()
            elif "giúp đỡ" in you:
                giup()
            else:
                bot_speak(f"Chức năng không có! ")

main_brain()
