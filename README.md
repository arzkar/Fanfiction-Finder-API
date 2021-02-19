<h1 align="center">Fanfiction Finder API</h1>

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

During the development of my Fanfiction Finder Discord bot, I scraped [ffnet](https://www.fanfiction.net/) and [ao3](https://archiveofourown.org/) for the metadata but I didnt include all the metadata I could scrape since that would make the bot's embed messages very long. So I decided to create an API which could scrape as much metadata as possible.<br>Currently it can search for ao3 works, series and ffnet stories. <br>
The API can be accessed using this- 
https://FanfictionApi.repl.co/search/ <br>
# Bot Usage
To search using the API, first you need to host the API somewhere, I will use localhost as an example.<br>

## For `ao3 works` searching-
`https://127.0.0.1:8000/search/ao3 Harry Potter and the Prince of Slytherin`
<br>
![](https://raw.githubusercontent.com/arzkar/Fanfiction-Finder-API/main/img/ao3_works.png)
<br>
## For `ao3 series` searching-
`https://127.0.0.1:8000/search/ao3 Harry Potter and the Prince of Slytherin series`
<br>
![](https://raw.githubusercontent.com/arzkar/Fanfiction-Finder-API/main/img/ao3_series.png)
<br>

## For `ffn story` searching-
`https://127.0.0.1:8000/search/ffn cadmean victory`
<br>
![](https://raw.githubusercontent.com/arzkar/Fanfiction-Finder-API/main/img/ffn_story.png)
<br>

