import os
import time

from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from base.models import Noticia

from base64 import b64decode
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from .get_text import extract_text


def print_pdf(url, filename):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(executable_path='webdrive/chromedriver', options=options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(10)
    driver.implicitly_wait(5)
    internal_id = filename.split('/pdf/')[ 1 ].split('.pdf')[0]
    try:
        driver.get(url)
    except TimeoutException:
        print(f'Timeout exception ({internal_id}): {url}')
        driver.quit()
        return None, None
    except Exception as e:
        print(f'General exception ({internal_id}): {url}')
        print(e.__str__())
        driver.quit()
        return None, None

    html = driver.page_source
    if url != driver.current_url:
        print(f'URL Redirected: filename: {filename}')
        print(f'{url}, {driver.current_url}')

    # código de exemplo para travar a página após encontrar um elemento
    # if driver.find_element(By.XPATH, '//*[@id="tags"]'):
    possible_btns = ["toolkit-privacy-box__btn",
                     "cookie-banner-lgpd_accept-button", "onesignal-slidedown-cancel-button"]
    #for class_btn in possible_btns:
    #    try:
    #        button = driver.find_element_by_class_name(class_btn)
    #        webdriver.ActionChains(driver).click(button)
    #        break
    #    except NoSuchElementException:
    #        None

    try:
        a = driver.execute_cdp_cmd("Page.printToPDF", {"path": 'html.pdf', "format": 'A4'})
        # Define the Base64 string of the PDF file
        if a:
            b64 = a['data']
            # Decode the Base64 string, making sure that it contains only valid characters
            raw_content = b64decode(b64, validate=True)
            if raw_content[0:4] != b'%PDF':
                raise ValueError('Missing the PDF file signature')
            # Write the PDF contents to a local file
            f = open(filename, 'wb')
            f.write(raw_content)
            f.close()
        else:
            raise ValueError('No data')
    except Exception as e:
        print(f'PDF exception ({internal_id}): {url}')
        print(e.__str__())
        filename = None
    finally:
        driver.quit()

    return html, filename


class Command(BaseCommand):
    help = 'Importa as URLs em formato de texto e PDF'

    def add_arguments(self, parser):
        parser.add_argument('-i', '--id', type=str, help='Id da Notícia')

    def handle(self, *args, **options):
        base_dir = os.path.dirname(os.path.abspath(__file__)).split('/')[:-3]
        base_dir = '/'.join(base_dir)
        html_path = os.path.join('/', base_dir, 'media', 'html')
        pdf_path = os.path.join('/', base_dir, 'media', 'pdf')
        img_path = os.path.join('/', base_dir, 'media', 'img')
        os.makedirs(pdf_path, exist_ok=True)
        os.makedirs(img_path, exist_ok=True)

        tot_lidos = 0
        tot_scrap = 0
        tot_pdfs = 0
        st = time.time()

        if options['id']:
            dataset = Noticia.objects.filter(id=options['id'], revisado=False)
        else:
            dataset = Noticia.objects.filter(url_valida=True, revisado=False, id__gt=299)

        for noticia in dataset:
            tot_lidos += 1
            if tot_lidos % 100 == 0:
                print(f'Lidos: {noticia.id} {noticia.id_externo}')

            # if not os.path.exists("%s/%d.pdf" % (html_path, noticia.id)):
            print(f'Scraping {noticia.url}')
            pdf_filename = '%s/%d.pdf' % (pdf_path, noticia.id)
            html, pdf_result = print_pdf(url=noticia.url, filename=pdf_filename)
            if html:
                if pdf_result:
                    tot_pdfs += 1
                else:
                    if os.path.exists(pdf_filename):
                        os.rename(pdf_filename, pdf_filename.replace('.pdf','_old.pdf'))

                tot_scrap += 1
                soup = BeautifulSoup(html, features="html.parser")
                # remove all script and style elements
                for script in soup(["script", "style", "noscript"]):
                    script.extract()
                with open(f"{html_path}/{noticia.id}.html",'w',encoding='utf-8') as f:
                    f.write(str(soup))

                # get text
                noticia.texto_completo = extract_text(soup)
                noticia.atualizado = True
                noticia.save()
            else:
                noticia.atualizado = False
                noticia.save()

        print(f'Total de registros lidos: {tot_lidos}')
        print(f'Total de pdfs gerados: {tot_pdfs}')
        print(f'Total de textos capturados: {tot_scrap}')
        elapsed_time = (time.time() - st) / 60
        print('Execution time:', elapsed_time, 'minutes')