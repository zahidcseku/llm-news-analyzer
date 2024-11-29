import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class ArticleClassifier:
    """
    A class to classify articles into predefined categories using Google Generative AI.

    Attributes:
        model: An instance of the GenerativeModel from Google Generative AI.
    """
    def __init__(self, categories: str):
        """
        Initializes the ArticleClassifier by loading the generative model and the 
        predefined categories.

        Raises:
            Exception: If there is an issue initializing the model.
        """
        # Initialize the model
        try:
            self.model = genai.GenerativeModel(model_name="gemini-1.5-flash") 
        except Exception as e:
            raise Exception(f"Failed to initialize the model: {e}")
        
        self.categories = categories
        # initilize the logger
        self.logger = logging.getLogger(__name__)


    def classify(self, text):
        """
        Classifies the given text into one of the predefined categories.

        Args:
            text (str): The article text to classify.

        Returns:
            str: The category of the article, which can be one of the following:
                 politics, sports, finance, technology, entertainment, or others.

        Raises:
            ValueError: If the input text is empty or only contains whitespace.
            Exception: If there is an issue generating content from the model.
        """
        
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty or whitespace.")
        
        # Create a prompt for classification 
        prompt = (
            f"Classify the following article into one of the following categories: "
            f"politics, sports, finance, technology, entertainment, or others.\n\n"
            f"Article: {text}\n"
            f"Category:"
        )
        try:
            # Generate content using the model
            response = self.model.generate_content(prompt)
            
            # Process the response to extract the category
            category = response.text.strip()
            
            # Define valid categories
            valid_categories = self.categories.split(",")
            
            # Check if the returned category is valid; if not, classify as 'others'
            if category.lower() in valid_categories:
                return category
            else:
                return "Sorry I cannot find it!!"
        
        except Exception as e:
            self.logger.error(f"Error generating content from model: {e}")
        

# Example usage
if __name__ == "__main__":
    from article_preprocessor import ArticlePreprocessor
    categories = "politics, sports, finance, technology, entertainment, others"

    classifier = ArticleClassifier(categories)
    preprocessor = ArticlePreprocessor()
    url = "https://www.abc.net.au/news/2024-11-28/melbourne-tram-network-is-largely-inaccessible/104634896"
    article_text = preprocessor.preprocess(url)

    # article_text = "Artificial Intelligence is transforming industries by automating tasks and providing insights."
    categories = classifier.classify(article_text)
    print("Categories:", categories)