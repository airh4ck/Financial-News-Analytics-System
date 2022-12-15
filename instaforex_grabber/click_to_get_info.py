import sys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

if __name__ == '__main__':
    url = sys.argv[1]
    clicks = int(sys.argv[2])

    opts = webdriver.ChromeOptions()
    opts.headless = True
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    # opts.add_argument('--no-sandbox')
    driver = webdriver.Remote(
        "http://selenium:4444/wd/hub", options=opts)

    driver.get(url)
    # print(driver.page_source, file=sys.stderr)

    errors_count = 0
    while (clicks > 0) and (errors_count < 10):
        try:
            button = WebDriverWait(driver, 2000).until(
                EC.element_to_be_clickable((By.ID, 'show-more-analysis')))
            sleep(1)
            button.location_once_scrolled_into_view
            button.click()
            clicks -= 1
        except:
            errors_count += 1
    sleep(1)

    article_refs = driver.find_elements(By.CLASS_NAME, 'news_card_title_list')

    # print(article_refs, file=sys.stderr)

    for reference in article_refs:
        print(reference.get_attribute('href'))

    driver.quit()
    print()
