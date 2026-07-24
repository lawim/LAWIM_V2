from lawim_runtime.conversation.entity import EntityExtractionEngine


def test_extract_property_type():
    eng = EntityExtractionEngine()
    r = eng.extract("Je cherche un appartement")
    assert r.entities.get("property_type") == "apartment"


def test_extract_house():
    eng = EntityExtractionEngine()
    r = eng.extract("Je cherche une maison à vendre")
    assert r.entities.get("property_type") == "house"
    assert r.entities.get("transaction_type") == "sell"


def test_extract_city():
    eng = EntityExtractionEngine()
    r = eng.extract("Je cherche à Douala")
    assert r.entities.get("city") == "Douala"


def test_extract_district():
    eng = EntityExtractionEngine()
    r = eng.extract("À Mvan")
    assert r.entities.get("district") == "Mvan"


def test_extract_budget():
    eng = EntityExtractionEngine()
    r = eng.extract("Budget 200 000 FCFA")
    assert r.entities.get("budget_max") == 200000


def test_extract_bedrooms():
    eng = EntityExtractionEngine()
    r = eng.extract("Je veux 3 chambres")
    assert r.entities.get("bedrooms") == 3


def test_extract_french_bedrooms():
    eng = EntityExtractionEngine()
    r = eng.extract("Je veux deux chambres")
    assert r.entities.get("bedrooms") == 2


def test_extract_missing_fields():
    eng = EntityExtractionEngine()
    r = eng.extract("Bonjour")
    assert len(r.missing) >= 2
    assert "property_type" in r.missing or "city" in r.missing


def test_extract_empty():
    eng = EntityExtractionEngine()
    r = eng.extract("")
    assert len(r.entities) == 0


def test_extract_rent():
    eng = EntityExtractionEngine()
    r = eng.extract("Je cherche en location")
    assert r.entities.get("transaction_type") == "rent"


def test_extract_full_message():
    eng = EntityExtractionEngine()
    r = eng.extract("Je cherche un appartement de 2 chambres à louer à Yaoundé à Mvan avec un budget de 200 000 FCFA")
    assert r.entities.get("property_type") == "apartment"
    assert r.entities.get("transaction_type") == "rent"
    assert r.entities.get("city") == "Yaounde"
    assert r.entities.get("district") == "Mvan"
    assert r.entities.get("budget_max") == 200000
    assert r.entities.get("bedrooms") == 2
