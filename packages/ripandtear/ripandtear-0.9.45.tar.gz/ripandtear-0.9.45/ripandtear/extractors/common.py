import httpx
import logging
import re
import os

from datetime import datetime
from urllib.parse import urlparse
import time

from ripandtear.utils.custom_types import UrlDictionary
from ripandtear.utils import rat_info
from ripandtear.utils.tracker import Tracker
from ripandtear.utils.file_extension_corrector import find_extension

log = logging.getLogger(__name__)


class Common():

    def __init__(self):
        self.common_headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

        self.tracker = Tracker.getInstance()

    def common_filename_creator(self, url_dictionary: UrlDictionary) -> str:
        '''
        Builds out the general standard filename format. It adds receives the information from
        url_dictionary and adds it to the filename string where appropriate. The standard format is:

        prefix-date_uploaded-album_name-count-id-description.ext

        prefix - name of the website
        date_uploaded - if a datetime from when it is uploaded is provided it is added
        album - add the album name the file belongs to (if it applies)
        count - applies if the file is apart of an album. Tries to keep the files in order
        name - name of the file. usually the id from the the url
        description - usually the title given to the file from the orignal site it was uploaded
        to. typically a sentence
        extension - the extension of the file
        '''
        # Template of all information that should be passed
        # in the url_dictionary. Copy and past into the extractor

        # if 'prefix' in url_dictionary:
        #     prefix = url_dictionary['prefix']
        # else:
        #     prefix = self.prefix
        #
        # if 'album_name' in url_dictionary:
        #     album_name = url_dictionary['album_name']
        # else:
        #     album_name = None
        #
        # if 'count' in url_dictionary:
        #     count = url_dictionary['count']
        # else:
        #     count = None
        #
        # if 'description' in url_dictionary:
        #     description = url_dictionary['description']
        # else:
        #     description = None
        #
        # url_dictionary['name'] = name
        # url_dictionary['date'] = date
        # url_dictionary['url_to_download'] = url_to_download
        # url_dictionary['url_to_record'] = url_to_record
        # url_dictionary['file_size'] = file_size
        # url_dictionary['extension'] = extension
        # url_dictionary['filename'] = self.common_filename_creator(url_dictionary.copy())

        filename = ''

        if url_dictionary.get('prefix'):
            filename += f"{url_dictionary['prefix']}-"

        if url_dictionary.get('date'):
            dt = datetime.fromtimestamp(
                url_dictionary['date']).strftime('%Y-%m-%d')
            filename += f"{dt}-"

        if url_dictionary.get('album_name'):
            filename += f"{url_dictionary['album_name']}-"

        if url_dictionary.get('count'):
            filename += f"{url_dictionary['count']:03}-"

        if url_dictionary.get('name'):
            filename += f"{url_dictionary['name']}"

        if url_dictionary.get('description'):
            filename += f"-{url_dictionary['description']}"

        valid_characters = '-_.,() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        filename = ''.join(
            c for c in filename if c in valid_characters)

        filename = filename.replace('\n', '  ').replace(
            '\r', '  ').replace('--', '-')

        filename = re.sub(r'\s+', ' ', filename)

        if len(str(filename)) > 220:
            filename = filename[:220]

        extension = self.common_find_extension(
            url_dictionary['extension']).lower()

        filename += f".{extension.lower()}.part"

        return filename

    def common_find_extension(self, extension: str) -> str:

        return find_extension(extension)

    def common_find_url_extension(self, url: str) -> str:
        path = urlparse(url)
        extension = os.path.splitext(path.path)[1].replace('.', '')
        return extension

    async def common_generic_downloader(self, url: str) -> None:

        response = httpx.get(url, verify=False)

        # print(response.headers)
        file_size: int = int(response.headers.get('content-length', 1))
        filename: str = url.split('/')[-1]

        url_dictionary: UrlDictionary = {}
        url_dictionary['url_to_download'] = url
        url_dictionary['filename'] = filename
        url_dictionary['file_size'] = file_size
        url_dictionary['response'] = response

        await downloader.download_file(url_dictionary.copy())

    async def common_get_epoch_time(self, date: str) -> int:

        file_creation_date = datetime.strptime(
            (date), "%a, %d %b %Y %H:%M:%S %Z")

        epoch_time = time.mktime(file_creation_date.timetuple())

        return epoch_time

    async def common_get_time(self):

        test = datetime.now().strftime("%H:%M:%S")
        print(test)

        return datetime.now().strftime("%H:%M:%S")

    async def common_bad_status_code(self, url_dictionary: UrlDictionary) -> None:

        log.debug("Finding bad status code")
        tracker = Tracker.getInstance()

        if url_dictionary['status_code'] in {401, 403}:

            log.error(f"Authorization Error - {url_dictionary['url']}")

            url_dictionary['fail'] = True
            await tracker.add_url_dictionary(url_dictionary.copy())

            rat_info.add_error_dictionary(url_dictionary.copy())

        elif url_dictionary['status_code'] == 404:

            log.error(
                f"Content was deleted or did not exist: {url_dictionary['status_code']} - {url_dictionary['url']}")

            url_dictionary['fail'] = True
            await tracker.add_url_dictionary(url_dictionary.copy())

            rat_info.add_error_dictionary(url_dictionary.copy())

        elif url_dictionary['status_code'] == 429:

            log.error(f"{url_dictionary['status_code']}: Too Many Requests")

            url_dictionary['fail'] = True
            await tracker.add_url_dictionary(url_dictionary.copy())

            rat_info.add_error_dictionary(url_dictionary.copy())

        elif 500 <= url_dictionary['status_code'] < 600:

            log.error(
                f"500 error. Saving the url to be attempted later: {url_dictionary['status_code']} - {url_dictionary['url']}")

            url_dictionary['fail'] = True
            await tracker.add_url_dictionary(url_dictionary.copy())

            rat_info.add_error_dictionary(url_dictionary.copy())

        else:
            log.error(
                f"Unable to download {url_dictionary['status_code']}: {url_dictionary['url']}")

    async def common_failed_attempt(self, url_dictionary: UrlDictionary) -> None:

        url_dictionary['fail'] = True
        await self.tracker.add_url_dictionary(url_dictionary.copy())
        await self.common_advance_search_count(url_dictionary.copy())

    async def common_advance_search_count(self, url_dictionary: UrlDictionary) -> None:

        url_dictionary['progress']['search_object'].advance(
            url_dictionary['progress']['search_id'], 1)
