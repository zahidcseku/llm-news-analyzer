import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


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
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join([p.text for p in soup.find_all('p')])


