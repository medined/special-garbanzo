from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import selenium
import time


class SeekingAlpha:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get('https://www.seekingalpha.com/')
        self.driver.maximize_window()
        self.waiter = WebDriverWait(self.driver, 20)

    def get_ratings(self, config, df):
        self.login(config.seekingalpha_username, config.seekingalpha_password)
        df['SARatings'] = df.apply(self.seeking_alpha_rating, axis=1)

    def seeking_alpha_rating(self, record):
        return self.get_rating_for_symbol(record.symbol)

    def login(self, email, password):
        signin_button = EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-test-id='header-button-sign-in']"))
        email_field = EC.visibility_of_element_located((By.NAME, "email"))
        password_field = EC.visibility_of_element_located((By.ID, "signInPasswordField"))
        form_field = EC.visibility_of_element_located((By.XPATH, "//form[1]"))

        # Click the Sign In link.
        self.waiter.until(signin_button).click()
        self.waiter.until(email_field).send_keys(email)
        self.waiter.until(password_field).send_keys(password)
        self.waiter.until(form_field).submit()

    def get_rating_for_symbol(self, symbol):
        input_xpath = "/html/body/div[2]/div[1]/header/div[1]/div/div[1]/div/div/div/input"
        input_xpath = "//input"
        anchor_xpath = "/html/body/div[2]/div[1]/header/div[1]/div/div[1]/div/div[2]/section[1]/div[1]/div[2]/a"
        input_element = EC.visibility_of_element_located((By.XPATH, input_xpath))
        self.waiter.until(input_element).send_keys(symbol)
        time.sleep(2)
        anchor_element = EC.visibility_of_element_located((By.XPATH, anchor_xpath))
        self.waiter.until(anchor_element).click()
        try:
            authors_rating = self.waiter.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/main/div[2]/div/div[4]/div/div[2]/div/div[1]/section/div/div[2]/div/table/tbody/tr[1]/td[2]/a/span/span"))).text
            street_rating = self.waiter.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/main/div[2]/div/div[4]/div/div[2]/div/div[1]/section/div/div[2]/div/table/tbody/tr[2]/td[2]/a/span/span"))).text
            quant_rating = self.waiter.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/main/div[2]/div/div[4]/div/div[2]/div/div[1]/section/div/div[2]/div/table/tbody/tr[3]/td[2]/a/span/span"))).text
        except selenium.common.exceptions.TimeoutException:
            authors_rating = "0"
            street_rating = "0"
            quant_rating = "0"

        if '-' in authors_rating:
            authors_rating = "0"
        if '-' in street_rating:
            street_rating = "0"
        if '-' in quant_rating:
            quant_rating = "0"

        rating = (float(authors_rating) + float(street_rating) + (float(quant_rating)*3)) / 5

        print(f'{symbol}: {authors_rating}, {street_rating}, {quant_rating}, {rating:.2f}')

        return f'{authors_rating}, {street_rating}, {quant_rating}, {rating:.2f}'

    def logout(self):
        self.driver.close()
