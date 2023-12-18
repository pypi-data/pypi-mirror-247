import asyncio
import httpx
import logging
import pathlib
import random
import re

from bs4 import BeautifulSoup
from pathlib import Path
from playwright.async_api import async_playwright

from ripandtear.extractors.common import Common
from ripandtear.utils.custom_types import UrlDictionary
from ripandtear.utils.tracker import Tracker

log = logging.getLogger(__name__)

# 'https://cdn.bunkr.ru/2316x3088_6f524042147f7b97c8c6e44ccab72374-jvBZFnON.jpg'
# 'https://i.bunkr.ru/2316x3088_6f524042147f7b97c8c6e44ccab72374-jvBZFnON.jpg'
re_bunkr_image_prefix = re.compile(
    r"(([i\w]+)|(i)|((cdn\w+)|(cdn)))")

# 'https://media-files10.bunkr.ru/2022-06-22-Natalie-Roush---Leggings-Haul-vJBce0DY.mp4'
re_bunkr_media_files = re.compile(
    r"((media-files[\w]+)|(media-files)|(i-kebab|kebab)|(i-taco|taco)|(i-pizza|pizza)|(i-burger|burger)|(i-fries|fries)|(i-meatballs|meatballs)|(i-milkshake|milkshake))")

# 'https://bunkr.su/v/0h1vsyrrw8558lb5agtx4_source-gigzea10.mp4'
re_bunkr_video_href = re.compile(
    r"(/|/[v|d]/)([\w\-_\(\)\.]+)\.(\w+)")

re_bunkr_file_extensions = re.compile(
    r"(zip|rar|7z|txt)")

re_bunkr_video_extensions = re.compile(
    r"(mkv|mp4|webm|mov|mp3)")


# 'https://bunkr.su/a/ouikRoFy'
# 'https://stream.bunkr.ru/v/2022-04-23_Fake-Tan-01-Av9w6Za4.mp4'
re_bunkr_album = re.compile(
    r"(https?://)((bunkr|bunkrr)\.(ru|su|is|la))/a/(\w+)")

# 'https://i.bunkr.ru/2316x3088_6f524042147f7b97c8c6e44ccab72374-jvBZFnON.jpg'
# re_bunkr_single = re.compile(
#     r"(https?://)([\w\-]+\.)?(bunkr\.(ru|la|su|is))(/|/[v|d]/)([\w\-_\(\)\.\%\’]+)\.(\w+)")
re_bunkr_single = re.compile(
    r"(https?://)([\w\-]+\.)?((bunkr|bunkrr)\.(ru|la|su|is))(/[v|d|i]/|/)(.*)(\.)?(\w+)?")

sem = asyncio.Semaphore(4)
sem_picture = asyncio.Semaphore(6)


class Bunkr(Common):

    def __init__(self):
        self.tracker = Tracker.getInstance()

    async def run(self, url_dictionary: UrlDictionary) -> None:

        if re_bunkr_album.match(url_dictionary['url']):

            try:
                log.debug("Found album. Collecting dictionaries")
                await self.album(url_dictionary)

            except TypeError:
                log.exception("TypeError")

                await self.common_failed_attempt(url_dictionary)
                return

        elif re_bunkr_single.match(url_dictionary['url']):

            log.debug(f"Found single media. {url_dictionary}")
            await self.single(url_dictionary)
            return

        else:
            log.info(
                f"Url doesn't match regex patterns {url_dictionary['url']}")

    async def single(self, url_dictionary: UrlDictionary) -> None:

        try:

            if re_bunkr_media_files.search(url_dictionary['url']):

                log.debug(
                    f"Direct media-files found. {url_dictionary['url']}")
                await self.url_dictionary_builder(url_dictionary.copy())
                return

            # 'https://bunkrr.su/i/sxlFBRJH4WIS6'
            elif re_bunkr_single.match(url_dictionary['url']).group(7) is not None and re_bunkr_single.match(url_dictionary['url']).group(6) == "/i/":

                async with sem_picture:
                    try:
                        log.debug("Sending request to get image page html")
                        async with httpx.AsyncClient() as client:
                            html = await client.get(f"{url_dictionary['url']}", timeout=None, follow_redirects=True)

                        soup = BeautifulSoup(
                            html.content, features='html.parser')

                        image_url = soup.find(
                            'div', {'class': 'mb-6'}).find('img').get('src')

                        log.debug("Sending request to get image information")
                        async with httpx.AsyncClient() as client:
                            response = await client.head(f"{image_url}", timeout=None, follow_redirects=True)

                        url_dictionary['name'] = pathlib.Path(re_bunkr_single.match(
                            image_url).group(7)).stem

                        url_dictionary['url_to_download'] = str(image_url)

                        try:
                            url_dictionary['file_size'] = response.headers['Content-Length']

                        except KeyError:
                            log.info(
                                f"No 'Content-Length' found for {response.url}. Link is probably dead. Status Code: {response.status_code}")
                            # url_dictionary['file_size'] = int(0)
                            return

                        url_dictionary['extension'] = response.headers['Content-Type']
                        url_dictionary['filename'] = self.common_filename_creator(
                            url_dictionary.copy())

                        log.debug("Url dictionary built. Sending to tracker")
                        # print(url_dictionary)
                        # return
                        await self.tracker.add_url_dictionary(url_dictionary.copy())
                        await self.common_advance_search_count(url_dictionary.copy())
                        return

                    except Exception as e:
                        log.error(f"Error Downloading Image: {e}")

            # 'https://bunkrr.su/d/Sendnudesx-Bunny-iUPWpUcc.zip'
            elif re_bunkr_single.match(url_dictionary['url']).group(7) is not None and re_bunkr_single.match(url_dictionary['url']).group(6) == "/d/":

                log.debug("File found")
                async with sem_picture:
                    try:
                        log.debug("Sending request to get file page html")
                        async with httpx.AsyncClient() as client:
                            html = await client.get(f"{url_dictionary['url']}", timeout=None, follow_redirects=True)

                        soup = BeautifulSoup(
                            html.content, features='html.parser')

                        file_url = soup.findAll(
                            'div', {'class': 'mb-6'})[1].find('a').get('href')
                        # print(file_url)
                        # return

                        log.debug("Sending request to get file information")
                        async with httpx.AsyncClient() as client:
                            response = await client.head(f"{file_url}", timeout=None, follow_redirects=True)

                        url_dictionary['name'] = pathlib.Path(re_bunkr_single.match(
                            file_url).group(7)).stem

                        url_dictionary['url_to_download'] = str(file_url)

                        try:
                            url_dictionary['file_size'] = response.headers['Content-Length']

                        except KeyError:
                            log.info(
                                f"No 'Content-Length' found for {response.url}. Link is probably dead. Status Code: {response.status_code}")
                            # url_dictionary['file_size'] = int(0)
                            return

                        url_dictionary['extension'] = response.headers['Content-Type']
                        url_dictionary['filename'] = self.common_filename_creator(
                            url_dictionary.copy())

                        log.debug("Url dictionary built. Sending to tracker")
                        # print(url_dictionary)
                        # return
                        await self.tracker.add_url_dictionary(url_dictionary.copy())
                        await self.common_advance_search_count(url_dictionary.copy())
                        return

                    except Exception as e:
                        log.error(f"Error Downloading File: {e}")

            elif re_bunkr_single.match(url_dictionary['url']).group(2) == 'stream.':

                log.debug("Direct stream found")
                async with sem:

                    url = await self.bunkr_stream(url_dictionary)

                    if url is None:
                        return

                    url_dictionary['url'] = str(url)
                    await self.url_dictionary_builder(url_dictionary.copy())
                    return
            elif re_bunkr_single.match(url_dictionary['url']).group(9) is not None and re_bunkr_video_extensions.match(re_bunkr_single.match(url_dictionary['url']).group(9).lower()):

                log.debug("Video page found. Finding url")
                async with sem:
                    await asyncio.sleep(random.randint(1, 4))

                    url = await self.bunkr_stream(url_dictionary)

                    if url is None:
                        return

                    url_dictionary['url'] = str(url)
                    await self.url_dictionary_builder(url_dictionary.copy())
                    return

            # 'https://bunkrr.su/v/4Mp0YbpjmLdwh'
            elif re_bunkr_single.match(url_dictionary['url']).group(7) is not None:

                log.debug("Video page found. Finding url")
                async with sem:
                    await asyncio.sleep(random.randint(1, 4))

                    url = await self.bunkr_stream(url_dictionary)

                    if url is None:
                        return

                    url_dictionary['url'] = str(url)
                    await self.url_dictionary_builder(url_dictionary.copy())
                    return

            elif re_bunkr_image_prefix.match(re_bunkr_single.match(url_dictionary['url']).group(2)):

                if re_bunkr_video_extensions.search(re_bunkr_single.match(url_dictionary['url']).group(7)):

                    log.debug("Direct video found")
                    async with sem:

                        url = await self.bunkr_stream(url_dictionary)

                        if url is None:
                            return

                        url_dictionary['url'] = str(url)
                        await self.url_dictionary_builder(url_dictionary.copy())
                        return

                else:
                    async with sem_picture:
                        log.debug("Direct image found")
                        await self.url_dictionary_builder(url_dictionary.copy())
                        return

            elif re_bunkr_single.match(url_dictionary['url']).group(6) == '/v/':

                log.debug("Video page found. Finding url")
                async with sem:
                    await asyncio.sleep(random.randint(1, 4))

                    url = await self.bunkr_stream(url_dictionary)

                    if url is None:
                        return

                    url_dictionary['url'] = str(url)
                    await self.url_dictionary_builder(url_dictionary.copy())
                    return

            else:
                log.info(
                    f"Given url doesn't match regex pattern {url_dictionary['url']}")
                return

        except AttributeError:
            log.exception(f"Unable to match {url_dictionary['url']}")
            await self.common_failed_attempt(url_dictionary)
            return

        except TypeError:
            log.exception(f"TypeError found for {url_dictionary['url']}")
            await self.common_failed_attempt(url_dictionary)
            return

    async def url_dictionary_builder(self, url_dictionary: UrlDictionary) -> None:

        try:

            log.debug("Sending request")
            async with httpx.AsyncClient() as client:
                response = await client.head(f"{url_dictionary['url']}", timeout=None, follow_redirects=True)

        except httpx.ReadError:
            log.error(
                f"Unable to confirm - {url_dictionary['url']}. Possible 404")

            await self.common_failed_attempt(url_dictionary)
            return

        # if a video is on a server that is under maintenance, the video is
        # redirected to this link. If this link is found then save the url_dictionary
        # to be downloaded later.

        if response.url == 'https://bnkr.b-cdn.net/maintenance.mp4':
            log.info(
                f"Server where content is hosted is under maintenance: {url_dictionary['url']}")

            await self.common_failed_attempt(url_dictionary)
            return

        url_dictionary['name'] = pathlib.Path(re_bunkr_single.match(
            url_dictionary['url']).group(7)).stem

        url_dictionary['url_to_download'] = str(response.url)

        try:
            url_dictionary['file_size'] = response.headers['Content-Length']

        except KeyError:
            log.info(
                f"No 'Content-Length' found for {response.url}. Link is probably dead. Status Code: {response.status_code}")
            # url_dictionary['file_size'] = int(0)
            return

        url_dictionary['extension'] = response.headers['Content-Type']
        url_dictionary['filename'] = self.common_filename_creator(
            url_dictionary.copy())

        log.debug("Url dictionary built. Sending to tracker")
        # print(url_dictionary)
        # return
        await self.tracker.add_url_dictionary(url_dictionary.copy())
        await self.common_advance_search_count(url_dictionary.copy())
        return

    async def album(self, url_dictionary: UrlDictionary) -> None:

        url = f"{url_dictionary['url']}"

        try:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(slow_mo=50)
                page = await browser.new_page()
                log.info(f"Navigating to url: {url_dictionary['url']}")
                await page.goto(url, wait_until='networkidle')

                log.info("Searching for content")

                if await page.query_selector("div.grid") is None:

                    if await page.query_selector("div.grid-images"):

                        small_layout = True
                        content = page.locator("div.grid-images > div")

                    else:
                        log.info(
                            f"Page Layout not recognized: {url_dictionary['url']}")
                        return

                else:
                    small_layout = False
                    content = page.locator("div.grid > div")

                for i in range(await content.count()):
                    if i % 50 == 0:
                        log.info(f"Number of content found: {i}")
                    await content.nth(i).hover()

                if small_layout is True:
                    html = await page.locator('div.grid-images').inner_html()

                else:
                    html = await page.locator('div.grid').inner_html()

                await page.close()
                await browser.close()

                soup = BeautifulSoup(html, features='html.parser')

                if len(soup.find_all('a')) > 0:
                    log.info(
                        f"Found {len(soup.find_all('a'))} pieces of content. Preparing for download...")

                    tasks = []
                    for link in soup.find_all('a'):
                        direct_link = str(link.get('href'))
                        if "bunkrr" not in direct_link or "bunkr" not in direct_link:
                            direct_link = f"https://bunkrr.su{direct_link}"
                        url_dictionary['url'] = direct_link
                        tasks.append(asyncio.create_task(
                            self.run(url_dictionary.copy())))

                    await asyncio.gather(*tasks)
                    return

                else:
                    log.info("No content found")
                    return

        except Exception:
            log.exception(f"Problem Loading {url_dictionary['url']}")
            await self.common_failed_attempt(url_dictionary)
            return

    async def bunkr_stream(self, url_dictionary: UrlDictionary) -> None:

        async with async_playwright() as pw:
            try:

                browser = await pw.chromium.launch()
                context = await browser.new_context(accept_downloads=True)
                # await context.tracing.start(screenshots=True, snapshots=True, sources=True)

                page = await context.new_page()
                response = await page.goto(url_dictionary['url'], wait_until="networkidle")

                if response.status >= 300:
                    log.debug("Bad Status Code")
                    url_dictionary['status_code'] = int(response.status)
                    await self.common_bad_status_code(url_dictionary.copy())
                    await page.close()
                    await context.close()
                    await browser.close()
                    return

                log.info(f"Searching for video: {url_dictionary['url']}")

                await asyncio.sleep(random.randint(3, 8))

                await page.is_visible('source')

                html = await page.locator('video').inner_html()

                soup = BeautifulSoup(html, features='html.parser')

                url = soup.find('source')['src']
                log.debug(f"Found url: {url}")
                return url

            except Exception:
                log.exception("Problem finding url from video page")

                await self.common_failed_attempt(url_dictionary)

            finally:
                await page.close()
                await context.close()
                await browser.close()

    async def bunkr_file(self, url_dictionary: UrlDictionary) -> None:

        async with async_playwright() as pw:
            try:
                browser = await pw.chromium.launch()
                context = await browser.new_context(accept_downloads=True)

                page = await context.new_page()
                await page.goto(url_dictionary['url'])

                log.info("Searching for files")
                await page.wait_for_timeout(3000)

                async with page.expect_download() as download_info:
                    await page.locator(
                        "xpath=/html/body/main/section[3]/div/div/div/div/div[2]/a").click()

                download = await download_info.value
                filename = download.suggested_filename
                destination_path = Path().cwd() / filename

                log.info(f"Downloading: {filename}")
                current_time = await self.common_get_time()
                url_dictionary['progress']['search_message'].add_task(
                    f"{current_time} Bunkr - Downloading {filename}")

                await download.save_as(destination_path)

                log.info(f"Downloaded: {filename}")
                current_time = await self.common_get_time()
                url_dictionary['progress']['search_message'].add_task(
                    f"{current_time} Bunkr - Downloaded {filename}")

            except Exception:
                log.exception("Error downloading file: {file_url}")

                await self.common_failed_attempt(url_dictionary)

            finally:

                await context.close()
                await page.close()
                await browser.close()
