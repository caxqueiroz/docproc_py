import pytest
from unittest.mock import Mock, patch
from docai.services.ai_processor.ai_processor import AIProcessor

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    class MockChoice:
        def __init__(self, text):
            self.message = Mock()
            self.message.content = text
    
    class MockResponse:
        def __init__(self, text):
            self.choices = [MockChoice(text)]
    
    return MockResponse("Enhanced text content")

@pytest.fixture
def mock_env_openai_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")

def test_enhance_extraction(mock_openai_response, mock_env_openai_key):
    """Test AI text enhancement"""
    with patch('openai.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_openai_response
        mock_openai.return_value = mock_client
        
        processor = AIProcessor()
        enhanced_text = processor.enhance_extraction("Original text", "pdf")
        
        assert enhanced_text == "Enhanced text content"
        mock_client.chat.completions.create.assert_called_once()

def test_enhance_extraction_with_empty_text():
    """Test AI enhancement with empty text"""
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
        processor = AIProcessor()
        with pytest.raises(ValueError):
            processor.enhance_extraction("", "pdf")
