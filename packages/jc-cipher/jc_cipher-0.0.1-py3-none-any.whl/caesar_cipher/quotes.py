import requests, random
from bs4 import BeautifulSoup as bs

from caesar_cipher \
import offline_quotes as oq

try:
    # Run program even if these dependencies (requests_cache, langid) are not installed
    import requests_cache, langid
    requests_cache.install_cache('goodreads_cache', backend='sqlite', expire_after=604800) # Cache will expire after 1 week
    lang_checker = True
except :
    pass


# Url for Julius Caesar quotes
url = "https://www.goodreads.com/work/quotes/2796883-the-tragedie-of-julius-c-sar"

# Set headers browser request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# Set timeout to 1 seconds
timeout = 1

def quote():
    """Returns Julius Caesar from good reads or offline quotes if resonse from url fails"""
    # Create a list to store the quotes
    quotes = []

    try:
        # Get response for url
        response = requests.get(url, headers=headers)  
        
        # Parse the HTML content of the page
        soup = bs(response.text, 'html.parser')
        

        response = requests.get(url, headers=headers, timeout=timeout) 
        if response.ok:
            # Parse the HTML content of the page
            soup = bs(response.text, 'html.parser')

            # Find the next page and select the maximum number of pages as text in previous sibling
            next_page_element = soup.find('a', class_='next_page')
            max_page = int(next_page_element.find_previous_sibling('a').text)

            # Choose a random page number
            page_number = random.choice(range(1, max_page)) 

            # Make page url
            page_url = f"{url}?page={page_number}"

            # Extract quotes using BeautifulSoup
            quote_elements = soup.find_all('div', class_='quoteText')

            # Extract and add quotes to the quotes list
            for quote_element in quote_elements:
                # Exclude text from elements with the class "authorOrTitle"
                author_title_elements = quote_element.find_all(class_='authorOrTitle')
                for element in author_title_elements:
                    element.decompose()

                # Extract quote text, replace line breaks with space, remove trailing whitespace and "-"
                quote_text = quote_element.text.replace('\n', ' ').lstrip()

                # Remove the last 16 characters from quote_text, that is "        ―       "
                quote_text = quote_text[:-16]                

                # Check language of quote_text
                if lang_checker: 
                    lang, _ = langid.classify(quote_text)
                else: 
                    lang = "unknown"

                # Add to quotes set if not too long, <=100 and language is english or unknown
                if len(quote_text) <= 100 and lang in {"en", "unknown"}: 
                    quotes.append(quote_text)            
            # print(list(quotes))
                    
        else:
            raise Exception
    except Exception as e:
        # When getting online quotes fail, use offline_quotes
        quotes = oq.quotes
        
        # print(f"Using offline quotes: {e}")
    
    finally:
        # Clean up- close connection            
        if 'response' in locals():
            response.close()

    # Get a random quote
    quote = random.choice(quotes)                
    
    return quote


