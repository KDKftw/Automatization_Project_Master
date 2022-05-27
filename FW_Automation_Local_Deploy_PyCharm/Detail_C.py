from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from FW_Automation_Local_Deploy_PyCharm.to_import import acceptConsent, closeExponeaBanner, URL_detail, sendEmail, setUp, tearDown, generalDriverWaitImplicit
import time
from selenium.webdriver.support import expected_conditions as EC
import unittest
from generalized_test_functions import generalized_Detail_terminyAceny_potvrdit_chooseFiltr, generalized_list_string_sorter

##global
terminyAcenyTabXpath = "//*[@id='terminyaceny-tab']"
potvrditPopupXpath = "//*[@data-testid='popup-closeButton']"

#meal filter
stravovaniBoxXpath= "//*[@class='fshr-button-content fshr-icon fshr-icon--forkSpoon js-selector--catering']"
valueToFilterStravaAllIncXpath = "//*[@id='filtr-stravy-detail']//*[contains(text(),'All inclusive')]"
zvolenaStravaVboxuXpath = "//*[@class='js-subvalue f_text--highlighted']"
stravaVterminechXpath = "//*[@class='fshr-termin-catering js-tooltip js-tooltip--onlyDesktop']"

#airport filter
dopravaBoxXpath = "//*[@class='fshr-button-content fshr-icon fshr-icon--plane js-selector--travel']"
dopravaBrnoXpath = "//*[@data-value='4305']"


class TestDetailHotelu_C(unittest.TestCase):
    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def omlouvamese_paragraph(self):
        time.sleep(1)
        try:
            omlouvameParagraph = self.driver.find_element_by_xpath(
                "//*[@class='fshr-paragraph fshr-paragraph--centered']")
            if omlouvameParagraph.is_displayed():
                return

        except NoSuchElementException:
            pass

    def test_detail_fotka(self):

        self.driver.get(URL_detail)

        acceptConsent(self.driver)

        time.sleep(1)
        closeExponeaBanner(self.driver)

        imageDetail = self.driver.find_element_by_xpath("//*[@id='gallery01Trigger']//img")
        imageDetailSrc = imageDetail.get_attribute("src")
        try:
            self.driver.set_page_load_timeout(5)
            self.driver.get(imageDetailSrc)
        except TimeoutException:
            url = self.driver.current_url
            msg = "Problem s fotkou src, detailhotelu,  TimeoutException " + url
            sendEmail(msg)

        try:
            image = self.driver.find_element_by_xpath("/html/body/img")
            assert image.is_displayed() == True
            if image.is_displayed():
                print("its ok")
        except NoSuchElementException:
            url = self.driver.current_url
            msg = "Problem s fotkou src, detailhotelu,  NoSuchElementException " + url
            sendEmail(msg)

        self.test_passed = True
    def test_detail_terminy_filtr_meal(self):
        self.driver.maximize_window()
        def omlouvamese_paragraph(self):
            time.sleep(1)
            try:
                omlouvameParagraph = self.driver.find_element_by_xpath(
                    "//*[@class='fshr-paragraph fshr-paragraph--centered']")
                if omlouvameParagraph.is_displayed():
                    return

            except NoSuchElementException:
                pass

        self.driver.get(URL_detail)

        time.sleep(1)
        acceptConsent(self.driver)



        generalized_Detail_terminyAceny_potvrdit_chooseFiltr(self.driver, terminyAcenyTabXpath, potvrditPopupXpath,
                                                             stravovaniBoxXpath, valueToFilterStravaAllIncXpath)
        time.sleep(1.2)

        zvolenaStravaVboxu = self.driver.find_element_by_xpath(zvolenaStravaVboxuXpath)
        zvolenaStravaVboxuString = zvolenaStravaVboxu.text.lower()
        print(zvolenaStravaVboxuString)


        generalized_list_string_sorter(self.driver, stravaVterminechXpath, zvolenaStravaVboxuString)


        self.test_passed = True

    def test_detail_terminy_filtr_airport(self):
        self.driver.maximize_window()
        def omlouvamese_paragraph(self, driver):
            time.sleep(1)
            try:
                omlouvameParagraph = self.driver.find_element_by_xpath(
                    "//*[@class='fshr-paragraph fshr-paragraph--centered']")
                if omlouvameParagraph.is_displayed():
                    return

            except NoSuchElementException:
                pass


        self.driver.get(URL_detail)

        time.sleep(1)
        acceptConsent(self.driver)



        generalized_Detail_terminyAceny_potvrdit_chooseFiltr(self.driver, terminyAcenyTabXpath, potvrditPopupXpath,
                                                             dopravaBoxXpath, dopravaBrnoXpath)
        wait = WebDriverWait(self.driver, 150)

        time.sleep(500)

        try:
            pocetZobrazenychTerminu = self.driver.find_elements_by_xpath(
                "//*[@class='fshr-termins-table-item-header js-toggleSlide']")  ##locator jen na pocet odletu alokuje vic veci nez je actual terminu tak
            ##pro
            ##for
            ##loop
            ##pouziju
            ##tohle
            ##=
            ##20
        except NoSuchElementException:
            url = self.driver.current_url
            msg = "pocetZobrazenychTerminu, filtrovani dle letu detail hotelu, mozna jen nema odlety na X, NoSuchElementException " + url
            sendEmail(msg)

        try:
            odletyTerminy = self.driver.find_elements_by_xpath(
                "//*[@class='fshr-termin-departure-from']")  ##prvni locator je "odlet" takze zacnu na pozici jedna, vyloopuje se to podle
            ##poctu terminu, should be ok
        except NoSuchElementException:
            url = self.driver.current_url
            msg = "odletyTerminy, nejsou odlety na brno, most likely not a bad thing, NoSuchElementException " + url
            sendEmail(msg)
        y = 1
        for _ in pocetZobrazenychTerminu:
            assert odletyTerminy[y].text == "Brno"
            if odletyTerminy[y].text == "Brno":  ##tady je nutny pricitat +2 protoze je tam 41 results (s tim ze jeden
                ##je "odlet"), kazdy sudy cislo je mezera/blank space for some reason
                ##print(odletyTerminy[y].text)
                y = y + 2
            else:
                url = self.driver.current_url
                ##print(odletyTerminy[y].text)
                msg = "na detailu jsem vyfiltroval odlet na brno ale pry to nesedi říká python " + url
                sendEmail(msg)
                y = y + 2

        self.test_passed = True

