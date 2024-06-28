from api import Zojnik
from settings import (admin_username, valid_email, admin_password, valid_password, valid_refresh_token,
                      valid_access_token, valid_email_2, valid_password_2, new_valid_password, user_id)
import os

# Создание нового объекта внутри класса Zojnik. Когда мы вызываем Zojnik(), создается новый экземпляр
# класса Zojnik (то есть объект), используя конструктор __init__. Переменная zf затем ссылается
# на этот объект, и мы можем использовать zf для доступа к атрибутам и методам этого объекта.
zf = Zojnik()

# Определяем переменные и задаём им начальные значения
# Далее вызов метода get_api_key и запись результатов в переменные status и result
def test_successful_get_access_and_refresh_token_pair(username=valid_email, password=valid_password):
    """ Takes a set of user credentials and returns an access and refresh JSON web token pair to prove
    the authentication of those credentials."""
    status, result = zf.get_access_and_refresh_token_pair(username, password)
    assert 200 <= status < 300
    assert 'access' in result
    assert 'refresh' in result

    # Запись access_token в .env файл
    zf.update_env_file('valid_access_token', result['access'])
    # Запись refresh_token в .env файл
    zf.update_env_file('valid_refresh_token', result['refresh'])

def test_successful_get_access_token_by_refresh_token(refresh_token=valid_refresh_token):
    """ Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid"""
    status, result = zf.get_access_token_by_refresh_token(refresh_token)
    assert 200 <= status < 300
    assert 'access' in result
    assert 'refresh' in result

def test_successful_verify_token(token=valid_access_token):
    """Takes a token and indicates if it is valid"""
    status = zf.verify_token(token)
    assert 200 <= status < 300

def test_successful_new_user_registration(first_name='', last_name='', username='', phone_number='', email=valid_email_2, password=valid_password_2):
    """Проверка возможности регистрации нового пользователя"""
    status, result = zf.new_user_registration(first_name, last_name, username, phone_number, email, password)
    assert 200 <= status < 300
    assert result ['email'] == email

def test_successful_open_user_profile():
    """Проверка возможности просмотра данных зарегистрированного пользователя"""
    status, result = zf.open_user_profile()
    assert 200 <= status < 300
    assert result ['email'] == valid_email

def test_successful_change_password(old_password=valid_password, new_password=new_valid_password):
    """Проверка возможности смены пароля"""
    status = zf.change_password(old_password, new_password)
    assert 200 <= status < 300

    # Перезапись паролей в .env файле
    zf.update_env_file('valid_password', new_password)
    zf.update_env_file('new_valid_password', old_password)

def test_successful_change_user_profile(first_name='Bob', last_name='White', email=valid_email, phone_number='', username='Bo', profile={}):
    """Проверка возможности частичного изменения данных пользователя"""
    status, result = zf.change_user_profile(first_name, last_name, email, phone_number, username, profile)
    assert 200 <= status < 300
    assert result ['first_name'] == first_name

def test_successful_get_food_categories():
    """Проверка возможности просмотра категорий продуктов для зарегистрированного пользователя"""
    status, result = zf.get_food_categories()
    assert 200 <= status < 300

    #Проверка, что список не пустой
    assert len(result) > 0

def test_successful_get_list_of_tags():
    """Проверка возможности получения списка тегов для зарегистрированного пользователя"""
    status, result = zf.get_list_of_tags()
    assert 200 <= status < 300

    #Проверка, что список не пустой
    assert len(result) > 0

def test_successful_get_list_of_antitags():
    """Проверка возможности получения списка антитегов для зарегистрированного пользователя"""
    status, result = zf.get_list_of_antitags()
    assert 200 <= status < 300

    #Проверка, что список не пустой
    assert len(result) > 0

def test_successful_get_list_of_plates():
    """Проверка возможности просмотра списка тарелок для зарегистрированного пользователя"""
    status, result = zf.get_list_of_plates()
    assert 200 <= status < 300
    # Проверка, что список не пустой
    assert len(result) > 0

def test_successful_create_plate(protein=18, garnish=3, vegetable=7):
    """Проверка возможности создания тарелки по id компонентов для зарегистрированного пользователя"""
    status, result = zf.create_plate(protein, garnish, vegetable)
    assert 200 <= status < 300

def test_successful_get_plate_details(plate_id = 5):
    """Проверка возможности просмотра полной информации о созданной тарелке по её id для зарегистрированного пользователя"""
    status, result = zf.get_plate_details(plate_id)
    assert 200 <= status < 300
    # Проверка, что id соответствует введённому
    assert result ['id'] == plate_id

def test_successful_get_menu_with_filters(tags='Мясо%Гарнир', antitags='Куркума%Паприка', category='Белковое блюдо'):
    """Проверка возможности фильтрации блюд по тегам, антитегам и категории для зарегистрированного пользователя"""
    status, result = zf.get_menu_with_filters(tags, antitags, category)
    assert 200 <= status < 300
    assert 'Куркума' and 'Паприка' not in result

def test_successful_create_dish(name='Шашлык из говядины', calories=465.5, protein=22.1, fat=40.8, carbohydrates=2.7, allergen=True, other=None, price=800, rating=0, avatar=None, category='PROTEIN_PRODUCTS'):
    """Проверка возможности создания тарелки по id компонентов для зарегистрированного пользователя"""
    status, result = zf.create_dish(name, calories, protein, fat, carbohydrates, allergen, other, price, rating, avatar, category)
    assert 200 <= status < 300
    assert result['name'] == name

def test_successful_get_dish_details(dish_id = 98):
    """Проверка возможности просмотра полной информации о созданном блюде по его id для зарегистрированного пользователя"""
    status, result = zf.get_dish_details(dish_id)
    assert 200 <= status < 300
    # Проверка, что id соответствует введённому
    assert result ['id'] == dish_id

#FAILED
def test_successful_change_dish(
        dish_id=98,
        name='Шашлык из свинины',
        calories=285,
        protein=14,
        fat=25,
        carbohydrates=1,
        allergen=True,
        other=None,
        price=800,
        rating=0,
        avatar=None,
        category='PROTEIN_PRODUCTS'):
    """Проверка возможности изменения блюда по его id для зарегистрированного пользователя"""
    status, result = zf.change_dish(dish_id, name, calories, protein, fat, carbohydrates, allergen, other, price, rating, avatar, category)
    assert 200 <= status < 300
    assert result['name'] == name

#Рейтинги и комментарии пока не работают
# def test_successful_get_list_of_comments(dish_id=97):
#     """Проверка возможности просмотра комментариев к блюду для зарегистрированного пользователя"""
#     status, result = zf.get_list_of_comments(dish_id)
#     assert 200 <= status < 300
#
# def test_successful_create_comment(dish_id=97, user_id=user_id, comment='Вкуснотииища!'):
#     """Проверка возможности просмотра комментариев к блюду для зарегистрированного пользователя"""
#     status, result = zf.create_comment(dish_id, user_id, comment)
#     assert 200 <= status < 300
#     assert result['comment'] == comment