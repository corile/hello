import time
import random
import re
import datetime
from playwright.sync_api import sync_playwright
import response_parser, database

# --- Configuration & Setup ---

# WARNING: Direct scraping of commercial sites is often against their ToS and can lead to IP bans.
# Use this framework ONLY for educational purposes and ensure compliance with site terms.
# Always introduce delays (time.sleep) to mimic human behavior and avoid overloading servers.

# Global variable to hold the browser context and page
BROWSER_CONTEXT = None
PAGE = None
# List of common User-Agents to rotate, which helps avoid simple bot detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
]



def setup_playwright(headless=False):
    """Initializes Playwright and launches the browser."""
    global BROWSER_CONTEXT, PAGE
    
    print("Initializing Playwright...")
    try:
        # Launching Playwright's synchronous API
        p = sync_playwright().start()
        # You can choose 'chromium', 'firefox', or 'webkit'
        BROWSER_CONTEXT = p.chromium.launch(
            headless=headless, 
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled'],
            proxy= {
                'server': "http://geo.iproyal.com:12321",
                'username': "HIonqauCSzVMDdwr",
                'password': "CXIAqiedAoRexv87_country-us"
            })
        PAGE = BROWSER_CONTEXT.new_page()
        
        # Set a random user-agent
        user_agent = random.choice(USER_AGENTS)
        PAGE.set_extra_http_headers({
            'User-Agent': user_agent
        })
        print(f"Using User-Agent: {user_agent}")

        # 3. APPLY DATA OPTIMIZATION ROUTING
        block_unnecessary_resources(PAGE)

        print("Playwright browser launched successfully.")
        return p
    except Exception as e:
        print(f"Error initializing Playwright: {e}")
        print("Ensure you have installed the browser drivers: 'playwright install'")
        exit()

def block_unnecessary_resources(page):
    """
    Sets up Playwright routing to block requests for images, fonts, and media.
    This significantly reduces data usage and often speeds up scraping.
    """
    
    # List of resource types to block
    BLOCKED_RESOURCE_TYPES = ["image", "media", "font"]
    
    def route_handler(route):
        # If the resource type is in our blocked list, abort the request
        if route.request.resource_type in BLOCKED_RESOURCE_TYPES:
            route.abort()
        else:
            # Otherwise, continue with the request normally
            route.continue_()

    # Apply the handler to all routes on the page
    page.route("**/*", route_handler)
    print("  - Data optimization enabled: Blocking images, media, and fonts.")

def close_playwright(p):
    """Closes the browser and stops Playwright."""
    if BROWSER_CONTEXT:
        BROWSER_CONTEXT.close()
    if p:
        p.stop()
    print("Playwright closed.")


def scrape_portal_for_hotel_corporation(search_url, parse_portal_page):
    """
    Navigates a portal, searches for a hotel brand, and attempts to scrape the cashback rate and notes.

    NOTE: The CSS selectors used for search bar, rate, and exclusions are placeholders.
    You MUST inspect the live page for Rakuten and TopCashBack to find the current, correct selectors.
    """
    global PAGE
    
    data = {}

    try:
        # 1. Navigate to the Portal
        PAGE.goto(search_url, wait_until="domcontentloaded")
        print(f"  - Navigated to {search_url}")
        time.sleep(random.uniform(0.9, 3.3)) # Small pause
        PAGE.evaluate(f'window.scrollBy(0, {random.randint(100, 500)});') # Random scroll to mimic user
        time.sleep(random.uniform(0.9, 3.3)) # Small pause after scroll
        PAGE.evaluate(f'window.scrollBy(0, {-random.randint(-100, 300)});') # Scroll a bit more

        rate, tnc = parse_portal_page(PAGE)
        if rate:
            data['rate'] = rate
        if tnc:
            data['terms_and_conditions'] = tnc
    except Exception as e:
        print(f"  - An unexpected error occurred during scraping: {e}")
        return data
    
    # 5. Return Results
    print(f"  - Rate Found: {data.get('rate', 'NOT FOUND')} | Terms and Conditions Extracted: {data.get('terms_and_conditions', 'N/A')[:100]}...")
    return data

def extract_cashback_rate_from_string(rate_string):
    """
    Extracts the numeric cashback rate from a string like '5% Cash Back' or 'Up to 10% Cash Back'.
    Returns the rate as a float, or None if extraction fails.
    """
    match = re.search(r'\d+(?:\.\d+)?(?=%)', rate_string)
    if match:
        return float(match.group(0))
    return 0
# --- Main Execution ---

if __name__ == "__main__":
    PORTAL_URLS = {
        'Marriott': {
            'Rakuten': 'http://www.rakuten.com/shop/marriotthotelsandresorts',
        },
        'IHG': {
            'Topcashback': 'https://www.topcashback.com/ihg/',
            'Rakuten': 'http://www.rakuten.com/shop/ihg',
        },
        'Hilton': {
            'Rakuten': 'http://www.rakuten.com/shop/hilton',
            'Topcashback': 'https://www.topcashback.com/hilton/'
        }
    }

    SCRAPE_FREQUENCY_HOURS = 300
    portal_results = {}
    
    playwright_instance = None
    try:
        # Start Playwright
        playwright_instance = setup_playwright(headless=False) # Run headless for production scraping
        for brand, urls in PORTAL_URLS.items():
            portal_results[brand] = {}
            for portal, url in urls.items():
                print(f"\n--- Scraping {portal} for '{brand}' ---")
                if portal not in response_parser.parser_map:
                    print(f"No parser found for {portal}. Skipping.")
                    continue
                last_seen = database.get_last_seen_time(portal, brand)
                if last_seen is not None and (datetime.datetime.now() - datetime.timedelta(hours=SCRAPE_FREQUENCY_HOURS) < last_seen):
                    print(f'{portal}/{brand} was scraped less than {SCRAPE_FREQUENCY_HOURS} hours ago. Skipping')
                    continue
                portal_results[brand][portal] = scrape_portal_for_hotel_corporation(url, response_parser.parser_map[portal])
                
                # BE POLITE: Wait after each hotel search to avoid rate limiting.
                time.sleep(random.uniform(2, 5)) 

    except Exception as main_e:
        print(f"\nFATAL ERROR in main loop: {main_e}")
    finally:
        # Clean up and close the browser session
        close_playwright(playwright_instance)
    
    print("\n--- Final Summary of Results ---")
    
    for brand, results in portal_results.items():
        print(f"\n{brand}:")
        for portal, data in results.items():
            if 'rate' not in data:
                print(f'Rate not found for {portal}/{brand}. Skip storing to DB')
                continue
            rate = data['rate']
            cashback_rate = extract_cashback_rate_from_string(rate)
            terms_and_conditions = data.get('terms_and_conditions', 'NOT FOUND')
            print(f"  > {portal}: Rate: {rate}, parses as {cashback_rate}%, Terms and Conditions: {terms_and_conditions[:100]}...")
            database.save_row_portal_cashback_without_commit(portal, brand, cashback_rate, terms_and_conditions)

    database.commit_all_and_close() 
    print("\nScraping finished!")