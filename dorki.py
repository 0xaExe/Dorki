#!/usr/bin/env python3

import requests
import os
from pathlib import Path

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def load_config():
    """Load configuration from .env file"""
    config = {
        "serpapi": "",
        "bing": "",
        "goduck": "",
        "debug": False
    }
    
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        if key == "SERPAPI_KEY":
                            config["serpapi"] = value
                        elif key == "BING_API_KEY":
                            config["bing"] = value
                        elif key == "GODUCK_API_KEY":
                            config["goduck"] = value
                        elif key == "DEBUG":
                            config["debug"] = value.lower() in ('true', '1', 'yes')
        except Exception as e:
            print(f"{YELLOW}[!] Warning: Could not read .env file: {e}{RESET}")
    else:
        print(f"{YELLOW}[!] No .env file found. Using empty configuration.{RESET}")
        print(f"{CYAN}[*] Copy .env.example to .env and add your API keys.{RESET}")
    
    return config

# Load configuration
CONFIG = load_config()

# ==== API KEYS SECTION (Deprecated - Use .env file instead) ====
# For backward compatibility, keep this but prefer .env file
API_KEYS = {
    "serpapi": CONFIG["serpapi"] or "",
    "bing": CONFIG["bing"] or "",
    "goduck": CONFIG["goduck"] or ""
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
    print(f"{CYAN}Enter Google Dork fields (leave blank to skip, For multiple terms use OR, quotes for exact phrases):{RESET}")
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
    
    # Build query with proper OR handling
    query_parts = []
    for k, v in dorks.items():
        if v.strip():
            value = v.strip()
            # Handle OR operations properly
            if " OR " in value.upper():
                # Split by OR and format each part
                or_parts = [part.strip() for part in value.split(" OR ") if part.strip()]
                formatted_parts = [f"{k}:{part}" for part in or_parts]
                query_parts.append(f"({' OR '.join(formatted_parts)})")
            else:
                query_parts.append(f"{k}:{value}")
    
    query = " ".join(query_parts)
    return query

def search_google_dork_serpapi(query, api_key):
    headers = {"User-Agent": generate_user_agent()}
    params = {"engine": "google", "q": query, "api_key": api_key}
    print(f"\n{CYAN}[+] Query: {query}{RESET}")
    print(f"{YELLOW}[*] Sending request to SerpAPI...{RESET}")
    try:
        res = requests.get("https://serpapi.com/search", headers=headers, params=params, timeout=30)
        if res.status_code != 200:
            print(f"{RED}[-] API request failed with status code: {res.status_code}{RESET}")
            return
        data = res.json()
        
        # Check for API errors
        if "error" in data:
            print(f"{RED}[-] SerpAPI Error: {data['error']}{RESET}")
            return
            
        if "organic_results" in data and data["organic_results"]:
            print(f"{GREEN}[+] Found {len(data['organic_results'])} results:{RESET}\n")
            for i, result in enumerate(data['organic_results'], start=1):
                title = result.get('title', 'No title')
                link = result.get('link', 'No link')
                snippet = result.get('snippet', '')
                print(f"{CYAN}{i}. {title}")
                print(f"   {link}")
                if snippet:
                    print(f"   {snippet[:100]}...{RESET}\n")
                else:
                    print(f"{RESET}\n")
        else:
            print(f"{RED}[-] No results found.{RESET}")
            if "search_information" in data:
                print(f"{YELLOW}[*] Search took {data['search_information'].get('query_displayed_time', 'unknown')} seconds{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[-] Network error: {e}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")

def search_bing_dork(query, api_key):
    headers = {"Ocp-Apim-Subscription-Key": api_key, "User-Agent": generate_user_agent()}
    params = {"q": query, "count": 10}
    print(f"\n{CYAN}[+] Query: {query}{RESET}")
    print(f"{YELLOW}[*] Sending request to Bing API...{RESET}")
    try:
        res = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params, timeout=30)
        if res.status_code != 200:
            print(f"{RED}[-] Bing API request failed with status code: {res.status_code}{RESET}")
            return
        data = res.json()
        
        if "error" in data:
            print(f"{RED}[-] Bing API Error: {data['error']['message']}{RESET}")
            return
            
        if "webPages" in data and "value" in data["webPages"]:
            print(f"{GREEN}[+] Found {len(data['webPages']['value'])} results:{RESET}\n")
            for i, result in enumerate(data['webPages']['value'], start=1):
                title = result.get('name', 'No title')
                url = result.get('url', 'No URL')
                snippet = result.get('snippet', '')
                print(f"{CYAN}{i}. {title}")
                print(f"   {url}")
                if snippet:
                    print(f"   {snippet[:100]}...{RESET}\n")
                else:
                    print(f"{RESET}\n")
        else:
            print(f"{RED}[-] No results found.{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}[-] Network error: {e}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error: {e}{RESET}")

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

def debug_api_keys():
    """Debug function to check API key configuration"""
    print(f"{CYAN}[DEBUG] API Key Status:{RESET}")
    for provider, key in API_KEYS.items():
        if key.strip():
            masked_key = key[:8] + "..." if len(key) > 8 else "***"
            print(f"{GREEN}  ✓ {provider}: {masked_key}{RESET}")
        else:
            print(f"{RED}  ✗ {provider}: Not set{RESET}")
    print()

if __name__ == "__main__":
    print_banner()
    print(f"{YELLOW}[!] Configure your API keys in the .env file to improve search results.{RESET}")
    
    # Debug API keys
    debug_api_keys()
    
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
