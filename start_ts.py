from ts import Library

class BookMain:
    """Класс для запуска консольной программы"""
    def __init__(self) -> None:
        """Создание экземпляра от класса"""
        self.library = Library()
    
    def main(self) -> None:
        """Функция для запуска"""
        while True:
            print('\nMeню: ')
            print('1. Добавить книгу')
            print('2. Удалить книгу')
            print('3. Поиск книги')
            print('4. Получить книги')
            print('5. Изменить статус книги')
            print('6. Выйти')
            res = input('Введите категорию: ')
            if res == '1':
                self.library.add_book()
            elif res == '2':
                self.library.delete_book()
            elif res == '3':
                self.library.suarch_book()
            elif res == '4':
                self.library.get_books()
            elif res == '5':
                self.library.change_status()
            elif res == '6':
                print('До свидания!')
                break
            else:
                print('\nНе правильный выбор')


# if __name__ == '__main__':
bookmain = BookMain()
bookmain.main()
