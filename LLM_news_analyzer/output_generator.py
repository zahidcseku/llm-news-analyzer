from LLM_news_analyzer.article_preprocessor import ArticlePreprocessor
from LLM_news_analyzer.article_classifier import ArticleClassifier
from LLM_news_analyzer.article_summarizer import ArticleSummarizer
import json

class OutputGenerator:
    def __init__(self, categories):
        self.preprocessor = ArticlePreprocessor()
        self.classifier = ArticleClassifier(categories)
        self.summarizer = ArticleSummarizer()

    def process(self, urls):
        results = []
        for url in urls:
            text = self.preprocessor.preprocess(url)
            categories = self.classifier.classify(text)
            summary = self.summarizer.summarize(text)
            results.append({
                "url": url,
                "categories": categories,
                "summary": summary
            })
        return json.dumps(results, indent=2)
    


if __name__ == "__main__":
    categories = "politics, sports, finance, technology, entertainment, others"
    preprocessor = OutputGenerator(categories)
    url = "https://www.abc.net.au/news/2024-11-28/melbourne-tram-network-is-largely-inaccessible/104634896"
        
    print(preprocessor.process(urls=[url]))
