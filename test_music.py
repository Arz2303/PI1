# test_music_shop.py
import pytest
from datetime import date
from er import Seller, Customer, MusicalInstrument


class TestSeller:
    """Тесты для класса Seller"""

    def test_seller_creation(self):
        """Тест создания продавца"""
        seller = Seller(1, "Иван Петров", "ivan@mail.ru")
        assert seller.id == 1
        assert seller.name == "Иван Петров"
        assert seller.contact_data == "ivan@mail.ru"

    def test_seller_attributes(self):
        """Тест атрибутов продавца"""
        seller = Seller(2, "Мария Смирнова", "maria@mail.ru")
        assert hasattr(seller, 'id')
        assert hasattr(seller, 'name')
        assert hasattr(seller, 'contact_data')


class TestCustomer:
    """Тесты для класса Customer"""

    def test_customer_creation(self):
        """Тест создания покупателя"""
        customer = Customer(1, "Анна Иванова", "anna@mail.ru")
        assert customer.id == 1
        assert customer.name == "Анна Иванова"
        assert customer.contact_data == "anna@mail.ru"

    def test_customer_attributes(self):
        """Тест атрибутов покупателя"""
        customer = Customer(2, "Петр Кузнецов", "petr@mail.ru")
        assert hasattr(customer, 'id')
        assert hasattr(customer, 'name')
        assert hasattr(customer, 'contact_data')


class TestMusicalInstrument:
    """Тесты для класса MusicalInstrument"""

    @pytest.fixture
    def sample_instrument(self):
        """Фикстура с примером инструмента"""
        return MusicalInstrument(
            item_id=1,
            name="Гитара Fender Stratocaster",
            brand="Fender",
            producer="Fender USA",
            material="дерево",
            style="рок,блюз",
            price=45000.0,
            quantity_in_stock=5
        )

    def test_instrument_creation(self, sample_instrument):
        """Тест создания музыкального инструмента"""
        assert sample_instrument.id == 1
        assert sample_instrument.name == "Гитара Fender Stratocaster"
        assert sample_instrument.brand == "Fender"
        assert sample_instrument.producer == "Fender USA"
        assert sample_instrument.material == "дерево"
        assert sample_instrument.style == "рок,блюз"
        assert sample_instrument.price == 45000.0
        assert sample_instrument.quantity_in_stock == 5

    def test_instrument_attributes(self, sample_instrument):
        """Тест наличия всех атрибутов"""
        expected_attrs = ['id', 'name', 'brand', 'producer', 'material',
                          'style', 'price', 'quantity_in_stock']
        for attr in expected_attrs:
            assert hasattr(sample_instrument, attr)
