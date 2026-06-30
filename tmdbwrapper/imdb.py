import aiohttp

GRAPHQL_ENDPOINT: str = r"https://api.graphql.imdb.com/"

GRAPHQL_SEARCH_QUERY: str = """
query ($id: ID!) {
    title(id: $id) {
    titleText { text }
    originalTitleText { text }
    releaseYear { year }
    releaseDate { day, month, year }
    runtime { seconds }
    spokenLanguages { spokenLanguages { id, text } }
    countriesOfOrigin { countries { id } }
    certificate { rating }
    ratingsSummary { aggregateRating }
    }
}
"""


class IMDBMovie:
    def __init__(
        self,
        id: str,
        title: str,
        original_title: str,
        release_year: int,
        release_date: dict,
        runtime_seconds: int,
        spoken_languages: list,
        countries_of_origin: list,
        certificate: str,
        imdb_rating: float,
    ):
        self.id: str = id
        self.title: str = title
        self.original_title: str = original_title
        self.release_year: int = release_year
        self.release_date: dict = release_date
        self.runtime_seconds: int = runtime_seconds
        self.spoken_languages: list = spoken_languages
        self.countries_of_origin: list = countries_of_origin
        self.certificate: str = certificate
        self.imdb_rating: float = imdb_rating
        self.errors: dict | None = None


async def get_imdb_movie(imdb_id: str, session: aiohttp.ClientSession) -> IMDBMovie | None:
    if not imdb_id:
        return None
    payload: dict = {
        "query": GRAPHQL_SEARCH_QUERY,
        "variables": {"id": imdb_id},
    }
    headers: dict = {
        "Content-Type": "application/json",
        "x-imdb-user-country": "US",
    }
    async with session.post(GRAPHQL_ENDPOINT, json=payload, headers=headers) as resp:
        data: dict = await resp.json()
        imdb_movie: IMDBMovie = IMDBMovie(
            id=imdb_id,
            title="",
            original_title="",
            release_year=None,
            release_date={},
            runtime_seconds=None,
            spoken_languages=[],
            countries_of_origin=[],
            certificate=None,
            imdb_rating=0.0,
        )
        if data.get("errors"):
            imdb_movie.errors = data.get("errors", [{}])[0]
            return imdb_movie

        movie_data: dict = data.get("data", {}).get("title")
        if not movie_data:
            return imdb_movie

        imdb_movie.id = imdb_id
        imdb_movie.title = movie_data.get("titleText").get("text") if movie_data.get("titleText") else None
        imdb_movie.original_title = movie_data.get("originalTitleText").get("text") if movie_data.get("originalTitleText") else None
        imdb_movie.release_year = movie_data.get("releaseYear").get("year") if movie_data.get("releaseYear") else None
        imdb_movie.release_date = movie_data.get("releaseDate")
        imdb_movie.runtime_seconds = movie_data.get("runtime").get("seconds") if movie_data.get("runtime") else None
        imdb_movie.spoken_languages = (
            [lang.get("id") for lang in movie_data.get("spokenLanguages", {}).get("spokenLanguages", [])]
            if movie_data.get("spokenLanguages")
            else []
        )
        imdb_movie.countries_of_origin = (
            [country.get("id") for country in movie_data.get("countriesOfOrigin", {}).get("countries", [])]
            if movie_data.get("countriesOfOrigin")
            else []
        )
        imdb_movie.certificate = movie_data.get("certificate").get("rating") if movie_data.get("certificate") else None
        imdb_movie.imdb_rating = movie_data.get("ratingsSummary").get("aggregateRating") if movie_data.get("ratingsSummary") else None
        return imdb_movie
