from __future__ import annotations

from lawim_runtime.project_profile.normalization.normalizers import (
    BooleanNormalizer,
    CityNormalizer,
    DistrictNormalizer,
    MoneyNormalizer,
    PropertyTypeNormalizer,
)


class TestMoneyNormalizer:
    def test_money_100000(self):
        n = MoneyNormalizer()
        result = n.normalize("100000")
        assert result.success
        assert result.normalized_value == 100000

    def test_money_100_mille(self):
        n = MoneyNormalizer()
        result = n.normalize("100 mille")
        assert result.success
        assert result.normalized_value == 100000

    def test_money_fcfa(self):
        n = MoneyNormalizer()
        result = n.normalize("50000 FCFA")
        assert result.success
        assert result.normalized_value == 50000


class TestCityNormalizer:
    def test_city_yaounde(self):
        n = CityNormalizer()
        result = n.normalize("yaounde")
        assert result.success
        assert result.normalized_value == "Yaound\u00e9"

    def test_city_douala(self):
        n = CityNormalizer()
        result = n.normalize("DOUALA")
        assert result.success
        assert result.normalized_value == "Douala"

    def test_city_unknown(self):
        n = CityNormalizer()
        result = n.normalize("nkongsamba")
        assert result.success
        assert result.normalized_value == "Nkongsamba"


class TestDistrictNormalizer:
    def test_district_biyem_assi(self):
        n = DistrictNormalizer()
        result = n.normalize("biyem assi")
        assert result.success
        assert result.normalized_value == "Biyem-Assi"

    def test_district_bonamoussadi(self):
        n = DistrictNormalizer()
        result = n.normalize("bonamoussadi")
        assert result.success
        assert result.normalized_value == "Bonamoussadi"


class TestPropertyTypeNormalizer:
    def test_property_type_appt(self):
        n = PropertyTypeNormalizer()
        result = n.normalize("appartement")
        assert result.success
        assert result.normalized_value == "APARTMENT"

    def test_property_type_studio(self):
        n = PropertyTypeNormalizer()
        result = n.normalize("studio")
        assert result.success
        assert result.normalized_value == "STUDIO"

    def test_property_type_maison(self):
        n = PropertyTypeNormalizer()
        result = n.normalize("maison")
        assert result.success
        assert result.normalized_value == "HOUSE"


class TestBooleanNormalizer:
    def test_boolean_oui(self):
        n = BooleanNormalizer()
        result = n.normalize("oui")
        assert result.success
        assert result.normalized_value is True

    def test_boolean_non(self):
        n = BooleanNormalizer()
        result = n.normalize("non")
        assert result.success
        assert result.normalized_value is False

    def test_boolean_non_meuble(self):
        n = BooleanNormalizer()
        result = n.normalize("non meubl\u00e9")
        assert result.success
        assert result.normalized_value is False

    def test_boolean_meuble(self):
        n = BooleanNormalizer()
        result = n.normalize("meubl\u00e9")
        assert result.success
        assert result.normalized_value is True
