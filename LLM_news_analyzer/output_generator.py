from LLM_news_analyzer.article_preprocessor import ArticlePreprocessor
from LLM_news_analyzer.article_classifier import ArticleClassifier
from LLM_news_analyzer.article_summarizer import ArticleSummarizer
import json
import logging

class OutputGenerator:
    """
    Generates processed output for a list of article URLs.

    This class combines article preprocessing, classification, and summarization
    to produce a structured output for each given URL.

    Attributes:
        preprocessor (ArticlePreprocessor): An instance of ArticlePreprocessor.
        classifier (ArticleClassifier): An instance of ArticleClassifier.
        summarizer (ArticleSummarizer): An instance of ArticleSummarizer.
    """

    def __init__(self, categories):
        """
        Initializes the OutputGenerator with specified categories.

        Args:
            categories (str): A string of comma-separated categories for classification.

        Raises:
            ValueError: If categories is empty or not a string.
        """
        if not isinstance(categories, str) or not categories.strip():
            raise ValueError("Categories must be a non-empty string.")
        
        self.preprocessor = ArticlePreprocessor()
        self.classifier = ArticleClassifier(categories)
        self.summarizer = ArticleSummarizer()

        # Set up basec logger
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"OutputGenerator initialized with categories: {categories}")


    def process(self, urls):
        """
        Process a list of URLs to generate classified and summarized output.

        Args:
            urls (list): A list of URL strings to process.

        Returns:
            str: A JSON string containing the processed results for each URL.

        Raises:
            ValueError: If urls is not a list or is empty.
            Exception: If there's an error processing any URL.
        """
        if not isinstance(urls, list) or not urls:
            raise ValueError("URLs must be provided as a non-empty list.")

        self.logger.info(f"Starting to process {len(urls)} URLs")

        results = []
        for url in urls:
            try:
                self.logger.info(f"Processing URL: {url}")
                text = self.preprocessor.preprocess(url)
                categories = self.classifier.classify(text)
                summary = self.summarizer.summarize(text)
                results.append({
                    "url": url,
                    "categories": categories,
                    "summary": summary
                })
                self.logger.info(f"Successfully processed URL: {url}")
            except Exception as e:
                self.logger.error(f"Error processing URL {url}: {str(e)}")
                results.append({
                    "url": url,
                    "error": str(e)
                })
        self.logger.info("Finished processing all URLs")
        
        return json.dumps(results, indent=2)
    


if __name__ == "__main__":
    categories = "politics, sports, finance, technology, entertainment, others"
    preprocessor = OutputGenerator(categories)
    url = "https://www.abc.net.au/news/2024-11-28/melbourne-tram-network-is-largely-inaccessible/104634896"
        
    print(preprocessor.process(urls=[url]))
