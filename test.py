# python -m pytest -v --driver Chrome --driver-path chromedriver.exe test_SF_RT_passport.py


from time import sleep
from base_data import *
from settings import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


### тест TC-02 - общий вид формы (сохранить скриншот)
def test_02_vision(selenium):
    form = AuthForm(selenium)
    form.driver.save_screenshot('screen_001.jpg')


### тест TC-05 - проверка, что по-умолчанию выбрана форма авторизации по телефону
def test_05_by_phone(selenium):
    form = AuthForm(selenium)

    assert form.placeholder.text == 'Мобильный телефон'


### тест TC-06 - проверка автосмены "таб ввода"
def test_06_change_placeholder(selenium):
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys('+79213747547')
    form.password.send_keys('_')
    sleep(5)

    assert form.placeholder.text == 'Мобильный телефон'

    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод почты
    form.username.send_keys('test@yandex.ru')
    form.password.send_keys('_')
    sleep(5)

    assert form.placeholder.text == 'Электронная почта'

    # очистка поля логина
    form.username.send_keys(Keys.CONTROL, 'a')
    form.username.send_keys(Keys.DELETE)

    # ввод логина
    form.username.send_keys('MyLogin')
    form.password.send_keys('_')
    sleep(5)

    assert form.placeholder.text == 'Логин'


### тест TC-07 - проверка позитивного сценария авторизации по телефону
def test_07_positive_by_phone(selenium):
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys(valid_phone)
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()

    assert form.get_current_url() != '/account_b2c/page'


### тест TC-08 - проверка негативного сценария авторизации по телефону
def test_07_negative_by_phone(selenium):
    form = AuthForm(selenium)

    # ввод телефона
    form.username.send_keys('+72502354356')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


### тест TC-09 - проверка позитивного сценария авторизации по почте
def test_09_positive_by_email(selenium):
    form = AuthForm(selenium)

    # ввод почты
    form.username.send_keys(valid_email)
    form.password.send_keys(valid_pass)
    sleep(5)
    form.btn_click()

    assert form.get_current_url() != '/account_b2c/page'


### тест TC-10 - проверка негативного сценария авторизации по почте
def test_10_negative_by_email(selenium):
    form = AuthForm(selenium)

    # ввод почты
    form.username.send_keys('qwerty@to.ru')
    form.password.send_keys('any_password')
    sleep(5)
    form.btn_click()

    err_mess = form.driver.find_element(By.ID, 'form-error-message')
    assert err_mess.text == 'Неверный логин или пароль'


### тест TC-16 - проверка получения временного кода на телефон и открытия формы для ввода кода
def test_16_get_code(selenium):
    form = CodeForm(selenium)

    # ввод телефона
    form.address.send_keys(valid_phone)

    # длительная пауза предназначена для ручного ввода капчи при необходимости
    sleep(30)
    form.get_click()

    rt_code = form.driver.find_element(By.ID, 'rt-code-0')

    assert rt_code


### тест TC-20 - проверка перехода в форму восстановления пароля и её открытия
def test_20_forgot_pass(selenium):
    form = AuthForm(selenium)

    # клик по надписи "Забыл пароль"
    form.forgot.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Восстановление пароля'


### тест TC-21 - проверка перехода в форму регистрации и её открытия
def test_21_register(selenium):
    form = AuthForm(selenium)

    # клик по надписи "Зарегистрироваться"
    form.register.click()
    sleep(5)

    reset_pass = form.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/h1')

    assert reset_pass.text == 'Регистрация'


### тест TC-22 - проверка открытия пользовательского соглашения
def test_22_agreement(selenium):
    form = AuthForm(selenium)

    original_window = form.driver.current_window_handle
    # клик по надписи "Пользовательским соглашением" в подвале страницы
    form.agree.click()
    sleep(5)
    WebDriverWait(form.driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in form.driver.window_handles:
        if window_handle != original_window:
            form.driver.switch_to.window(window_handle)
            break
    win_title = form.driver.execute_script("return window.document.title")

    assert win_title == 'User agreement'


### тест TC-23 - проверка перехода по ссылке авторизации пользователя через вконтакте
def test_23_auth_vk(selenium):
    form = AuthForm(selenium)
    form.vk_btn.click()
    sleep(5)

    assert form.get_base_url() == 'oauth.vk.com'


### тест TC-24 - проверка перехода по ссылке авторизации пользователя через одноклассники
def test_24_auth_ok(selenium):
    form = AuthForm(selenium)
    form.ok_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.ok.ru'


### тест TC-25 - проверка перехода по ссылке авторизации пользователя через майлру
def test_25_auth_mailru(selenium):
    form = AuthForm(selenium)
    form.mailru_btn.click()
    sleep(5)

    assert form.get_base_url() == 'connect.mail.ru'


### тест TC-26 - проверка перехода по ссылке авторизации пользователя через google
def test_26_auth_google(selenium):
    form = AuthForm(selenium)
    form.google_btn.click()
    sleep(5)

    assert form.get_base_url() == 'accounts.google.com'


### тест TC-27 - проверка перехода по ссылке авторизации пользователя через яндекс
def test_27_auth_ya(selenium):
    form = AuthForm(selenium)
    form.ya_btn.click()
    sleep(5)

    assert form.get_base_url() == 'passport.yandex.ru'