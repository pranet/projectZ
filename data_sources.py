from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from models import Result


class AbstractDataSource(ABC):
    @abstractmethod
    def get_all_entries(self, keyword: str):
        pass


class ChromeSeleniumDataSource(AbstractDataSource):
    def __init__(self, username, password, query_url):
        chromedriver_path = "resources/chromedriver"
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        self.browser = webdriver.Chrome(chromedriver_path, chrome_options=options)
        self.browser.implicitly_wait(100)
        self.query_url = query_url
        self.__login(username, password)

    def __login(self, username: str, password: str):
        self.browser.get(self.query_url)
        self.browser.find_element_by_id("elInput_auth").send_keys(username)
        self.browser.find_element_by_id("elInput_password").send_keys(password)
        self.browser.find_element_by_xpath("//button[text()='Sign In']").click()

    @staticmethod
    def __get_row_data(element):
        columns = element.find_elements_by_xpath("td")
        return Result(name=columns[0].text, price=int(columns[1].text.replace(",", "")), quantity=columns[2].text,
                      s_name=columns[3].text,
                      where=columns[4].text)

    def get_all_entries(self, keyword: str):
        self.browser.get(self.query_url)
        item_name = self.browser.find_element_by_id("form-itemname")
        item_name.clear()
        item_name.send_keys(keyword)
        self.browser.find_element_by_xpath("//button[text()='Search']").click()
        data = []
        while True:
            results_on_this_page = self.browser.find_element_by_id("datatable1").find_element_by_tag_name(
                "tbody").find_elements_by_tag_name("tr")
            for result in results_on_this_page:
                try:
                    data.append(self.__get_row_data(result))
                except:
                    continue
            next_button = self.browser.find_element_by_id("datatable1_next")
            if "disabled" in next_button.get_attribute("class"):
                break
            else:
                next_button.click()
        return data

    def __del__(self):
        self.browser.close()
