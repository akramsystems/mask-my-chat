import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv; load_dotenv()


def replace_pii(text: str) -> str:
    """
    Replace PII in text using Azure AI Language.
    """
    credential = AzureKeyCredential(os.getenv("AZURE_LANGUAGE_KEY"))
    client = TextAnalyticsClient(endpoint=os.getenv("AZURE_LANGUAGE_ENDPOINT"), credential=credential)
    
    # Use recognize_pii_entities to detect PII and get redacted text
    documents = [text]
    result = client.recognize_pii_entities(documents)
    
    if result and not result[0].is_error:
        return result[0].redacted_text
    else:
        return text  # Return original text if PII detection fails


if __name__ == "__main__":
    from dotenv import load_dotenv; load_dotenv()
    print(replace_pii("My name is John Doe and my SSN is 123-45-6789."))