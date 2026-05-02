# tmdbwrapper <a href="https://www.python.org/downloads/release/python-3100/"><img src="https://img.shields.io/badge/Python-3.10%2B-brightgreen" alt="Python 3.10+"></a>
A wrapper for the TMDB API that allows for asynchronous building of TMDBMovie objects and retrieving streaming provider deep links.

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
```python
from tmdbwrapper.tmdb import TMDBClient

client = TMDBClient("tmdb_api_key", proxy=None) # optionally provide a proxy for requests made to the TMDB API
```

Once your client instance is initialized, there are a few functions available:  
- get_movie
- get_all_watch_providers
- get_provider_url
- search

### get_movie
Builds a TMDBMovie object containing these fields:  
- ``id``: The TMDB ID of the movie.
- ``imdb_id``: The IMDB ID of the movie, ``None`` if TMDB has not stored an IMDB ID for the movie.
- ``title``: The title of the movie.
- ``year``: The release year of the movie, ``None`` if TMDB has not stored a year for the movie.
- ``original_title``: The original title of the movie, ``None`` if the movie has no original_title.
- ``alternative_titles``: A dict where the keys are regions and the values are the alternative titles of the movie belonging to the regions.
- ``duration``: The duration of the movie in seconds.
- ``original_language``: The original language of the movie as a BCP 47 code, ``None`` if TMDB does not have an original language for the movie.
- ``spoken_languages``: The spoken languages in the movie as a list of BCP 47 codes.
- ``origin_countries``: The country or countries of origin for the movie (where the movie was originally released).
- ``genres``: The list of genres the movie falls under.
- ``overview``: The short overview (synopsis) of the movie, ``None`` if TMDB has not stored an overview for the movie.
- ``vote_average``: The average rating for the movie on TMDB, ``None`` if no users have voted on the movie.
- ``providers``: A list of Provider objects which represent the streaming providers which the movie is on.
```python
from tmdbwrapper.tmdb import TMDBClient
from tmdbwrapper.tmdbmovie import ProviderName

client = TMDBClient("tmdb_api_key")
movie = await client.get_movie(14367) # the given ID may be a string or int
print(f"{movie.title} ({movie.year}) [{movie.id}]")
print(movie.providers)

"""
Output:  
Adventures in Babysitting (1987) [14367]  
[Provider(Disney Plus, regions=[{'ad': 'flatrate'}, {'al': 'flatrate'}, {'ar': 'flatrate'}, {'at': 'flatrate'}, {'au': 'flatrate'}, {'ba': 'flatrate'}, {'be': 'flatrate'}, {'bg': 'flatrate'}, {'bo': 'flatrate'}, {'br': 'flatrate'}, {'bz': 'flatrate'}, {'ca': 'flatrate'}, {'ch': 'flatrate'}, {'cl': 'flatrate'}, {'co': 'flatrate'}, {'cr': 'flatrate'}, {'de': 'flatrate'}, {'dk': 'flatrate'}, {'do': 'flatrate'}, {'ec': 'flatrate'}, {'ee': 'flatrate'}, {'eg': 'flatrate'}, {'es': 'flatrate'}, {'fi': 'flatrate'}, {'fr': 'flatrate'}, {'gb': 'flatrate'}, {'gt': 'flatrate'}, {'hn': 'flatrate'}, {'hr': 'flatrate'}, {'ie': 'flatrate'}, {'is': 'flatrate'}, {'it': 'flatrate'}, {'jm': 'flatrate'}, {'lc': 'flatrate'}, {'li': 'flatrate'}, {'lt': 'flatrate'}, {'lu': 'flatrate'}, {'lv': 'flatrate'}, {'me': 'flatrate'}, {'mk': 'flatrate'}, {'mx': 'flatrate'}, {'ni': 'flatrate'}, {'nl': 'flatrate'}, {'no': 'flatrate'}, {'nz': 'flatrate'}, {'pa': 'flatrate'}, {'pe': 'flatrate'}, {'ph': 'flatrate'}, {'pt': 'flatrate'}, {'py': 'flatrate'}, {'rs': 'flatrate'}, {'se': 'flatrate'}, {'si': 'flatrate'}, {'sm': 'flatrate'}, {'sv': 'flatrate'}, {'tr': 'flatrate'}, {'tt': 'flatrate'}, {'us': 'flatrate'}, {'uy': 'flatrate'}, {'ve': 'flatrate'}]), Provider(Apple TV, regions=[{'au': 'buy'}, {'ca': 'buy'}, {'ca': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'ie': 'buy'}, {'ie': 'rent'}, {'nz': 'buy'}, {'us': 'buy'}, {'us': 'rent'}, {'za': 'buy'}, {'za': 'rent'}]), Provider(Amazon Prime Video, regions=[{'au': 'buy'}, {'be': 'rent'}, {'ca': 'buy'}, {'ca': 'rent'}, {'es': 'buy'}, {'es': 'rent'}, {'fr': 'buy'}, {'fr': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'gg': 'buy'}, {'gg': 'rent'}, {'ie': 'buy'}, {'ie': 'rent'}, {'nz': 'buy'}, {'pl': 'buy'}, {'pl': 'rent'}, {'se': 'rent'}, {'us': 'buy'}, {'us': 'rent'}]), Provider(Google Play Movies, regions=[{'au': 'buy'}, {'ca': 'buy'}, {'es': 'buy'}, {'es': 'rent'}, {'fr': 'buy'}, {'fr': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'hu': 'buy'}, {'hu': 'rent'}, {'ie': 'buy'}, {'ie': 'rent'}, {'nz': 'buy'}, {'pl': 'buy'}, {'pl': 'rent'}, {'sk': 'buy'}, {'sk': 'rent'}, {'ua': 'buy'}, {'ua': 'rent'}, {'us': 'buy'}]), Provider(YouTube, regions=[{'au': 'buy'}, {'ca': 'buy'}, {'fr': 'buy'}, {'fr': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'pl': 'buy'}, {'pl': 'rent'}, {'us': 'buy'}]), Provider(CosmoGo, regions=[{'ca': 'buy'}, {'ca': 'rent'}]), Provider(Crave, regions=[{'ca': 'flatrate'}]), Provider(Crave Amazon Channel, regions=[{'ca': 'flatrate'}]), Provider(Tubi TV, regions=[{'ca': 'ads'}]), Provider(MovistarTV, regions=[{'cl': 'flatrate'}, {'co': 'flatrate'}]), Provider(More TV, regions=[{'ru': 'flatrate'}]), Provider(Fandango At Home, regions=[{'us': 'buy'}, {'us': 'rent'}])]
"""

# If you want to get a specific Provider from a TMDBMovie object, you can call get_provider.
print(movie.get_provider(ProviderName.MOVISTARTV))

"""
Output:  
Provider(MovistarTV, regions=[{'cl': 'flatrate'}, {'co': 'flatrate'}])
"""
```

### get_all_watch_providers
This result of this function is encapsulated in ``get_movie``, but if you want to skip building a full TMDBMovie object and just want a list of Provider objects for a given TMDB ID, you can call ``get_all_watch_providers`` and pass the TMDB ID in as an argument.
```python
from tmdbwrapper.tmdb import TMDBClient

client = TMDBClient("tmdb_api_key")
providers = await client.get_all_watch_providers(14367)
print(providers)

"""
Output:  
[Provider(Disney Plus, regions=[{'ad': 'flatrate'}, {'al': 'flatrate'}, {'ar': 'flatrate'}, {'at': 'flatrate'}, {'au': 'flatrate'}, {'ba': 'flatrate'}, {'be': 'flatrate'}, {'bg': 'flatrate'}, {'bo': 'flatrate'}, {'br': 'flatrate'}, {'bz': 'flatrate'}, {'ca': 'flatrate'}, {'ch': 'flatrate'}, {'cl': 'flatrate'}, {'co': 'flatrate'}, {'cr': 'flatrate'}, {'de': 'flatrate'}, {'dk': 'flatrate'}, {'do': 'flatrate'}, {'ec': 'flatrate'}, {'ee': 'flatrate'}, {'eg': 'flatrate'}, {'es': 'flatrate'}, {'fi': 'flatrate'}, {'fr': 'flatrate'}, {'gb': 'flatrate'}, {'gt': 'flatrate'}, {'hn': 'flatrate'}, {'hr': 'flatrate'}, {'ie': 'flatrate'}, {'is': 'flatrate'}, {'it': 'flatrate'}, {'jm': 'flatrate'}, {'lc': 'flatrate'}, {'li': 'flatrate'}, {'lt': 'flatrate'}, {'lu': 'flatrate'}, {'lv': 'flatrate'}, {'me': 'flatrate'}, {'mk': 'flatrate'}, {'mx': 'flatrate'}, {'ni': 'flatrate'}, {'nl': 'flatrate'}, {'no': 'flatrate'}, {'nz': 'flatrate'}, {'pa': 'flatrate'}, {'pe': 'flatrate'}, {'ph': 'flatrate'}, {'pt': 'flatrate'}, {'py': 'flatrate'}, {'rs': 'flatrate'}, {'se': 'flatrate'}, {'si': 'flatrate'}, {'sm': 'flatrate'}, {'sv': 'flatrate'}, {'tr': 'flatrate'}, {'tt': 'flatrate'}, {'us': 'flatrate'}, {'uy': 'flatrate'}, {'ve': 'flatrate'}]), Provider(Apple TV, regions=[{'au': 'buy'}, {'ca': 'buy'}, {'ca': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'ie': 'buy'}, {'ie': 'rent'}, {'nz': 'buy'}, {'us': 'buy'}, {'us': 'rent'}, {'za': 'buy'}, {'za': 'rent'}]), Provider(Amazon Prime Video, regions=[{'au': 'buy'}, {'be': 'rent'}, {'ca': 'buy'}, {'ca': 'rent'}, {'es': 'buy'}, {'es': 'rent'}, {'fr': 'buy'}, {'fr': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'gg': 'buy'}, {'gg': 'rent'}, {'ie': 'buy'}, {'ie': 'rent'}, {'nz': 'buy'}, {'pl': 'buy'}, {'pl': 'rent'}, {'se': 'rent'}, {'us': 'buy'}, {'us': 'rent'}]), Provider(Google Play Movies, regions=[{'au': 'buy'}, {'ca': 'buy'}, {'es': 'buy'}, {'es': 'rent'}, {'fr': 'buy'}, {'fr': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'hu': 'buy'}, {'hu': 'rent'}, {'ie': 'buy'}, {'ie': 'rent'}, {'nz': 'buy'}, {'pl': 'buy'}, {'pl': 'rent'}, {'sk': 'buy'}, {'sk': 'rent'}, {'ua': 'buy'}, {'ua': 'rent'}, {'us': 'buy'}]), Provider(YouTube, regions=[{'au': 'buy'}, {'ca': 'buy'}, {'fr': 'buy'}, {'fr': 'rent'}, {'gb': 'buy'}, {'gb': 'rent'}, {'pl': 'buy'}, {'pl': 'rent'}, {'us': 'buy'}]), Provider(CosmoGo, regions=[{'ca': 'buy'}, {'ca': 'rent'}]), Provider(Crave, regions=[{'ca': 'flatrate'}]), Provider(Crave Amazon Channel, regions=[{'ca': 'flatrate'}]), Provider(Tubi TV, regions=[{'ca': 'ads'}]), Provider(MovistarTV, regions=[{'cl': 'flatrate'}, {'co': 'flatrate'}]), Provider(More TV, regions=[{'ru': 'flatrate'}]), Provider(Fandango At Home, regions=[{'us': 'buy'}, {'us': 'rent'}])]
"""
```

### get_provider_url
Gets the deep link for the given TMDBMovie object, provider name, and optional region.  
```python
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
```python
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