import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class ArticleSummarizer:
    """
    To summarize articles using Google's Gemini model.

    Attributes:
        model: An instance of the GenerativeModel from Google Generative AI.
    """
    def __init__(self):
        """
        Initializes the ArticleSummarizer by loading the Gemini model.

        Raises:
            Exception: If there is an issue initializing the model.
        """

        # initilize the logger
        self.logger = logging.getLogger(__name__)

        try:
            self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        except Exception as e:
            raise Exception(f"Failed to initialize the model: {e}")
        

    def summarize(self, text, max_words=50):
        """
        Summarizes the given text.

        Args:
            text (str): The article text to summarize.

        Returns:
            str: The summary of the article.

        Raises:
            ValueError: If the input text is empty or only contains whitespace.
            Exception: If there is an issue generating content from the model.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or whitespace.")
        
        prompt = f"Please summarize the following text in no more than {max_words} words:\n\n{text}"
        
        try:
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            return summary
        except Exception as e:
            self.logger.error(f"Error in generating summary from model: {e}")
            raise

if __name__ == "__main__":
    from article_preprocessor import ArticlePreprocessor
    
    preprocessor = ArticlePreprocessor()
    url = "https://www.abc.net.au/news/2024-11-28/melbourne-tram-network-is-largely-inaccessible/104634896"
    article_text = preprocessor.preprocess(url)
    
    summarizer = ArticleSummarizer()
    try:
        summary = summarizer.summarize(article_text)
        print("Summary:", summary)
    except Exception as e:
        print(f"An error occurred: {e}")