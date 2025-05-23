#!/Users/collinskigen/miniconda3/envs/selenium/bin/python
"""
Web scrapper!
"""
import os
import csv
import requests
import pdfplumber
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from .constants import PATH, URL, SEARCH_TERM, DIR, DATA


class Thesis:
    def __init__(self):
        service = Service(executable_path=PATH)
        driver = webdriver.Chrome(service=service)
        self.driver = driver
        all_data = []
        self.all_data = all_data
        super(Thesis, self).__init__()

    def land_site_page(self):
        self.driver.get(URL)
        self.driver.maximize_window()

    def thesis_profile(self, thesis):
        title = thesis.text
        thesis.find_element(By.XPATH, './/a').click()
        try:
            author = self.driver.find_element(
                By.XPATH, '//div[contains(@class,"simple-item-view-authors")]').text
        except BaseException:
            author=None
        date = self.driver.find_element(
            By.XPATH, '//span[text()="Date:"]/following::span[1]').text
        try:
            url = self.driver.find_element(
                By.XPATH, '//a[contains(@href,".pdf")]').get_attribute("href")
            response = requests.get(url)
            os.makedirs(DIR, exist_ok=True)
            if not os.path.isfile(
                    f"./{DIR}/{title[:50].replace('/', '_')}.pdf"):
                with open(f"./{DIR}/{title[:50].replace('/', '_')}.pdf", "wb") as f:
                    f.write(response.content)
        except BaseException:
            print("No pdf")
        search_term = SEARCH_TERM
        course = None
        if os.path.isfile(f"./{DIR}/{title[:50].replace('/', '_')}.pdf"):
            with pdfplumber.open(f"./{DIR}/{title[:50].replace('/', '_')}.pdf") as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        lines = text.split("\n")
                        for i, line in enumerate(lines):
                            if search_term in line:
                                course = f" {lines[i + 1]}" if i + \
                                    1 < len(lines) else None
                                break
                        if 'course' in locals():
                            break
        print(title, course)
        return (title, course, author, date)

    def scrape_thesis(self):
        page = 1
        thesis_count = 1
        self.driver.find_element(By.XPATH, '//a[text()="View more"]').click()
        while True:
            print(f"Scrapping.......page {page}")
            theses = self.driver.find_elements(
                By.XPATH, '//div[contains(@class,"artifact-title")]')
            for thesis in theses:
                print(f"thesis {thesis_count}")
                data = self.thesis_profile(thesis)
                self.all_data.append(data)
                self.driver.back()
                thesis_count = thesis_count + 1
                self.driver.execute_script("window.scrollBy(0, 125)")
            try:
                self.driver.find_element(
                    By.XPATH, '//a[text()="Next Page"]').click()
                page = page + 1
            except BaseException:
                break
        self.driver.close()
        print("Scrapping complete!!")
        return self.all_data

    def save_data(self):
        with open(DATA, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            header = ['Title', 'Course', 'Author', 'Date']
            writer.writerow(header)
            writer.writerows(self.all_data)
