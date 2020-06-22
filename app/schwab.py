import time
from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class Schwab:
    def __init__(self, download_dir):
        # set profile to enable easier downloading
        # see https://selenium-python.readthedocs.io/faq.html#how-to-auto-save-files-using-custom-firefox-profile  # noqa: E504

        fp = webdriver.FirefoxProfile()

        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", download_dir)
        fp.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/pdf"
        )
        fp.set_preference("pdfjs.disabled", True)

        self.driver = webdriver.Firefox(firefox_profile=fp)

    def login(self):
        self.driver.get("https://schwab.com/")
        input("Authenticate and then press Enter to continue...")

    def download_statements(self):

        # statements page
        self.driver.get("https://client.schwab.com/Apps/accounts/statements")
        time.sleep(5)

        # 10 years
        self.driver.find_element_by_xpath(
            "//*[@id='statements-daterange1']/option[text()='Last 10 Years']"
        ).click()

        # select statements
        stmt_box = self.driver.find_element_by_xpath(
            "//*[@id='StatementsChkBx']"
        )
        if not stmt_box.is_selected():
            stmt_box.click()

        # deselect other doc types
        other_doc_types = [
            "TaxFormsChkBx",
            "LettersChkBx",
            "ReportsPlansChkBx",
            "TradeConfirmsChkBx",
        ]
        for odt in other_doc_types:
            box = self.driver.find_element_by_xpath(f"//*[@id='{odt}']")
            if box.is_selected():
                box.click()

        # click search
        self.driver.find_element_by_xpath("//*[@id='btnSearch']").click()
        time.sleep(5)
        # self.driver.find_element_by_xpath("")

        # select table rows
        table = self.driver.find_element_by_xpath("//*[@id='gridTable']")
        rows: List[WebElement] = table.find_elements_by_xpath(
            ".//tr[@scope='row']"
        )
        for row in rows:
            # position browser
            ActionChains(self.driver).move_to_element(row).perform()
            time.sleep(0.25)
            self.driver.execute_script("arguments[0].scrollIntoView();", row)
            time.sleep(0.25)

            # download statement
            save_button = row.find_element_by_xpath(".//a[@role='link']")
            save_button.click()
