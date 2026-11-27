from app.language_service import detect_language


def test_english_language():
    result = detect_language("The payment service is unavailable")

    assert result["language"] == "en"
    assert result["is_english"] is True


def test_spanish_language():
    result = detect_language(
        "El servicio de pago no está disponible"
    )

    assert result["language"] == "es"
    assert result["is_english"] is False


def test_french_language():
    result = detect_language(
        "Le service de paiement n'est pas disponible"
    )

    assert result["language"] == "fr"
    assert result["is_english"] is False
    

def test_language_detection_failure(monkeypatch):
    import app.language_service

    def mock_detect(text):
        raise Exception("Detection failed")

    monkeypatch.setattr(
        app.language_service,
        "detect",
        mock_detect
    )

    result = app.language_service.detect_language("")

    assert result["language"] == "unknown"
    assert result["is_english"] is False