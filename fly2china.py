# -*- coding: utf-8 -*-
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from playsound import playsound
from datetime import datetime
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# from fake_useragent import UserAgent
import random

def notification(to_list, body, flight):
    sender = 'chenxuzhen@163.com'  # 邮件发送人
    receiver = '99999999@qq.com'  # 邮件收件人
    subject = 'flight2china by python scraper: ' + flight + ' ' + str(datetime.today())[:16]  # 主题
    smtpserver = 'smtp.163.com'  # 网易的STMP地址 默认端口号为25
    username = 'chenxuzhen@163.com'  # 发送邮件的人
    password = 'authentication_pass_of_163_email'  # 你所设置的授权码.网易在开通SMTP服务后会有个密码设置

    # 中文需参数‘utf-8'，单字节字符不需要
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # 头部信息:标题
    msg['From'] = 'chenxuzhen<chenxuzhen@163.com>'  # 头部信息:名称<发件人的地址>
    msg['To'] = ",".join(to_list)  # 头部信息:收件人地址
    m = True
    while m == True:
        try:
    #         smtp = smtplib.SMTP()
    #         smtp.connect('smtp.163.com')  # 链接服务器
            smtp = smtplib.SMTP_SSL('smtp.163.com', 465)
            smtp.login(username, password)
            smtp.sendmail(sender, receiver, msg.as_string())
            smtp.quit()
            print('success')
            m = False
        except smtplib.SMTPException as e:
            print('Error: ', e)
            time.sleep(25)

to_list = ["chenxuzhen@163.com", "9999999@qq.com"]     

# Googleflights的链接，注意，如果你的主机在某些地区链接可能不太一样，比如阿里云香港主机就需要加上国家，不然后面会找不到元素，因为链接会定向到选择国家
# Googleflights并不是在所有国家都可用，香港就没有该服务
# 'https://www.google.com/flights?lite=0&hl=en&gl=us#flt=JFK.PVG.2020-11-25.JFKPVG0MU298;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.141599',

base_urls = [
'https://www.google.com/flights?lite=0&hl=en#flt=JFK.PVG.2020-11-25.JFKPVG0MU298;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.141599',
'https://www.google.com/flights?lite=0&hl=en#flt=SEA.PVG.2020-11-26.SEAPVG0DL281;c:USD;e:1;ca:ICN;a:DL;sd:1;t:b;tt:o;sp:2.USD.522510',
'https://www.google.com/flights?lite=0&hl=en#flt=DTW.PVG.2020-11-27.DTWPVG0DL389;c:USD;e:1;ca:ICN;a:DL;sd:1;t:b;tt:o;sp:2.USD.564910',
'https://www.google.com/flights?lite=0&hl=en#flt=SFO.PVG.2020-11-25.SFOPVG0UA857;c:USD;e:1;ca:ICN;a:UA;sd:1;t:b;tt:o;sp:2.USD.482210',
'https://www.google.com/flights?lite=0&hl=en#flt=SFO.PVG.2020-11-28.SFOPVG0UA857;c:USD;e:1;ca:ICN;a:UA;sd:1;t:b;tt:o;sp:2.USD.482210',
'https://www.google.com/flights?lite=0&hl=en#flt=LAX.CAN.2020-11-29.LAXCAN0CZ328;c:USD;e:1;a:CZ;sd:1;t:b;tt:o;sp:2.USD.207310',
'https://www.google.com/flights?lite=0&hl=en#flt=ICN.PVG.2020-11-20.ICNPVG0MU5042;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.42077',
'https://www.google.com/flights?lite=0&hl=en#flt=ICN.SHE.2020-11-22.ICNSHE0CZ682;c:USD;e:1;a:CZ;sd:1;t:b;tt:o;sp:2.USD.30117',
'https://www.google.com/flights?lite=0&hl=en#flt=NRT.PVG.2020-11-27.NRTPVG0MU524;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.283595',
'https://www.google.com/flights?lite=0&hl=en#flt=NRT.XIY.2020-11-24.NRTXIY0MU594;c:USD;e:1;s:0;a:MU;sd:1;t:b;tt:o;sp:2.USD.283595',
'https://www.google.com/flights?lite=0&hl=en#flt=NRT.SHE.2020-11-26.NRTSHE0CZ628;c:USD;e:1;a:CZ;sd:1;t:b;tt:o;sp:2.USD.158730',
'https://www.google.com/flights?lite=0&hl=en#flt=NRT.FOC.2020-11-27.NRTFOC0MF810;c:USD;e:1;a:MF;sd:1;t:b;tt:o;sp:2.USD.265117',
'https://www.google.com/flights?lite=0&hl=en#flt=NRT.SZX.2020-11-29.NRTSZX0ZH9052;c:USD;e:1;a:ZH;sd:1;t:b;tt:o;sp:2.USD.264464',
'https://www.google.com/flights?lite=0&hl=en#flt=KIX.PVG.2020-11-24.KIXPVG0HO1334;c:USD;e:1;a:HO;sd:1;t:b;tt:o;sp:2.USD.283604',
'https://www.google.com/flights?lite=0&hl=en#flt=KUL.PVG.2020-11-29.KULPVG0FM886;c:USD;e:1;a:FM;sd:1;t:b;tt:o;sp:2.USD.79680',
'https://www.google.com/flights?lite=0&hl=en#flt=KUL.CAN.2020-11-24.KULCAN0CZ350;c:USD;e:1;a:CZ;sd:1;t:b;tt:o;sp:2.USD.113919',
'https://www.google.com/flights?lite=0&hl=en#flt=KUL.CAN.2020-11-23.KULCAN0MH376;c:USD;e:1;a:MH;sd:1;t:b;tt:o;sp:2.USD.75727',
'https://www.google.com/flights?lite=0&hl=en#flt=KUL.CAN.2020-11-25.KULCAN0AK116;c:USD;e:1;a:AK;sd:1;t:b;tt:o;sp:2.USD.8825',
'https://www.google.com/flights?lite=0&hl=en#flt=KUL.CAN.2020-11-23.KULCAN0OD612;c:USD;e:1;a:OD;sd:1;t:b;tt:o;sp:.USD.',
'https://www.google.com/flights?lite=0&hl=en#flt=KUL.XMN.2020-11-27.KULXMN0MF848;c:USD;e:1;a:MF;sd:1;t:b;tt:o;sp:2.USD.171032',
'https://www.google.com/flights?lite=0&hl=en#flt=DXB.CAN.2020-11-28.DXBCAN0EK362;c:USD;e:1;a:EK;sd:1;t:b;tt:o;sp:2.USD.52340',
'https://www.google.com/flights?lite=0&hl=en#flt=AUH.PVG.2020-11-23.AUHPVG0EY862;c:USD;e:1;a:EY;sd:1;t:b;tt:o;sp:2.USD.270868',
'https://www.google.com/flights?lite=0&hl=en#flt=DOH.CAN.2020-11-29.DOHCAN0QR874;c:USD;e:1;a:QR;sd:1;t:b;tt:o;sp:2.USD.86658',
'https://www.google.com/flights?lite=0&hl=en#flt=DOH.CAN.2020-11-22.DOHCAN0QR874;c:USD;e:1;a:QR;sd:1;t:b;tt:o;sp:2.USD.86658',
'https://www.google.com/flights?lite=0&hl=en#flt=LHR.PVG.2020-11-22.LHRPVG0MU552;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.210899',
'https://www.google.com/flights?lite=0&hl=en#flt=LHR.PVG.2020-11-24.LHRPVG0VS250;c:USD;e:1;a:VS,VA;sd:1;t:b;tt:o;sp:2.USD.62180',
'https://www.google.com/flights?lite=0&hl=en#flt=LHR.PVG.2020-11-26.LHRPVG0BA169;c:USD;e:1;a:BA;sd:1;t:b;tt:o;sp:2.USD.64790',
'https://www.google.com/flights?lite=0&hl=en#flt=LHR.PVG.2020-11-22.LHRPVG0BA169;c:USD;e:1;a:BA;sd:1;t:b;tt:o;sp:2.USD.64790',
'https://www.google.com/flights?lite=0&hl=en#flt=CDG.PVG.2020-11-22.CDGPVG0MU570;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.208299',
'https://www.google.com/flights?lite=0&hl=en#flt=CDG.CAN.2020-11-24.CDGCAN0CZ348;c:USD;e:1;a:CZ;sd:1;t:b;tt:o;sp:2.USD.240243',
'https://www.google.com/flights?lite=0&hl=en#flt=FRA.PVG.2020-11-24.FRAPVG0MU220;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.201644',
'https://www.google.com/flights?lite=0&hl=en#flt=FRA.PVG.2020-11-23.FRAPVG0LH728;c:USD;e:1;a:LH;sd:1;t:b;tt:o;sp:2.USD.284571',
'https://www.google.com/flights?lite=0&hl=en#flt=FRA.PVG.2020-11-25.FRAPVG0LH728;c:USD;e:1;a:LH;sd:1;t:b;tt:o;sp:2.USD.284786',
'https://www.google.com/flights?lite=0&hl=en#flt=FRA.PVG.2020-11-23.FRAPVG0LH728;c:USD;e:1;a:LH;sd:1;t:b;tt:o;sp:2.USD.284571',
'https://www.google.com/flights?lite=0&hl=en#flt=AMS.PVG.2020-11-23.AMSPVG0MU772;c:USD;e:1;a:MU;sd:1;t:b;tt:o;sp:2.USD.89199',
'https://www.google.com/flights?lite=0&hl=en#flt=AMS.CAN.2020-11-27.AMSCAN0CZ308;c:USD;e:1;a:CZ;sd:1;t:b;tt:o;sp:2.USD.136664',
'https://www.google.com/flights?lite=0&hl=en#flt=IST.CAN.2020-11-24.ISTCAN0TK72;c:USD;e:1;a:TK;sd:1;t:b;tt:o;sp:2.USD.106106',
'https://www.google.com/flights?lite=0&hl=en#flt=SVO.PVG.2020-11-26.SVOPVG0SU208;c:USD;e:1;a:SU;sd:1;t:b;tt:o;sp:2.USD.24868',
'https://www.google.com/flights?lite=0&hl=en#flt=ADD.PVG.2020-11-26.ADDPVG0ET684;c:USD;e:1;a:ET;sd:1;t:b;tt:o;sp:2.USD.557245'    
]


time_out_seconds = 15 # set the time to wait till web fully loaded
executable_path = r'C:\Program Files (x86)\Google\chromedriver.exe'
# ua = UserAgent()
# user_agent = ua.random
options = webdriver.ChromeOptions()
options.add_argument('headless') 
# options.add_argument(f'user-agent={user_agent}')
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")    
options.add_argument('--no-sandbox')
options.add_experimental_option('excludeSwitches', ['enable-automation'])



all_flights = []
for i in range(0,250): # loop. anyhow selenium chrome is not stable and will need reboot manually.
    for base_url in base_urls:
        search_dates = []
    #     driver.get(base_url)
        # url中的日期提取出来 
        date2replace = base_url[56:66]
        day = datetime.strptime(date2replace, '%Y-%m-%d')
        print(str(day)[:10])
        # 这里的周期就是一周，因为这些航班一周一次
        dates = pd.date_range(end=str(day)[:10], periods=18, freq='7d')
        print('dates:', dates)
        for val in dates:
    #         print(str(val)[:10])
            search_dates.append(str(val)[:10])   
        print(search_dates)
        found = False
        for my_date in search_dates:
            if found:
                break
            my_url = base_url.replace(date2replace, my_date) #replace the date in the base_url into date in date_range     
            flight = my_url.split(';')[0].split('.')[-1]
            driver = webdriver.Chrome(executable_path, options=options) 
            # 打开页面，并留出时间加载万页面元素
            driver.get(my_url)
            time.sleep(time_out_seconds)
            try:
                # 这里的元素是错误信息'Sorry, the itinerary you selected is no longer available'
                search_result = driver.find_element_by_xpath('//*[@id="flt-app"]/div[2]/main[2]/div[1]/div/p[3]')          
                print(datetime.now())
                print(search_result.text)
                print(flight + ': no result on date: ' + my_date + '\n') # no flights found
#                 driver.quit()
                time.sleep(random.uniform(3, 5)) 
                continue
            except Exception as e:
                print(e)
#                 playsound('D:\python\pydata-book\TextNow.mp3')  # play a sound if flight found
                print('❥△❥ flight search attempted on date ' +  my_date + '; flight found!❥△❥')
                print('  url:', my_url)
                mail_body = 'flight search attempted on date ' +  my_date + ' ' + flight + '; url: ' + my_url
                # 如果找到8月份的航班发送邮件提醒并播放声音
                if my_date[5:7]=='08':
                    playsound('D:\python\pydata-book\Style.mp3')  # play a sound if desirable flight is found. in this case, August flight
                    notification(to_list, mail_body, flight)
                # 如果航班不是8月份的，只是播放声音
                else:
                    print('flight date:', my_date)
                    playsound('D:\python\pydata-book\TextNow.mp3')
#                 time.sleep(10)
                # 将所有航班的最早飞行日期和url汇总发送邮件
                all_flights.append(mail_body)
                found = True
                break
            # 如果不及时退出，会有很多chrome, chromedriver在运行，内存消耗很大
            finally:
                driver.close()
                driver.quit()
        print('\n\n\n')
    print(all_flights)
    emails = ''.join(all_flights)
    notification(to_list, emails, 'all_flights')
    print('End of round {}\n\n\n'.format(i))
# playsound('D:\python\pydata-book\Style.mp3') 
driver.quit()  
