#!/usr/bin/env python
# coding: utf-8

# In[1]:

import threading
import queue





from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
from requests_html import HTMLSession
import time
import datetime
import os








user= "posds2"
password = "5Y0v2LQyk87"


current_date = datetime.datetime.now()

if current_date.weekday() == 0:
    current_date = current_date-datetime.timedelta(days=3)
else:
    current_date = current_date-datetime.timedelta(days=1)




year = str(current_date.year)
month = str(current_date.month) if(len(str(current_date.month))) >= 2 else '0'+str(current_date.month)
day = str(current_date.day) if(len(str(current_date.day))) >= 2 else '0'+str(current_date.day)




used_date = year+'-'+month+'-'+ day








def get_dates_and_run(dates):
    for date in dates:
        get_attendance(date)

#get the user choice

def get_input(message, channel):
    response = input(message)
    channel.put(response)


def input_with_timeout(message, timeout):
    channel = queue.Queue()
    message = message + " [{} sec timeout]:".format(timeout)
    thread = threading.Thread(target=get_input, args=(message, channel))
    # by setting this as a daemon thread, python won't wait for it to complete
    thread.daemon = True
    thread.start()

    try:
        response = channel.get(True, timeout)
        return response
    except queue.Empty:
        pass
    return None



def get_attendance(date):
    print(date)
    session = HTMLSession()
    session.auth = (user, password)
    for server in ['',2,4]:
        time_list = {}
        start = time.time()
        ext = 0
        if server== 4 :
            ext = 9040
        else:
            ext = 9151
        pause = 'r'
        for num in range(9001,ext):

            prog = (num-9000)/(ext-9000)
            
            while True :
##                pause = input_with_timeout('if you want to pause press (p)',3)
##                if pause == 'p':
##                    pause = input('the scraping process is paused press any key to continue!')
                try:
                    hostname = 'pos'+str(server)+'.mscall.net/vicidial/user_stats.php?DB=0&NVAuser=&did_id=&did=&pause_code_rpt=&park_rpt=&begin_date='+date+'&end_date='+date+'&user='+str(num)+'&call_status=&submit=submit'
            


                    auth = session.post('http://' + hostname,timeout=20)
                    response = session.get('http://' + hostname )
                    bs = BeautifulSoup(response.text,"html.parser")
                    result = bs.find_all('center')[4].find_all('td')[11].text
                    #print(num, result)
                    time_list[num] = [result,f'pos{server}']
                    break
                except:
                    print('connection lost trying again...')
                

            os.system('cls')
            print(f'scraping pos{server} data ==>')
            print('|','='*round(20*prog),' '*round(20*(1-prog)),'|',str(round((prog*100),2)),'%')
            

        #saving the results in dataframes then convert it to excel 
        df = pd.DataFrame(index= time_list.keys(),data=time_list.values())
        df.to_excel(f'd:/php_db/txt/scraping the new data/{date}POS{server}.xlsx')
        end = time.time()
        print(f'the pos{server} list took : ',round((end-start)/60),'min')
        

choice = input_with_timeout("Commands: 1 ==> noraml 2 ==> run now:", 5)
time.sleep(3)




while True:
    if ((time.localtime().tm_hour > 0 or time.localtime().tm_min > 31)and (choice != '2')):
        os.system('cls')
        print(f'the time remaining for the next scrape is {23- time.localtime().tm_hour} h ' +
        f'{60 - time.localtime().tm_min} m {60 - time.localtime().tm_sec} s ')
        
        time.sleep(1)
        continue
    else:
        date = [used_date]
        get_dates_and_run(date)
        choice = '1'
    





