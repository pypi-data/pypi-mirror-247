#!/usr/bin/env python3
import mmh3
import codecs
import sys
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from .fingerprints import FINGERPRINTS
from functools import partial
import base64
import ssl
import urllib3
import warnings
warnings.filterwarnings("ignore")

requests.packages.urllib3.disable_warnings()

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
TIMEOUT = 5
CHECK_CERTIFICATE = False

def parse_args():
    parser = argparse.ArgumentParser(
        description="Detect web technologies based on favicon"
    )

    parser.add_argument(
        "url",
        help="URL or file with URLs (per line). "
        "If none then stdin will be used",
        nargs="*",
    )

    parser.add_argument(
        "-a", "--all",
        action="store_true",
        default=False,
        help="Return also results without identified technology"
    )

    parser.add_argument(
        "-j", "--json",
        action="store_true",
        default=False,
        help="Print result in JSON Lines"
    )

    parser.add_argument(
        "-t", "--timeout",
        default=TIMEOUT,
        type=int,
        help="HTTP request timeout in seconds"
    )

    parser.add_argument(
        "-A", "--user-agent",
        default=USER_AGENT,
        help="User Agent to perform requests"
    )

    parser.add_argument(
        "-w", "--workers",
        default=10,
        type=int,
        help="Number of concurrent workers"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="count",
        help="Verbosity",
        default=0
    )

    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    init_log(args.verbose)

    global TIMEOUT
    global USER_AGENT

    TIMEOUT = args.timeout
    USER_AGENT = args.user_agent

    pool = ThreadPoolExecutor(args.workers)
    print_lock = Lock()

    if args.json:
        print_result = partial(print_jsonl, wo_tech=not args.all)
    else:
        print_result = partial(print_grepl, wo_tech=not args.all)

    for line in read_text_targets(args.url):
        url = line
        pool.submit(
            check_url,
            url,
            print_lock,
            print_result
        )


def check_url(url, print_lock, print_result):
    try:
        logger.info("Retrieve URL: %s", url)
        favicon = retrieve_favicon(url)
        favicon_hash = calc_favicon_hash(favicon)
        tech = FINGERPRINTS.get(favicon_hash, "")

        with print_lock:
            print_result(url, tech, favicon_hash)
    except Exception as e:
        logger.info("Error retrieving %s: %s", url, e)
        raise e

def retrieve_favicon(url):
    icon_urls = retrieve_favicon_urls(url)
    primary_url = icon_urls["primary"]

    if primary_url:
        logger.debug("Retrieving primary icon: %s", primary_url)

        if primary_url.startswith("data:image"):
            return extract_image_from_data_url(primary_url)
        else:
            resp = get(primary_url)
            if resp.ok:
                return resp.content

    default_url = icon_urls["default"]

    logger.debug("Retrieving default icon: %s", default_url)
    resp = get(default_url)
    return resp.content

def extract_image_from_data_url(url):
    img_b64 = url.split("base64,")[1]
    return base64.b64decode(img_b64)

def retrieve_favicon_urls(url):
    icon_urls = {
        "default": urljoin(url, "favicon.ico"),
        "primary": "",
    }

    resp = get(url)

    soup = BeautifulSoup(resp.text, "html.parser")

    icon_path = retrieve_link_rel_path(soup, "icon")
    if not icon_path:
        icon_path = retrieve_link_rel_path(soup, "shortcut icon")

    if icon_path:
        icon_urls["primary"] = urljoin(url, icon_path)

    return icon_urls

def retrieve_link_rel_path(soup, rel_name):
    link_soup = soup.find("link", {"rel": rel_name})
    if link_soup:
        try:
            return link_soup["href"]
        except KeyError:
            pass
    return ""

def print_jsonl(url, tech, favicon_hash, wo_tech=False):
    if wo_tech and not tech:
        return

    print(json.dumps({
        "url": url,
        "tech": tech,
        "favicon_hash": favicon_hash
    }))

def print_grepl(url, tech, favicon_hash, wo_tech=False):
    if wo_tech and not tech:
        return
    print(url, tech, favicon_hash)

def init_log(verbosity=0):

    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    else:
        level = logging.WARN

    logging.basicConfig(
        level=logging.ERROR,
        format="%(levelname)s:%(message)s"
    )
    logger.level = level


def calc_favicon_hash(favicon_bytes):
    favicon = codecs.encode(favicon_bytes,"base64")
    return mmh3.hash(favicon)



## To allow old SSL versions
class CustomHttpAdapter (requests.adapters.HTTPAdapter):
    # "Transport adapter" that allows us to use custom ssl_context.

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    if not CHECK_CERTIFICATE:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

def get(url):
    headers = {
        'User-Agent': USER_AGENT
    }
    return get_legacy_session().get(
        url,
        timeout=TIMEOUT,
        headers=headers,
        verify=CHECK_CERTIFICATE
    )


def read_text_targets(targets):
    yield from read_text_lines(read_targets(targets))

def read_targets(targets):
    """Function to process the program ouput that allows to read an array
    of strings or lines of a file in a standard way. In case nothing is
    provided, input will be taken from stdin.
    """
    if not targets:
        yield from sys.stdin

    for target in targets:
        try:
            with open(target) as fi:
                yield from fi
        except FileNotFoundError:
            yield target


def read_text_lines(fd):
    """To read lines from a file and skip empty lines or those commented
    (starting by #)
    """
    for line in fd:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue

        yield line

if __name__ == '__main__':
    exit(main())
