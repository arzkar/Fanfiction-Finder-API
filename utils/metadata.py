import re


from utils.search import get_ao3_url, get_ffn_url
from adapters.adapter_archiveofourown import ArchiveOfOurOwn
from adapters.adapter_fanfictionnet import FanFictionNet

URL_VALIDATE = r"(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"


def ao3_metadata(query):

    if re.search(URL_VALIDATE, query) is None:
        query = query.replace(" ", "+")
        ao3_url = get_ao3_url(query)

    else:  # clean the url if the query contains a url
        ao3_url = re.search(URL_VALIDATE, query).group(0)

    if re.search(r"/works/\b", ao3_url):

        # extract work id from the url
        ao3_works_id = str(re.search(r"\d+", ao3_url).group(0))
        ao3_url = "https://archiveofourown.org/works/"+ao3_works_id

        fic = ArchiveOfOurOwn(ao3_url)
        fic.get_works_metadata()

        if fic.ao3_works_name is None:
            return {
                'status': 'Fanfiction Not Found'
            }

        result = {
            'story_id': fic.ao3_works_id,
            'story_name': fic.ao3_works_name,
            'story_url': fic.BaseUrl,
            'author': fic.ao3_author_name,
            'author_url': fic.ao3_author_url,
            'story_warnings': fic.ao3_works_warnings,
            'story_category': fic.ao3_works_category,
            'story_fandom': fic.ao3_works_fandom,
            'story_relationships': fic.ao3_works_relationships,
            'story_characters': fic.ao3_works_characters,
            'story_additional_tags': fic.ao3_works_additional_tags,
            'story_language': fic.ao3_works_language,
            'story_summary': fic.ao3_works_summary,
            'story_status': fic.ao3_works_status,
            'story_last_updated': fic.ao3_works_last_up,
            'story_published': fic.ao3_works_published,
            'story_length': fic.ao3_works_length,
            'story_chapters': fic.ao3_works_chapters,
            'story_rating': fic.ao3_works_rating,
            'story_kudos': fic.ao3_works_kudos,
            'story_bookmarks': fic.ao3_works_bookmarks,
            'story_comments': fic.ao3_works_comments,
            'story_hits': fic.ao3_works_hits
        }

    elif re.search(r"/series/\b", ao3_url):

        # extract series id from the url
        ao3_series_id = str(re.search(r"\d+", ao3_url).group(0))
        ao3_url = "https://archiveofourown.org/series/"+ao3_series_id

        fic = ArchiveOfOurOwn(ao3_url)
        fic.get_series_metadata()

        if fic.ao3_series_name is None:
            return {
                'status': 'Fanfiction Not Found'
            }

        result = {
            'series_id': fic.ao3_series_id,
            'series_name': fic.ao3_series_name,
            'series_url': fic.BaseUrl,
            'author': fic.ao3_author_name,
            'author_url': fic.ao3_author_url,
            'series_fandom': fic.ao3_series_fandom,
            'series_summary': fic.ao3_series_summary,
            'series_status': fic.ao3_series_status,
            'series_last_updated': fic.ao3_series_last_up,
            'series_begun': fic.ao3_series_begun,
            'series_length': fic.ao3_series_length,
            'series_bookmarks': fic.ao3_series_bookmarks,
            'series_total_works': fic.ao3_series_works,
            'series_works_index': fic.ao3_series_works_index

        }
    else:
        result = {
            'status': 'Fanfiction Not Found'
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

    fic = FanFictionNet(ffn_url)
    fic.get_story_metadata()

    if fic.ffn_story_name is None:
        return {
            'status': 'Fanfiction Not Found'
        }

    result = {
        'story_id': fic.ffn_story_id,
        'story_name': fic.ffn_story_name,
        'story_url': fic.BaseUrl,
        'author': fic.ffn_author_name,
        'author_id': fic.ffn_author_id,
        'author_url': fic.ffn_author_url,
        'story_fandom': fic.ffn_story_fandom,
        'story_summary': fic.ffn_story_summary,
        'story_rating': fic.ffn_story_rating,
        'story_language': fic.ffn_story_lang,
        'story_genre': fic.ffn_story_genre,
        'story_characters': fic.ffn_story_characters,
        'story_status': fic.ffn_story_status,
        'story_last_updated': fic.ffn_story_last_updated,
        'story_published': fic.ffn_story_published,
        'story_length': fic.ffn_story_length,
        'story_chapters': fic.ffn_story_chapters,
        'story_reviews': fic.ffn_story_reviews,
        'story_favs': fic.ffn_story_favs,
        'story_follows': fic.ffn_story_follows
    }

    return result
