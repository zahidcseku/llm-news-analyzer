import pytest
from unittest.mock import patch, MagicMock
from LLM_news_analyzer.article_classifier import ArticleClassifier


@pytest.fixture
def classifier():
    categories = "politics,sports,finance,technology,entertainment,others"
    return ArticleClassifier(categories)


def test_init(classifier):
    """
    Test that the ArticleClassifier is correctly initialized.
    Verifies:
        - Instance is created successfully
        - Categories are set correctly
    """
    assert isinstance(classifier, ArticleClassifier)
    assert classifier.categories == "politics,sports,finance,technology,entertainment,others"


def test_init_failure():
    """
    Test the behavior when model initialization fails.
    Verifies:
    - An exception is raised
    - The exception message contains the expected error text
    """
    with patch('google.generativeai.GenerativeModel', side_effect=Exception("Model initialization failed")):
        with pytest.raises(Exception) as context:
            ArticleClassifier("politics,sports,finance,technology,entertainment,others")
            assert "Failed to initialize the model" in str(context.value)


def test_classify_empty_input(classifier):
    """
    Test classification with an empty input.
    Verifies:
    - A ValueError is raised
    - The error message matches the expected text
    """
    with pytest.raises(ValueError) as context:
        classifier.classify("")
    assert str(context.value) == "Input text cannot be empty or whitespace."


@patch('google.generativeai.GenerativeModel.generate_content')
def test_classify_valid_category(mock_generate_content, classifier):
    """
    Test classification with a valid category.
    Verifies:
    - The model returns a valid category
    - The returned category matches the mocked response
    """    
    mock_response = MagicMock()
    mock_response.text = "technology"
    mock_generate_content.return_value = mock_response

    assert classifier.classify("AI is revolutionizing various industries.") == "technology"


@patch('google.generativeai.GenerativeModel.generate_content')
def test_classify_invalid_category(mock_generate_content, classifier):    
    """
    Test classification with an invalid category.
    Verifies:
    - When an unrecognized category is returned
    - The method defaults to "Cant do it!!"
    """
    mock_response = MagicMock()
    mock_response.text = "invalid_category"
    mock_generate_content.return_value = mock_response

    assert classifier.classify("This is a test article.") == "Cant do it!!"


@patch('google.generativeai.GenerativeModel.generate_content')
def test_classify_exception_handling(mock_generate_content, classifier, caplog):
    """
    Test error handling during classification.
    Verifies:
    - Exceptions are caught and logged
    - No unhandled exceptions are raised
    - Error is logged with the correct message
    """    
    mock_generate_content.side_effect = Exception("API error")

    result = classifier.classify("Test article")
    assert result is None
    assert "Error generating content from model: API error" in caplog.text
