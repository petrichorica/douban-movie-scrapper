from bs4 import BeautifulSoup as soup
import re, time
from selenium import webdriver


page_url = 'https://movie.douban.com/top250'

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'}
# r = requests.get(page_url, headers=headers)
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37

'''
Need to download the chromedriver of appropriate version
'''
browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
browser.get(page_url)
browser.implicitly_wait(100)

file_name = 'douban_movie_top250.csv'
file_headers = 'title,release date,region,starring,rating\n'
with open(file_name, 'w') as f:
    f.write(file_headers)

xpath = '//*[@id="content"]/div/div[1]/div[2]/span[3]/a'

count = 0
page = 0
while True:
    page_soup = soup(browser.page_source, 'html.parser')

    content = page_soup.findAll('div', {'id': 'content'})
    films = content[0].findAll('div', {'class': 'item'})

    for film in films:
        title_container = film.find('span', {'class': 'title'})
        title = title_container.text
        # title = title.replace(' ', '').replace('\n', '').replace('\r', '')
        
        detail_container = film.find('div', {'class': 'bd'})
        starring_and_date = detail_container.text

        date = re.search('[0-9]{4}', starring_and_date).group()
        region = re.search('[0-9]{4}(\(.*\))?\s/\s([^/0-9]*)', starring_and_date).group(2)
        region = region.replace('\xa0', ' ').strip()
        starring = re.search('\S.*(?=\n)', starring_and_date).group()
        starring = starring.strip()
        
        rating_container = film.find('span', {'class': 'rating_num'})
        rating = rating_container.text
        
        count += 1
        print('--%d--'%count, '\n')
        print(title, date, region)
        print(starring)
        print('Rating:', rating)
        print()
        
        seq = [title, date, region, starring, rating]
        line = ','.join(seq)
        with open(file_name, 'a') as f:
            f.write(line.encode("gbk", 'ignore').decode("gbk", "ignore") + '\n')
    
    page += 1
    if page >= 10:
        break

    try:
        browser.find_element_by_xpath(xpath).click()
        time.sleep(2)
    except:
        break

browser.quit()