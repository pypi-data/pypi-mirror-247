import os
import re
import time
from selenium import webdriver
import undetected_chromedriver as uc

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium_stealth import stealth

from selenium.webdriver.support.wait import WebDriverWait
import random


class FacebookAccountCreator:
    def __init__(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",


            # Añade más user-agents aquí
        ]
        random_user_agent = random.choice(user_agents)
        print(random_user_agent)
        current_directory = os.path.dirname(os.path.realpath(__file__))
        chromedriver_path = os.path.join(current_directory, 'chromedriver')

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notification": 2}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('detach', True)






        chrome_options.add_argument("--headless")
        # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f"user-agent={random_user_agent}")

        # chrome_options.add_argument(f"user-agent={user_agent}")

        chrome_service = webdriver.chrome.service.Service(chromedriver_path)

        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


        self.driver.maximize_window()

    def create_account(self, email, password, firstname, lastname, birth_year=None, gender=None):
        print(f"Intentando con el email: {email}")
        birth_year = birth_year if birth_year else random.randint(1965, 2000)
        gender = gender if gender else "Hombre"
        self.driver.get("https://web.facebook.com")
        self.driver.find_element(By.XPATH, "//*[text()='Crear cuenta nueva']").click()
        time.sleep(3)

        self.driver.find_element(By.NAME, "firstname").send_keys(firstname)
        time.sleep(2)
        self.driver.find_element(By.NAME, "lastname").send_keys(lastname)
        time.sleep(2)
        self.driver.find_element(By.NAME, "reg_email__").send_keys(email)
        time.sleep(2)
        self.driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(email)
        time.sleep(2)
        self.driver.find_element(By.ID, "password_step_input").send_keys(password)
        time.sleep(3)
        day = Select(self.driver.find_element(By.XPATH, "//select[@title='Día']"))
        day.select_by_visible_text("18")

        month = Select(self.driver.find_element(By.NAME, "birthday_month"))
        month_options = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        month.select_by_visible_text(random.choice(month_options))

        year = Select(self.driver.find_element(By.NAME, "birthday_year"))
        year.select_by_visible_text(str(birth_year))

        self.driver.find_element(By.XPATH, f"//label[text()='{gender}']").click()
        self.driver.find_element(By.XPATH, "//button[text()='Registrarte']").click()
        time.sleep(35)
        print("Validando valido email")
        try:
            print("val 1")
            validation = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div/div[2]/h2')
        except Exception:
            try:
                print("val 2")
                validation = self.driver.find_element(By.XPATH, "//h2[text()='Ingresa el código de seguridad']")
            except Exception:
                try:
                    error_message = self.driver.find_element(By.XPATH, "//span[text()='Necesitamos más información']")
                    if error_message.text == 'Necesitamos más información':
                        print("No pasó el correo")
                        self.driver.quit()
                        return False
                except Exception:
                    print("No pasó el correo")
                    time.sleep(2)
                    self.driver.quit()
                    return False


        if validation.text == "Ingresa el código que aparece en el correo electrónico" or validation.text == "Ingresa el código de seguridad":
            print("Buscando código email")
            self.driver.execute_script("window.open();")
            self.driver.switch_to.window(self.driver.window_handles[1])

            self.driver.get("https://yopmail.com/es/")
            self.driver.find_element(By.NAME, "login").send_keys(email)
            self.driver.find_element(By.XPATH, "//button[@class='md']").click()

            patron = r'FB-(\d+)'


            while True:
                print(".")
                time.sleep(10)

                self.driver.switch_to.frame('ifinbox')
                time.sleep(5)

                try:
                    element_span_code = self.driver.find_element(By.XPATH,
                                                                 '//div[@currentmail]/button/div[@class="lms"]')
                    code = element_span_code.text
                    code = re.search(patron, code)

                    if code:
                        code = code.group(1)
                        break
                except Exception:
                    pass

                self.driver.switch_to.default_content()
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//*[@id="refresh"]').click()

            print(f'Código: {code}')

            print("Ingresando código en Facebook")
            self.driver.switch_to.window(self.driver.window_handles[0])
            try:
                self.driver.find_element(By.XPATH, '//*[@id="code_in_cliff"]').send_keys(code)
            except:
               pass
            self.driver.find_element(By.XPATH, "//button[text()='Continuar']").click()
            time.sleep(10)
            self.driver.quit()
            print("Se creó la cuenta con éxito")
            #AQUI CREA LA INSERCION
            return True

        else:
            print("No pasó el correo")
            self.driver.quit()
            return False





