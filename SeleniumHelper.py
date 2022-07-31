import sys
import time
import logging
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Set, Dict, List, Tuple

# 3rd party libraries
import psutil

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC

# logger config
selLogger: Any = logging.getLogger('')
selLogger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s', \
                              datefmt='%a, %d %b %Y %H:%M:%S')
sh.setFormatter(formatter)
selLogger.addHandler(sh)

@dataclass
class SeleniumData:
    """Dataclass for web element shortcuts in selenium"""
    vel: Any

# This is needed to ensure that we run in the current terminal
# ensure that Xvfb is running like so: sudo Xvfb &
# os.environ["DISPLAY"] = ":0"

class SeleniumHelper:
    """Service class for Selenium"""
    def __init__(self, driverLocation: str, isHeadLess: bool, isProxy: bool, proxyAddress: str):
        """
        Parameters
        ----------
        driverLocation: str
            filepath of the firefox driver
        isHeadLess: bool
            do you want the browser to show itself while executing the program or no?
        isProxy: bool
            should the browser use proxy or no?
        proxyAddress: str
            proxy ip address along with port eg: 123.456.789.012:12345
        """
        try:
            browserOptions = Options()
            browserOptions.headless = False
            proxy: Any = Proxy({})
            if isProxy:
                proxy = Proxy({
                    'proxyType': ProxyType.MANUAL,
                    'httpProxy': proxyAddress,
                    'ftpProxy': proxyAddress,
                    'sslProxy': proxyAddress,
                    })

            if isHeadLess:
                browserOptions.headless = True    
            # the location to the selenium driver for the browser
            firefoxLocation = driverLocation
            if psutil.WINDOWS:
                firefoxLocation = driverLocation

            self.driver = webdriver.Firefox(
                proxy=proxy,
                options=browserOptions,
                service_log_path="/dev/null",
                executable_path=firefoxLocation,
            )
            self.driver.maximize_window()
            # driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 20)
            # using shortforms
            self.seleniumData = SeleniumData(EC.visibility_of_element_located)

        except Exception as eobj:
            selLogger.error(eobj)
            traceback.print_exc()

    def selectElement(self, tagName: str, eid: str):
        """Selects the tagName identified by id"""
        time.sleep(10)
        select = Select(self.driver.find_element(by=By.NAME, value=tagName))
        select.select_by_value(eid)
        time.sleep(20)

    def waitForElementId(self, eid: str):
        """Waits for the element identified by its id"""
        selLogger.debug("waiting for the element with id: %s", eid)
        self.wait.until(self.seleniumData.vel((By.ID, eid)))

    def waitForElementName(self, name: str):
        """Waits for the element identified by its name"""
        selLogger.debug("waiting for the element with name: %s", name)
        self.wait.until(self.seleniumData.vel((By.NAME, name)))

    def waitForElementXp(self, xPath: str):
        """Waits for the element identified by its xpath"""
        selLogger.debug("waiting for the element with xpath: %s", xPath)
        self.wait.until(self.seleniumData.vel((By.XPATH, xPath)))

    def waitForElementCName(self, className: str):
        """Waits for the element identified by its class name"""
        selLogger.debug("waiting for the element with class name: %s", className)
        self.wait.until(self.seleniumData.vel((By.CLASS_NAME, className)))

    def sendKeysId(self, eid: str, val: str):
        """Sends the val to the element identified by its id"""
        selLogger.debug("inputting text %s in element-id %s", val, eid)
        self.driver.find_element(by=By.ID, value=eid).send_keys(val)

    def sendKeysName(self, name: str, val: str):
        """Sends the val to the element identified by its name"""
        selLogger.debug("inputting text %s in element-name %s", val, name)
        self.driver.find_element(by=By.NAME, value=name).send_keys(val)

    def sendKeysXp(self, xPath: str, val: str):
        """Sends the val to the element identified by its xp"""
        selLogger.debug("inputting text %s in element-xpath %s", val, xPath)
        self.driver.find_element(by=By.XPATH, value=xPath).send_keys(val)

    def clickById(self, eid: str):
        """Click the element identified by its id"""
        selLogger.debug("clicking element-id %s", eid)
        self.driver.find_element(by=By.ID, value=eid).click()

    def clickByXp(self, xPath: str):
        """Click the element identified by its xpath"""
        selLogger.debug("clicking element-xpath %s", xPath)
        self.driver.find_element(by=By.XPATH, value=xPath).click()

    def clickByName(self, name: str):
        """Click the element identified by its name"""
        selLogger.debug("clicking element-name %s", name)
        self.driver.find_element(by=By.NAME, value=name).click()

    def clickByCss(self, css: str):
        """Click the element identified by its css"""
        selLogger.debug("clicking element-css %s", css)
        self.driver.find_element(by=By.CSS_SELECTOR, value=css).click()
