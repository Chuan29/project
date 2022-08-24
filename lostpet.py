import requests, time
from bs4 import BeautifulSoup
import pandas as pd

url = "https://wepet.tw/%E8%B5%B0%E5%A4%B1%E5%8D%94%E5%B0%8B?page={}"

pet_list = []
links = [url.format(i) for i in range(1,39)]
for link in links:
    html = requests.get(link).text
    soup = BeautifulSoup(html,"html.parser")
    data = soup.find_all(class_="media-img")
    for d in data:
        href = d.get('href')   #每隻寵物網址
        html_1 = requests.get(href).text
        soup_1 = BeautifulSoup(html_1 ,"html.parser")
        conts = soup_1.find_all(class_="col-12 mb-1")  #寵物表格內容
        name = soup_1.find(class_="font-size-40 font-weight-bold mt-2 mb-4").text  #寵物名字
        img = soup_1.find(class_='img-fluid').get('src')   #寵物圖片
        list_cont = list()
        for cont in conts:
            try:
                cont.span.extract()   #把span的內容拿掉
                list_cont.append(cont.text)
            except:
                pass
        try:
            item = dict()
            item['href'] = href
            item['name'] = name
            item['variety'] = list_cont[0]
            item['type'] = list_cont[1]
            item['gender'] = list_cont[2]
            item['body'] = list_cont[3]
            item['color'] = list_cont[4]
            item['age'] = list_cont[5]
            item['lostdate'] = list_cont[6]
            item['area'] = list_cont[7]
            item['date'] = list_cont[8]
            item['img'] = img
            pet_list.append(item)
        except Exception:
            print("error")   
        time.sleep(2)

df = pd.DataFrame.from_dict(pet_list)
df.to_csv("pet.csv", index = False, encoding="utf_8_sig")
print("done")