from bs4 import BeautifulSoup as B_S
import requests
import csv
import time
# from urllib3.exceptions import InsecureRequestWarning
# from urllib3 import disable_warnings

html_file_path = 'main_source.html'  
file = open(html_file_path, "r")   
html = file.read()

def get_html_data(url):
    try:
        time.sleep(5)
        #disable_warnings(InsecureRequestWarning)
        res = requests.get(url)
        html = res.text
    except:
        html = None

    return html

def get_faculty_links(html):
    soup = B_S(html , 'html.parser')
    list_1 = []
    all_faculity_list = soup.find_all('li', class_=["wdp-faculty-index-row", "wdp_listing-row"])
    for i in all_faculity_list:
        a_tag = i.find('a')
        url = a_tag ['href']
        list_1.append(url)
    return list_1 
all_links = get_faculty_links(html)        

def faculty_info(html_text):
    soup = B_S(html_text , 'html.parser')
    prof_info = soup.find('div', class_=["wfp-header"])
    n = prof_info.find('h1')
    name = n.text 
    title_info= prof_info.find('ul', class_=['wfp-header-titles group'])
    title_text = title_info.text.strip()

    try:
       department = title_text.split(" of ")[1]
    except:
        department = '----'
    contact = prof_info.find_all('ul',class_=['wfp-contact-information'])
    ul_1 = contact[0]
    ul_2 = contact[1]
    ul_1_li = ul_1.find_all("li")
    try:
        e = ul_1_li[0].find('a')
        email = e.text
    except:
        email = '----'
    try:
        p = ul_1_li[1].find('a')
        phone = p.text 
    except:
        phone = "----"
    try:
        a = ul_2.find('li').text 
        _list = a.split(':')[1].strip().splitlines() 
        if len(_list) == 1:
            info = _list.pop()
            c = info.split(',')
            address = c[0]  
            city = "----"
            z = c[1].strip()
            s = z.split(' ')
            state = s[0]
            zip_code = s[1].strip()
            
        else:
            info = _list.pop()
            c = info.split(',')
            city = c[0]
            z = c[1].strip()
            s = z.split(' ')
            state = s[0]
            zip_code = s[1].strip()
            address = ' '.join(i for i in _list)
    except:
        address = '----'
        city = '----' 
        state = '----'
        zip_code = '----'   
    list_3 = []
    list_3.append(name)
    list_3.append(title_text)
    list_3.append(department)
    list_3.append(email)   
    list_3.append(phone)
    list_3.append(address)
    list_3.append(city)
    list_3.append(state)
    list_3.append(zip_code)          
    return list_3


def csv_writer(lst):
    with open('faculty_data.csv' ,'w',newline ='') as f:
        w = csv.writer(f)
        w.writerow(['Name','Title','Department','Email','Phone No.','Address','City','State','Zip_code'])
        w.writerows(lst) 

lst_4=[]
"""here we extract the data of only 20 faculties just to 
check that this program is perfectly working or not.
You can also extract the data of all 280 faculties"""

for url in all_links[:20]:
    print("Getting data of url : ", url)
    html = get_html_data(url)
    if html:
        print("Getting faculty info from html")    
        _list_ = faculty_info(html)

        lst_4.append(_list_)

print("Writing data into csv file")
csv_writer(lst_4)