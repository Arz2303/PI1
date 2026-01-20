import tkinter as tk
from tkinter import messagebox, ttk
import datetime


class MusicShop:
    def __init__(self, root):
        self.root = root
        self.root.title("Магазин Мелодия")
        self.root.geometry("1000x750")

        # ГЛАВНЫЙ ЗАГОЛОВОК С КНОПКОЙ ИНСТРУКЦИИ
        header_frame = ttk.Frame(root)
        header_frame.pack(fill=tk.X, pady=(10, 5))

        title_frame = ttk.Frame(header_frame)
        title_frame.pack()

        title_label = tk.Label(title_frame, text="🏪 МАГАЗИН МЕЛОДИЯ 🏪",
                               font=('Arial', 20, 'bold'),
                               bg='lightblue',
                               relief=tk.RAISED,
                               padx=20, pady=10)
        title_label.pack(side=tk.LEFT)

        ttk.Button(title_frame, text="📖 Инструкция", command=self.show_instructions).pack(side=tk.RIGHT, padx=10)

        # База инструментов с жанрами
        self.instruments = [
            {'id': 1, 'name': 'Гитара', 'price': 25000, 'description': 'Классическая акустическая гитара',
             'genres': ['Рок', 'Поп', 'Классика']},
            {'id': 2, 'name': 'Барабанная установка', 'price': 80000,
             'description': 'Профессиональная барабанная установка', 'genres': ['Рок', 'Метал', 'Джаз']},
            {'id': 3, 'name': 'Синтезатор', 'price': 45000, 'description': 'Цифровой синтезатор с 61 клавишей',
             'genres': ['Электронная', 'Поп', 'Хип-хоп']},
            {'id': 4, 'name': 'Скрипка', 'price': 35000, 'description': 'Профессиональная скрипка 4/4',
             'genres': ['Классика', 'Фолк']},
            {'id': 5, 'name': 'Электрогитара', 'price': 45000, 'description': 'Fender Stratocaster реплика',
             'genres': ['Рок', 'Метал', 'Блюз']},
            {'id': 6, 'name': 'Фортепиано', 'price': 120000, 'description': 'Ямаха цифровое пианино',
             'genres': ['Классика', 'Джаз', 'Поп']},
            {'id': 7, 'name': 'Саксофон', 'price': 55000, 'description': 'Альт-саксофон Yamaha',
             'genres': ['Джаз', 'Блюз']},
            {'id': 8, 'name': 'DJ-контроллер', 'price': 30000, 'description': 'Pioneer DDJ-200',
             'genres': ['Электронная', 'Хип-хоп']},
        ]
        self.cart = []

        # Notebook ниже заголовка (БЕЗ вкладки инструкции)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.setup_catalog()
        self.setup_genres()
        self.setup_cart()

    def show_instructions(self):
        """Показать инструкцию"""
        instr_window = tk.Toplevel(self.root)
        instr_window.title("📖 Инструкция по использованию")
        instr_window.geometry("700x600")
        instr_window.transient(self.root)
        instr_window.grab_set()

        # Scrollable текст инструкции
        text_frame = ttk.Frame(instr_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        scroll = ttk.Scrollbar(text_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        instr_text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scroll.set, font=('Arial', 11))
        scroll.config(command=instr_text.yview)
        instr_text.pack(fill=tk.BOTH, expand=True)

        instructions = """
🏪 МАГАЗИН МЕЛОДИЯ - ИНСТРУКЦИЯ

🎵 КАК ПОЛЬЗОВАТЬСЯ:

1. КАТАЛОГ / ПО ЖАНРАМ:
   • Выбирайте инструменты: Ctrl+клик (несколько) или Shift+клик (диапазон)
   • "Подробнее о выбранных" - вся информация справа
   • "Добавить выбранные в корзину" - добавляет по 1 шт.

2. КОРЗИНА:
   • Ctrl+клик для выбора нескольких товаров
   • "Удалить выбранные" - удаляет отмеченные
   • "Очистить всю корзину" - полная очистка (с подтверждением)
   • "Оформить заказ" - завершает покупку

3. ФИЛЬТР ПО ЖАНРАМ:
   • Выберите жанр в выпадающем списке
   • Нажмите "Показать"

💡 СОВЕТЫ:
• Все цены в рублях
• Итоговая сумма обновляется автоматически
• Заказ показывает дату/время и список товаров

🎼 Приятных покупок! 🎼
        """
        instr_text.insert(tk.END, instructions)
        instr_text.config(state=tk.DISABLED)

        ttk.Button(instr_window, text="Закрыть", command=instr_window.destroy).pack(pady=10)

    def setup_catalog(self):
        self.catalog_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.catalog_frame, text="Каталог")

        # Левая часть - список
        left_frame = ttk.Frame(self.catalog_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        columns = ('ID', 'Название', 'Цена')
        self.tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Цена', text='Цена (руб)')
        self.tree.column('ID', width=50)
        self.tree.column('Название', width=250)
        self.tree.column('Цена', width=100)
        self.tree['selectmode'] = 'extended'
        self.tree.pack(fill=tk.BOTH, expand=True)

        for instr in self.instruments:
            self.tree.insert('', tk.END, values=(instr['id'], instr['name'], instr['price']))

        # Правая часть - кнопки и детали
        right_frame = ttk.Frame(self.catalog_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Подробнее о выбранных", command=self.show_details).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Добавить выбранные в корзину", command=self.add_selected_to_cart).pack(fill=tk.X,
                                                                                                           pady=2)

        # Scrollable детали справа
        details_scroll = ttk.Scrollbar(right_frame)
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.details_text = tk.Text(right_frame, wrap=tk.WORD, width=35, height=25, yscrollcommand=details_scroll.set)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        details_scroll.config(command=self.details_text.yview)

    def setup_genres(self):
        self.genres_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.genres_frame, text="По жанрам")

        # Верх - фильтр
        genre_frame = ttk.LabelFrame(self.genres_frame, text="Выберите жанр:")
        genre_frame.pack(fill=tk.X, padx=10, pady=5)

        self.genre_var = tk.StringVar()
        genres = ['Все', 'Рок', 'Поп', 'Классика', 'Метал', 'Джаз', 'Электронная', 'Хип-хоп', 'Блюз', 'Фолк']
        combo = ttk.Combobox(genre_frame, textvariable=self.genre_var, values=genres, state='readonly')
        combo.set('Все')
        combo.pack(pady=5, side=tk.LEFT)
        combo.bind('<<ComboboxSelected>>', self.filter_by_genre)

        ttk.Button(genre_frame, text="Показать", command=self.filter_by_genre).pack(pady=5, side=tk.LEFT)

        # Левая часть - список по жанрам
        left_frame = ttk.Frame(self.genres_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        columns = ('ID', 'Название', 'Цена', 'Жанры')
        self.genre_tree = ttk.Treeview(left_frame, columns=columns, show='headings', height=15)
        self.genre_tree.heading('ID', text='ID')
        self.genre_tree.heading('Название', text='Название')
        self.genre_tree.heading('Цена', text='Цена (руб)')
        self.genre_tree.heading('Жанры', text='Жанры')
        self.genre_tree.column('ID', width=50)
        self.genre_tree.column('Название', width=200)
        self.genre_tree.column('Цена', width=80)
        self.genre_tree.column('Жанры', width=150)
        self.genre_tree['selectmode'] = 'extended'
        self.genre_tree.pack(fill=tk.BOTH, expand=True)

        # Правая часть - кнопки для жанров
        right_frame = ttk.Frame(self.genres_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Добавить выбранные в корзину", command=self.add_selected_genre_to_cart).pack(
            fill=tk.X)

        self.show_all_genres()

    def setup_cart(self):
        self.cart_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cart_frame, text="Корзина")

        self.cart_tree = ttk.Treeview(self.cart_frame, columns=('Название', 'Цена'), show='headings', height=15)
        self.cart_tree.heading('Название', text='Название')
        self.cart_tree.heading('Цена', text='Цена (руб)')
        self.cart_tree.column('Название', width=300)
        self.cart_tree.column('Цена', width=150)

        # Множественный выбор в корзине
        self.cart_tree['selectmode'] = 'extended'

        self.cart_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        total_frame = ttk.Frame(self.cart_frame)
        total_frame.pack(fill=tk.X, padx=10, pady=10)
        self.total_label = ttk.Label(total_frame, text="Итого: 0 руб.", font=('Arial', 12, 'bold'))
        self.total_label.pack()

        # Кнопки управления корзиной
        btn_frame = ttk.Frame(total_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Удалить выбранные", command=self.remove_selected_from_cart).pack(side=tk.LEFT,
                                                                                                     padx=5)
        ttk.Button(btn_frame, text="Очистить всю корзину", command=self.clear_all_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Оформить заказ", command=self.checkout).pack(side=tk.LEFT, padx=5)

    def remove_selected_from_cart(self):
        """ИСПРАВЛЕНО: Удалить выбранные товары из корзины"""
        selected = list(self.cart_tree.selection())
        if not selected:
            messagebox.showwarning("Удаление", "Выберите товары для удаления! (Ctrl+клик / Shift+клик)")
            return

        # Получаем индексы treeitem'ов для удаления из дерева
        tree_indices_to_remove = []
        for sel in selected:
            tree_index = self.cart_tree.index(sel)
            tree_indices_to_remove.append(tree_index)

        # Находим соответствующие элементы в cart по индексу tree (один-к-одному)
        removed_count = 0
        for tree_idx in sorted(tree_indices_to_remove, reverse=True):
            # Берем данные из tree
            item_values = self.cart_tree.item(self.cart_tree.get_children()[tree_idx])['values']
            cart_item_name = item_values[0]
            cart_item_price_str = item_values[1].replace(' ', '').replace(',', '')
            cart_item_price = int(cart_item_price_str)

            # Находим в cart
            for i, cart_item in enumerate(self.cart):
                if (cart_item['name'] == cart_item_name and
                        cart_item['price'] == cart_item_price):
                    del self.cart[i]
                    removed_count += 1
                    break

        # Удаляем из tree
        for tree_idx in sorted(tree_indices_to_remove, reverse=True):
            tree_item = self.cart_tree.get_children()[tree_idx]
            self.cart_tree.delete(tree_item)

        self.total_label.config(text=f"Итого: {sum(item['price'] for item in self.cart):,} руб.")
        messagebox.showinfo("Корзина", f"Удалено {removed_count} товаров из корзины!")

    def clear_all_cart(self):
        """Очистить всю корзину"""
        if not self.cart:
            messagebox.showinfo("Корзина", "Корзина уже пуста!")
            return

        if messagebox.askyesno("Очистить корзину", "Очистить ВСЮ корзину?"):
            self.cart.clear()
            for i in self.cart_tree.get_children():
                self.cart_tree.delete(i)
            self.total_label.config(text="Итого: 0 руб.")
            messagebox.showinfo("Корзина", "Корзина полностью очищена!")

    def get_selected_catalog(self):
        selected = self.tree.selection()
        instruments = []
        for sel in selected:
            item = self.tree.item(sel)
            instr_id = int(item['values'][0])
            instr = next((i for i in self.instruments if i['id'] == instr_id), None)
            if instr:
                instruments.append(instr)
        return instruments

    def get_selected_genre(self):
        selected = self.genre_tree.selection()
        instruments = []
        for sel in selected:
            item = self.genre_tree.item(sel)
            instr_id = int(item['values'][0])
            instr = next((i for i in self.instruments if i['id'] == instr_id), None)
            if instr:
                instruments.append(instr)
        return instruments

    def show_details(self):
        selected = self.get_selected_catalog()
        if not selected:
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(tk.END, "Выберите инструменты для просмотра деталей\n(Ctrl+клик / Shift+клик)")
            return

        self.details_text.delete(1.0, tk.END)
        details_text = f"Выбрано инструментов: {len(selected)}\n\n"

        for instr in selected:
            genres_str = ', '.join(instr['genres'])
            details_text += f"📦 {instr['name']}\n"
            details_text += f"   {instr['description']}\n"
            details_text += f"   💰 {instr['price']:,} руб.\n"
            details_text += f"   🎵 {genres_str}\n\n"

        self.details_text.insert(tk.END, details_text)

    def add_selected_to_cart(self):
        selected = self.get_selected_catalog()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите хотя бы один инструмент!")
            return
        for instr in selected:
            self.cart.append(instr)
        self.update_cart()
        messagebox.showinfo("Корзина", f"Добавлено {len(selected)} товаров в корзину!")

    def add_selected_genre_to_cart(self):
        selected = self.get_selected_genre()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите хотя бы один инструмент!")
            return
        for instr in selected:
            self.cart.append(instr)
        self.update_cart()
        messagebox.showinfo("Корзина", f"Добавлено {len(selected)} товаров в корзину!")

    def update_cart(self):
        for i in self.cart_tree.get_children():
            self.cart_tree.delete(i)
        total = sum(item['price'] for item in self.cart)
        for item in self.cart:
            self.cart_tree.insert('', tk.END, values=(item['name'], f"{item['price']:,}"))
        self.total_label.config(text=f"Итого: {total:,} руб.")

    def show_all_genres(self):
        for i in self.genre_tree.get_children():
            self.genre_tree.delete(i)
        for instr in self.instruments:
            genres_str = ', '.join(instr['genres'])
            self.genre_tree.insert('', tk.END, values=(instr['id'], instr['name'], instr['price'], genres_str))

    def filter_by_genre(self, event=None):
        genre = self.genre_var.get()
        for i in self.genre_tree.get_children():
            self.genre_tree.delete(i)

        for instr in self.instruments:
            if genre == 'Все' or genre in instr['genres']:
                genres_str = ', '.join(instr['genres'])
                self.genre_tree.insert('', tk.END, values=(instr['id'], instr['name'], instr['price'], genres_str))

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Корзина", "Корзина пуста!")
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        total = sum(item['price'] for item in self.cart)
        items_list = '\n'.join([f"{item['name']} - {item['price']:,} руб." for item in self.cart])
        msg = f"Заказ оформлен {now}!\n\n{items_list}\n\nИтого: {total:,} руб.\nСпасибо за покупку!"
        messagebox.showinfo("Заказ", msg)
        self.cart.clear()
        self.update_cart()


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicShop(root)
    root.mainloop()
