import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()


def test_show_all_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')

    # Настраиваем неявные ожидания:
    pytest.driver.implicitly_wait(10)

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # # Ищем на странице все фотографии, имена, породу (вид) и возраст питомцев:
    # images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    # names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    # descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
    #
    # # Проверяем, что на странице есть фотографии питомцев, имена, порода (вид) и возраст питомцев не пустые строки:
    # for i in range(len(names)):
    #     assert images[i].get_attribute('src') != ''
    #     assert names[i].text != ''
    #     assert descriptions[i].text != ''
    #     assert ', ' in descriptions[i]
    #     parts = descriptions[i].text.split(", ")
    #     assert len(parts[0]) > 0
    #     assert len(parts[1]) > 0

# Проверяем, что на странице присутствуют все мои питомцы
def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    #Настраиваем переменную явного ожидания:
    wait = WebDriverWait(pytest.driver, 5)

    # Проверяем, что мы оказались на главной странице сайта.
    # Ожидаем в течение 5с, что на странице есть тег h1 с текстом "PetFriends"
    assert wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), "PetFriends"))

    # Открываем страницу /my_pets.
    pytest.driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Ищем в теле таблицы все строки с полными данными питомцев (имя, порода, возраст, "х" удаления питомца):
    css_locator = 'tbody>tr'
    data_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, css_locator)
    # Ожидаем, что данные всех питомцев, найденных локатором css_locator = 'tbody>tr', видны на странице:
    for i in range(len(data_my_pets)):
        assert wait.until(EC.visibility_of(data_my_pets[i]))

    # Ищем в теле таблицы все фотографии питомцев и ожидаем, что все загруженные фото, видны на странице:
    image_my_pets = pytest.driver.find_elements(By.CSS_SELECTOR, 'img[style="max-width: 100px; max-height: 100px;"]')
    for i in range(len(image_my_pets)):
        if image_my_pets[i].get_attribute('src') != '':
            assert wait.until(EC.visibility_of(image_my_pets[i]))

    # Ищем в теле таблицы все имена питомцев и ожидаем увидеть их на странице:
    name_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[1]')
    for i in range(len(name_my_pets)):
        assert wait.until(EC.visibility_of(name_my_pets[i]))

    # Ищем в теле таблицы все породы питомцев и ожидаем увидеть их на странице:
    type_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[2]')
    for i in range(len(type_my_pets)):
        assert wait.until(EC.visibility_of(type_my_pets[i]))

    # Ищем в теле таблицы все данные возраста питомцев и ожидаем увидеть их на странице:
    age_my_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr/td[3]')
    for i in range(len(age_my_pets)):
        assert wait.until(EC.visibility_of(age_my_pets[i]))

    # Ищем на странице /my_pets всю статистику пользователя,
    # и вычленяем из полученных данных количество питомцев пользователя:
    all_statistics = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n")
    statistics_pets = all_statistics[1].split(" ")
    all_my_pets = int(statistics_pets[-1])

   # Проверяем, что количество строк в таблице с моими питомцами равно общему количеству питомцев,
   # указанному в статистике пользователя:
    assert len(data_my_pets) == all_my_pets


# Проверка, что хотя бы половина питомцев имеют фото
def test_presence_of_photo():
    # авторизация
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # открываем вкладку мои животные
    my_pets = pytest.driver.find_element(By.XPATH, '//*[@href=\"/my_pets\"]')
    my_pets.click()

    # получаем список с количеством строк (блоков), где содержится информация о конкретном животном
    list_of_pets = pytest.driver.find_elements(By.XPATH, '//tbody/tr')

    # обращаемся к тегам, которые должны содержать фото животных
    images = pytest.driver.find_elements(By.XPATH, '//th/img[@src]')

    # получаем количество питомцев, у которых нет фото
    count = 0
    for i in range(len(images)):
        # если значение атрибута 'src' пустое, то прибавляем единицу к счетчику
        if images[i].get_attribute('src') != '':
            count += 1

    # ожидаем, что хотя бы половина питомцев имеют фото
    # если количество животных - нечетно, то округляем в большую сторону
    # так как, если округлять в меньшую сторону,
    # то половина от округленного числа будет меньше половины от неокругленного
    assert math.ceil(((len(list_of_pets))/2)) == count or math.ceil(((len(list_of_pets))/2)) < count, "Error"
    # return str(len(list_of_pets)), str(count)


# Проверяем, что все питомцы имеют имя, возраст и породу
def test_all_pets_have_data():
    # авторизация
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # открываем вкладку мои животные
    my_pets = pytest.driver.find_element(By.XPATH, '//*[@href=\"/my_pets\"]')
    my_pets.click()

    # получаем 3 списка с именем, типом и возрастом каждого животного
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    types = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')

    for i in range(len(names)): # длины списков names, types и ages должны быть одинаковыми

        # проверяем, что длина каждого имени больше 0; т.е. имя имеет какое-то значение
        assert len(names[i]) > 0, f"Найдено животное без имени с индексом: {i}"

        # проверяем, что длина каждого типа больше 0; т.е. тип имеет какое-то значение
        assert len(types[i]) > 0,  f"Найдено животное без типа с индексом: {i}"

        # проверяем, что длина возраста больше 0; т.е. возраст имеет какое-то значение
        assert len(ages[i]) > 0,  f"Найдено животное без возраста с индексом: {i}"

# Проверяем, что у всех питомцев разные имена
def test_all_pets_have_different_names():
    # авторизация
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # открываем вкладку мои животные
    my_pets = pytest.driver.find_element(By.XPATH, '//*[@href=\"/my_pets\"]')
    my_pets.click()

    # получаем список с именами животных
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')

    # проверяем, что длина списка с уникальными именами соответствует длине списка со всеми именами
    assert len(list(set(names))) == len(names), "Есть животные с повторяющимися именами"

def test_all_pets_are_unique():
    # авторизация
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('vasya@mail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # открываем вкладку мои животные
    my_pets = pytest.driver.find_element(By.XPATH, '//*[@href=\"/my_pets\"]')
    my_pets.click()

    # получаем 3 списка с именем, типом и возрастом каждого животного
    names = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[1]')
    types = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//tr/th/following-sibling::td[3]')

    # создаем пустые списки
    parts = []
    pets_info = []

    for i in range(len(names)):
        # в список parts добавляем последовательно имя, тип и возраст
        parts.append(names[i].text)
        parts.append(types[i].text)
        parts.append(ages[i].text)
        # получившийся список добавляем в основной список в качестве одного элемента и так на каждой итерации
        pets_info.append(parts)

        # проверяем, что ничего не потерялось
    assert len(pets_info) == len(names), "Что-то потерялось"

    # так как к спискам внутри списка нельзя применить set(),
    # поэтому сравним каждый элемент с каждым в основном списке,
    # тем самым проверим уникальность животных
    # установим метку со значением True
    flag = True
    for i in range(len(pets_info)):
        for j in range(len(pets_info)):
            # если индекс элемента не равен самому себе...
            if i != j:
                # ...сравним элементы с разными индексами
                if pets_info[i] == pets_info[j]:
                    # метка получает значение False, если найдены не уникальные элементы
                    flag = False

    assert flag, "Есть повторяющиеся животные"