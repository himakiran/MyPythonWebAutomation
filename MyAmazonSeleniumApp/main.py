
from helium import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants
import guiBoxes
import sys
import requests
import bs4

if __name__ == '__main__':
    start_chrome(constants.AMZN_SIGIN_URL)
    driver = get_driver()
    write(constants.EMAIL_USERNAME)
    click("continue")
    signed_in_checkbox = driver.find_element_by_name("rememberMe")
    click(signed_in_checkbox)
    password_element = driver.find_element_by_id("ap_password")
    click(password_element)
    password = guiBoxes.ask_password(sys.argv)
    write(password, into=password_element)
    login_btn = driver.find_element_by_id("signInSubmit")
    click(login_btn)
    otp_password = guiBoxes.ask_OTP(sys.argv)
    otp_input_element = driver.find_element_by_id("auth-mfa-otpcode")
    write(otp_password, into=otp_input_element)
    otp_sign_in_element = driver.find_element_by_id("auth-signin-button")
    click(otp_sign_in_element)
    new_releases = driver.find_element_by_xpath('// *[ @ id = "nav-xshop"] / a[2]')
    click(new_releases)
    WebDriverWait(driver, 10).until(EC.url_contains(
        "https://www.amazon.in/gp/new-releases"))  # here you are waiting until url will match your output pattern
    new_releases_url = driver.current_url
    request_cookies_browser = driver.get_cookies()
    user_agent = driver.execute_script("return navigator.userAgent;")
    

