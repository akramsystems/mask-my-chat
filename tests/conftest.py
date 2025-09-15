import os
import pytest
from dotenv import load_dotenv

# Load environment variables at module level
load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """
    Session-scoped fixture that ensures environment is properly configured.
    Automatically used for all tests.
    """
    # Ensure dotenv is loaded
    load_dotenv()
    
    # Set default mock values if Azure credentials are not available
    # This allows tests to run in CI/development without real Azure credentials
    mock_env_vars = {
        "AZURE_LANGUAGE_ENDPOINT": "https://mock.cognitiveservices.azure.com/",
        "AZURE_LANGUAGE_KEY": "mock_key_for_testing"
    }
    
    for key, default_value in mock_env_vars.items():
        if key not in os.environ:
            os.environ[key] = default_value
    
    yield
    
    # Cleanup if needed (though typically not necessary for environment variables)


@pytest.fixture
def azure_credentials():
    """
    Fixture providing Azure credentials for tests.
    Returns a dict with the necessary environment variables.
    """
    return {
        "endpoint": os.environ.get("AZURE_LANGUAGE_ENDPOINT"),
        "key": os.environ.get("AZURE_LANGUAGE_KEY")
    }


def pytest_collection_modifyitems(config, items):
    """
    Automatically skip integration tests if only mock credentials are available.
    This runs during test collection and applies skips before tests execute.
    """
    # Check if we have real credentials (not mock values)
    endpoint = os.environ.get("AZURE_LANGUAGE_ENDPOINT", "")
    key = os.environ.get("AZURE_LANGUAGE_KEY", "")
    
    has_real_creds = (
        endpoint and not endpoint.startswith("mock") and
        key and key != "mock_key_for_testing"
    )
    
    if not has_real_creds:
        skip_integration = pytest.mark.skip(reason="Only mock Azure credentials available. Set real credentials in .env to run integration tests.")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
