import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


def download_pic(url, name, path):

    if not os.path.exists(path):
        os.makedirs(path)
    res = urllib.request.urlopen(url, timeout=3).read()

    with open(path + name +'.jpg', 'wb') as file:
        file.write(res)
        file.close()


#//*[@id="hdtb-msb"]/div[1]/div/div[3]/a


def get_image_url(num, key_word):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #url = "https://www.google.com/" omit this step, because we can directly use google image url
    
    #driver.maximize_window() if you want to see what driver does in fullscreen
    url = 'https://images.google.com/'
    driver.get(url)
    box = driver.find_element('xpath','/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
    #key_word = input('Search for word:\n')
    box.send_keys(key_word)
    box.send_keys(Keys.ENTER)
    #box = driver.find_element('xpath','//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()


    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element('xpath','//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
        except:
            pass
        if new_height == last_height:
            try:
                box = driver.find_element('xpath','//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
            except:
                break
        last_height = new_height
    # num set 10 for testing

    image_urls=[]
    for i in range(1, num):
        try:
            driver.execute_script("window.scrollTo(0, 0);")
            image = driver.find_element('xpath', '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img').click()
            time.sleep(4)
            image_original = driver.find_element('xpath', '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
            image_url = image_original.get_attribute("src")
            image_urls.append(image_url)
            print(str(i) + ': ' + image_url)
        except:
            print(str(i) + ': error')

    return image_urls


if __name__ == '__main__':
    key_word = input('Keyword for Searching:\n')
    num = int(input('How many images you want to download:\n'))
    folder_name = input('give a name for Folder storing images:\n')


    path = os.getcwd() + '\\'+ key_word + '\\'
    print(path)
    image_urls = get_image_url(num, key_word)
    count = 0
    for index, url in enumerate(image_urls):
        try:
            print('image: '+ str(index) + " start to download")
            download_pic(url, str(index), path)
            count += 1
        except Exception as e:
            print(e)
            print('image: '+ str(index) + ' download failure')
            continue
    print()
    print(f'Overall, successfully download {count} images')




