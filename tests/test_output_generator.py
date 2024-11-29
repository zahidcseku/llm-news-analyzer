import pytest
from unittest.mock import patch, MagicMock
import json
from LLM_news_analyzer.output_generator import OutputGenerator

@pytest.fixture
def output_generator():
    return OutputGenerator("politics,sports,finance,technology,entertainment")


def test_output_generator_initialization(output_generator):
    """
    Verifies that the OutputGenerator is correctly initialized. Checks that the object has 
        the required attributes (preprocessor, classifier, summarizer). 
        Ensures the basic setup of the class is correct
    """
    assert isinstance(output_generator, OutputGenerator)
    assert hasattr(output_generator, 'preprocessor')
    assert hasattr(output_generator, 'classifier')
    assert hasattr(output_generator, 'summarizer')


@patch('LLM_news_analyzer.article_preprocessor.ArticlePreprocessor.preprocess')
@patch('LLM_news_analyzer.article_classifier.ArticleClassifier.classify')
@patch('LLM_news_analyzer.article_summarizer.ArticleSummarizer.summarize')
def test_process_valid_urls(mock_summarize, mock_classify, mock_preprocess, output_generator):
    """
    Tests the processing of multiple valid URLs. Mocks the preprocessing, 
    classification, and summarization methods. 
    """
    mock_preprocess.return_value = "Mocked article text"
    mock_classify.return_value = ["technology"]
    mock_summarize.return_value = "Mocked summary"

    urls = ["http://example.com/article1", "http://example.com/article2"]
    result = output_generator.process(urls)

    assert isinstance(result, str)
    result_json = json.loads(result)
    assert len(result_json) == 2
    for item in result_json:
        assert "url" in item
        assert "categories" in item
        assert "summary" in item
    assert mock_preprocess.call_count == 2
    assert mock_classify.call_count == 2
    assert mock_summarize.call_count == 2


def test_process_empty_url_list(output_generator):
    """
    Ensures that an empty URL list raises a ValueError
    """
    with pytest.raises(ValueError, match="URLs must be provided as a non-empty list."):
        output_generator.process([])


@patch('LLM_news_analyzer.article_preprocessor.ArticlePreprocessor.preprocess')
def test_process_invalid_url(mock_preprocess, output_generator):
    """
    Simulates processing an invalid URL. 
    """
    mock_preprocess.side_effect = Exception("Invalid URL")

    urls = ["http://invalid.url"]
    result = output_generator.process(urls)

    result_json = json.loads(result)
    assert len(result_json) == 1
    assert "error" in result_json[0]
    assert "Invalid URL" in result_json[0]["error"]

def test_invalid_categories():
    """
    Tests the initialization of OutputGenerator with invalid categories
    """
    with pytest.raises(ValueError, match="Categories must be a non-empty string."):
        OutputGenerator("")