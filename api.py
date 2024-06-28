import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv, set_key, find_dotenv
import os

class Zojnik:
    def __init__(self):
        self.base_url = 'https://api.dev.zojnikfood.ru'
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        self.dotenv_path = dotenv_path  # Сохранение пути к .env файлу

    def get_access_and_refresh_token_pair(self, username: str, password: str) -> json:
        '''Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON с уникальной парой
        из access token и refresh token, найденным по указанным username и password'''

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'username': username,
            'password': password
        }

        response = requests.post(self.base_url + '/api/auth/jwt/create/', headers = headers, json=data)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        # print(f"\n\nStatus Code: {status}")
        print(f"\nResponse: {result}")
        return status, result

    def update_env_file(self, key: str, value: str):
        """Обновляет переменную в .env файле"""
        if not self.dotenv_path:
            raise FileNotFoundError("Не удалось найти .env файл")
        set_key(self.dotenv_path, key, value)

    def get_authorized_headers(self):
        """Возвращает заголовки с токеном авторизации"""
        access_token = os.getenv('valid_access_token')
        if not access_token:
            raise ValueError("Не удалось найти 'valid_access_token' в .env файле")
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def get_access_token_by_refresh_token(self, refresh_token: str) -> json:
        '''Метод делает запрос к API сервера, передаёт refresh token и возвращает статус запроса и результат в формате JSON,
        содержащий access token, если переданный refresh token является действительным'''

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'refresh': refresh_token
        }

        response = requests.post(self.base_url + '/api/auth/jwt/refresh/', headers = headers, json=data)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        # print(f"\n\nStatus Code: {status}")
        # print(f"\nResponse: {result}")
        return status, result

    def verify_token(self, token: str) -> json:
        '''Метод делает запрос к API сервера, передаёт access token или refresh token и возвращает статус запроса 200
        если токен является действительным'''

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'token': token
        }

        response = requests.post(self.base_url + '/api/auth/jwt/verify/', headers = headers, json=data)

        status = response.status_code
        return status

    def new_user_registration(self, first_name: str, last_name: str, username: str, phone_number: str, email: str, password: str) -> json:
        '''Метод делает запрос к API сервера на регистрацию нового пользователя и возвращает статус запроса и
        результат в формате JSON с данными о добавленном пользователе. Обязательные поля для заполнения email и password'''

        headers = {
            'Content-Type': 'application/json'
        }

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'phone_number': phone_number,
            'email': email,
            'password': password
        }

        response = requests.post(self.base_url + '/api/users/reg/', headers = headers, json=data)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def change_password(self, old_password: str, new_password: str) -> json:
        '''Метод делает запрос к API сервера на смену пароля и возвращает статус запроса'''

        headers = self.get_authorized_headers()

        data = {
            'old_password': old_password,
            'new_password': new_password
        }

        response = requests.post(self.base_url + '/api/users/change-passwd/', headers = headers, json=data)

        status = response.status_code

        return status

    def open_user_profile(self) -> json:
        '''Метод делает запрос к API сервера на получение данных зарегистрированного пользователя и возвращает
        статус запроса и результат в формате JSON с данными пользователя'''

        headers = self.get_authorized_headers()

        response = requests.get(self.base_url + '/api/users/me/', headers = headers)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def change_user_profile(self, first_name: str, last_name: str, email: str, phone_number: str, username: str, profile: dict) -> json:
        '''Метод делает запрос к API сервера на частичное изменение данных зарегистрированного пользователя и
        возвращает статус запроса и результат в формате JSON с обновлёнными данными пользователя'''

        headers = self.get_authorized_headers()

        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'username': username,
            'profile': profile
        }

        response = requests.patch(self.base_url + '/api/users/me/', headers = headers, json=data)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def get_food_categories(self) -> json:
        '''Метод делает запрос к API сервера на получение категорий продуктов для авторизованного пользователя и возвращает
        статус запроса и результат в формате JSON с данными'''

        headers = self.get_authorized_headers()

        response = requests.get(self.base_url + '/api/food/dicts/foodcategory/', headers = headers)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def get_list_of_tags(self) -> json:
        '''Метод делает запрос к API сервера на получение списка тегов для авторизованного пользователя и возвращает
        статус запроса и результат в формате JSON с данными'''

        headers = self.get_authorized_headers()

        response = requests.get(self.base_url + '/api/food/dicts/tag/', headers = headers)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def get_list_of_antitags(self) -> json:
        '''Метод делает запрос к API сервера на получение списка антитегов для авторизованного пользователя и возвращает
        статус запроса и результат в формате JSON с данными'''

        headers = self.get_authorized_headers()

        response = requests.get(self.base_url + '/api/food/dicts/antitag/', headers = headers)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def get_list_of_plates(self) -> json:
        '''Метод делает запрос к API сервера на получение списка созданных тарелок с расчитанными КБЖУ, ценой и рейтингом.
        Возвращает статус запроса и результат в формате JSON'''

        headers = self.get_authorized_headers()

        response = requests.get(self.base_url + '/api/plate/', headers = headers)
        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def create_plate(self, protein: int, garnish: int, vegetable: int) -> json:
        '''Метод делает запрос к API сервера на создание тарелки по id компонентов для зарегистрированного пользователя и
        возвращает статус запроса и результат в формате JSON'''

        headers = self.get_authorized_headers()

        data = {
            'proteinproduct': protein,
            'garnishproduct': garnish,
            'vegetableproduct': vegetable,
        }

        response = requests.post(self.base_url + '/api/plate/', headers = headers, json=data)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def get_plate_details(self, plate_id: int) -> json:
        '''Метод делает запрос к API сервера на получение информации о тарелке по её id. Возвращает статус запроса и
        результат в формате JSON'''

        headers = self.get_authorized_headers()

        response = requests.get(f'{self.base_url}/api/plate/{plate_id}', headers = headers)
        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def get_menu_with_filters(self, tags: str, antitags: str, category: str) -> json:
        '''Метод делает запрос к API сервера на получение списка блюд отфильтрованного по тегам, антитегам и категориям.
        Возвращает статус запроса и результат в формате JSON'''

        headers = self.get_authorized_headers()

        response = requests.get(f'{self.base_url}/api/food?tags={tags}&{antitags}&{category}', headers = headers)
        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def create_dish(self, name: str, calories: float, protein: float, fat: float, carbohydrates: float, allergen: bool,
                    other: str, price: float, rating: int, avatar: str, category: str) -> json:
        '''Метод делает запрос к API сервера на создание нового блюда. Возвращает статус запроса и результат в формате JSON'''

        headers = self.get_authorized_headers()

        data = {
            'name': name,
            'calories': calories,
            'protein': protein,
            'fat': fat,
            'carbohydrates': carbohydrates,
            'allergen': allergen,
            'other': other,
            'price': price,
            'rating': rating,
            'avatar': avatar,
            'category': category
        }

        response = requests.post(self.base_url + '/api/food/', headers = headers, json=data)

        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def get_dish_details(self, dish_id: int) -> json:
        '''Метод делает запрос к API сервера на получение информации о блюде по его id. Возвращает статус запроса и
        результат в формате JSON'''

        headers = self.get_authorized_headers()

        response = requests.get(f'{self.base_url}/api/food/{dish_id}', headers = headers)
        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result

    def change_dish(
            self,
            dish_id: int,
            name: str,
            calories: float,
            protein: float,
            fat: float,
            carbohydrates: float,
            allergen: bool,
            other: str,
            price: float,
            rating: int,
            avatar: str,
            category: str) -> json:
        '''Метод делает запрос к API сервера на изменение информации о блюде по его id. Возвращает статус запроса и
        результат в формате JSON'''

        headers = self.get_authorized_headers()


        data = {
            'name': name,
            'calories': calories,
            'protein': protein,
            'fat': fat,
            'carbohydrates': carbohydrates,
            'allergen': allergen,
            'other': other,
            'price': price,
            'rating': rating,
            'avatar': avatar,
            'category': category
        }

        response = requests.patch(f'{self.base_url}/api/food/{dish_id}', headers = headers, json=data)
        status = response.status_code
        result = ""

        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text

        print(f"\nStatus Code: {status}")
        print(f"\nResponse:")
        if isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
                else:
                    print(item)
        elif isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)

        return status, result


    #Рейтинги и комментарии пока не работают
    # def get_list_of_comments(self, dish_id: int) -> json:
    #     '''Метод делает запрос к API сервера на получение комментариев к блюду. Возвращает статус запроса и результат
    #     в формате JSON'''
    #
    #     headers = self.get_authorized_headers()
    #
    #     response = requests.get(self.base_url + '/api/food/{dish_id}/comments/', headers = headers)
    #     status = response.status_code
    #     result = ""
    #
    #     try:
    #         result = response.json()
    #     except json.decoder.JSONDecodeError:
    #         result = response.text
    #
    #     print(f"\nStatus Code: {status}")
    #     print(f"\nResponse:")
    #     if isinstance(result, list):
    #         for item in result:
    #             if isinstance(item, dict):
    #                 for key, value in item.items():
    #                     print(f"{key}: {value}")
    #                 print()
    #             else:
    #                 print(item)
    #     elif isinstance(result, dict):
    #         for key, value in result.items():
    #             print(f"{key}: {value}")
    #     else:
    #         print(result)
    #
    #     return status, result
    #
    # def create_comment(self, dish_id: int, user_id: int, comment: str, ) -> json:
    #     '''Метод делает запрос к API сервера на создание комментария к блюду. Возвращает статус запроса и результат
    #     в формате JSON'''
    #
    #     headers = self.get_authorized_headers()
    #
    #     data = {
    #         'comment': comment,
    #         'food_id': dish_id,
    #         'user_id': user_id
    #     }
    #
    #     response = requests.post(self.base_url + '/api/food/{dish_id}/comments/', headers = headers, json=data)
    #     status = response.status_code
    #     result = ""
    #
    #     try:
    #         result = response.json()
    #     except json.decoder.JSONDecodeError:
    #         result = response.text
    #
    #     print(f"\nStatus Code: {status}")
    #     print(f"\nResponse:")
    #     if isinstance(result, list):
    #         for item in result:
    #             if isinstance(item, dict):
    #                 for key, value in item.items():
    #                     print(f"{key}: {value}")
    #                 print()
    #             else:
    #                 print(item)
    #     elif isinstance(result, dict):
    #         for key, value in result.items():
    #             print(f"{key}: {value}")
    #     else:
    #         print(result)
    #
    #     return status, result
