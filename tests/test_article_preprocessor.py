import pytest
from unittest.mock import patch, Mock
from bs4 import FeatureNotFound
import requests
from LLM_news_analyzer.article_preprocessor import ArticlePreprocessor  


@pytest.fixture
def preprocessor():
    return ArticlePreprocessor()

def test_preprocess_successful(preprocessor):
    """
    Tests if the preprocessor correctly extracts and concatenates text 
    from paragraph elements when given a valid HTML response.
    """
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = '<html><body><p>Test paragraph 1</p><p>Test paragraph 2</p></body></html>'
        mock_get.return_value = mock_response
        
        result = preprocessor.preprocess('http://example.com')
        
        assert result == 'Test paragraph 1 Test paragraph 2'
        mock_get.assert_called_once_with('http://example.com', timeout=10)


def test_preprocess_request_exception(preprocessor):
    """
    Verifies that the preprocessor returns an empty string when a RequestException occurs during the HTTP request.
    """
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.RequestException('Test error')
        
        result = preprocessor.preprocess('http://example.com')
        
        assert result == ''


def test_preprocess_feature_not_found(preprocessor):
    """
    Checks if the preprocessor handles a FeatureNotFound exception 
    (which could occur if the HTML parser is not available) 
    by returning an empty string.
    """
    with patch('requests.get') as mock_get, \
         patch('bs4.BeautifulSoup') as mock_bs:
        mock_response = Mock()
        mock_get.return_value = mock_response
        mock_bs.side_effect = FeatureNotFound('Test error')
        
        result = preprocessor.preprocess('http://example.com')
        
        assert result == ''


def test_preprocess_unexpected_exception(preprocessor):
    """
    Ensures that the preprocessor gracefully handles any unexpected exceptions by returning an empty string.
    """
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception('Unexpected error')
        
        result = preprocessor.preprocess('http://example.com')
        
        assert result == ''

def test_preprocess_empty_response(preprocessor):
    """
    Verifies that the preprocessor returns an empty string when the HTML 
    response doesn't contain any paragraph elements.
    """
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = '<html><body></body></html>'
        mock_get.return_value = mock_response
        
        result = preprocessor.preprocess('http://example.com')
        
        assert result == ''


def test_preprocess_http_error(preprocessor):
    """
    Tests if the preprocessor correctly handles HTTP errors (like 404 Not Found) by returning an empty string.
    """
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.HTTPError('404 Client Error')
        
        result = preprocessor.preprocess('http://example.com')
        
        assert result == ''