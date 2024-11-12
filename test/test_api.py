import pytest
import config
import allure


@allure.epic("Search functionality")
@allure.feature("API testing")
@allure.story("Search movie by movie ID")
@allure.severity("blocker")
@allure.title("test_search_id_movie")
@pytest.mark.api
def test_search_id_movie(auth_api):
    """
    Тест API для получения сведений о фильме по ID
    """
    with allure.step("Отправить запрос GET, который включает id фильма."):
        response = auth_api.search_movie_by_id(config.id_movie)

    with allure.step("Проверить, что id запроса соответствует id ответа."):
        assert "id" in response.json(), "Response does not contain 'id' key"
        assert response.json()["id"] == config.id_movie, (
            f"Expected movie ID to be {
                config.id_movie} but got {response.json()['id']}"
                )
    with allure.step(
        "Проверить, что ответ содержит наименование фильма и соответвует указанному id."
    ):
        assert "name" in response.json(), (
            "Response does not contain 'name' key"
            )
        movie_name = response.json()["name"]
        assert movie_name == config.movie_to_search, (
            f"Expected movie name to be '{
                config.movie_to_search}' but got '{movie_name}'"
            )


@allure.epic("Search functionality")
@allure.feature("API testing")
@allure.story("Search movie by movie name")
@allure.severity("blocker")
@allure.title("test_movie_search")
@pytest.mark.api
def test_movie_search(auth_api):
    """
    Тест API для поиска фильма c помощью расширенного поиска.
    """
    with allure.step("Отправить запрос GET с параметрами."):
        response = auth_api.search_movie_with_query()

        data = response.json()

    with allure.step("Проверить, что ответ содержит тело ответа."):
        assert "docs" in data, "Response does not contain 'docs' key"
        assert data["docs"], "Response 'docs' key contains an empty list"

    # Проверяем первый фильм в списке результата поиска.
    first_movie = data["docs"][0]

    with allure.step(
        "Проверить, что наименование фильма соответствует искомому в запросе."
    ):
        assert "name" in first_movie, "First movie does not contain 'name' key"
        assert config.search_query.lower() in first_movie["name"].lower(), (
            f"Expected query '{
                config.search_query
                }' in movie name but got {first_movie['name']}"
            )

    with allure.step(
        "Проверить, что год выпуска фильма соответствует искомому в запросе."
    ):
        assert "year" in first_movie, "First movie does not contain 'year' key"
        assert first_movie["year"] == config.movie_year_api, (
            f"Year does not match {config.movie_year_api}"
            )

    with allure.step(
        "Проверить, что жанр фильма соответствует искомому в запросе."
    ):
        genres = [genre["name"] for genre in first_movie.get("genres", [])]
        assert config.genre_api_first in genres, (
            f"Genre {config.genre_api_first} not found in movie genres"
            )
        assert config.genre_api_second in genres, (
            f"Genre {config.genre_api_second} not found in movie genres"
            )

    with allure.step(
        "Проверить, что страна производства фильма соответствует искомому в запросе."
    ):
        countries = [
            country["name"] for country in first_movie.get("countries", [])
            ]
        assert config.country_api in countries, (
            f"Country {config.country_api} not found in movie countries"
            )

    with allure.step(
        "Проверить, что рейтинг фильма соответствует искомому в запросе."
    ):
        assert "rating" in first_movie, (
            "First movie does not contain 'rating' key"
            )
        assert "kp" in first_movie["rating"], (
            "No 'kp' rating found in movie ratings"
            )
        min_rate, max_rate = map(float, config.rating.split("-"))
        movie_rating = first_movie['rating']["kp"]
        assert min_rate <= movie_rating <= max_rate, (
            f"Movie rating {
                movie_rating} is not in the range {min_rate}-{max_rate}"
            )


@allure.epic("Search functionality")
@allure.feature("API testing")
@allure.story("Search actor by actor name")
@allure.severity("blocker")
@allure.title("test_actor_search")
@pytest.mark.api
def test_actor_search(auth_api):
    """
    Тест API для поиска актера по параметрам.
    """
    with allure.step("Отправить запрос GET, который содержит параметр Актер."):
        response = auth_api.search_actor_with_query()
    data = response.json()

    with allure.step("Проверить, что ответ содержит тело ответа."):
        assert "docs" in data, "Response does not contain 'docs' key"
        assert data["docs"], "Response 'docs' key contains an empty list"

    # Проверка данных первого актера в списке результата поиска.
    first_actor = data["docs"][0]

    with allure.step("Проверить, что ответ содержит искомое имя актера"):
        assert "name" in first_actor, "First movie does not contain 'name' key"
        assert config.actor_api.lower() in first_actor["name"].lower(), (
            f"Expected query '{
                config.actor_api}' in movie name but got {first_actor['name']}"
            )


@allure.epic("Search functionality")
@allure.feature("API testing")
@allure.story("Search movie by release year and movie rating")
@allure.severity("blocker")
@allure.title("test_search_by_years_and_rating")
@pytest.mark.api
def test_search_by_years_and_rating(auth_api):
    """
    Тест API для поиска фильма по годам релиза и рейтингу.
    """
    with allure.step(
        "Отправить запрос GET, который содержит параметры: релиз и рейтинг."
    ):
        response = auth_api.alternative_searching()

    if 'error' in response:
        pytest.fail(f"API returned an error: {response['error']}")
    with allure.step("Проверить, что ответ содержит тело ответа."):
        data = response
        assert "docs" in data, "'docs' key not found in response"
        assert isinstance(data["docs"], list), "'docs' is not a list"

    with allure.step(
        "Проверить, что тело ответа содержит необходимые запрашиваемые атрибуты."
    ):
        if data["docs"]:
            movie = data["docs"][0]
            assert "id" in movie, "'id' key not found in movie"
            assert "name" in movie, "'name' key not found in movie"
            assert "rating" in movie, "'rating' key not found in movie"
            assert "kp" in movie["rating"], "'kp' rating not found in movie"
            assert "description" in movie, (
                "'description' key not found in movie"
                )
            assert "genres" in movie, "'genres' key not found in movie"
            assert isinstance(movie["genres"], list), "'genres' is not a list"

            with allure.step(
                "Проверить, что тело ответа содержит необходимое количество результатов"
            ):
                assert data["limit"] == 1, (
                    f"Expected limit of 1, but got {data['limit']}"
                    )
                assert data["page"] == 1, (
                    f"Expected page 1, but got {data['page']}"
                    )

            with allure.step(
                "Проверить, что тело ответа содержит запрашиваемые года релиза."
            ):
                min_year, max_year = map(int, config.years.split("-"))
                movie_year = movie["year"]
                assert min_year <= movie_year <= max_year, (
                    f"Movie year {
                        movie_year} is not in the range {min_year}-{max_year}"
                    )

            with allure.step(
                "Проверить, что рейтинг фильма в пределах указанного."
            ):
                min_rate, max_rate = map(int, config.rating.split("-"))
                movie_rating = movie['rating']["kp"]
                assert min_rate <= movie_rating <= max_rate, (
                    f"Movie rating {
                        movie_rating
                        } is not in the range {min_rate}-{max_rate}"
                    )

        else:
            print("No movies found in the response")


@allure.epic("Search functionality")
@allure.feature("API testing")
@allure.story("Search movie by release genre and movie years")
@allure.severity("blocker")
@allure.title("test_search_by_genre_and_interval")
@pytest.mark.api
def test_search_by_genre_and_interval(auth_api):
    """
    Тест API для поиска фильма по жанру и годам релиза.
    """
    with allure.step(
        "Отправить запрос GET, который содержит параметры: жанр и года релиза."
    ):
        response = auth_api.search_genre_and_interval()

    # Печать тела ответа для диагностики
    print(f"API response: {response}")

    if 'error' in response:
        pytest.fail(f"API returned an error: {response['error']}")

    with allure.step("Проверить, что ответ содержит тело ответа."):
        data = response
        assert "docs" in data, "'docs' key not found in response"
        assert isinstance(data["docs"], list), (
            "'docs' is not a list"
            )

    with allure.step(
        "Проверить, что тело ответа содержит необходимые запрашиваемые атрибуты."
    ):
        if data["docs"]:
            movie = data["docs"][0]
            assert "id" in movie, "'id' key not found in movie"
            assert "name" in movie, "'name' key not found in movie"
            assert "rating" in movie, "'rating' key not found in movie"
            assert "kp" in movie["rating"], "'kp' rating not found in movie"
            assert "description" in movie, (
                "'description' key not found in movie"
                )
            assert "genres" in movie, "'genres' key not found in movie"
            assert isinstance(movie["genres"], list), "'genres' is not a list"

            with allure.step(
                "Проверить, что жанр, переданный в запросе, присутствует в жанрах фильма"
            ):
                genres = [genre["name"] for genre in movie["genres"]]
                assert config.genre in genres, (
                    f"Genre '{
                        config.genre}' not found in movie genres: {genres}"
                    )

            with allure.step(
                "Проверить, что год фильма в пределах указанного диапазона"
            ):
                min_year, max_year = map(int, config.years.split("-"))
                movie_year = movie["year"]
                assert min_year <= movie_year <= max_year, (
                    f"Movie year {
                        movie_year} is not in the range {min_year}-{max_year}"
                    )

        else:
            print("No movies found in the response")