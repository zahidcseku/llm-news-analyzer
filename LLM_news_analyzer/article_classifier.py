class ArticleClassifier:
    def __init__(self):
        self.llm = OpenAI(temperature=0)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="Classify the following article into categories: {text}\nCategories:"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def classify(self, text):
        categories = self.chain.run(text)
        return categories.strip().split(', ')