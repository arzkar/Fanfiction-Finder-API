<h1 align="center">Fanfiction Finder API</h1>

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This API can scrape both [ffnet](https://www.fanfiction.net/) and [ao3](https://archiveofourown.org/) fanfiction metadata. Currently it can search for ao3 works, series and ffnet stories. <br>

# Hosting

- Install all the dependencies using `pip install -r requirements.txt`
- Then run `main.py` and the API will be accessible at `0.0.0.0:5000`. See the examples below.

# API Usage

To search using the API, you need to host the API in your server. I will use localhost for the examples below.<br>

## For `ao3 works` searching-

`https://0.0.0.0:5000/search?=ao3 Prince of Slytherin`
<br>
![](https://raw.githubusercontent.com/arzkar/Fanfiction-Finder-API/main/img/ao3_works.png)
<br>

## For `ao3 series` searching-

`https://0.0.0.0:5000/search?=ao3 Prince of Slytherin series`
<br>
![](https://raw.githubusercontent.com/arzkar/Fanfiction-Finder-API/main/img/ao3_series.png)
<br>

## For `ffn story` searching-

`https://0.0.0.0:5000/search?=ffn cadmean victory`
<br>
![](https://raw.githubusercontent.com/arzkar/Fanfiction-Finder-API/main/img/ffn_story.png)
<br>

## For searching using url-

`https://0.0.0.0:5000/search?=https://www.fanfiction.net/s/11446957/1/A-Cadmean-Victory`
<br>
![](https://raw.githubusercontent.com/arzkar/Fanfiction-Finder-API/main/img/url_search.png)
<br>
