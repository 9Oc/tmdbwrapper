import asyncio
import atexit
import re
from typing import Iterable

import aiohttp
import requests
from aiohttp_socks import ProxyConnector
from rich import print
from simplejustwatchapi.justwatch import search
from simplejustwatchapi.query import Offer

from tmdbwrapper.tmdbmovie import Provider, ProviderName, TMDBMovie

_active_clients = []


class TMDBClient:
    def __init__(self, api_key: str, proxy: str | None = None):
        self.api_key = api_key
        self.proxy = proxy
        self._session: aiohttp.ClientSession | None = None
        _active_clients.append(self)

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create the aiohttp session."""
        if self._session is None or self._session.closed:
            aiohttp_kwargs = {"timeout": aiohttp.ClientTimeout(total=30)}
            if self.proxy:
                aiohttp_kwargs["connector"] = ProxyConnector.from_url(self.proxy.replace(r"socks5h://", r"socks5://"))
            self._session = aiohttp.ClientSession(**aiohttp_kwargs)
        return self._session

    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            if self in _active_clients:
                _active_clients.remove(self)

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def search(self, query: str, year: int | None = None, region: str | None = None) -> list[TMDBMovie] | None:
        """
        Search the TMDB search endpoint with a query.
        Optionally provide a year and/or region to narrow results.
        Returns a list of TMDBMovie objects.

        Args:
            query (str): The search query.
            year (int | None): The year to filter results by. Defaults to None.
            region (str | None): The region to filter results by. Defaults to None.
        Returns:
            list[TMDBMovie]: A list of TMDBMovie objects if results are found, otherwise an empty list.
        """
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
        }
        if year:
            params["year"] = year
        if region:
            params["region"] = region.lower()

        proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
        r = requests.get(url, params=params, proxies=proxies, timeout=15)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])

        if not results:
            return []

        # limit concurrency to avoid rate limiting
        sem = asyncio.Semaphore(5)

        async def sem_get_movie(movie_id: str):
            async with sem:
                return await self.get_movie(movie_id)

        # create tasks only for results that have an id
        tasks = [asyncio.create_task(sem_get_movie(str(r["id"]))) for r in results if r.get("id") is not None]
        if not tasks:
            return []

        movies = await asyncio.gather(*tasks)
        # filter out None results (failed fetches)
        movies = [m for m in movies if m is not None]

        return movies if movies else []

    async def get_movie(self, movie_id: str, get_alternative_titles: bool = False) -> TMDBMovie | None:
        """
        Build a TMDBMovie object from TMDB API data for the given movie ID.

        Args:
            movie_id (str): The TMDB movie ID to fetch data for.
            get_alternative_titles (bool): Whether to fetch alternative titles data (additional API call cost). Defaults to False.
        Returns:
            TMDBMovie | None: The TMDBMovie object if the movie is found, otherwise None.
        """
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        alternative_titles_url = f"https://api.themoviedb.org/3/movie/{movie_id}/alternative_titles"
        watch_providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
        params = {"api_key": self.api_key}

        session = await self._get_session()

        async def _fetch(url: str, params: dict, timeout: int = 15) -> dict | None:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                try:
                    response.raise_for_status()
                    return await response.json()
                except aiohttp.ClientResponseError as e:
                    if e.status == 404:
                        return None
                    raise

        async def _none():
            return None

        main_task = _fetch(movie_url, params)
        alt_task = _fetch(alternative_titles_url, params) if get_alternative_titles else _none()
        providers_task = _fetch(watch_providers_url, params)

        main_data, alt_data, providers_data = await asyncio.gather(main_task, alt_task, providers_task)
        if main_data is None or providers_data is None:
            return None

        main_parsed = self._parse_movie_data(main_data)

        alternative_titles = self._parse_alternative_titles_data(alt_data) if alt_data else []

        providers: list[Provider] = []
        if providers_data is not None:
            providers: list[Provider] = self._parse_providers_data(providers_data) if providers_data else []

        return TMDBMovie(
            id=movie_id,
            imdb_id=main_parsed.get("imdb_id"),
            title=main_parsed.get("title"),
            original_title=main_parsed.get("original_title"),
            alternative_titles=alternative_titles,
            year=main_parsed.get("year"),
            duration=main_parsed.get("duration"),
            original_language=main_parsed.get("original_language"),
            spoken_languages=main_parsed.get("spoken_languages"),
            origin_countries=main_parsed.get("origin_countries"),
            overview=main_parsed.get("overview"),
            genres=main_parsed.get("genres"),
            vote_average=main_parsed.get("vote_average"),
            providers=providers,
        )

    def _parse_movie_data(self, data: dict) -> dict | None:
        """
        Parse movie data from TMDB API response and return a dictionary of movie attributes.

        Args:
            data (dict): The raw JSON from the TMDB API response for a movie.
        Returns:
            dict | None: A dict of the movie attributes.
        """
        if not data:
            return None

        imdb_id: str = data.get("imdb_id") or None
        title: str = data.get("title") or None
        original_title: str = data.get("original_title") or None
        duration: int = data.get("runtime") or None
        if duration:
            duration = duration * 60  # convert duration to seconds

        release_date = data.get("release_date") or data.get("first_air_date") or None
        year = None
        if release_date:
            match = re.match(r"(\d{4})", release_date)
            if match:
                year = int(match.group(1))

        original_language: str = data.get("original_language") or None
        spoken_languages: list[str] = []
        for spoken_lang in data.get("spoken_languages", []):
            lang_code = spoken_lang.get("iso_639_1")
            if lang_code:
                spoken_languages.append(lang_code.lower())

        origin_countries: list[str] = data.get("origin_country", [])

        genre_objects = data.get("genres", [])
        genres: list[str] = []
        for genre in genre_objects:
            genres.append(genre.get("name") or None)

        overview: str = data.get("overview") or None
        vote_average: float = data.get("vote_average") or None

        return {
            "imdb_id": imdb_id,
            "title": title,
            "original_title": original_title,
            "year": year,
            "duration": duration,
            "original_language": original_language,
            "spoken_languages": spoken_languages,
            "origin_countries": origin_countries,
            "genres": genres,
            "overview": overview,
            "vote_average": vote_average,
        }

    def _parse_alternative_titles_data(self, data: dict) -> list[dict]:
        """
        Parse alternative titles data from TMDB API response and return a list of alternative titles.

        Args:
            data (dict): The raw JSON from the TMDB API response for alternative titles.
        Returns:
            list[dict]: A list of alternative titles for the movie.
        """
        alternative_titles = []
        if data:
            for t in data.get("titles", []):
                alt_title = t.get("title")
                if not alt_title:
                    continue

                region = t.get("iso_3166_1", "unknown").lower()
                alternative_titles.append(
                    {
                        "region": region,
                        "title": alt_title,
                    }
                )

        return alternative_titles

    def _parse_providers_data(self, data: dict) -> list[Provider]:
        """
        Parse watch providers data from TMDB API response and return a list of Provider objects.

        Args:
            data (dict): The raw JSON from the TMDB API response for watch providers.
        Returns:
            list[Provider]: A list of Provider objects for the movie.
        """
        results = data.get("results", {})
        buckets: dict[str, Provider] = {}

        for region_code, info in results.items():
            for key in ("buy", "rent", "flatrate", "free", "ads"):
                for item in info.get(key, []) or []:
                    provider_name = item.get("provider_name")
                    if not provider_name:
                        continue
                    canonical = Provider.normalize_name(provider_name)
                    bucket = buckets.setdefault(canonical, Provider(canonical_name=canonical))
                    bucket.names.add(provider_name)
                    region_entry = {region_code.lower(): key}
                    if not any(region_entry == existing for existing in bucket.regions):
                        bucket.regions.append(region_entry)

        return list(buckets.values())

    def _get_justwatch_node_id(self, movie: TMDBMovie, country: str) -> str | None:
        """
        Search JustWatch for the given TMDBMovie and get its node ID.
        Unused function for now, may be needed in the future.
        """
        if not movie.title:
            return None

        # search with title and country
        results = search(movie.title, country.upper(), "en", count=10, best_only=True, object_types=["MOVIE"])

        if results is None or not results:
            return None

        for entry in results:
            if not entry:
                continue
            # check TMDB ID and IMDB ID for matching
            imdb_match = str(entry.imdb_id) == str(movie.imdb_id) if entry.imdb_id else False
            tmdb_match = str(entry.tmdb_id) == str(movie.id) if entry.tmdb_id else False
            release_year_match = entry.release_year == movie.year if entry.release_year and movie.year else False
            if (tmdb_match or imdb_match) and release_year_match:
                return entry.entry_id

            runtime_match = (
                int(entry.runtime_minutes * 60) == movie.duration if entry.runtime_minutes and movie.duration else False
            )
            title_match = entry.title.lower() == movie.title.lower() if entry.title and movie.title else False
            tmdb_score_match = entry.scoring.tmdb_score == movie.vote_average if entry.scoring else False
            if title_match and release_year_match and runtime_match and tmdb_score_match:
                return entry.entry_id

        return None

    def _fetch_provider_url(self, offers: Iterable[Offer], provider_name: ProviderName) -> str | None:
        """Fetch provider URL for a given ProviderName and list of Offers."""

        if not offers or not provider_name:
            return None

        # get all alises for the given ProviderName
        canonical_name = provider_name.value
        all_provider_names = {canonical_name.lower()}

        if canonical_name in Provider.ALIASES:
            all_provider_names.update(Provider.ALIASES[canonical_name])

        # look through offers for matching provider and return the URL if a match is found
        for offer in offers:
            offer_name = offer.package.name if hasattr(offer, "package") else None
            if offer_name:
                offer_name_lower = offer_name.lower()
                if any(provider_name.lower() == offer_name_lower for provider_name in all_provider_names):
                    url = getattr(offer, "url", None)
                    if url:
                        return url

        return None

    def get_provider_url(
        self, movie: TMDBMovie, provider_name: ProviderName, region: str = None, fuzzy_match: bool = False
    ) -> str | None:
        """
        Get the deep link for the given TMDBMovie on the specified provider.
        Optionally provide a region to get the deep link from that region.

        Args:
            movie (TMDBMovie): The TMDBMovie to get the provider URL for.
            provider_name (ProviderName): The provider to get the URL for.
            region (str, optional): The region to get the URL from. Defaults to None.
            fuzzy_match (bool, optional): Whether to allow matching by title, year, runtime, and TMDB vote average instead of TMDB/IMDB ID. Defaults to False.
        Returns:
            str | None: The provider deep link for the movie if found, otherwise None.
        """
        if not movie or not provider_name:
            return None
        provider = movie.get_provider(provider_name)
        if provider is None:
            return None
        regions = [region] if region else list(provider.regions)
        for r in regions:
            region_name = region or next(iter(r.keys())).upper()
            # search with title and region to get MediaEntry's
            results = search(
                movie.title,
                country=region_name.upper(),
                language="en",
                count=20,
                best_only=True,
                object_types=["MOVIE"],
            )
            if not results:
                continue

            # check each entry for a match to the given movie
            # if a match is found, look through offers and to find the URL for the given provider
            for entry in results:
                if not entry:
                    continue
                offers = entry.offers

                # check TMDB ID and IMDB ID + (title or year) and (runtime or overview)
                # due to justwatch frequently having mismatched or out-of-date data,
                # adding the 2 additional checks prevents many false positives when the TMDB or IMDB ID's match but lead to the wrong movie deep link
                imdb_match = str(entry.imdb_id) == str(movie.imdb_id) if entry.imdb_id else False
                tmdb_match = str(entry.tmdb_id) == str(movie.id) if entry.tmdb_id else False
                title_match = entry.title.lower() == movie.title.lower() if entry.title and movie.title else False
                release_year_match = entry.release_year == movie.year if entry.release_year and movie.year else False
                runtime_match = (
                    int(entry.runtime_minutes * 60) == movie.duration
                    if entry.runtime_minutes and movie.duration
                    else False
                )
                overview_match = (
                    entry.short_description == movie.overview if entry.short_description and movie.overview else False
                )
                if (
                    (tmdb_match or imdb_match)
                    and (title_match or release_year_match)
                    and (runtime_match or overview_match)
                ):
                    url = self._fetch_provider_url(offers, provider_name)
                    if url:
                        return url

                # check by title, year, runtime, and (tmdb vote average or overview) if fuzzy_match is True
                # this can help catch matches which have bad TMDB/IMDB ID's from JustWatch but are otherwise correct
                # however, it can lead to false positives in some cases
                if fuzzy_match:
                    tmdb_score_match = entry.scoring.tmdb_score == movie.vote_average if entry.scoring else False
                    if title_match and release_year_match and runtime_match and (tmdb_score_match or overview_match):
                        url = self._fetch_provider_url(offers, provider_name)
                        if url:
                            return url

        return None

    async def get_all_watch_providers(self, tmdb_id: str) -> list[Provider]:
        """
        Returns a list of Provider objects which the given TMDB ID is available on.

        Args:
            tmdb_id (str): The TMDB movie ID to fetch providers for.
        Returns:
            list[Provider]: List of Provider objects if the movie is available on any providers, otherwise an empty list.
        Raises:
            aiohttp.ClientResponseError: If the TMDB API request fails with a status other than 404.
                                         A 404 status is treated as "movie not found" and results in an empty list being returned.
        """
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers"
        params = {"api_key": self.api_key}

        session = await self._get_session()

        async def fetch(url: str, params: dict, timeout: int = 15) -> dict | None:
            """Fetch json response from given URL with retry."""
            try:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                if e.status == 404:
                    # if the movie is not found, return an empty list
                    return []
                raise

        data = await fetch(url, params)
        if not data:
            return []
        return self._parse_providers_data(data)


def _cleanup_clients():
    """Cleanup function called at program exit."""
    if _active_clients:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            for client in _active_clients[:]:  # copy list to avoid modification during iteration
                if client._session and not client._session.closed:
                    loop.run_until_complete(client.close())
        finally:
            loop.close()
            print("[green][TMDB][/green] Closed all active TMDBClient sessions.")


# register cleanup function to run at program exit
atexit.register(_cleanup_clients)
