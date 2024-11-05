from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

base_url = "https://only.digital/"

# Список страниц
pages = [
    base_url,
    base_url + "projects",
    base_url + "company",
    base_url + "job"
]

service = Service('/chromedriver')
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Проверка футера на каждой странице
for page in pages:
    try:
        driver.get(page)

        # Прокручиваем страницу до футера
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            # Ожидаем появления футера с указанием класса
            footer = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.TAG_NAME, "footer"))
            )
            assert footer.is_displayed(), f"Footer is not have: {page}"

            # Поиск номера телефона
            phone = footer.find_element(By.XPATH, ".//a[contains(@href, 'tel:')]").get_attribute("href")
            email = footer.find_element(By.XPATH, ".//a[contains(@href, 'mailto:')]").get_attribute("href")

            # Ссылки социальных сетей
            social_links = footer.find_elements(By.XPATH,
                                                ".//a[contains(@href, 'awwwards') or contains(@href, 'vk') or contains(@href, 'telegram') or contains(@href, 'vimeo') or contains(@href, 'behance')]")
            assert len(social_links) > 0, f"No social links found on page: {page}"

            print(f"Footer have in: {page}")
            print(f"Phone {phone} have in: {page}")
            print(f"Email {email} have in: {page}")
            print("Social links:", [link.get_attribute('href') for link in social_links])

        except TimeoutException:
            print(f"Error in: {page}")
            continue

    except Exception as e:
        print(f"Test failed on page {page} with error: {e}")

driver.quit()
