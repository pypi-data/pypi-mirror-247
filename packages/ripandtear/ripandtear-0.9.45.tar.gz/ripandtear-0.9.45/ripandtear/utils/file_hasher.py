import hashlib
import logging
import os

from ripandtear.utils import rat_info
from ripandtear.utils import file_extension_corrector
from multiprocessing.pool import ThreadPool
from pathlib import Path

log = logging.getLogger(__name__)


async def file_hasher():

    file_extension_corrector.correct_all_file_extensions()

    log.info("Searching for matching files")
    files_to_delete = await finding_duplicates()

    log.info("Deleting duplicate files")
    try:
        for root, dirs, files in os.walk(os.getcwd()):
            for file in files_to_delete:
                if file in files:
                    Path(Path(file).resolve()).unlink()

    except FileNotFoundError:
        pass

    log.info(f"Removed {len(files_to_delete)} files")


async def finding_duplicates():

    files = [file for file in Path().cwd().iterdir() if file.is_file()]
    files_to_delete = []

    # Dict - hash: filename
    file_hashes = rat_info.get_file_hashes()

    no_rat_file = False

    if file_hashes is None:
        no_rat_file = True
        file_hashes = {}

    log.info("Calculating hashes")
    number_of_workers = os.cpu_count()
    with ThreadPool(number_of_workers) as pool:
        files_hash = pool.map(file_hash, files)

    for file in files_hash:

        hash = file[0]
        name = Path(file[1]).name

        # imgur file deleted picture
        if hash == "d835884373f4d6c8f24742ceabe74946":
            files_to_delete.append(name)
            continue

        if name == rat_info.get_rat_name():
            continue

        if '.part' in name:
            continue

        if hash not in file_hashes:
            file_hashes[hash] = name
            continue

        if len(file_hashes[hash]) < len(name):
            files_to_delete.append(file_hashes[hash])
            file_hashes[hash] = name

        elif len(file_hashes[hash]) > len(name):
            files_to_delete.append(name)

        elif len(file_hashes[hash]) == len(name):

            current_file_dashes = file_hashes[hash].count('-')
            new_file_dashes = name.count('-')

            if current_file_dashes < new_file_dashes:
                files_to_delete.append(file_hashes[hash])
                file_hashes[hash] = name

            elif current_file_dashes > new_file_dashes:
                files_to_delete.append(name)

            elif current_file_dashes == new_file_dashes and file_hashes[hash] != name:
                files_to_delete.append(file_hashes[hash])
                file_hashes[hash] = name

    log.info("Returning found hashes")

    if no_rat_file is not True:
        rat_info.update_rat(category_1='file_hashes',
                            category_2=file_hashes)
    return files_to_delete


def file_hash(file):

    buffer_size = 1024 * 1024

    with open(file, 'rb') as file:

        md5 = hashlib.md5()
        while True:
            data = file.read(buffer_size)
            if not data:
                break
            md5.update(data)

        hash = md5.hexdigest()
        return (hash, file.name)
