

class ArticlePreprocessor:
    def preprocess(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return ' '.join([p.text for p in soup.find_all('p')])


