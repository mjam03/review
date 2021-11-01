import numpy as np
import re
import time
from typing import Tuple

from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import BaseWebElement


def click_element(driver: Chrome, element: BaseWebElement) -> None:
    # move to the element
    ActionChains(driver).move_to_element(element).perform()
    # add random delay to mask immediate click
    random_delay(1, 0.5)
    # click element
    driver.execute_script("arguments[0].click();", element)
    # return nothing
    return


def literal_search(driver: Chrome) -> None:
    # force search to be literal (to avoid ambiguous names) if Google corrects
    try:
        # find link referring to original search term
        check_correction_link: list = driver.find_elements(
            By.CSS_SELECTOR,
            'input[jsaction="pane.correctionSection.originalQueryClick"]',
        )
        # click on it
        check_correction_link[0].click()
    except:
        pass
    return


def get_geo(driver: Chrome) -> Tuple[float, float]:
    # get gmaps url which contains lat and long
    url: str = driver.current_url
    # use regex to strip them, make floats and return
    geocode = re.search(r"(?<=/@)(.*?),(.*?)(?=,)", url)[0]
    latitude = float(geocode.split(",")[0])
    longitude = float(geocode.split(",")[1])
    return (latitude, longitude)


def scroll_down_section(driver: Chrome, css_identifier: str) -> None:
    try:
        results_box: BaseWebElement = driver.find_element(
            By.CSS_SELECTOR, css_identifier
        )
        driver.execute_script(
            "arguments[0].scrollTo(0, arguments[0].scrollHeight)", results_box
        )
        random_delay(2)
    except NoSuchElementException:
        print("Cannot find results box to scroll down")
    return


def back_to_results(driver: Chrome) -> None:
    # finds back button in top left of search bar and clicks it
    back_button: BaseWebElement = driver.find_elements(
        By.XPATH, "//button[contains(@aria-label, 'Back')]"
    )[-1]
    ActionChains(driver).move_to_element(back_button).perform()
    # add random delay to mask immediate click
    random_delay(1, 0.5)
    driver.execute_script("arguments[0].click();", back_button)
    random_delay(1, 0.5)
    return


def random_delay(
    constant: float, var: float = 1, min_delay: float = 0.5, max_delay: float = 10
) -> None:
    # create a random delay to mask automated behaviour
    delay: float = constant + np.random.uniform(-1, 1) * var
    delay = np.max([min_delay, delay])
    delay = np.min([max_delay, delay])
    time.sleep(delay)
    return
