from google.cloud import translate


def turn_array_to_str(arr):
    return ', '.join(arr)


def translate_text(text):
    if type(text).__name__ == 'list':
        text = turn_array_to_str(text)

    translate_client = translate.Client()
    target = 'ru'
    translation = translate_client.translate(
        text,
        target_language=target)
    response = translation['translatedText']
    return response
