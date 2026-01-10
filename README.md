# tmdbwrapper <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/Python-3.10%2B-brightgreen" alt="Python 3.10+"></a>
A wrapper for the TMDB API that allows for asynchronous building of TMDBMovie objects and retrieving streaming provider URLs.

## Requirements
- Python 3.10+

## Installation
```
pip install git+https://github.com/9Oc/tmdbwrapper.git
```

Alternatively, clone the repository locally and install from the source:
```
git clone https://github.com/9Oc/tmdbwrapper
cd tmdbwrapper
pip install .
```

Updating:
```
pip install --upgrade git+https://github.com/9Oc/tmdbwrapper.git
```

## Usage
To use the wrapper, create a TMDBClient object with your TMDB API key passed in as an argument:
```
from tmdbwrapper.tmdb import TMDBClient

client = TMDBClient("tmdb_api_key")
```

Once your client instance is initialized, there are a few functions available:  
- get_movie
- get_all_watch_providers
- get_provider_url
- search

### get_movie
Builds a TMDBMovie object containing these fields:  
- ``id``: The TMDB ID of the movie
- ``imdb_id``: The IMDB ID of the movie
- ``title``: The title of the movie
- ``original_title``: The original title of the movie, ``None`` if the movie has no original_title
- ``alternative_titles``: A dict where the keys are regions and the items are the alternative titles of the movie belonging to the regions
- ``year``: The release year of the movie
- ``duration``: The duration of the movie in seconds
- ``providers``: A list of Provider objects which represent the streaming providers which the movie is on
```
from tmdbwrapper.tmdb import TMDBClient

client = TMDBClient("tmdb_api_key")
movie = await client.get_movie("550")
print(f"{movie.title} ({movie.year}) [{movie.id}]")
print(movie.providers)

"""
Output:  
Adventures in Babysitting (1987) [14367]
[Provider(Disney Plus, regions={'se', 'pa', 'tr', 'rs', 'do', 'no', 'sv', 'lt', 'us', 'es', 'gt', 'ec', 'bz', 'sm', 'uy', 'ca', 'fi', 'bg', 'ee', 'pt', 'ni', 'au', 'lu', 'me', 'lc', 'jm', 'li', 'de', 'fr', 'ba', 'dk', 'be', 'br', 'eg', 'lv', 'al', 'mk', 'nl', 'bo', 'ph', 'si', 'it', 'tt', 'ar', 'cr', 'pe', 'py', 'ie', 'hn', 'mx', 'gb', 'at', 'ch', 'hr', 'nz', 'ad', 'is', 'cl', 've', 'co'}), Provider(Apple TV, regions={'ie', 'za', 'gb', 'nz', 'us', 'ca', 'au'}), Provider(Amazon Prime Video, regions={'fr', 'se', 'be', 'ie', 'gb', 'nz', 'us', 'es', 'ca', 'au', 'pl', 'gg'}), Provider(Google Play Movies, regions={'fr', 'hu', 'ie', 'ua', 'gb', 'nz', 'us', 'es', 'sk', 'ca', 'au', 'pl'}), Provider(YouTube, regions={'fr', 'gb', 'us', 'ca', 'au', 'pl'}), Provider(CosmoGo, regions={'ca'}), Provider(Crave Amazon Channel, regions={'ca'}), Provider(MovistarTV, regions={'co', 'cl'}), Provider(More TV, regions={'ru'}), Provider(Fandango At Home, regions={'us'})]
"""

# If you want to get a specific Provider from a TMDBMovie object, you can call get_provider.
print(movie.get_provider(ProviderName.MOVISTARTV))

"""
Output:  
Provider(MovistarTV, regions={'cl', 'co'})
""""
```

### get_all_watch_providers
This function is called when you use ``get_movie``, but if you want to skip building a full TMDBMovie object and just want a list of Provider objects for a given TMDB ID, you can call ``get_all_watch_providers`` and pass the TMDB ID in as an argument.
```
from tmdbwrapper.tmdb import TMDBClient

client = TMDBClient("tmdb_api_key")
providers = await client.get_all_watch_providers(14367)
print(providers)

"""
Output:  
[Provider(Disney Plus, regions={'uy', 'sm', 'lc', 'is', 'at', 'li', 'rs', 'fr', 'lu', 'ie', 'br', 'no', 'ni', 'pe', 'ec', 'es', 'pt', 'de', 've', 'mk', 'sv', 'ch', 'al', 'au', 'dk', 'lv', 'ph', 'bo', 'mx', 'cr', 'si', 'us', 'fi', 'py', 'nz', 'ar', 'lt', 'gt', 'co', 'be', 'pa', 'ad', 'gb', 'ba', 'jm', 'tr', 'tt', 'bg', 'eg', 'it', 'me', 'nl', 'se', 'bz', 'cl', 'ee', 'ca', 'do', 'hn', 'hr'}), Provider(Apple TV, regions={'gb', 'us', 'za', 'nz', 'ca', 'ie', 'au'}), Provider(Amazon Prime Video, regions={'be', 'es', 'gb', 'us', 'se', 'pl', 'nz', 'ca', 'fr', 'ie', 'au', 'gg'}), Provider(Google Play Movies, regions={'ua', 'gb', 'es', 'us', 'hu', 'nz', 'pl', 'ca', 'fr', 'sk', 'ie', 'au'}), Provider(YouTube, regions={'gb', 'us', 'pl', 'ca', 'fr', 'au'}), Provider(CosmoGo, regions={'ca'}), Provider(Crave Amazon Channel, regions={'ca'}), Provider(MovistarTV, regions={'cl', 'co'}), Provider(More TV, regions={'ru'}), Provider(Fandango At Home, regions={'us'})]
"""
```

### get_provider_url
Gets the streaming provider url for a given TMDBMovie object, provider name, and optional region.
```
from tmdbwrapper.tmdb import TMDBClient
from tmdbwrapper.tmdbmovie import ProviderName

client = TMDBClient("tmdb_api_key")
movie = await client.get_movie(671)
provider_url = await client.get_provider_url(movie, ProviderName.HBO_MAX)
print(provider_url)

"""
Output:  
https://play.hbomax.com/show/4b990c5d-38ab-4daf-8092-2617cbc6d062?utm_source=universal_search
"""

# Some providers return different URLs based on the region, so if you want a specific regions URL, pass a region as an argument.
provider_url = await client.get_provider_url(movie, ProviderName.APPLE_TV, region="AR")
print(provider_url)
"""
Output:  
https://tv.apple.com/ar/movie/harry-potter-y-la-piedra-filosofal/umc.cmc.55wxtmrughu40phd8lgr6qejr?at=1000l3V2&ct=app_tv&itscg=30200&itsct=justwatch_tv&playableId=tvs.sbd.9001%3A314918278
"""
```

### search
Searches the TMDB API using the search endpoint with the specified query and returns a list of TMDBMovie objects parsed from the results. Optionally provide a year and/or region to narrow down results.
```
from tmdbwrapper.tmdb import TMDBClient

client = TMDBClient("tmdb_api_key")
movies = await client.search("The Cabin in the Woods")
print(movies)

"""
Output:
[TMDBMovie(id=22970, title='The Cabin in the Woods', original_title='The Cabin in the Woods', year=2012, duration=5700), TMDBMovie(id=1384336, title='Another Cabin in the Woods Movie', original_title='Another Cabin in the Woods Movie', year=2024, duration=4620), TMDBMovie(id=1316258, title='A Cabin in the Woods, But Not That Cabin, Nor Those Woods', original_title='A Cabin in the Woods, But Not That Cabin, Nor Those Woods', year=2024, duration=None), TMDBMovie(id=1567846, title='We Are Not Who We Are: Making The Cabin in the Woods', original_title='We Are Not Who We Are: Making The Cabin in the Woods', year=None, duration=1740)]
"""
```

Any TMDBClients which have open sessions will automatically have their sessions closed upon program exit. If you need to close a clients session before the program exits, you can call ``close()`` which will close the active session of the client. If the session of the client is already closed, ``close()`` will simply return.