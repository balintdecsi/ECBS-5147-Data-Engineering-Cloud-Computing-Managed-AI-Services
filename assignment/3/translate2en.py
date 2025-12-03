import boto3

# AWS Clients
REGION = 'eu-west-1'
translate_client = boto3.client('translate', region_name=REGION)

def translate_to_english(text, source_lang):
    """
    Translates text from source_lang to English using AWS Translate.
    """
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode='en'
        )
        return response['TranslatedText']
    except Exception as e:
        raise e
