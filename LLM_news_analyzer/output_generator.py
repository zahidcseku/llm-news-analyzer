
class ArticleProcessor:
    def __init__(self):
        self.preprocessor = ArticlePreprocessor()
        self.classifier = ArticleClassifier()
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