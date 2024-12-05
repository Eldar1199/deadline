import unittest
from unittest.mock import patch, MagicMock
from .ts_test import Library

class TestLibraryAddBook(unittest.TestCase):
    def setUp(self):
        """Подготовка перед тестами."""
        self.library = Library()
        self.library.gen_id = MagicMock(return_value=1)  # Мокируем генерацию ID

    @patch('builtins.input', side_effect=['Преступление и наказание', 'Ф.М. Достоевский', '1866'])
    @patch.object(Library, 'save_json', return_value=None)
    def test_add_book_success(self, mock_save_json, mock_input):
        """Тест успешного добавления книги."""
        self.library.books = []  # Инициализируем пустую библиотеку
        self.library.add_book()

        # Проверяем, что книга добавлена
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0]['title'], 'Преступление и наказание')
        self.assertEqual(self.library.books[0]['author'], 'Ф.М. Достоевский')
        self.assertEqual(self.library.books[0]['year'], 1866)
        self.assertEqual(self.library.books[0]['status'], 'В наличии')
        self.assertEqual(self.library.books[0]['id'], 1)

        # Проверяем, что save_json был вызван
        mock_save_json.assert_called_once()

    @patch('builtins.input', side_effect=['Преступление и наказание', 'Ф.М. Достоевский', 'abcd', '1866'])
    @patch.object(Library, 'save_json', return_value=None)
    def test_add_book_invalid_year(self, mock_save_json, mock_input):
        """Тест обработки некорректного ввода года."""
        self.library.books = []  # Инициализируем пустую библиотеку
        self.library.add_book()

        # Проверяем, что книга добавлена после корректного ввода
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0]['year'], 1866)

        # Проверяем, что save_json был вызван
        mock_save_json.assert_called_once()

if __name__ == "__main__":
    unittest.main()
