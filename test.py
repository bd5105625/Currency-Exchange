from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge('./msedgedriver.exe')
driver.get("https://www.google.com/")

element = driver.find_element(By.CLASS_NAME, "gLFyf")
element.send_keys("My name is Brad")
while True:
    pass
# driver.close()