from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By     

driver = Chrome()

driver.get('https://www.google.com/search?q=dollar')

element = driver.find_element(By.CLASS_NAME, "span.DFlfde")
