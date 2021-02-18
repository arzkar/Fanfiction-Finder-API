import re
from bs4 import BeautifulSoup
import cloudscraper

from utils.search import get_ao3_id, get_ffn_id
from utils.processing import ffn_process_details, ao3_convert_chapters_to_works
from utils.metadata_processing import ao3_metadata_works, ao3_metadata_series


def ao3_metadata(query):
    if re.search(r"https?:\/\/(www/.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*", query) is None:

        query = query.replace(" ", "+")
        ao3_id = get_ao3_id(query)

        if not ao3_id:
            result = None
            return result

        if ao3_id == 1:
            result = None
            return result

        # if its an ao3 series, get_ao3_id will return the ao3 series url
        if re.search(r"https?:\/\/(www/.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*", ao3_id) is not None:
            ao3_url = ao3_id  # ao3_url was returned inplace of ao3_id
            ao3_series_name, ao3_author_name, ao3_author_url, ao3_series_summary, ao3_series_status, ao3_series_last_up, ao3_series_begun, ao3_series_length, ao3_series_works_index, ao3_series_works, ao3_series_bookmarks = ao3_metadata_series(
                ao3_url)

            result = {
                'series': ao3_series_name,
                'series_url': ao3_url,
                'author': ao3_author_name,
                'author_url': ao3_author_url,
                'series_summary': ao3_series_summary,
                'series_status': ao3_series_status,
                'series_last_updated': ao3_series_last_up,
                'series_begun': ao3_series_begun,
                'series_length': ao3_series_length,
                'series_total_works': ao3_series_works,
                'series_works_index': ao3_series_works_index,
                'series_bookmarks': ao3_series_bookmarks
            }

            return result
        else:
            ao3_url = "https://archiveofourown.org/works/"+''.join(ao3_id)

    else:  # if the query was ao3 url, not get_fic_id needed
        ao3_url = re.search(
            r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*\b", query)
        ao3_url = ao3_url.group()

    if re.search(r"archiveofourown.org/works/\b", ao3_url) is not None:
        ao3_story_name, ao3_author_name, ao3_author_url, ao3_story_summary, ao3_story_status, ao3_story_last_up, ao3_story_published, ao3_story_length, ao3_story_chapters, ao3_story_rating, ao3_story_fandom, ao3_story_relationships, ao3_story_characters, ao3_story_additional_tags, ao3_story_language, ao3_story_kudos, ao3_story_bookmarks, ao3_story_comments, ao3_story_hits = ao3_metadata_works(
            ao3_url)

    elif re.search(r"archiveofourown.org/chapters/\b", ao3_url) is not None:
        ao3_url = ao3_convert_chapters_to_works(
            ao3_url)  # convert the url from /chapters/ to /works/

        ao3_story_name, ao3_author_name, ao3_author_url, ao3_story_summary, ao3_story_status, ao3_story_last_up, ao3_story_published, ao3_story_length, ao3_story_chapters, ao3_story_rating, ao3_story_fandom, ao3_story_relationships, ao3_story_characters, ao3_story_additional_tags, ao3_story_language, ao3_story_kudos, ao3_story_bookmarks, ao3_story_comments, ao3_story_hits = ao3_metadata_works(
            ao3_url)

    elif re.search(r"archiveofourown.org/series/\b", ao3_url) is not None:
        ao3_series_name, ao3_author_name, ao3_author_url, ao3_series_summary, ao3_series_status, ao3_series_last_up, ao3_series_length, ao3_series_works_index, ao3_series_works, ao3_series_bookmarks = ao3_metadata_series(
            ao3_url)

        result = {
            'series': ao3_series_name,
            'series_url': ao3_url,
            'author': ao3_author_name,
            'author_url': ao3_author_url,
            'series_summary': ao3_series_summary,
            'series_status': ao3_series_status,
            'series_last_updated': ao3_series_last_up,
            'series_begun': ao3_series_begun,
            'series_length': ao3_series_length,
            'series_total_works': ao3_series_works,
            'series_works_index': ao3_series_works_index,
            'series_bookmarks': ao3_series_bookmarks
        }
        return result

    result = {
        'story_name': ao3_story_name,
        'story_url': ao3_url,
        'author': ao3_author_name,
        'author_url': ao3_author_url,
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

    if re.search(r"https?:\/\/(www/.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*", query) is None:

        if re.search(r"ao3\b", query):
            result = None
            return result

        query = query.replace(" ", "+")
        ffn_id = get_ffn_id(query)

        if not ffn_id:
            result = None
            return result

        if ffn_id == 1:
            result = None
            return result

        ffn_url = "https://www.fanfiction.net/s/"+''.join(ffn_id)
    else:  # if the query was ffn url, not get_fic_id needed
        ffn_url = query

    # Replace cloudscraper with requests if ffnet cloudflare issue is resolved
    scraper = cloudscraper.create_scraper()
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

        ffn_story_status, ffn_story_last_up, ffn_story_published, ffn_story_length, ffn_story_chapters, ffn_story_reviews, ffn_story_favs, ffn_story_follows, ffn_story_rating = ffn_process_details(
            ffn_soup)

        ffn_author_url = "https://www.fanfiction.net"+ffn_author_url

        result = {
            'title': ffn_story_name,
            'story_url': ffn_url,
            'author': ffn_author_name,
            'author_url': ffn_author_url,
            'story_summary': ffn_story_summary,
            'story_rating': ffn_story_rating,
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
        result = None

    return result