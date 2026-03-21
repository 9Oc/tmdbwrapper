import asyncio
import atexit
import re

import aiohttp
import requests
from rich import print
from simplejustwatchapi.justwatch import details, search

from tmdbwrapper.tmdbmovie import Provider, ProviderName, TMDBMovie

_active_clients = []


class TMDBClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._session: aiohttp.ClientSession | None = None
        _active_clients.append(self)

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create the aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
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
        """
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": self.api_key,
            "query": query,
        }
        if year:
            params["year"] = year
        if region:
            params["region"] = region

        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])

            if not results:
                return None
            # limit concurrency to avoid rate limiting
            sem = asyncio.Semaphore(10)

            async def sem_get_movie(movie_id: str):
                async with sem:
                    return await self.get_movie(movie_id)

            # create tasks only for results that have an id
            tasks = [asyncio.create_task(sem_get_movie(str(r["id"]))) for r in results if r.get("id") is not None]
            if not tasks:
                return None

            movies = await asyncio.gather(*tasks)
            # filter out None results (failed fetches)
            movies = [m for m in movies if m is not None]

            return movies if movies else None
        except Exception as e:
            print(f"[red][TMDB][/red] Error searching for movie: {e}")
            return None

    async def get_movie(self, movie_id: str) -> TMDBMovie | None:
        """
        Build a TMDBMovie object from TMDB API data for the given movie ID.
        Returns None if the movie could not be found or an error occurred.
        """
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        alternative_titles_url = f"https://api.themoviedb.org/3/movie/{movie_id}/alternative_titles"
        watch_providers_url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
        params = {"api_key": self.api_key}

        session = await self._get_session()

        async def fetch_with_retry(url: str, params: dict, timeout: int = 15, retries: int = 1) -> dict | None:
            """Fetch json response from given URL with retry."""
            for attempt in range(retries + 1):
                try:
                    async with session.get(
                        url, params=params, timeout=aiohttp.ClientTimeout(total=timeout)
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
                except Exception:
                    if attempt == retries:
                        raise
                    await asyncio.sleep(0.1)

        try:
            main_task = fetch_with_retry(movie_url, params)
            alt_task = fetch_with_retry(alternative_titles_url, params)
            providers_task = fetch_with_retry(watch_providers_url, params)

            main_data, alt_data, providers_data = await asyncio.gather(main_task, alt_task, providers_task)

            if main_data is None:
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
                overview=main_parsed.get("overview"),
                genres=main_parsed.get("genres"),
                vote_average=main_parsed.get("vote_average"),
                providers=providers,
            )

        except Exception as e:
            print(f"[red][TMDB][/red] Error building TMDBMovie object: {e}")
            return None

    def _parse_movie_data(self, data: dict) -> dict | None:
        """Parse movie data from TMDB API response."""
        if not data:
            return None

        imdb_id = data.get("imdb_id") or None
        title = data.get("title") or None
        original_title = data.get("original_title") or None
        duration = data.get("runtime") or None
        if duration:
            duration = duration * 60  # convert duration to seconds

        release_date = data.get("release_date") or data.get("first_air_date") or None
        year = None
        if release_date:
            match = re.match(r"(\d{4})", release_date)
            if match:
                year = int(match.group(1))

        original_language = data.get("original_language") or None

        genre_objects = data.get("genres") or []
        genres: list[str] = []
        for genre in genre_objects:
            genres.append(genre.get("name") or None)

        overview = data.get("overview") or None
        vote_average = data.get("vote_average") or None

        return {
            "imdb_id": imdb_id,
            "title": title,
            "original_title": original_title,
            "year": year,
            "duration": duration,
            "original_language": original_language,
            "genres": genres,
            "overview": overview,
            "vote_average": vote_average,
        }

    def _parse_alternative_titles_data(self, data: dict) -> list[dict]:
        alternative_titles = []
        if data:
            for t in data.get("titles", []):
                alt_title = t.get("title")
                if not alt_title:
                    continue

                region = t.get("iso_3166_1").lower()
                alternative_titles.append(
                    {
                        "region": region,
                        "title": alt_title,
                    }
                )

        return alternative_titles

    def _parse_providers_data(self, data: dict) -> list[Provider]:
        results = data.get("results", {})
        buckets: dict[str, Provider] = {}

        for region_code, info in results.items():
            for key in ("buy", "rent", "flatrate", "free"):
                for item in info.get(key, []) or []:
                    provider_name = item.get("provider_name")
                    if not provider_name:
                        continue
                    canonical = Provider.normalize_name(provider_name)
                    bucket = buckets.setdefault(canonical, Provider(canonical_name=canonical))
                    bucket.names.add(provider_name)
                    bucket.regions.append({region_code.lower(): key})

        return list(buckets.values())

    def _get_justwatch_node_id(self, movie: TMDBMovie, country: str) -> str | None:
        """
        Search JustWatch for the given TMDBMovie and get its node ID.
        Uses TMDB/IMDB for matching.
        Returns the node ID if found, else None.
        """
        if not movie.title:
            return None

        try:
            # search with title and country
            results = search(movie.title, country.upper(), "en", count=100, best_only=False)

            if results is None or not results:
                return None

            for entry in results:
                # check TMDB ID and IMDB ID for matching
                imdb_match = entry.imdb_id == str(movie.imdb_id) if entry.imdb_id else False
                tmdb_match = entry.tmdb_id == str(movie.id) if entry.tmdb_id else False
                if tmdb_match or imdb_match:
                    return entry.entry_id
                release_year_match = entry.release_year == movie.year if entry.release_year and movie.year else False
                runtime_match = (
                    entry.runtime_minutes == int(movie.duration // 60)
                    if entry.runtime_minutes and movie.duration
                    else False
                )
                title_match = entry.title.lower() == movie.title.lower() if entry.title and movie.title else False
                if title_match and release_year_match and runtime_match:
                    return entry.entry_id

        except Exception as e:
            print(f"[red][JUSTWATCH][/red] Error searching for movie in {country.upper()}: {e}")

        return None

    def _get_justwatch_offers(self, node_id: str, country: str) -> list:
        """
        Get JustWatch offers for given node ID and country.
        Returns a list of offers if found.
        """
        if not node_id or not country:
            return []

        try:
            # get full details for this country which includes offers
            entry = details(node_id, country.upper(), "en", best_only=True)

            if not entry or not entry.offers:
                return []

            return entry.offers

        except Exception as e:
            print(f"[red][JUSTWATCH][/red] Error getting offers for {country.upper()}: {e}")

        return []

    async def get_provider_url(
        self, tmdb_movie: TMDBMovie, provider_name: ProviderName, region: str = None
    ) -> str | None:
        """
        Get the URL for a specific provider for a TMDBMovie.
        If region is specified, only that region is checked; otherwise all regions for the provider are checked.
        """
        if not tmdb_movie or not provider_name:
            return None

        provider = tmdb_movie.get_provider(provider_name)
        if provider is None:
            return None

        regions = [region] if region else list(provider.regions)
        checked_node_ids = set()

        # JustWatch is synchronous, so asyncio.to_thread must be used for concurrency
        node_semaphore = asyncio.Semaphore(2)
        url_semaphore = asyncio.Semaphore(2)

        async def fetch_node_id(region: str) -> str | None:
            """Fetch node ID for a region."""
            async with node_semaphore:
                return await asyncio.to_thread(
                    self._get_justwatch_node_id,
                    tmdb_movie,
                    region,
                )

        async def fetch_provider_url(node_id: str, region: str) -> str | None:
            """Fetch provider URL for a node_id/region."""
            async with url_semaphore:
                offers = await asyncio.to_thread(
                    self._get_justwatch_offers,
                    node_id,
                    region,
                )

            if not offers:
                return None

            # get all possible names for this provider (canonical + aliases)
            canonical_name = provider_name.value
            all_names = {canonical_name.lower()}

            if canonical_name in Provider.ALIASES:
                all_names.update(Provider.ALIASES[canonical_name])

            # look through offers for matching provider
            for offer in offers:
                offer_name = offer.package.name if hasattr(offer, "package") else None
                if offer_name:
                    offer_name_lower = offer_name.lower()
                    if offer_name_lower in all_names or any(name in offer_name_lower for name in all_names):
                        url = getattr(offer, "url", None)
                        if url:
                            return url

            return None

        # create node fetching tasks for all regions
        node_tasks = [asyncio.create_task(fetch_node_id(next(iter(region.keys())))) for region in regions]

        try:
            for node_task in asyncio.as_completed(node_tasks):
                node_id = await node_task

                if not node_id or node_id in checked_node_ids:
                    continue

                checked_node_ids.add(node_id)

                # create tasks to fetch URLs for all regions with this node_id
                url_tasks = [
                    asyncio.create_task(fetch_provider_url(node_id, next(iter(region.keys())))) for region in regions
                ]

                for url_task in asyncio.as_completed(url_tasks):
                    provider_url = await url_task
                    if provider_url:
                        # cancel remaining tasks if a url is found
                        for t in node_tasks + url_tasks:
                            if not t.done():
                                t.cancel()
                        return provider_url

                # ensure all URL tasks are awaited/cancelled cleanly
                for t in url_tasks:
                    if not t.done():
                        t.cancel()

        finally:
            for t in node_tasks:
                if not t.done():
                    t.cancel()

        return None

    async def get_all_watch_providers(self, tmdb_id: str) -> list[Provider]:
        """
        Returns a list of Provider objects which the given TMDB ID is available on.
        """
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/watch/providers"
        params = {"api_key": self.api_key}

        session = await self._get_session()

        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                data = await response.json()

            results = data.get("results", {})
            buckets: dict[str, Provider] = {}

            for region_code, info in results.items():
                for key in ("buy", "rent", "flatrate", "free"):
                    for item in info.get(key, []) or []:
                        provider_name = item.get("provider_name")
                        if not provider_name:
                            continue
                        canonical = Provider.normalize_name(provider_name)
                        bucket = buckets.setdefault(canonical, Provider(canonical_name=canonical))
                        bucket.names.add(provider_name)
                        bucket.regions.append({region_code.lower(): key})

            return list(buckets.values())

        except Exception as e:
            print(f"[TMDB] Error getting watch/providers for ID {tmdb_id}: {e}")
            return []


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
