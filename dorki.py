#!/usr/bin/env python3
import sys
import subprocess

def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"\033[91m[!] {pkg} not found, installing...\033[0m")
        try:
            import ensurepip
            ensurepip.bootstrap()
        except Exception:
            pass
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", pkg])
        print(f"\033[92m[+] {pkg} installed.\033[0m")

# Ensure required packages
ensure_package("requests")
ensure_package("fake_useragent")

import requests
import os

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ==== API KEYS SECTION ====
# Add your API keys below. Leave as "" if you don't have one.
API_KEYS = {
    "serpapi": "",   # Example: "SERPAPI_KEY_HERE"
    "bing": "",      # Example: "BING_API_KEY_HERE"
    "goduck": ""     # Example: "GODUCK_API_KEY_HERE"
}
# ==== END API KEYS SECTION ====

def print_banner():
    banner = f"""{GREEN}
██████╗  ██████╗ ██████╗ ██╗  ██╗██╗
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██║
██║  ██║██║   ██║██████╔╝█████╔╝ ██║
██║  ██║██║   ██║██╔══██╗██╔═██╗ ██║
██████╔╝╚██████╔╝██║  ██║██║  ██╗██║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
{RESET}"""
    print(banner)

def generate_user_agent():
    try:
        from fake_useragent import UserAgent
        ua = UserAgent()
        return ua.random
    except Exception:
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

def build_query():
    print(f"{CYAN}Enter Google Dork fields (leave blank to skip , For adding multi words use OR):{RESET}")
    dorks = {
        "site": input(f"{YELLOW}site: {RESET}"),
        "inurl": input(f"{YELLOW}inurl: {RESET}"),
        "intitle": input(f"{YELLOW}intitle: {RESET}"),
        "intext": input(f"{YELLOW}intext: {RESET}"),
        "filetype": input(f"{YELLOW}filetype: {RESET}"),
        "allinurl": input(f"{YELLOW}allinurl: {RESET}"),
        "allintitle": input(f"{YELLOW}allintitle: {RESET}"),
        "allintext": input(f"{YELLOW}allintext: {RESET}"),
        "link": input(f"{YELLOW}link: {RESET}"),
        "numrange": input(f"{YELLOW}numrange: {RESET}"),
        "before": input(f"{YELLOW}before (YYYY-MM-DD): {RESET}"),
        "after": input(f"{YELLOW}after (YYYY-MM-DD): {RESET}"),
        "allinanchor": input(f"{YELLOW}allinanchor: {RESET}"),
        "inanchor": input(f"{YELLOW}inanchor: {RESET}"),
        "allinpostauthor": input(f"{YELLOW}allinpostauthor: {RESET}"),
        "inpostauthor": input(f"{YELLOW}inpostauthor: {RESET}"),
        "related": input(f"{YELLOW}related: {RESET}"),
        "cache": input(f"{YELLOW}cache: {RESET}")
    }
    query = " ".join([f"{k}:{v}" for k, v in dorks.items() if v.strip()])
    return query

def search_google_dork_serpapi(query, api_key):
    headers = {"User-Agent": generate_user_agent()}
    params = {"engine": "google", "q": query, "api_key": api_key}
    print(f"\n{CYAN}[+] Query: {query}{RESET}")
    print(f"{YELLOW}[*] Sending request to SerpAPI...{RESET}")
    res = requests.get("https://serpapi.com/search", headers=headers, params=params)
    data = res.json()
    if "organic_results" in data and data["organic_results"]:
        print(f"{GREEN}[+] Found {len(data['organic_results'])} results:{RESET}\n")
        for i, result in enumerate(data['organic_results'], start=1):
            print(f"{CYAN}{i}. {result.get('title')}\n   {result.get('link')}{RESET}\n")
    else:
        print(f"{RED}[-] No results or error occurred.{RESET}")
        import json
        print(json.dumps(data, indent=2))

def search_bing_dork(query, api_key):
    headers = {"Ocp-Apim-Subscription-Key": api_key, "User-Agent": generate_user_agent()}
    params = {"q": query, "count": 10}
    print(f"\n{CYAN}[+] Query: {query}{RESET}")
    print(f"{YELLOW}[*] Sending request to Bing API...{RESET}")
    res = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    data = res.json()
    if "webPages" in data and "value" in data["webPages"]:
        print(f"{GREEN}[+] Found {len(data['webPages']['value'])} results:{RESET}\n")
        for i, result in enumerate(data['webPages']['value'], start=1):
            print(f"{CYAN}{i}. {result.get('name')}\n   {result.get('url')}{RESET}\n")
    else:
        print(f"{RED}[-] No results or error occurred (Bing).{RESET}")
        import json
        print(json.dumps(data, indent=2))

def search_goduck_dork(query, api_key):
    print(f"{YELLOW}[*] GoDuck API integration not implemented yet.{RESET}")

def search_google_dork_cli(query):
    import re
    from urllib.parse import quote_plus
    headers = {"User-Agent": generate_user_agent()}
    search_url = f"https://www.google.com/search?q={quote_plus(query)}"
    print(f"\n{CYAN}[+] Query: {query}{RESET}")
    print(f"{YELLOW}[*] Fetching results from Google (may be limited or blocked)...{RESET}")
    try:
        res = requests.get(search_url, headers=headers, timeout=10)
        html = res.text
        links = re.findall(r'/url\?q=(https://[^&]+)&', html)
        if links:
            print(f"{GREEN}[+] Found {len(links)} results (raw URLs):{RESET}\n")
            for i, link in enumerate(links[:10], start=1):
                print(f"{CYAN}{i}. {link}{RESET}")
        else:
            print(f"{RED}[-] No results found or blocked by Google.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error fetching results: {e}{RESET}")

def get_api_provider():
    for provider, key in API_KEYS.items():
        if key.strip():
            return provider, key.strip()
    return None, None

if __name__ == "__main__":
    print_banner()
    print(f"{YELLOW}[!] You can add an API key in the script (API_KEYS section) to improve your search results.{RESET}")
    query = build_query()
    if query:
        provider, api_key = get_api_provider()
        if provider == "serpapi":
            search_google_dork_serpapi(query, api_key)
        elif provider == "bing":
            search_bing_dork(query, api_key)
        elif provider == "goduck":
            search_goduck_dork(query, api_key)
        else:
            search_google_dork_cli(query)
    else:
        print(f"{RED}[-] No query provided.{RESET}")