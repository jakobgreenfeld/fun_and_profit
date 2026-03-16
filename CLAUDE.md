# CLAUDE.md - Codebase Documentation for AI Assistants

## Repository Overview

This repository contains a collection of web scraping scripts designed to extract data from various websites and APIs. The project name "fun_and_profit_webscrape" reflects its educational and practical purpose - demonstrating various web scraping techniques and patterns.

**Primary Purpose**: Educational web scraping examples showing different approaches to data extraction including:
- API scraping (REST & GraphQL)
- HTML parsing
- Sitemap extraction
- RSS feed parsing
- Search result scraping
- JavaScript-rendered content handling

## Codebase Structure

```
fun_and_profit_webscrape/
├── .gitignore                          # Python standard gitignore
├── proxy_controller.py                 # Proxy configuration reference/examples
├── sitemap_scraper.py                  # Utility for XML sitemap parsing
├── *_scraper.py                        # Individual scraper implementations
└── *.csv                               # Output data files (scraped results)
```

### File Categories

**Utility Modules**:
- `proxy_controller.py` - Proxy setup examples (rotating proxies, ScraperAPI, ScrapingBee)
- `sitemap_scraper.py` - XML sitemap parsing utilities

**Scraper Scripts** (standalone executables):
- `yc_scraper.py` - Y Combinator company data (Algolia API)
- `messari_scraper.py` - Cryptocurrency data (Algolia + GraphQL)
- `pitchbook_scraper.py` - Company profiles (HTML + sitemap + multiprocessing)
- `goodreads_scraper.py` - Quote scraping with pagination
- `shopify_scraper.py` - E-commerce product data (JSON API)
- `rss_scraper.py` - RSS feed parsing (news, jobs)
- `javascript_scraper.py` - JavaScript-rendered content (requests-html)
- `udemy_scraper.py` - Course data
- `rallyrd_scraper.py` - Investment platform data
- `search_scraper.py` - Search engine result scraping
- `scrapemysite_scraper.py` - General-purpose scraping

**Data Files**:
- All `.csv` files contain scraped output data
- Generally not version-controlled in production (educational examples here)

## Dependencies

### Core Libraries Used

**HTTP & Web**:
- `requests` - HTTP requests (used in all scrapers)
- `requests-html` - JavaScript rendering capabilities
- `BeautifulSoup` (bs4) - HTML parsing
- `feedparser` - RSS/Atom feed parsing

**Data Processing**:
- `pandas` - Data manipulation and CSV export
- `multiprocessing` - Parallel scraping operations

**Configuration**:
- `python-dotenv` - Environment variable management

**Standard Library**:
- `xml.etree.ElementTree` - XML parsing
- `gzip`, `io` - Compressed sitemap handling
- `string` - Character set generation for search queries

### Installation

No `requirements.txt` exists yet. Based on code analysis, create one with:

```txt
requests
requests-html
beautifulsoup4
pandas
feedparser
python-dotenv
```

Install with: `pip install -r requirements.txt`

## Configuration & Environment

### Environment Variables

All scrapers use `.env` file for configuration (gitignored):

```bash
# .env file structure
PROXY=http://username:password@proxy-host:port/
```

**Pattern**: Every scraper loads environment variables using:
```python
import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {
    "http": PROXY,
    "https": PROXY
}
```

### Proxy Configuration

Three proxy patterns demonstrated in `proxy_controller.py`:

1. **Rotating Proxies** (Webshare):
   ```python
   PROXY = "http://username-rotate:password@p.webshare.io:80/"
   ```

2. **ScraperAPI** (API-based):
   ```python
   url = f'http://api.scraperapi.com?api_key={API_KEY}&url={target_url}'
   ```

3. **ScrapingBee** (Premium features):
   ```python
   # Supports JS rendering, country selection, etc.
   ```

**Convention**: Most scrapers accept but don't require proxies (graceful degradation).

## Common Code Patterns

### Pattern 1: Basic Scraper Structure

```python
# Standard imports
import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {"http": PROXY, "https": PROXY}

import requests
import pandas as pd
from bs4 import BeautifulSoup

# Scraping function
def scrape_data(url):
    r = requests.get(url, proxies=proxies, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    # ... parsing logic ...
    return results

# Main execution
if __name__ == "__main__":
    results = scrape_data(url)
    df = pd.DataFrame(results)
    df.to_csv("output.csv", index=False)
```

### Pattern 2: API Scraping

**Algolia Search API** (YC, Messari):
```python
# POST to Algolia DSN endpoint
headers = {'accept': 'application/json', ...}
params = {'x-algolia-api-key': 'KEY', ...}
data = '{"requests":[{"indexName":"...","params":"..."}]}'
response = requests.post(ALGOLIA_URL, headers=headers, params=params, data=data)
results = response.json()["results"][0]["hits"]
```

**GraphQL API** (Messari):
```python
json_data = {
    'operationName': 'QueryName',
    'variables': {'slug': slug},
    'query': 'query QueryName($slug: String!) { ... }'
}
response = requests.post(GRAPHQL_URL, headers=headers, json=json_data)
```

**REST API** (Shopify):
```python
url = f"{root_url}/collections/best-sellers/products.json?limit=250"
response = requests.get(url, proxies=proxies)
data = response.json()["products"]
```

### Pattern 3: Pagination Handling

**Page Number Iteration**:
```python
i = 1
while True:
    url = f"https://example.com/quotes?page={i}"
    results = scrape_page(url)
    if results[-30:] == previous_results:  # Duplicate detection
        break
    all_results += results
    i += 1
```

**Alphabetic Iteration** (search exhaustion):
```python
import string
results = []
for letter in string.ascii_letters:
    query_results = search(letter)
    results += query_results
```

### Pattern 4: Multiprocessing

```python
import multiprocessing

def process_item(item):
    # Processing logic
    return result

if __name__ == "__main__":
    items = get_items()
    with multiprocessing.Pool(processes=12) as pool:
        results = pool.map(process_item, items)
    df = pd.DataFrame(results)
    df.to_csv("output.csv", index=False)
```

**Note**: Always use `if __name__ == "__main__":` guard with multiprocessing.

### Pattern 5: Error Handling

**Permissive Try-Except** (common pattern):
```python
details = {}
try:
    details['field'] = soup.find('element').text.strip()
except:
    pass  # Field remains missing
return details
```

**Convention**: Scripts prioritize data collection over strict error reporting.

## Scraping Techniques

### 1. HTML Parsing (BeautifulSoup)
- **Files**: `goodreads_scraper.py`, `pitchbook_scraper.py`
- **Use Case**: Static HTML content
- **Pattern**: CSS selectors, class/tag finding

### 2. API Scraping
- **Files**: `yc_scraper.py`, `messari_scraper.py`, `shopify_scraper.py`
- **Use Case**: Public APIs (often discovered via browser DevTools)
- **Pattern**: Replicate browser requests with proper headers

### 3. Sitemap Extraction
- **Files**: `sitemap_scraper.py`, `pitchbook_scraper.py`
- **Use Case**: Discovering all pages on a site
- **Pattern**: Parse XML sitemaps, handle gzipped sitemaps

### 4. RSS Feed Parsing
- **Files**: `rss_scraper.py`
- **Use Case**: News, job listings, blog posts
- **Pattern**: feedparser library with proxy support

### 5. Search Result Scraping
- **Files**: `pitchbook_scraper.py` (DuckDuckGo method)
- **Use Case**: Discovery via search engines
- **Pattern**: `site:domain.com keyword` queries

### 6. JavaScript Rendering
- **Files**: `javascript_scraper.py`, `proxy_controller.py`
- **Libraries**: `requests-html`
- **Pattern**:
  ```python
  from requests_html import HTMLSession
  session = HTMLSession()
  r = session.get(url)
  r.html.render()  # Executes JavaScript
  ```

### 7. Brute Force Discovery
- **Files**: `pitchbook_scraper.py`
- **Pattern**: Generate all 2-letter/3-letter combinations as search queries
- **Use Case**: Exhaustive URL discovery

## Data Handling Conventions

### Output Format
- **Standard**: CSV files via pandas
- **Naming**: `{source}_scraper.csv` or descriptive names
- **Index**: Always `index=False` when saving

### Data Cleaning
- **Deduplication**: Often by 'slug' or URL
  ```python
  df = df.drop_duplicates(subset=['slug'])
  ```
- **Text Processing**: `.strip()`, `.replace()` for cleaning
- **Structure**: List of dictionaries → DataFrame → CSV

### Field Extraction
```python
details = {}
details["field1"] = extracted_value
details["field2"] = processed_value
results.append(details)
```

**Convention**: Use dictionaries for each record, accumulate in lists.

## Development Workflow

### Running Individual Scrapers

```bash
# 1. Set up environment
echo "PROXY=your_proxy_url" > .env

# 2. Install dependencies
pip install requests beautifulsoup4 pandas python-dotenv

# 3. Run scraper
python yc_scraper.py
```

### Modifying Scrapers

1. **Change target limits**: Look for list slicing (e.g., `[:5]`, `[:4]`)
2. **Adjust concurrency**: Modify `processes=N` in multiprocessing.Pool
3. **Update output**: Change CSV filename in `to_csv()` call
4. **Add fields**: Extend the `details` dictionary in scraping functions

### Testing Approach

- **Limit data first**: Use small slices (`[:5]`) for testing
- **Check output**: Inspect CSV files after each run
- **Proxy testing**: Scripts work with/without proxy configuration
- **Incremental development**: Test parsing before adding multiprocessing

## Key Conventions for AI Assistants

### 1. Code Style
- **Imports**: Group by standard lib, third-party, local
- **Env loading**: Always at top after imports
- **Main guard**: Use `if __name__ == "__main__":` for executable code
- **Indentation**: 4 spaces (Python standard)

### 2. Safety & Ethics
- **Rate limiting**: Consider adding delays for production use
- **Robots.txt**: Not currently checked - should be considered
- **API keys**: Should be in .env, not hardcoded (some examples have placeholders)
- **Data privacy**: Be cautious with scraped personal data

### 3. Error Handling Philosophy
- **Permissive**: Bare `except:` blocks are common (not best practice, but intentional)
- **Continue on error**: Scripts prefer partial data over complete failure
- **No logging**: Errors generally silently skipped (add logging for production)

### 4. When Adding New Scrapers

**Template Structure**:
```python
import os
from dotenv import load_dotenv
load_dotenv()
PROXY = os.getenv('PROXY')
proxies = {"http": PROXY, "https": PROXY}

import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_[target](url):
    """Scrape [description] from [source]"""
    headers = {'User-Agent': 'Mozilla/5.0 ...'}
    r = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')

    results = []
    # ... parsing logic ...
    return results

if __name__ == "__main__":
    data = scrape_[target]("[url]")
    df = pd.DataFrame(data)
    df.to_csv("[target]_scraper.csv", index=False)
```

### 5. Dependencies Management

**When adding new libraries**:
1. Check if similar functionality exists in current dependencies
2. Add to requirements.txt (create if doesn't exist)
3. Document usage in scraper comments

**Current dependency philosophy**: Minimal and focused
- Prefer `requests` over heavy frameworks
- Use `BeautifulSoup` for HTML (not lxml/scrapy)
- `pandas` for all data manipulation

### 6. Multiprocessing Guidelines

- Use only for I/O-bound tasks (network requests)
- Typical pool size: 4-12 processes
- Always include main guard: `if __name__ == "__main__":`
- Test single-threaded first, then add multiprocessing

### 7. API Scraping Best Practices

**Discovery**:
- Use browser DevTools Network tab
- Look for XHR/Fetch requests
- Copy request headers exactly

**Implementation**:
- Replicate headers faithfully
- Include proper referer/origin
- Handle pagination in API responses
- Check for rate limits in response headers

### 8. Output Conventions

- **CSV naming**: `{source}_{description}.csv`
- **No index column**: Always `index=False`
- **Preserve raw data**: Minimal transformation before saving
- **Test files**: Use same names (will overwrite)

## Common Debugging Scenarios

### Issue: Empty Results
1. Check if proxy is required/working
2. Verify headers (especially User-Agent)
3. Check if site structure changed (selectors)
4. Look for API changes (endpoints, parameters)

### Issue: Blocked/403 Errors
1. Add/update User-Agent header
2. Enable proxy configuration
3. Add delays between requests
4. Check for authentication requirements

### Issue: Incomplete Data
1. Review try-except blocks (might be silently failing)
2. Verify CSS selectors match current HTML
3. Check for pagination (might be missing pages)
4. Inspect API response structure

### Issue: Multiprocessing Errors
1. Ensure `if __name__ == "__main__":` guard exists
2. Check function is picklable (no lambdas, local functions)
3. Reduce pool size if resource-constrained
4. Test without multiprocessing first

## Security Considerations

### Current State
- **API Keys**: Some hardcoded (placeholders) - should be in .env
- **Credentials**: Proxy credentials in examples - use environment variables
- **.env file**: Properly gitignored
- **CSV data**: Not gitignored (educational repo - consider for production)

### Recommendations for Production
1. Move all credentials to `.env`
2. Add `.env.example` template
3. Gitignore all `.csv` files
4. Add rate limiting
5. Implement proper logging
6. Add robots.txt checking
7. Include terms of service compliance checks

## File-Specific Notes

### proxy_controller.py
- **Purpose**: Reference/example file showing proxy patterns
- **Not imported**: Serves as documentation
- **Contains**: Example API keys (should be replaced)

### sitemap_scraper.py
- **Purpose**: Reusable utility module
- **Imported by**: pitchbook_scraper.py
- **Functions**: `scrape_sitemap()`, `download_and_extract_gz_file()`
- **Note**: Can be used standalone or imported

### pitchbook_scraper.py
- **Complexity**: Most sophisticated scraper
- **Techniques**: 3 different methods (brute force, search engine, sitemap)
- **Features**: Multiprocessing, module imports
- **Two-phase**: URL discovery → detail scraping

## Testing & Validation

### Quick Test Checklist
```bash
# 1. Check imports
python -c "import requests, bs4, pandas, dotenv"

# 2. Test single scraper
python yc_scraper.py

# 3. Verify output
ls -lh *.csv
head -5 yc_scraper.csv

# 4. Check for errors
# Review any console output
```

### Validation Patterns
- Check record count: `len(results)`
- Print sample: `print(results[0])`
- Verify uniqueness: `df.drop_duplicates()`
- Inspect first/last pages for pagination

## Version Control

### Current Setup
- **Git**: Repository initialized
- **Branch**: Development on feature branch
- **Ignored**: Standard Python + .env files
- **Tracked**: Source code + example CSV files

### Commit Conventions
- Individual scraper additions: "Add [source] scraper"
- Bug fixes: "Fix [issue] in [scraper]"
- Dependencies: "Add [library] for [purpose]"

## Future Enhancements

Potential improvements to suggest:

1. **Dependencies**: Create `requirements.txt`
2. **Documentation**: Add README.md with usage examples
3. **Configuration**: Centralize headers, user-agents
4. **Utilities**: Extract common functions to `utils.py`
5. **Error Handling**: Add proper logging
6. **Testing**: Add unit tests for parsers
7. **Rate Limiting**: Implement request throttling
8. **CLI**: Add argparse for configurable scrapers
9. **Data Validation**: Schema validation for outputs
10. **Async**: Consider aiohttp for better performance

## Quick Reference

### Starting New Scraper
1. Copy template structure (see section 4)
2. Add target URL
3. Implement parsing logic
4. Test with small dataset
5. Add to repository

### Modifying Existing Scraper
1. Read current implementation
2. Test current functionality
3. Make minimal changes
4. Verify output format unchanged
5. Update this documentation if needed

### Common Commands
```bash
# Run scraper
python [name]_scraper.py

# Check output
head [name]_scraper.csv

# Install dependencies
pip install -r requirements.txt

# Set proxy
echo "PROXY=http://user:pass@host:port/" >> .env
```

## AI Assistant Guidelines Summary

When working with this codebase:

1. **Preserve patterns**: Follow existing code style and structure
2. **Test safely**: Use small data limits first ([:5], [:10])
3. **Respect .env**: Never commit credentials
4. **Document changes**: Update this file for significant changes
5. **Consider ethics**: Add rate limiting, respect robots.txt
6. **Validate output**: Always check CSV files after modifications
7. **Error gracefully**: Match existing error handling philosophy
8. **Stay focused**: Each scraper is standalone, minimal dependencies
9. **Explain clearly**: Code comments should explain "why", not "what"
10. **Think production**: Suggest improvements for robustness

---

**Last Updated**: 2025-11-18
**Repository**: fun_and_profit_webscrape
**Python Version**: 3.x (no specific version requirements)
**Status**: Educational/Active Development



Use case for substack marketing ideas:

Here's a summary of what we covered:
1. API Discovery with Browser DevTools

Open DevTools → Network tab → Filter by Fetch/XHR
Interact with the site (search, scroll, paginate)
Watch for JSON responses - those are your hidden APIs
Copy the request details to replicate in Python

2. Substack's Architecture

Archive API: /api/v1/archive?sort=new&limit=50&offset=0
Search API: /api/v1/post/search
Full content is embedded in page HTML inside window._preloads = JSON.parse("...")
Paid content requires authentication via cookies

3. Cookie-Based Authentication

Get cookies from DevTools → Application → Cookies
Key cookies: connect.sid and substack.sid
Add them to your Python requests.Session()

4. Parsing Nested/Escaped JSON

Sometimes JSON is embedded as an escaped string inside another JSON
Need to unescape (\" → ", \\ → \) before parsing
Use regex to extract, then json.loads() to parse

5. Debugging Strategy

When scraping fails, save the raw HTML and inspect it
Check what's actually in the page vs. what you expected
Print intermediate values to trace the problem

6. Rate Limiting & Politeness

Add time.sleep() between requests
Use a proper User-Agent header

The key lesson: websites often have undocumented APIs that are much easier to scrape than parsing HTML directly - you just need to find them using DevTools.
