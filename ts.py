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
        return max(book.get("id") for book in self.books) + 1


    def add_book(self) -> None:
        """
        Функция для добавления:
        title: Название книги(строка)
        author: Автора книги(строка)
        year: Год книги(число)
        status: По дефолту(в наличии)
        """
        while True:
            title: str = input('Введите название книги: ').strip()
            if not title:
                print('Поле не может быть пустым')
                continue
            author: str = input('Введите автора книги: ').strip()
            if not author:
                print('Поле не может быть пустым')
                continue
            try:
                year: str = input('Введите год издания книги: ')
                if not year.isdigit():
                    raise ValueError('Поле должно быть числом')
                year = int(year)
                if not 1000 < year <= 2024:
                    print('Год должен быть положительным числом и не меньше 4 цифр')
                    continue
                break
            except ValueError:
                print('Введите корректные данные!')
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
                book: dict = next((book for book in self.books if book.get('id') == book_id), None)
                if not book:
                    print('Нет такой книги')
                else:
                    self.books = [book for book in self.books if book.get('id') != book_id]
                    break
            except ValueError:
                print('Введите корректные данные')
        self.save_json()
        print(f'Книга с ID:{book_id} удален')


    def suarch_book(self) -> None:
        """
        Функция поиска по названию, автору и год издания
        
        boo: Хранит строку введенную пользователем, переводит в нижний регистр
        res: Хранит строку, проверяет введенную пользователем строку в бд

        
        """
        boo: str = input('Поиск по названию, автору и год издания: ').lower()
        res: str = [book for book in self.books if boo in book.get('title').lower() or
                boo in book.get('author').lower() or boo in str(book.get('year'))
                ] 
        if res:
            for book in res:
                print(f"\nID: {book.get('id')}\nНазвание: {book.get('title')}\nАвтор: {book.get('author')}\nГод: {book.get('year')}\nСтатус: {book.get('status')}")
        else:
            print('Такой книги нету')


    def get_books(self) -> None:
        """Возвращает список всех книг"""
        for book in self.books:
            print(f"\nID: {book.get('id')}\nНазвание: {book.get('title')}\nАвтор: {book.get('author')}\nГод: {book.get('year')}\nСтатус: {book.get('status')}")


    def change_status(self) -> None:
        """
        Функция изменения статуса книги
        
        book_id: Число
        book: Словарь
        current_status: Строка, хранит текущее состояние статуса
        status: Строка, новое состояние статуса
        """
        while True:
            book_id: str = input('Введите ID: ').strip()
            if not book_id:
                print('Поле не может быть пустым')
                continue
            if not book_id.isdigit():
                print('Должно быть числом')
                continue
            book_id = int(book_id)
            book: dict = next((book for book in self.books if book.get('id') == book_id), None)
            if not book:
                print('Нет такой книги')
                continue
            current_status: str = book.get('status')
            print(f'Текущий статус книги "{current_status.upper()}"')
            while True:
                status: str = input('Изменить статус на Выдана/В наличии?: ').strip().lower()
                if status not in ['выдана', 'в наличии']:
                    print('Введите корректные данные\nВыдана/В наличии?')
                    continue
                if current_status == status:
                    print(f'Статус книги уже {current_status}')
                book['status'] = status
                self.save_json()
                print(f'Статус изменен на "{status}"')
                break
            break