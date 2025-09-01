import boto3

translate_client = boto3.client("translate")

def translate(text, target_lang="ar", source_lang="en"):
    """
    Translate a given text from a source language to a target language using AWS Translate.
    ---
    Args:
        text (str): The text to translate. If empty or None, returns an empty string.
        target_lang (str, optional): The target language code (default is "ar" for Arabic).
        source_lang (str, optional): The source language code (default is "en" for English).

    Returns:
        str: The translated text.

    Raises:
        botocore.exceptions.ClientError: If the AWS Translate API call fails.
    """
    if not text:
        return ""
    
    response = translate_client.translate_text(
        Text = text,
        SourceLanguageCode = source_lang,
        TargetLanguageCode = target_lang
    )

    return response["TranslatedText"]