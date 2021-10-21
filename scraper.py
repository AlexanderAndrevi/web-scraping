import requests
import lxml.html as html
import os 
import datetime


HOME_URL = 'https://www.laestrella.com.pa/'
XPATH_LINK_TO_ARTICLE ='//h3[@class="title"]/a/@href'
XPATH_TITLE = '//h1[@class="article-title "]/text()'
XPATH_SUMMARY = '//p[@class="article-epigraph "]/text()'
XPATH_BODY = '//p[@class="paragraph "]/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                try:
                    title = parsed.xpath(XPATH_TITLE)[0]
                except:
                    title = 'Sin título'
                try:
                    summary = parsed.xpath(XPATH_SUMMARY)[0]
                except:
                    summary = 'Sin resumen'
                try:
                    body = parsed.xpath(XPATH_BODY)
                except:
                    body = 'No existe la noticia'
            except IndexError as ie:
                print(ie)
            with open(f'{today}/{title}.txt', 'w' , encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)



def parse_home():

    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            links_fixed_list = []
            for link in links_to_notices:
                link_fixed = 'https://www.laestrella.com.pa' + link
                links_fixed_list.append(link_fixed)
            
            print(links_fixed_list)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_fixed_list:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
        pass
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()