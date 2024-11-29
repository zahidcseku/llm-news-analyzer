import pytest
from unittest.mock import Mock, patch
from LLM_news_analyzer.article_summarizer import ArticleSummarizer 


@pytest.fixture
def summarizer():
    return ArticleSummarizer()

def test_summarizer_initialization():
    """
    Ensures that the ArticleSummarizer is correctly initialized with the necessary attributes.
    """
    summarizer = ArticleSummarizer()
    assert isinstance(summarizer, ArticleSummarizer)
    assert hasattr(summarizer, 'model')


def test_summarize_empty_input(summarizer):
    """
    Verifies that the summarizer raises a ValueError when given an empty string as input.
    """
    with pytest.raises(ValueError, match="Input text cannot be empty or whitespace."):
        summarizer.summarize("")


def test_summarize_whitespace_input(summarizer):
    """
    Checks that the summarizer raises a ValueError when given only whitespace as input.
    """
    with pytest.raises(ValueError, match="Input text cannot be empty or whitespace."):
        summarizer.summarize("   ")


@patch('google.generativeai.GenerativeModel.generate_content')
def test_successful_summarization(mock_generate_content, summarizer):
    """
    Mocks the API response and verifies that the summarizer returns the expected summary.
    """
    mock_response = Mock()
    mock_response.text = "This is a summary of the article."
    mock_generate_content.return_value = mock_response

    result = summarizer.summarize("This is a long article that needs summarization.")
    assert result == "This is a summary of the article."


def test_summarizer_initialization_failure():
    """
    Checks that an exception is raised if there's an error during the summarizer's initialization.
    """
    with patch('google.generativeai.GenerativeModel', side_effect=Exception("Model initialization failed")):
        with pytest.raises(Exception, match="Failed to initialize the model: Model initialization failed"):
            ArticleSummarizer()


@patch('google.generativeai.GenerativeModel.generate_content')
def test_summarization_long_input(mock_generate_content, summarizer):
    """
    Ensures the summarizer can handle very long input texts without issues.
    """
    long_input = "Long " * 1000  
    mock_response = Mock()
    mock_response.text = "Summary of long input."
    mock_generate_content.return_value = mock_response

    result = summarizer.summarize(long_input, max_words=10)
    assert len(result.split()) <= 10


@patch('google.generativeai.GenerativeModel.generate_content')
def test_summarization_preserves_important_info(mock_generate_content, summarizer):
    """
    Verifies that the summarization process retains important information from the original text.
    """
    input_text = "The quick brown fox jumps over the lazy dog. This is an important sentence."
    mock_response = Mock()
    mock_response.text = "Quick fox jumps over lazy dog. Important sentence."
    mock_generate_content.return_value = mock_response

    result = summarizer.summarize(input_text)
    assert "important sentence" in result.lower()
