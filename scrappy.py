from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import logging
import pickle
import os


class ScrapyBot:
    def __init__(self, delay=5):
        if not os.path.exists("data"):
            os.makedirs("data")
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        self.delay=delay
        logging.info("Starting driver")
        self.driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe")

    def login(email, password):
        #логинимся в линкедине
        logging.info("Logging in")
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/login')
        #time.sleep(self.delay)

        self.driver.find_element_by_id('username').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)

        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)
        time.sleep(self.delay)

   """ def save_cookie(path):
                 with open(path, 'wb') as filehandler:
                     pickle.dump(self.driver.get_cookies(), filehandler)
         
             def load_cookie(path):
                 with open(path, 'rb') as cookiesfile:
                     cookies = pickle.load(cookiesfile)
                     for cookie in cookies:
                         self.driver.add_cookie(cookie)"""

    def search_linkedin(keywords, location):
        #функция, чтобы вводить вакансии в поле поиска
        logging.info("Searching jobs page")
        self.driver.get("https://www.linkedin.com/jobs/")

        search_keywords = self.driver.find_elements_by_class_name('jobs-search-box__text-input')
        search_bars = search_keywords[0]
        search_bars.send_keys(keywords)
        search_bars.send_keys(Keys.RETURN)
    
    def wait(self, t_delay=None):
        #функция, чтобы делать дэлеи и ждать, пока загрузится сайт
        delay = self.delay if t_delay == None else t_delay
        time.sleep(delay)

    def scroll_to(self, job_list_item):
        #функция чтобы скроллить
        self.driver.execute_script("arguments[0].scrollIntoView();", job_list_item)
        job_list_item.click()
        time.sleep(self.delay)
    
    def get_position_data(self, job):
        #возвращает список строк о вакансии в таком формате [position, company, location, details]
        [position, company, location] = job.text.split('\n')[:3]
        details = self.driver.find_element_by_id("job-details").text
        return [position, company, location, details]

    def wait_for_element_ready(self, by, text):
        try:
            WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((by, text)))
        except TimeoutException:
            logging.debug("wait_for_element_ready TimeoutException")
            pass

    def close_session(self):
        logging.info("Closing session")
        self.driver.close()

    def run(email, password, keywords, location):
        """if os.path.exists("data/cookies.txt"):
                                    self.driver.get("https://www.linkedin.com/")
                                    self.load_cookie("data/cookies.txt")
                                    self.driver.get("https://www.linkedin.com/")
                                else:"""
        self.login(
            email = email,
            password = password
        )
        #self.save_cookie("data/cookies.txt")

        logging.info("Begin linkedin keyword search")
        self.search_linkedin(keywords, location)
        self.wait()

        # скрейпим странички
        for pg in range(2, 1):
            # создаем список вакансий и скроллим
            jobs = self.driver.find_elements_by_class_name("occludable-update")
            for job in jobs:
                self.scroll_to(job)
                [position, company, location, details] = self.get_position_data(job)
                print(position)
                # do something with the data...

            # на след страницу
            bot.driver.find_element_by_xpath(f"//button[@aria-label='Page {pg}']").click()
            bot.wait()
        logging.info("Done scraping.")
        logging.info("Closing DB connection.")
        bot.close_session()


if __name__ == "__main__":
    email = "myemail@com"
    password = "mypswd"
    # log in and save cookies:
    bot.login(email=EMAIL, password=PASSWORD)
    bot.save_cookie("data/cookies.txt")

    # go to jobs page and search:
    keywords = "some string"
    location = "whatever location"
    bot.search_linkedin(keywords, location)
    bot.wait()

    # get all jobs from sidebar, scroll to each job and scrape info:
    jobs = bot.driver.find_elements_by_class_name("occludable-update")
    for job in jobs:
        bot.scroll_to(job)
        [position, company, location, details] = bot.get_position_data(job)

        # here I need to collect the data

    bot.close_session()