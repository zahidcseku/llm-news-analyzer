import requests
from bs4 import BeautifulSoup, FeatureNotFound
import logging


class ArticlePreprocessor:
    """
    A class used to preprocess articles from web URLs.

    This class provides functionality to fetch web content from a given URL
    and extract the main text content, typically from paragraph elements.

    Attributes:
        None

    Methods:
        preprocess(url): Fetches and processes the content from a given URL.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def preprocess(self, url):
        """
        Fetches the content of a web page and extracts the text from all paragraph elements.

        This method sends a GET request to the specified URL, parses the HTML content,
        and extracts text from all <p> tags, joining them into a single string.

        Args:
            url (str): The URL of the web page to process.

        Returns:
            str: A string containing the concatenated text content of all paragraph
                 elements found on the page.

        Raises:
            requests.RequestException: If there's an error in fetching the web page.
            bs4.FeatureNotFound: If the HTML parser is not found.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            return ' '.join([p.text for p in soup.find_all('p')])
        except requests.RequestException as e:
            self.logger.error(f"Error fetching URL {url}: {str(e)}")
        except FeatureNotFound as e:
            self.logger.error(f"HTML parser not found: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error processing {url}: {str(e)}")
        
        return ""  # Return an empty string if any error occurs


