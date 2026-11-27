from langdetect import detect


def detect_language(text):
    try:
        language = detect(text)

        return {
            "language": language,
            "is_english": language == "en"
        }

    except Exception:
        return {
            "language": "unknown",
            "is_english": False
        }