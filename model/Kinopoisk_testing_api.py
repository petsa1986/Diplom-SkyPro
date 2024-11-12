import requests
import config


class Kinopoisk_testing_api:
    def __init__(self, base_url_api: str, api_key=None):
        self.base_url = base_url_api
        self.api_key = api_key

    def connect_to_api_with_params(self, params=None):
        """
        Запрос без обязательного эндпоинта, только параметры
        """
        url = self.base_url
        headers = {
            'X-API-KEY': config.auth_token,
            'accept': 'application/json'
            }
        response = requests.get(url, headers=headers, params=params)
        return response

    def connect_to_api_with_endpoint(self, endpoint: str, params=None):
        """
        Запрос с обязательным эндпоинтом и параметрами
        """
        url = self.base_url + endpoint
        headers = {
            'X-API-KEY': config.auth_token,
            'accept': 'application/json'
        }
        response = requests.get(url, headers=headers, params=params)
        return response

    def search_movie_by_id(self, movie_id: int):
        """
        Запрос для получения деталей фильма по ID
        """
        endpoint = f"/{movie_id}"
        params = {}
        return self.connect_to_api_with_endpoint(endpoint, params)

    def search_movie_with_query(self):
        """
        Запрос с параметром для получения информации,
        например о фильме.
        """
        endpoint = "/search"
        params = {
            "page": config.page,
            "limit": config.limit,
            "query": config.search_query
            }
        return self.connect_to_api_with_endpoint(endpoint, params=params)

    def alternative_searching(self):
        """
        Запрос информации о фильме по альтернативным параметрам,
        такие как года релиза и рейтинг фильма.
        """
        params = {
            "page": config.page,
            "limit": config.limit,
            "releaseYears.start": config.years,
            "rating.kp": config.rating
            }
        # Логируем параметры запроса
        print(f"Request parameters: {params}")
        response = self.connect_to_api_with_params(params=params)
        # Логируем ответ для диагностики
        print(f"API response: {response.text}")
        return response.json()

    def search_genre_and_interval(self):
        """
        Запрос информации о фильме по альтернативным параметрам,
        такие как года релиза и жанра фильма.
        """
        params = {
            "page": config.page,
            "limit": config.limit,
            "year": config.years,
            "genres.name": config.genre
            }
        # Логируем параметры запроса
        print(f"Request parameters: {params}")
        response = self.connect_to_api_with_params(params=params)
        # Логируем ответ для диагностики
        print(f"API response: {response.text}")
        return response.json()

    def search_actor_with_query(self):
        """
        Запрос с параметрами для получения информации об актере.
        """
        endpoint = "/search"
        params = {
            "page": config.page,
            "limit": config.limit,
            "query": config.actor_api
            }
        return self.connect_to_api_with_endpoint(endpoint, params=params)