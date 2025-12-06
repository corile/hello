from playwright.sync_api import Page, TimeoutError

def parse_rakuten(page: Page):
    rate_text = None
    terms_and_conditions = None
    print('Inside parse_rakuten')

    # 3. Wait for Dynamic Content to Load (Crucial for JS sites)
    # Wait for an element that indicates the search results have loaded.
    # UPDATED SELECTOR: Using the data-testid attribute and explicitly selecting the first <span> child
    RESULT_RATE_SELECTOR = '[data-testid="online-cash-back"] > span:nth-child(1)'
    try:
        print('Wait up to 5 seconds for the results to appear.')
        page.wait_for_selector(RESULT_RATE_SELECTOR, timeout=5000)
        print("  - Search results loaded successfully.")
    except TimeoutError:
        print("  - TIMEOUT: Search results took too long to load. The search term may not exist or the selector is wrong.")
        return rate_text, terms_and_conditions
    
    # A. Extract the Cashback Rate
    # Use locator() to find the element based on the robust CSS selector
    rate_element = page.locator(RESULT_RATE_SELECTOR)
    if rate_element.count() > 0:
        rate_text = rate_element.inner_text()
    else:
        print("Rate element not found (Selector might be wrong).")
        rate_text = None

    # B. Extract the T&C using the robust inner div selector.
    # This selector targets the content div within the 'merchant-term' container.
    TERMS_AND_CONDITIONS_SELECTOR = 'merchant-term'
    
    terms_element = page.get_by_test_id(TERMS_AND_CONDITIONS_SELECTOR)
    if terms_element.count() > 0:
        # First div in the merchant terms contains the T&C
        # The structure of the content div is:
        # <strong>Exclusions: </strong> Text <br><br> Text <strong>Special Terms: </strong> Text
        first_div = terms_element.locator("div").first
        
        # Playwright's textContent method should handle combining this structure cleanly.
        terms_and_conditions = first_div.text_content()
    else:
        print("Terms and Conditions section content div not found (Selector might be wrong).")
        terms_and_conditions = None

    return rate_text, terms_and_conditions

def parse_topcashback(page: Page):
    rate_text = None
    terms_and_conditions = None
    print('Inside parse_topcashback')

    # 3. Wait for Dynamic Content to Load (Crucial for JS sites)
    RESULT_RATE_SELECTOR = '.merch-logged-out-text__header'
    try:
        print('Wait up to 5 seconds for the results to appear.')
        page.wait_for_selector(RESULT_RATE_SELECTOR, timeout=5000)
        print("  - Search results loaded successfully.")
    except TimeoutError:
        print("  - TIMEOUT: Search results took too long to load. The search term may not exist or the selector is wrong.")
        return rate_text, terms_and_conditions
    
    # A. Extract the Cashback Rate
    # Use locator() to find the element based on the robust CSS selector
    rate_element = page.locator(RESULT_RATE_SELECTOR)
    if rate_element.count() > 0:
        rate_text = rate_element.inner_text()
    else:
        print("Rate element not found (Selector might be wrong).")
        rate_text = None

    # B. Extract the T&C using the robust inner div selector.
    # This selector targets the content div within the 'merchant-term' container.
    TERMS_AND_CONDITIONS_SELECTOR = '.merch-accordion__desc'
    
    terms_element = page.locator(TERMS_AND_CONDITIONS_SELECTOR)
    if terms_element.count() > 0:
        # Playwright's textContent method should handle combining this structure cleanly.
        # Use the .first property (Locator) and then call .text_content().
        # In Playwright Python, .first is a Locator attribute (not callable),
        # so use `.first.text_content()` or `nth(0).text_content()`.
        terms_and_conditions = terms_element.first.text_content()
    else:
        print("Terms and Conditions section content div not found (Selector might be wrong).")
        terms_and_conditions = None

    return rate_text, terms_and_conditions

parser_map = {
    'Rakuten': parse_rakuten,
    'Topcashback': parse_topcashback
}
