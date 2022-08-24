from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import jieba

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
PATH = "C:/Users/user/Desktop/chromedriver.exe"
driver = webdriver.Chrome(PATH,options=options)
#輸入想搜尋的寵物品種中英文
kw = {"柴犬":"Shiba_Inu"}

#driver.maximize_window()   #視窗最大化
driver.get("https://www.dcard.tw/f/pet")  
WebDriverWait(driver, 10).until( 
    EC.presence_of_element_located((By.CLASS_NAME,"sc-a6efb4b-0")))
search = driver.find_element("name","query")
search.send_keys(next(iter(kw)))
search.send_keys(Keys.RETURN) 
time.sleep(3)

list1 = []

for i in range(3):
    data = driver.find_elements(By.CLASS_NAME,'sc-8fe4d6a1-3')
    for d in data:
        href = d.get_attribute('href')
        if href in list1:
            pass
        else:
            list1.append(href)
        print(href)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
time.sleep(5)

print(f'總共{len(list1)}筆')

list2 = []

for j in list1:
    try:
        driver.get(j)
        time.sleep(5)
        datas = driver.find_element(By.CLASS_NAME,'sc-ba53eaa8-0').text
        list2.append(datas)
    except:
        print("err")

driver.quit()

print(f'總共{len(list2)}篇')

# 存成txt檔
# with open('{}.txt'.format(kw[next(iter(kw))]), 'w+', encoding='utf-8') as f:
#     f.write(str(list2))
#     f.seek(0)
#     data = f.read()

with open("stopwords.txt", "rt", encoding="utf-8") as fp:
    stopwords = [word.strip() for word in fp.readlines()]

jieba.load_userdict("dict.txt")   #自定義詞庫
keyterms = [keyterm for keyterm in jieba.cut(str(list2)) 
            if keyterm not in stopwords]
text = ",".join(keyterms)
mask = np.array(Image.open('cloud.jpg'))
wd = WordCloud(background_color='white',mask=mask, 
                width=1000, height=860, margin=2, 
                font_path='simhei.ttf').generate(text)

#print(text)

plt.imshow(wd, interpolation="bilinear")
plt.axis("off")
plt.show()