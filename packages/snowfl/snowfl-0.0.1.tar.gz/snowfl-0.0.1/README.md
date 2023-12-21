# Snowfl API Python Wrapper

This is an unofficial Python wrapper for the [Snowfl](https://snowfl.com/) API, inspired by the work of [c0dysharma](https://github.com/c0dysharma/snowfl-api). Snowfl is a platform for searching and accessing torrent files. With this wrapper, you can programmatically search for torrents based on your queries and preferences.

## Installation

To use this Snowfl API Python wrapper, you can install it using pip:

```bash
pip install snowfl
```

## Usage

### Initializing Snowfl

Before making API requests, you need to initialize the Snowfl instance by fetching the API key. This key is required to access the Snowfl API.

```python
from snowfl import Snowfl, ApiError, FetchError

snowfl = Snowfl()
try:
    snowfl.initialize()
except ApiError as e:
    print(f"Error initializing Snowfl: {e}")
```

### Searching Snowfl

You can use the `parse` method to search the Snowfl site for torrents. You need to provide a search query, and you can optionally specify various parameters to customize your search.

```python
from pprint import pprint


try:
    query = "JoJo"
    sort = "MAX_SEED"  # Sorting by maximum seeders
    include_nsfw = False  # Exclude NSFW content

    result = snowfl.parse(query, sort=sort, include_nsfw=include_nsfw)
    pprint(result)
except FetchError as e:
    print(f"Error searching Snowfl: {e}")
```

### Configuration

You can customize your search by specifying the following parameters:

-   `query`: The search query you want to use.
-   `sort`: Sorting method for the search results. Available options:
    -   `MAX_SEED`: Sort by decreasing number of seed counts (default).
    -   `MAX_LEECH`: Sort by decreasing number of leech counts.
    -   `SIZE_ASC`: Sort by increasing size per file.
    -   `SIZE_DSC`: Sort by decreasing size per file.
    -   `RECENT`: Sort by recent torrents first.
    -   `NONE`: No sorting (Snowfl default).
-   `include_nsfw`: Include NSFW (Not Safe For Work) content in the search results. Set to `True` to include NSFW content; `False` by default.

### Return Value

The `parse` method returns a dictionary with the following structure:

```python
{
    "status": <HTTP status code>,
    "message": <status message>,
    "data": [<array of objects>]
}
```

### Example Responses

#### Found Something

```python
{
    "status": 200,
    "message": "OK",
    "data": [
        {
            "magnet": "magnet:?xt=urn:btih:F3B5014A2E048E9286163B3A6A9D95942F3D8F3B&tr=udp%3A%2F%2Ftracker",
            "age": "12 months",
            "name": "John Coltrane - Ole Coltrane [V0](Big Papi) Jazz Music",
            "size": "86.92 MB",
            "seeder": 2,
            "leecher": 1,
            "type": "Music",
            "site": "****",
            "url": "https://www.*****.info/John-Coltrane--Ole-Coltrane-[V0](Big-Papi)-Jazz-Music-torrent-4500787.html",
            "trusted": False,
            "nsfw": False
        },
        {
            "magnet": "magnet:?xt=urn:btih:6f1fe981ab6624ef5c235278128c00d1c7ff534e&dn",
            "age": "6 years",
            "name": "John Newman Ft. Calvin Harris Ole MP3 Download, 2016",
            "size": "9.41 MB",
            "seeder": 1,
            "leecher": 0,
            "type": "Music",
            "site": "****",
            "url": "https://www.****.com/file/2742569/john-newman-ft.-calvin-harris-ole-mp3-download-2016/",
            "trusted": False,
            "nsfw": False
        }
    ]
}
```

#### Nothing Found

```python
{
    "status": 200,
    "message": "OK",
    "data": []
}
```

## Conclusion

This Python wrapper allows you to interact with the Snowfl API easily, making it convenient to search for torrents and customize your search preferences. Remember to handle exceptions and errors gracefully when using this wrapper in your applications.
