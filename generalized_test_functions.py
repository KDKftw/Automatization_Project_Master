from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from to_import_master import sendEmail


def generalized_map_test_click_through_circles(driver, zobrazitNaMapeXpath):
    def click_on_map_circle(driver, circlexpath):
        try:
            driver.find_element_by_xpath(circlexpath).click()
        except:
            print("nenasel se kolecko" +circlexpath)
            pass
        time.sleep(1.2)

    zobrazitNaMape = driver.find_element_by_xpath(zobrazitNaMapeXpath)
    zobrazitNaMape.click()
    largeCircleXpath = "//*[@class='leaflet-marker-icon marker-cluster marker-cluster-large leaflet-zoom-animated leaflet-interactive']"
    mediumCircleXpath = "//*[@class='leaflet-marker-icon marker-cluster marker-cluster-medium leaflet-zoom-animated leaflet-interactive']"
    smallCircleXpath = "//*[@class='leaflet-marker-icon marker-cluster marker-cluster-small leaflet-zoom-animated leaflet-interactive']"
    time.sleep(10)##loading time
    click_on_map_circle(driver, largeCircleXpath)
    time.sleep(2)
    click_on_map_circle(driver, largeCircleXpath)
    time.sleep(2)
    click_on_map_circle(driver, largeCircleXpath)

    click_on_map_circle(driver, mediumCircleXpath)
    time.sleep(2)
    click_on_map_circle(driver, mediumCircleXpath)

    click_on_map_circle(driver, smallCircleXpath)
    time.sleep(2)
    click_on_map_circle(driver, smallCircleXpath)

def generalized_map_test_click_on_pin_and_hotel_bubble(driver):
    actualHotelPin = driver.find_element_by_xpath(
        "//*[@class='leaflet-marker-icon leaflet-zoom-animated leaflet-interactive']")
    driver.execute_script("arguments[0].click();", actualHotelPin)  ##at this point im at detail hotelu na mapě

    try:
        imgMissing = driver.find_element_by_xpath(
            "//*[@class='f_image f_image--missing']")  ##when theres no photo on the detail on map theres actually class that says it is missing
        if imgMissing.is_displayed():  ##so if I dont find this class = good
            hotelBubble = driver.find_element_by_xpath("//*[@class='leaflet-popup-content'] //*[@class='f_bubble']")
            msg = "V mape v bublibně hotelu se nezobrazuje fotka hotelu " + hotelBubble.text
            sendEmail(msg)

    except NoSuchElementException:
        print("actually OK")

    time.sleep(2)

    hotelBubble = driver.find_element_by_xpath("//*[@class='leaflet-popup-content'] //*[@class='f_bubble']")
    hotelBubble.click()

def generalized_SRL_choose_meal_filter_EW_like(driver, stravaMenuXpath):
    stravaMenu = driver.find_element_by_xpath(stravaMenuXpath)
    stravaMenu.click()
    time.sleep(2)

def generalized_SRL_choose_meal_filter_FW_like(driver, stravaMenuXpath, stravaMenuAllInclusiveXpath, potvrditMenuXpath):
    #stravaMenu = driver.find_element_by_xpath("//*[@class='f_menu-item']//*[contains(text(), 'Strava')]")
    stravaMenuBox = driver.find_element_by_xpath(stravaMenuXpath)

    stravaMenuBox.click()
    generalized_SRL_choose_meal_filter_EW_like(driver, stravaMenuAllInclusiveXpath)

    potvrditMenu = driver.find_element_by_xpath(potvrditMenuXpath)
    potvrditMenu.click()

##variable_to_assert_to == .lower should be on default
def generalized_list_string_sorter(driver, web_elements_Xpath, variable_to_assert_to, plusPozice=None, list_web_element_starter=None):
    time.sleep(2)
    if plusPozice==None:
        plusPozice=1

    if plusPozice==2:
        plusPozice = 2

    else:
        plusPozice=1

    if list_web_element_starter==None:
        list_web_elements_Position = 0

    if list_web_element_starter==1:
        list_web_elements_Position = 1

    else:
        list_web_elements_Position = 0


    print(list_web_elements_Position)
    web_elements = driver.find_elements_by_xpath(web_elements_Xpath)


    list_web_elements = []

    for _ in web_elements:
        list_web_elements_String = web_elements[list_web_elements_Position].text.lower()
        list_web_elements.append(list_web_elements_String)

        list_web_elements_Position = list_web_elements_Position + plusPozice

    list_web_elements_Position = 0

    for _ in list_web_elements:
        assert variable_to_assert_to in list_web_elements[list_web_elements_Position]
        if variable_to_assert_to in list_web_elements[list_web_elements_Position]:
            print("ok")
            list_web_elements_Position = list_web_elements_Position + plusPozice

        else:
            print("výsledky nesedi k filtru")
            list_web_elements_Position = list_web_elements_Position + plusPozice

    print(list_web_elements)



#predisposition:
#loaded SRL -> clicks on sorter (expensive VS cheap)
#gets all prices
##typeOfSort = cheap or expensive

def generalized_SRL_price_sorter(driver, sorter_Xpath, hotelyKartyXpath, cenaZajezduXpath,  typeOfSort):
        wait = WebDriverWait(driver, 25)

        cenaZajezduAllList = []                     ##one list that takes prices from the srl
        cenaZajezduAllListSorted = []               ##second list takes the values too, then sorts it low to high
        time.sleep(3)
        sorter_Element = driver.find_element_by_xpath(sorter_Xpath)
        wait.until(EC.visibility_of(sorter_Element))
        sorter_Element.click()
        time.sleep(6)
        hotelyKarty = driver.find_element_by_xpath(hotelyKartyXpath)
        wait.until(EC.visibility_of(hotelyKarty))
        #time.sleep(4)
        list_web_elements_Position = 0
        cenaZajezduAll = driver.find_elements_by_xpath(cenaZajezduXpath)
        wait.until(EC.visibility_of(cenaZajezduAll[0]))

        for WebElement in cenaZajezduAll:
            cenaZajezduAllString = cenaZajezduAll[list_web_elements_Position].text
            #cenaZajezduAllString = cenaZajezduAllString[:-3]
            cenaZajezduAllString = cenaZajezduAllString[:-2]        ##was adjsuted for webs where is euro prices, works on everything else as well
            cenaZajezduAllString = ''.join(cenaZajezduAllString.split())        ##delete spaces
            cenaZajezduAllString = int(cenaZajezduAllString)        ##convert to int to do sort easily
            list_web_elements_Position = list_web_elements_Position + 1
            cenaZajezduAllList.append(cenaZajezduAllString)
            cenaZajezduAllListSorted.append(cenaZajezduAllString)


        if typeOfSort == "cheap":
            cenaZajezduAllListSorted.sort()  ##sorting second list low to high

            if cenaZajezduAllListSorted == cenaZajezduAllList:  ##compare first list to second list, if is equal = good
                print("Cheap sorter is OK")

            else:
                print("Cheap sorter is NOT OK")

        if typeOfSort == "expensive":
            cenaZajezduAllListSorted.sort(reverse=True)

            if cenaZajezduAllListSorted == cenaZajezduAllList:
                print("Expensive sorter is OK")

            else:
                print("Expensive sorter is NOT OK")

        print("LIST FROM WEB:")
        print(cenaZajezduAllList)
        print("CORRECTLY SORTED LIST")
        print(cenaZajezduAllListSorted)

        assert cenaZajezduAllListSorted == cenaZajezduAllList


def generalized_Detail_terminyAceny_potvrdit_chooseFiltr(driver, terminyAcenyTabXpath, potvrditPopupXpath, boxFiltrXpath, valueToFilterXpath):


    terminyAcenyTabElement = driver.find_element_by_xpath(terminyAcenyTabXpath)
    driver.execute_script("arguments[0].click();", terminyAcenyTabElement)


    time.sleep(1.5)

    potvrditPopupElement = driver.find_element_by_xpath(potvrditPopupXpath)
    driver.execute_script("arguments[0].click();", potvrditPopupElement)

    time.sleep(1)

    boxElement = driver.find_element_by_xpath(boxFiltrXpath)
    driver.execute_script("arguments[0].click();", boxElement)
    time.sleep(1.5)

    valueToFilterElement = driver.find_element_by_xpath(valueToFilterXpath)
    driver.execute_script("arguments[0].scrollIntoView();", valueToFilterElement)

    time.sleep(0.5)

    valueToFilterElement.click()
    time.sleep(0.5)

    driver.execute_script("arguments[0].click();", boxElement)

    time.sleep(1)

def generalized_detail_departure_check(driver, pocetZobrazenychTerminuXpath, odletyTerminyXpath, departureToCompareTo ):

            try:
                pocetZobrazenychTerminu = driver.find_elements_by_xpath(pocetZobrazenychTerminuXpath)  ##locator jen na pocet odletu alokuje vic veci nez je actual terminu tak
            except NoSuchElementException:
                url = driver.current_url
                msg = "pocetZobrazenychTerminu, filtrovani dle letu detail hotelu, mozna jen nema odlety na X, NoSuchElementException " + url
                sendEmail(msg)

            try:
                odletyTerminy = driver.find_elements_by_xpath(odletyTerminyXpath)  ##prvni locator je "odlet" takze zacnu na pozici jedna, vyloopuje se to podle
                ##poctu terminu, should be ok
            except NoSuchElementException:
                url = driver.current_url
                msg = "odletyTerminy, nejsou odlety na brno, most likely not a bad thing, NoSuchElementException " + url
                sendEmail(msg)
            y = 1
            for _ in pocetZobrazenychTerminu:
                assert odletyTerminy[y].text.lower() == departureToCompareTo
                if odletyTerminy[y].text.lower() == departureToCompareTo:  ##tady je nutny pricitat +2 protoze je tam 41 results (s tim ze jeden
                    ##je "odlet"), kazdy sudy cislo je mezera/blank space for some reason
                    print(odletyTerminy[y].text.lower())
                    y = y + 2
                else:
                    url = driver.current_url
                    print(odletyTerminy[y].text.lower())
                    msg = "na detailu jsem vyfiltroval odlet na brno ale pry to nesedi říká python " + url
                    sendEmail(msg)
                    y = y + 2

def generalized_EW_like_top_nabidka_URL_status_check(driver, topNabidkaLinkXpath):

    links_to_check = []
    links_list_counter = 0
    for _ in topNabidkaLinkXpath:
        #topNabidkaElementHref = driver.find_elements_by_xpath(topNabidkaLinkXpath[links_list_counter]).get_attribute("href")
        topNabidkaElementHref = driver.find_elements_by_xpath(topNabidkaLinkXpath[links_list_counter]).text
        links_to_check.append(topNabidkaElementHref)
        links_list_counter = links_list_counter+1
        print(topNabidkaElementHref)
        print(links_to_check)