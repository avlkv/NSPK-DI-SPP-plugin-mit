"""
Нагрузка плагина SPP

1/2 документ плагина
"""
# from pdfminer.high_level import extract_text           # Для извлечения текстов из pdf
from datetime import datetime                          # Для подсчета времени выполнения
# from datetime import timedelta                         # Для вывода пройденного времени
import time                                            # Для сна процесса
import logging                                         # Для логирования процесса
from selenium import webdriver                         # Для взаимодействия с драйвером браузера Chrome
# from selenium.webdriver.chrome.options import Options  # Для обозначения особенностей работы драйвера браузера Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By            # Для описания элементов
from selenium.webdriver.chrome.service import Service
# https://stackoverflow.com/questions/44503576/selenium-python-how-to-stop-page-loading-when-certain-element-gets-loaded
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import dateparser
from random import uniform
import pytz

from src.spp.types import SPP_document


class MIT:
    """
    Класс парсера плагина SPP

    :warning Все необходимое для работы парсера должно находится внутри этого класса

    :_content_document: Это список объектов документа. При старте класса этот список должен обнулиться,
                        а затем по мере обработки источника - заполняться.


    """

    SOURCE_NAME = 'mit'
    _content_document: list[SPP_document]

    def __init__(self, webdriver: WebDriver, last_document: SPP_document = None, max_count_documents: int = 100, *args, **kwargs):
        """
        Конструктор класса парсера

        По умолчанию внего ничего не передается, но если требуется (например: driver селениума), то нужно будет
        заполнить конфигурацию
        """
        # Обнуление списка
        self._content_document = []

        self.driver = webdriver
        self.wait = WebDriverWait(self.driver, timeout=20)
        self.max_count_documents = max_count_documents
        self.last_document = last_document

        # Логер должен подключаться так. Вся настройка лежит на платформе
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Parser class init completed")
        self.logger.info(f"Set source: {self.SOURCE_NAME}")
        ...

    def content(self) -> list[SPP_document]:
        """
        Главный метод парсера. Его будет вызывать платформа. Он вызывает метод _parse и возвращает список документов
        :return:
        :rtype:
        """
        self.logger.debug("Parse process start")
        try:
            self._parse()
        except Exception as e:
            self.logger.debug(f'Parsing stopped with error: {e}')
        else:
            self.logger.debug("Parse process finished")
        return self._content_document

    def _parse(self):
        """
        Метод, занимающийся парсингом. Он добавляет в _content_document документы, которые получилось обработать
        :return:
        :rtype:
        """
        # HOST - это главная ссылка на источник, по которому будет "бегать" парсер
        self.logger.debug(F"Parser enter")

        # ========================================
        # Тут должен находится блок кода, отвечающий за парсинг конкретного источника
        # -

        topics = {'Social media': 'https://news.mit.edu/topic/social-media',
                  'Wearable sensors': 'https://news.mit.edu/topic/wearable-sensors',
                  # 'Data': 'https://news.mit.edu/topic/data',
                  # 'School of Engineering': 'https://news.mit.edu/topic/school-engineering',
                  # 'Wearables': 'https://news.mit.edu/topic/wearables',
                  # 'Web': 'https://news.mit.edu/topic/web',
                  # 'Web development': 'https://news.mit.edu/topic/web-development',
                  # 'Social networks': 'https://news.mit.edu/topic/social-networks',
                  # 'Sustainability': 'https://news.mit.edu/topic/sustainability',
                  # 'System Design and Management': 'https://news.mit.edu/topic/system-design-and-management',
                  # 'Systems design': 'https://news.mit.edu/topic/systems-design',
                  # 'Systems engineering': 'https://news.mit.edu/topic/systems-engineering',
                  # 'Taxes': 'https://news.mit.edu/topic/taxes',
                  # 'Technology': 'https://news.mit.edu/topic/technology',
                  # 'Technology and policy': 'https://news.mit.edu/topic/technology-and-policy',
                  # 'Technology and society': 'https://news.mit.edu/topic/technology-society',
                  # 'Information systems and technology': 'https://news.mit.edu/topic/information-systems-and-technology',
                  # 'Information theory': 'https://news.mit.edu/topic/information-theory',
                  # 'Innovation and Entrepreneurship (I&E)': 'https://news.mit.edu/topic/innovation',
                  # 'Internet': 'https://news.mit.edu/topic/internet',
                  # 'Internet of things': 'https://news.mit.edu/topic/internet-things',
                  # 'Internet privacy': 'https://news.mit.edu/topic/internet-privacy',
                  # 'Machine learning': 'https://news.mit.edu/topic/machine-learning',
                  # 'Marketing': 'https://news.mit.edu/topic/marketing',
                  # 'Natural language processing': 'https://news.mit.edu/topic/natural-language-processing',
                  # 'Programming': 'https://news.mit.edu/topic/programming',
                  # 'Programming languages': 'https://news.mit.edu/topic/programming-languages',
                  # 'Quantum mechanics': 'https://news.mit.edu/topic/quantum-mechanics',
                  # 'Quantum computing': 'https://news.mit.edu/topic/quantum-computing',
                  # 'Quantum dots': 'https://news.mit.edu/topic/quantumdots',
                  # 'smartphones': 'https://news.mit.edu/topic/smartphones',
                  # 'Global economic crisis': 'https://news.mit.edu/topic/global-economic-crisis',
                  # 'Global economy': 'https://news.mit.edu/topic/global-economy',
                  # 'Google': 'https://news.mit.edu/topic/google',
                  # 'Facebook': 'https://news.mit.edu/topic/facebook',
                  # 'Finance': 'https://news.mit.edu/topic/finance',
                  # 'finances': 'https://news.mit.edu/topic/finances',
                  # 'Financial aid': 'https://news.mit.edu/topic/financial-aid',
                  # 'Electrical engineering and electronics': 'https://news.mit.edu/topic/electrical-engineering',
                  # 'Electrical engineering and computer science (EECS)': 'https://news.mit.edu/topic/electrical-engineering-and-computer-science-eecs',
                  # 'Electrical Engineering & Computer Science (eecs)': 'https://news.mit.edu/topic/electrical-engineering-computer-science-eecs',
                  # 'Cryptography': 'https://news.mit.edu/topic/cryptography',
                  # 'Cybersecurity': 'https://news.mit.edu/topic/cyber-security',
                  # 'Computer science and technology': 'https://news.mit.edu/topic/computers',
                  # 'Computer vision': 'https://news.mit.edu/topic/computer-vision',
                  # 'Analytics': 'https://news.mit.edu/topic/analytics',
                  # 'Artificial intelligence': 'https://news.mit.edu/topic/artificial-intelligence2',
                  # 'Big data': 'https://news.mit.edu/topic/big-data',
                  'Blockchain': 'https://news.mit.edu/topic/blockchain'}

        # chrome_options = webdriver.ChromeOptions()
        """Объект опций запуска драйвера браузера Chrome"""

        # chrome_options.add_argument('--headless')
        """Опция Chrome - Запуск браузера без пользовательского интерфейса (в фоне)"""

        # chrome_options.add_experimental_option('prefs', {'download.default_directory': downloads_dir, # Переопределение пути сохранения файлов для текущего запуска драйвера браузера Chrome
        #                                                 'profile.default_content_setting_values.automatic_downloads': 1}) # Разрешить автоматическую загрузку файла без доп. согласия

        counter = 0

        # chrome_options.page_load_strategy = 'none'

        # s = Service(executable_path=driver_path)
        # driver = webdriver.Chrome(service=s, options=chrome_options)
        # wait = WebDriverWait(driver, timeout=20)

        for i, topic in enumerate(topics):
            try:
                self.driver.get(topics[topic])
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.page-term--views--list')))
            except:
                print(f'=== Не удалось загрузить ({i + 1}/{len(topics)}) {topic} ===\nПропуск...')
                continue
            print(f'=== ({i + 1}/{len(topics)}) {topic} ===')
            more_pages = True
            while more_pages:
                try:
                    el_list = self.driver.find_elements(By.TAG_NAME, 'article')
                except Exception as e:
                    print('Error finding articles')
                for i, el in enumerate(el_list):
                    title = el_list[i].find_element(By.CLASS_NAME, 'term-page--news-article--item--title--link').text
                    web_link = el_list[i].find_element(By.CLASS_NAME,
                                                       'term-page--news-article--item--title--link').get_attribute(
                        'href')

                    # if web_link in df['web_link'].to_list():
                    #     # print(f'web_link already in df, skipping: {web_link}')
                    #     # print('-'*45)
                    #     continue
                    # else:
                    # print(f'new web_link: {web_link}')
                    try:
                        abstract = el_list[i].find_element(By.CLASS_NAME, 'term-page--news-article--item--dek').text
                    except:
                        print('No abstract')
                        abstract = ''

                    pub_date = dateparser.parse(el_list[i].find_element(By.TAG_NAME, 'time').get_attribute('datetime'))

                    # if pub_date < date_begin:
                    #     # print(f"Достигнута дата раньше {date_begin}. Далее...")
                    #     break
                    # else:
                    #     print(f'new up-to-date web_link: {web_link}')
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    try:
                        self.driver.get(web_link)
                        self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.news-article--content--body--inner')))
                        # time.sleep(uniform(0.5, 1.5))
                    except Exception as e:
                        # print('!!! Не удалось загрузить страницу. Пропуск...')
                        # print('-' * 45)
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        continue
                    text_content = self.driver.find_element(By.CLASS_NAME, 'news-article--content--body--inner').text
                    try:
                        related_topics = [x.text for x in self.driver.find_elements(By.XPATH,
                                                                               '//li[@class=\'news-article--topics-list--item\']')]
                    except:
                        related_topics = ''
                    try:
                        author = self.driver.find_element(By.CLASS_NAME, 'news-article--authored-by').text
                    except:
                        author = ''
                    other_data = {}
                    other_data['tags'] = related_topics
                    other_data['author'] = author

                    # print(web_link)
                    # print(title)
                    # print(pub_date)
                    # print(related_topics)
                    # print(text_content)
                    # row_data_list = [title, abstract, text_content, web_link, None,
                    #                  other_data, pub_date, datetime.now()]

                    # df.loc[df.shape[0]] = row_data_list

                    doc = SPP_document(None,
                                       title,
                                       abstract,
                                       text_content,
                                       web_link,
                                       None,
                                       other_data,
                                       pub_date,
                                       datetime.now())

                    self.find_document(doc)

                    # print('added to df')
                    # print('-' * 45)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                try:
                    next_page = self.driver.find_element(By.XPATH, '//*[contains(@class, \'pager--button--next\')]')
                    # print('Found next page')
                    self.driver.execute_script('arguments[0].click()', next_page)
                    time.sleep(uniform(0.5, 1.5))
                    # print('Next page load')
                    more_pages = True
                except Exception as e:
                    # print('No more pages in topic, next topic...')
                    # print(e)
                    more_pages = False
            # df.to_csv(df_path, sep='\t', index=False)
            # print(f' ============ Сохранен df: {df_path}')

        # print('=' * 90)
        # print(f'new docs: {counter}')

        # df.to_csv(df_path, sep='\t', index=False)



        # ---
        # ========================================
        ...

    @staticmethod
    def _find_document_text_for_logger(doc: SPP_document):
        """
        Единый для всех парсеров метод, который подготовит на основе SPP_document строку для логера
        :param doc: Документ, полученный парсером во время своей работы
        :type doc:
        :return: Строка для логера на основе документа
        :rtype:
        """
        return f"Find document | name: {doc.title} | link to web: {doc.web_link} | publication date: {doc.pub_date}"

    def find_document(self, _doc: SPP_document):
        """
        Метод для обработки найденного документа источника
        """
        if self.last_document and self.last_document.hash == _doc.hash:
            raise Exception(f"Find already existing document ({self.last_document})")

        if self.max_count_documents and len(self._content_document) >= self.max_count_documents:
            raise Exception(f"Max count articles reached ({self.max_count_documents})")

        self._content_document.append(_doc)
        self.logger.info(self._find_document_text_for_logger(_doc))

