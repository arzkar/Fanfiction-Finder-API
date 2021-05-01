import re
from bs4 import BeautifulSoup
import cloudscraper
import time

from utils.search import get_ao3_url, get_ffn_url
from utils.processing import ffn_process_details, ao3_convert_chapters_to_works
from utils.ao3_metadata_processing import ao3_metadata_works, ao3_metadata_series

URL_VALIDATE = r"(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"


def ao3_metadata(query):

    if re.search(URL_VALIDATE, query) is None:
        query = query.replace(" ", "+")
        ao3_url = get_ao3_url(query)

    else:  # clean the url if the query contains a url
        ao3_url = re.search(URL_VALIDATE, query).group(0)

    if re.search(r"/chapters/\b", ao3_url) is not None:

        ao3_url = ao3_convert_chapters_to_works(
            ao3_url)  # convert the url from /chapters/ to /works/

        ao3_story_name, ao3_author_name, ao3_author_url, ao3_story_summary, \
            ao3_story_status, ao3_story_last_up, ao3_story_published, \
            ao3_story_length, ao3_story_chapters, ao3_story_rating,\
            ao3_story_fandom, ao3_story_relationships, ao3_story_characters, \
            ao3_story_additional_tags, ao3_story_language, ao3_story_kudos, \
            ao3_story_bookmarks, ao3_story_comments, ao3_story_hits, \
            ao3_story_warnings, ao3_story_category = ao3_metadata_works(
                ao3_url)

    elif re.search(r"/works/\b", ao3_url) is not None:

        ao3_story_name, ao3_author_name, ao3_author_url, ao3_story_summary,\
            ao3_story_status, ao3_story_last_up, ao3_story_published, \
            ao3_story_length, ao3_story_chapters, ao3_story_rating, \
            ao3_story_fandom, ao3_story_relationships, ao3_story_characters, \
            ao3_story_additional_tags, ao3_story_language, ao3_story_kudos, \
            ao3_story_bookmarks, ao3_story_comments, ao3_story_hits, \
            ao3_story_warnings, ao3_story_category = ao3_metadata_works(
                ao3_url)

    elif re.search(r"/series/\b", ao3_url) is not None:

        ao3_series_name, ao3_author_name, ao3_author_url, ao3_series_summary, \
            ao3_series_status, ao3_series_last_up, ao3_series_begun, \
            ao3_series_length, ao3_series_works_index, ao3_series_works, \
            ao3_series_bookmarks, ao3_series_fandom = ao3_metadata_series(
                ao3_url)

        # remove everything after &sa from the url
        if re.search(r"^(.*?)&", ao3_url) is not None:
            ao3_url = re.search(
                r"^(.*?)&", ao3_url).group(1)

        ao3_series_id = (re.search(r"\d+", ao3_url)).group(0)

        result = {
            'series_id': ao3_series_id,
            'series_name': ao3_series_name,
            'series_url': ao3_url,
            'author': ao3_author_name,
            'author_url': ao3_author_url,
            'series_fandom': ao3_series_fandom,
            'series_summary': ao3_series_summary,
            'series_status': ao3_series_status,
            'series_last_updated': ao3_series_last_up,
            'series_begun': ao3_series_begun,
            'series_length': ao3_series_length,
            'series_bookmarks': ao3_series_bookmarks,
            'series_total_works': ao3_series_works,
            'series_works_index': ao3_series_works_index

        }
        return result

    # remove everything after &sa from the url
    if re.search(r"^(.*?)&", ao3_url) is not None:
        ao3_url = re.search(
            r"^(.*?)&", ao3_url).group(1)

    ao3_story_id = (re.search(r"\d+", ao3_url)).group(0)

    result = {
        'story_id': ao3_story_id,
        'story_name': ao3_story_name,
        'story_url': ao3_url,
        'author': ao3_author_name,
        'author_url': ao3_author_url,
        'story_warnings': ao3_story_warnings,
        'story_category': ao3_story_category,
        'story_fandom': ao3_story_fandom,
        'story_relationships': ao3_story_relationships,
        'story_characters': ao3_story_characters,
        'story_additional_tags': ao3_story_additional_tags,
        'story_language': ao3_story_language,
        'story_summary': ao3_story_summary,
        'story_status': ao3_story_status,
        'story_last_updated': ao3_story_last_up,
        'story_published': ao3_story_published,
        'story_length': ao3_story_length,
        'story_chapters': ao3_story_chapters,
        'story_rating': ao3_story_rating,
        'story_kudos': ao3_story_kudos,
        'story_bookmarks': ao3_story_bookmarks,
        'story_comments': ao3_story_comments,
        'story_hits': ao3_story_hits
    }
    return result


def ffn_metadata(query):

    if re.search(URL_VALIDATE, query) is None:
        if re.search(r"ao3\b", query):
            embed = None
            return embed
        query = query.replace(" ", "+")
        ffn_url = get_ffn_url(query)

    else:  # clean the url if the query contains a url
        ffn_url = re.search(
            URL_VALIDATE, query).group(0)

    scraper = cloudscraper.CloudScraper(delay=3, browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False,
        'desktop': True,
    })

    time.sleep(2)
    ffn_page = scraper.get(ffn_url).text
    ffn_soup = BeautifulSoup(ffn_page, 'html.parser')

    try:
        ffn_story_name = ffn_soup.find_all('b', 'xcontrast_txt')[
            0].string.strip()

        ffn_author_name = ffn_soup.find_all(
            'a', {'href': re.compile('^/u/\d+/.')})[0].string.strip()

        ffn_author_url = (ffn_soup.find(
            'div', attrs={'id': 'profile_top'}).find('a', href=True))['href']

        ffn_story_summary = ffn_soup.find_all('div', {
            'style': 'margin-top:2px',
            'class': 'xcontrast_txt'})[0].string.strip()

        ffn_story_fandom = ffn_soup.find(
            'span', attrs={'class': 'lc-left'}).find(
            'a', attrs={'class': 'xcontrast_txt'}).findNext('a').text

        ffn_story_status, ffn_story_last_up, ffn_story_published, \
            ffn_story_length, ffn_story_chapters, ffn_story_reviews, \
            ffn_story_favs, ffn_story_follows, ffn_story_rating, \
            ffn_story_lang, ffn_story_genre, ffn_story_characters = ffn_process_details(
                ffn_soup)

        ffn_story_id = re.search(r"\d+", ffn_url).group(0)
        ffn_author_id = re.search(r"\d+", ffn_author_url).group(0)
        ffn_author_url = "https://www.fanfiction.net"+ffn_author_url

        # remove everything after &sa from the url
        if re.search(r"^(.*?)&", ffn_url) is not None:
            ffn_url = re.search(
                r"^(.*?)&", ffn_url).group(1)

        result = {
            'story_id': ffn_story_id,
            'story_name': ffn_story_name,
            'story_url': ffn_url,
            'author': ffn_author_name,
            'author_id': ffn_author_id,
            'author_url': ffn_author_url,
            'story_fandom': ffn_story_fandom,
            'story_summary': ffn_story_summary,
            'story_rating': ffn_story_rating,
            'story_language': ffn_story_lang,
            'story_genre': ffn_story_genre,
            'story_characters': ffn_story_characters,
            'story_status': ffn_story_status,
            'story_last_updated': ffn_story_last_up,
            'story_published': ffn_story_published,
            'story_length': ffn_story_length,
            'story_chapters': ffn_story_chapters,
            'story_reviews': ffn_story_reviews,
            'story_favs': ffn_story_favs,
            'story_follows': ffn_story_follows
        }

    except IndexError:
        result = {
            'status': 'Connection Error'
        }
    return result
