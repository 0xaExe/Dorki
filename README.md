# Dorki

A simple, old-school Google dorking tool for the terminal.  
Supports Google, Bing, and GoDuck APIs (if you add your keys), or works with classic scraping if no API keys are set.

---

## Features

- Interactive CLI for building Google dork queries
- Supports Google, Bing, and GoDuck APIs (just add your keys in the script)
- Falls back to direct scraping if no API keys are set
- Auto-installs dependencies (`requests`, `fake-useragent`) if missing
- Colorful terminal output and banner

---

## Usage

1. **Clone or Download**
   ```sh
   git clone https://github.com/yourusername/Dorki.git
   cd Dorki
  
   ```

2. **(Optional) Add API Keys**

   Open `dorki` in your editor and add your API keys in the `API_KEYS` section at the top:
   ```python
   API_KEYS = {
       "serpapi": "",   # Example: "SERPAPI_KEY_HERE"
       "bing": "",      # Example: "BING_API_KEY_HERE"
       "goduck": ""     # Example: "GODUCK_API_KEY_HERE"
   }
   ```

3. **Run the Tool**
   ```sh
   python3 dorki.py
   ```

   Or make it executable:
   ```sh
   chmod +x dorki.py
   ./dorki.py
   ```

4. **Follow the prompts** to enter your dork fields.

---

## Notes

- If you do **not** add any API keys, the tool will use direct scraping (may be limited or blocked by Google).
- To improve results and avoid scraping limits, add your API keys.
- Dependencies are installed automatically on first run.

---

## Disclaimer

This tool is for educational and research purposes only.  
Use responsibly and respect the terms of service of search engines and APIs.

---

## License

MIT License
