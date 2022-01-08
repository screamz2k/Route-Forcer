# Route-Forcer
Python3 Pentesting Tool to bruteforce for website subdirectories.

![Screenshot at 2022-01-08 17-50-20](https://user-images.githubusercontent.com/78593516/148652581-4bcdb555-0d7b-4aa1-bed9-0496611d8ba0.png)
# Credits
Inspired by the popular Pentesting Tool <a href="https://github.com/OJ/gobuster">Gobuster</a>.

I just wanted to make my own Version of it using Python3.
# Features
- Change Amount of Threads
- Bypass Cloudflare
- Change Useragent, Headers, Authorization, Cookies
- Specify Fileend
# Setup
1. Clone this Repository
2. cd into it
3. python3 route-forcer.py -h
# Usage
```
usage: python3 route-forcer.py -u URL -w Wordlist

required arguments:
  -u URL                Url you want to routeforce.
  -w Wordlist           Path to the wordlist you want to use.

optional arguments:
  -sc Showed Codes [Showed Codes ...]
                        Codes to show in log. [Example=200, 201]
  -ic Ignored Codes [Ignored Codes ...]
                        Codes to ignore in log. [Example=302, 304]
  -c C                  Bypass Cloudflare protected websites.
  -l Log                Path to File where to log the output.
  -t Threads            Set the Amount of Threads . [Default=20]
  -useragent Useragent  Specify your Useragent.
  -headers Headers      Specify your Headers. [Example={'useragent': 'Your-Useragent'}]
  -cookies Cookies      Specify your Cookies. [Example={'fingerprint': '3498353058'}]
  -auth Authorization   Specify your Authorization. [Example={'username': 'Your-Username'}]
  -end Fileend          Set the file-end to append to the words. [Example=php]
```
