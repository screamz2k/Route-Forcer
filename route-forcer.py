
import requests as r
from datetime import datetime
import cloudscraper
from rich.console import Console
import argparse
import json
import time
from threading import Thread
console = Console()
logo = """[blue]██████╗  ██████╗ ██╗   ██╗████████╗███████╗    ███████╗ ██████╗ ██████╗  ██████╗███████╗██████╗ 
██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
██████╔╝██║   ██║██║   ██║   ██║   █████╗█████╗█████╗  ██║   ██║██████╔╝██║     █████╗  ██████╔╝
██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝╚════╝██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  ██╔══██╗
██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗    ██║     ╚██████╔╝██║  ██║╚██████╗███████╗██║  ██║
╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝"""
log = ""
version = 1
found_subs = []
allowed_codes = []
disallowed_codes = []
threads_started = False
threads_alive = True


def check_dir(_url, words, library, useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36", headers=None, auth=None, cookies=None):
    global found_subs
    if headers is None:
        headers = {
            "useragent": useragent
        }
    while not threads_started:
        time.sleep(1)
    for word in words:
        headers = {

        }
        try:
            res = library.get(_url + word, allow_redirects=False,
                            headers=headers, auth=auth, cookies=cookies)
        except:
            try:
                res = library.get(_url + word, allow_redirects=False,
                                headers=headers, auth=auth, cookies=cookies)
            except:
                continue
        code = res.status_code
        if code != 404:
            if str(code) in disallowed_codes:
                continue
            if str(code) not in allowed_codes and allowed_codes != []:
                continue
            if 200 >= code < 300:
                console.print(f"[{code}] /{word} Success", style="green")
            elif 300 >= code < 400:
                console.print(f"[{code}] /{word} Redirection", style="red")
            elif 400 >= code < 500:
                console.print(f"[{code}] /{word} Client Error", style="yellow")
            elif 500 <= code:
                console.print(f"[{code}] /{word} Server Error", style="blue")
            else:
                console.print(f"[{code}] /{word}")
            found_subs.append(f"{code} | /{word} \n")


if __name__ == '__main__':
    console.print(logo, justify="center", style="blue")
    console.print(f"[ Made by github.com/screamz2k | Version {version} ]",
                  justify="center", style="yellow")
    parser = argparse.ArgumentParser(
        usage="python3 route-forcer.py -u URL -w Wordlist")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument("-u", metavar="URL",
                          help="Url you want to routeforce.", required=True)
    required.add_argument("-w", metavar="Wordlist",
                          help="Path to the wordlist you want to use.", required=True)
    optional.add_argument("-sc", nargs="+", metavar="Showed Codes", default=[],
                          help="Codes to show in log. [Example=200, 201]")
    optional.add_argument("-ic", nargs="+", metavar="Ignored Codes", default=[],
                          help="Codes to ignore in log. [Example=302, 304]")
    optional.add_argument(
        "-c", default=False, help="Bypass Cloudflare protected websites.")
    optional.add_argument("-l", metavar="Log", default=None,
                          help="Path to File where to log the output.")
    optional.add_argument("-t" , metavar="Threads", type=int, default=20,
                          help="Set the Amount of Threads . [Default=20]")
    optional.add_argument("-useragent", metavar="Useragent", default=None,
                          help="Specify your Useragent.")
    optional.add_argument("-headers", metavar="Headers", default=None,
                          help="Specify your Headers. [Example={'useragent': 'Your-Useragent'}]")
    optional.add_argument("-cookies", metavar="Cookies", default=None,
                          help="Specify your Cookies. [Example={'fingerprint': '3498353058'}]")
    optional.add_argument("-auth", metavar="Authorization", type=dict, default=None,
                          help="Specify your Authorization. [Example={'username': 'Your-Username'}]")
    optional.add_argument("-end", metavar="Fileend", default=None,
                          help="Set the file-end to append to the words. [Example=php]")
    args = parser.parse_args()
    if args.u[-1] != "/":
        url = args.u + "/"
    else:
        url = args.u
    try:
        r.get(url)
    except r.exceptions.MissingSchema:
        console.print("[Error] The Url is invalid.", style="red")
        exit()
    except r.exceptions.ConnectionError:
        console.print(
            "[Error] Couldnt connect to the url. PLease check your spelling, and if you url is online.", style="red")
        exit()
    except Exception as e:
        console.print(e, style="red")
        exit()
    else:
        console.print("[Success] Url is valid.", style="green")
    try:
        with open(args.w) as f:
            word_list = f.read().splitlines()
    except FileNotFoundError:
        console.print("[Error] The wordlist couldn't be found.", style="red")
        exit()
    except Exception as e:
        console.print(e, style="red")
        exit()
    if args.l is not None:
        console.print(f"[Info] Logging output to '{args.l}'", style="blue")
    if args.t <= 0:
        console.print(f"[Error] Amount of Threads can't be zero.", style="red")
        exit()
    if args.sc != [] and args.ic != []:
        console.print(
            f"[Error] You can only use one option of -nc and -ac", style="red")
        exit()
    allowed_codes = args.sc
    disallowed_codes = args.ic
    if args.headers is not None:
        try: 
            choosen_headers = json.loads(args.headers)
        except:
            console.print(
                f'[Error] Invalid Headers Format.', style="red")
            exit()
    else:
        choosen_headers = None
    if args.cookies is not None:
        try: 
            choosen_cookies = json.loads(args.cookies)
        except:
            console.print(
                f'[Error] Invalid Cookies Format.', style="red")
            exit()
    else:
        choosen_cookies = None
    if args.auth is not None:
        try: 
            choosen_auth = json.loads(args.auth)
        except:
            console.print(
                f'[Error] Invalid Auth Format.', style="red")
            exit()
    else:
        choosen_auth = None
    if args.end is not None:
        for word_i in range(0, len(word_list) - 1):
            if args.e in word_list[word_i]:
                continue
            word_list[word_i] += "." + args.e
    splitted_wordlist = []
    for i in range(0, len(word_list), args.t):
        splitted_wordlist.append(word_list[i:i+args.t])
    threads = []
    if args.c:
        console.print("[Info] Using Cloudflare Bypass.", style="blue")
        cs = cloudscraper.create_scraper()
        console.print("[Info] Starting Threads.", style="blue")
        deb = 0
        for word_packet in splitted_wordlist:
            th = Thread(target=check_dir, kwargs={
                "_url": url, "words": word_packet, "library": cs, "useragent": args.useragent, "headers": choosen_headers, "auth": choosen_auth, "cookies": choosen_cookies})
            threads.append(th)
            th.start()
        console.print(
            "[Success] All Threads started successfully.", style="green")
        threads_started = True
    else:
        console.print("[Info] Starting Threads.", style="blue")
        for word_packet in splitted_wordlist:
            th = Thread(target=check_dir, kwargs={
                "_url": url, "words": word_packet, "library": r, "useragent": args.useragent, "headers": choosen_headers, "auth": choosen_auth, "cookies": choosen_cookies})
            threads.append(th)
            th.start()
        console.print(
            "[Success] All Threads started successfully.", style="green")
        threads_started = True

    while threads_alive:
        alive_threads = 0
        for thread in threads:
            if thread.is_alive():
                alive_threads += 1
        if alive_threads == 0:
            threads_alive = False
    if args.l is not None:
        with open(args.l, "a") as f:
            f.write(f"# Route-Forcer LOG \n[{datetime.now()}]\n{url}\n")
            for sub in found_subs:
                f.write(sub)
