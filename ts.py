import json
import os

JSON_PATH: str = 'json_file.json'

class Library:
    """
    Основной класс с функциями добавления, удаления, 
    поиск, изменение статуса и получение всех книг. 
    """
    def __init__(self) -> None:
        """Инициализации(создание) json файла, если файл не создан
        (books) промежуточная переменная между бд и основным кодом"""
        if not os.path.exists(JSON_PATH):
            with open(JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)

        self.books: list = self.load_json()
    
    def load_json(self) -> list:
        """Загрузка данных"""
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self) -> None:
        """Сохранение данных"""
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def gen_id(self) -> int:
        """Генерация ID"""
        if not self.books:
            return 1
        return max(book["id"] for book in self.books) + 1

    def add_book(self) -> None:
        """
        Функция для добавления:
        title: Название книги(строка)
        author: Автора книги(строка)
        year: Год книги(число)
        status: По дефолту(в наличии)
        """
        title: str = input('Введите название книги: ')
        author: str = input('Введите автора книги: ')
        while True:
            try:
                year: int = int(input('Введите год издания книги: '))
                if not 1000 < year <= 2024:
                    print('Год должен быть положительным числом и не меньше 4 цифр')
                    continue
                break
            except ValueError:
                print('Введите целое число!')
        book = {
            'id': self.gen_id(),
            'title': title,
            'author': author,
            'year': year,
            'status': 'В наличии'
                }
        self.books.append(book)
        self.save_json()
        print('Книга успешно добавлена')


    def delete_book(self) -> None:
        """Функция удаления
        book_id: Принимает число
        book: Хранит словарь одной книги
        self.books: Перезаписывает json исключая введенный пользователем ID"""
        while True:
            try:
                book_id: int = int(input('Введите ID удаляемой книги: '))
                book: dict = next((book for book in self.books if book['id'] == book_id), None)
                print(book)
                if not book:
                    print('Нет такой книги')
                else:
                    self.books = [book for book in self.books if book['id'] != book_id]
                    break
            except ValueError:
                print('Введите корректные данные')
        self.save_json()
        print(f'Книга с ID:{book_id} удален')



    def suarch_book(self) -> str:
        """
        Функция поиска по названию, автору и год издания
        
        boo: Хранит строку введенную пользователем, переводит в нижний регистр
        res: Хранит строку, проверяет введенную пользователем строку в бд

        
        """
        boo: str = input('Поиск по названию, автору и год издания: ').lower()
        res: str = [book for book in self.books if boo in book['title'].lower() or
                boo in book['author'].lower() or boo in str(book['year'])
                ] 
        if res:
            for book in res:
                print(f"\nID: {book['id']}\nНазвание: {book['title']}\nАвтор: {book['author']}\nГод: {book['year']}\nСтатус: {book['status']}")
        else:
            print('Такой книги нету')

    def get_books(self) -> str:
        """Возвращает список всех книг"""
        for book in self.books:
            print(f"\nID: {book['id']}\nНазвание: {book['title']}\nАвтор: {book['author']}\nГод: {book['year']}\nСтатус: {book['status']}")

    def change_status(self) -> None:
        """
        Функция изменения статуса книги
        
        book_id: Число
        book: Словарь
        current_status: Строка, хранит текущее состояние статуса
        status: Строка, новое состояние статуса
        """
        while True:
            book_id: int = int(input('Введите ID: '))
            book: dict = next((book for book in self.books if book['id'] == book_id), None)
            if not book:
                print('Нет такой книги')
                continue
            current_status: str = next((book['status'] for book in self.books if book['id'] == book_id), None)
            while True:
                status: str = input('Изменить статус на Выдана/В наличии?: ').lower()
                if status not in ['выдана', 'в наличии'] or current_status == status:
                    print('Введите корректные данные\nНеверный статус')
                else:
                    book['status'] = status
                    self.save_json()
                    print(f'Статус изменен на "{status}"')
                    break
            break

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
# bookmain = BookMain()
# bookmain.main()
