import requests
import re
import urllib.request
import pdfkit
import sys
from bs4 import BeautifulSoup

url = 'https://www.passeidireto.com/arquivo/39116684/black-hat-python-programacao-p-justin-seitz'

#url = 'https://www.passeidireto.com/arquivo/16451988/aprenda_a_programar-luciano_ramalho' 
#url = 'https://www.passeidireto.com/arquivo/18068120/use-a-cabeca-python' 
def get_key(url):
    page = requests.get(url)
    #print(page.content)
    soup = BeautifulSoup(page.content,'html.parser')
    cover = soup.find(attrs={'class':'cover'})
    src_values = cover.img['src']
    print(cover.img['src'])
    key_re = re.compile(r'.{8}-.{4}-.{4}-.{4}-.{12}')
    res = key_re.findall(src_values)
    print(res)
    print()
    #print(cover.prettify())
    return res[0]
def get_link_root(key):
    link = ('https://files.passeidireto.com/'+ key + '/')
    print(link)
    return link

def get_css(link, key):
    css_url = link + key + '.css'
    urllib.request.urlretrieve(css_url, key +'.css')
    return css_url

def get_html_pages(link, n_page):
    links_html = []
    for indexI in range(1, n_page):
        link_html = link + str(indexI) + '.html'
        links_html.append(link_html)
    print(links_html)
    return links_html

def download_html_page(links_html, css):
    print(len(links_html))
    for indexI in range(0, len(links_html)):
        page = add_css_in_page(links_html[indexI],css)
        with open(str(indexI) +'.html', 'w' ) as file:
            file.write(str(page))
       #urllib.request.urlretrieve(links_html[indexI], )
        print('>OK')

    return 
def add_css_in_page(url, css):
    print('dentro')
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    outros_css = '''<link rel="stylesheet" href="pd-material-viewer.3b3f13a5.css">
<link rel="stylesheet" href="pd-material-viewer~pd-profile~pd-search~pd-subject.f4b332e0.css">'''
    link_ref = BeautifulSoup('<link rel="stylesheet" href="'+ css +'">', 'html.parser')
    soup.append(link_ref)  
    return soup  
    

def get_fonts(css, url):
    arq = open(css)
    font_re1 = re.compile('/.{2}.woff|/.{3}.woff')
    fonts_links = font_re1.findall(str(arq.read()))
    res_fonts_link = []
    print(fonts_links)
    print(len(fonts_links))
    for indexI in fonts_links:        
        namefile = indexI.replace('/' , '')
        print(namefile)
        res_fonts_link.append(url+ namefile)
        urllib.request.urlretrieve(url+ namefile, namefile)
        print('>OK')
    return res_fonts_link
    

def modf_css(css, links_font):        
    with open(css) as file:
        css_content = str(file.read())
        file.close()
    
    
    for indexI in range(0 ,links_font):
        link = 'https://files.passeidireto.com/f4ddf77c-ac64-4d45-a6f9-be81925086cf/'
        css_content = css_content.replace(link, '')
    with open(css, 'w') as arq:
        arq.write(css_content)

def convert_pdf(qntd):
    files = []
    for indexI in range(0,qntd-1):
        file = str(indexI) +'.html'
        files.append(file)

    pdfkit.from_file(files, 'out.pdf')
def inputUser():
    try:
        value = str(sys.argv[1])
        valueNumber = str(sys.argv[2])
    except:
        value = str(input('Informe o Link'))
        valueNumber = str(input('qntd pagina'))
    return value, valueNumber

url_test, qntd = inputUser()
print(qntd)
key_test = get_key(url_test)
link_test = get_link_root(key_test)
get_css(link_test, key_test)
links_html_pages_test = get_html_pages(link_test, int(qntd))
css_link = key_test+'.css'
fonts_links = get_fonts(css_link,link_test)
download_html_page(links_html_pages_test, css_link)
modf_css(css_link, len(fonts_links))
convert_pdf(int(qntd))
#add_css_in_page(links_html_pages_test[30], css_link)

