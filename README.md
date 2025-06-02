# Dorki

A simple, old-school Google dorking tool for the terminal.  
Supports Google, Bing, and GoDuck APIs (if you add your keys), or works with classic scraping if no API keys are set.

---

![dorki](https://github.com/user-attachments/assets/eb64918d-a33f-460a-aa2e-7c43af6700bd)

---

## Features

- Interactive CLI for building Google dork queries
- Supports Google, Bing, and GoDuck APIs (just add your keys in the script)
- Falls back to direct scraping if no API keys are set
- Auto-installs dependencies (`requests`, `fake-useragent`) if missing
- Colorful terminal output and banner

---
## Requirements
   ```sh
   sudo apt install python3-requests python3-fake-useragent
   ```
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
   cp dorki.py /usr/local/bin/dorki
   dorki
   ```
---

## Notes

- If you do **not** add any API keys, the tool will use direct scraping (may be limited or blocked by Google).
- To improve results and avoid scraping limits, add your API keys.
---

