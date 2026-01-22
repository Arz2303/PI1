import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from datetime import date


class Seller:
    def __init__(self, seller_id: int, name: str, contact_data: str):
        self.id = seller_id
        self.name = name
        self.contact_data = contact_data


class Customer:
    def __init__(self, customer_id: int, name: str, contact_data: str):
        self.id = customer_id
        self.name = name
        self.contact_data = contact_data


class MusicalInstrument:
    def __init__(self, item_id: int, name: str, brand: str, producer: str, material: str, style: str, price: float,
                 quantity_in_stock: int):
        self.id = item_id
        self.name = name
        self.brand = brand
        self.producer = producer
        self.material = material
        self.style = style
        self.price = price
        self.quantity_in_stock = quantity_in_stock


class Sale:
    def __init__(self, sale_id: int, customer: Customer, seller: Seller, sale_date: date):
        self.id = sale_id
        self.customer = customer
        self.seller = seller
        self.sale_date = sale_date
        self.items = []  # Список кортежей (товар, количество)
        self.total_amount = 0.0

    def add_item(self, item, quantity=1):
        if item.quantity_in_stock >= quantity:
            for i, (existing_item, existing_qty) in enumerate(self.items):
                if existing_item.id == item.id:
                    self.items[i] = (existing_item, existing_qty + quantity)
                    self.total_amount += item.price * quantity
                    item.quantity_in_stock -= quantity
                    return

            self.items.append((item, quantity))
            self.total_amount += item.price * quantity
            item.quantity_in_stock -= quantity
        else:
            raise ValueError(f"Недостаточно товара на складе. Доступно: {item.quantity_in_stock}")

    def remove_item(self, item, quantity=None):
        for i, (existing_item, existing_qty) in enumerate(self.items):
            if existing_item.id == item.id:
                if quantity is None or quantity >= existing_qty:
                    self.total_amount -= existing_item.price * existing_qty
                    item.quantity_in_stock += existing_qty
                    del self.items[i]
                else:
                    self.items[i] = (existing_item, existing_qty - quantity)
                    self.total_amount -= existing_item.price * quantity
                    item.quantity_in_stock += quantity
                return


class Return:
    def __init__(self, return_id: int, customer: Customer, return_date: date, reason: str, has_receipt: bool):
        self.id = return_id
        self.customer = customer
        self.return_date = return_date
        self.reason = reason
        self.has_receipt = has_receipt
        self.returned_items = []

    def get_info(self):
        """Получить информацию о возврате в виде строки"""
        receipt_status = "Есть чек" if self.has_receipt else "Нет чека"
        items_info = ""
        if self.returned_items:
            items_info = "\nТовары:\n"
            for i, (item, quantity) in enumerate(self.returned_items, 1):
                items_info += f"  {i}. {item.name} × {quantity}\n"

        return (f"Возврат #{self.id}\n"
                f"Покупатель: {self.customer.name}\n"
                f"Дата возврата: {self.return_date}\n"
                f"Причина: {self.reason}\n"
                f"Статус чека: {receipt_status}"
                f"{items_info}")


class Database:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def find(self, style="", brand=""):
        result = self.items
        if style:
            result = [i for i in result if style.lower() in i.style.lower()]
        if brand:
            result = [i for i in result if brand.lower() in i.brand.lower()]
        return result


class MusicShop:
    def __init__(self, root):
        self.root = root
        self.root.title("Магазин Звучёк")
        self.root.geometry("1000x750")

        self.db = Database()
        self.sellers = {}
        self.customers = {}
        self.current_sale = None
        self.sale_id_counter = 1
        self.returns = []  # Список созданных возвратов
        self.return_id_counter = 1

        self._setup_ui()
        self._load_sample_data()

    def _setup_ui(self):
        # Заголовок
        tk.Label(self.root, text="🎸 Магазин Звучёк 🎹",
                 font=("Arial", 16, "bold"), bg="lightblue", padx=20, pady=10).pack(fill=tk.X)

        # Блокнот с вкладками
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Создаем вкладки
        self._setup_genres_tab()
        self._setup_stock_tab()
        self._setup_sale_tab()
        self._setup_return_tab()
        self._setup_returns_list_tab()
        self._setup_search_tab()

    def _setup_genres_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎼 Жанры")

        # Фильтр
        ttk.Label(frame, text="Фильтр по жанрам:").pack(pady=5)
        self.genre_var = tk.StringVar(value="Все")
        genres = ["Все", "рок", "джаз", "классика", "поп", "электроника"]
        combo = ttk.Combobox(frame, textvariable=self.genre_var, values=genres, state="readonly", width=20)
        combo.pack(pady=5)
        combo.bind('<<ComboboxSelected>>', lambda e: self._filter_by_genre())

        # Таблица инструментов
        self.genre_tree = ttk.Treeview(frame, columns=("ID", "Название", "Бренд", "Цена", "Жанры", "Наличие"),
                                       show="headings")
        for col in ("ID", "Название", "Бренд", "Цена", "Жанры", "Наличие"):
            self.genre_tree.heading(col, text=col)
        self.genre_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _setup_stock_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Склад")

        # Форма добавления товара
        form_frame = ttk.LabelFrame(frame, text="Добавить товар")
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        fields = ["Название", "Бренд", "Материал", "Стиль", "Цена", "Количество"]
        self.entry_vars = {}

        for i, field in enumerate(fields):
            ttk.Label(form_frame, text=f"{field}:").grid(row=i // 2, column=(i % 2) * 2, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(form_frame, width=20)
            entry.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=5)
            self.entry_vars[field] = entry

        ttk.Button(form_frame, text="Добавить товар", command=self._add_item).grid(row=3, column=0, columnspan=4,
                                                                                   pady=10)

        # Таблица товаров
        self.stock_tree = ttk.Treeview(frame, columns=("ID", "Название", "Бренд", "Цена", "Количество"),
                                       show="headings")
        for col in ("ID", "Название", "Бренд", "Цена", "Количество"):
            self.stock_tree.heading(col, text=col)
        self.stock_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Удалить выбранный", command=self._remove_item).pack(pady=5)

    def _setup_sale_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💰 Продажа")

        # Выбор продавца и покупателя
        frame1 = ttk.Frame(frame)
        frame1.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(frame1, text="Продавец:").pack(side=tk.LEFT)
        self.seller_var = tk.StringVar()
        self.seller_combo = ttk.Combobox(frame1, textvariable=self.seller_var, state="readonly", width=20)
        self.seller_combo.pack(side=tk.LEFT, padx=10)

        ttk.Label(frame1, text="Покупатель:").pack(side=tk.LEFT)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(frame1, textvariable=self.customer_var, state="readonly", width=20)
        self.customer_combo.pack(side=tk.LEFT, padx=10)

        ttk.Button(frame1, text="Создать продажу", command=self._create_sale).pack(side=tk.LEFT, padx=10)

        # Товары на складе
        ttk.Label(frame, text="Доступные товары:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.sale_tree = ttk.Treeview(frame, columns=("ID", "Название", "Цена", "Наличие"), show="headings", height=8)
        for col in ("ID", "Название", "Цена", "Наличие"):
            self.sale_tree.heading(col, text=col)
        self.sale_tree.pack(fill=tk.X, padx=10, pady=5)

        # Количество и кнопка добавления
        frame2 = ttk.Frame(frame)
        frame2.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame2, text="Количество:").pack(side=tk.LEFT)
        self.quantity_var = tk.StringVar(value="1")
        self.quantity_spinbox = tk.Spinbox(frame2, from_=1, to=100, textvariable=self.quantity_var, width=10)
        self.quantity_spinbox.pack(side=tk.LEFT, padx=10)

        ttk.Button(frame2, text="Добавить в продажу", command=self._add_to_sale).pack(side=tk.LEFT)

        # Список товаров в продаже
        ttk.Label(frame, text="Товары в продаже:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.sale_listbox = tk.Listbox(frame, height=8)
        self.sale_listbox.pack(fill=tk.X, padx=10, pady=5)

        # Кнопки управления продажей
        frame3 = ttk.Frame(frame)
        frame3.pack(pady=10)
        ttk.Button(frame3, text="Удалить выбранный", command=self._remove_from_sale).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame3, text="Завершить продажу", command=self._complete_sale).pack(side=tk.LEFT, padx=5)

        self.sale_tree.bind('<<TreeviewSelect>>', self._on_item_selected)

    def _setup_return_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔄 Создать возврат")

        # Форма создания возврата
        form_frame = ttk.LabelFrame(frame, text="Форма возврата")
        form_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(form_frame, text="Покупатель:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.return_customer_var = tk.StringVar()
        self.return_customer_combo = ttk.Combobox(form_frame, textvariable=self.return_customer_var, state="readonly")
        self.return_customer_combo.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(form_frame, text="Причина возврата:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.reason_entry = ttk.Entry(form_frame)
        self.reason_entry.pack(fill=tk.X, padx=10, pady=5)

        self.has_receipt_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="Есть чек", variable=self.has_receipt_var).pack(anchor=tk.W, padx=10, pady=5)

        ttk.Button(form_frame, text="Создать возврат", command=self._create_return).pack(pady=10)

        # Информация о созданном возврате
        ttk.Label(frame, text="Информация о возврате:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.return_info_text = tk.Text(frame, height=10, wrap=tk.WORD)
        self.return_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def _setup_returns_list_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Список возвратов")

        # Таблица возвратов
        self.returns_tree = ttk.Treeview(frame, columns=("ID", "Покупатель", "Дата", "Причина", "Чек"), show="headings")
        for col in ("ID", "Покупатель", "Дата", "Причина", "Чек"):
            self.returns_tree.heading(col, text=col)
        self.returns_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Кнопки управления
        frame1 = ttk.Frame(frame)
        frame1.pack(pady=5)
        ttk.Button(frame1, text="Обновить список", command=self._refresh_returns_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame1, text="Показать детали", command=self._show_return_details).pack(side=tk.LEFT, padx=5)

    def _setup_search_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔍 Поиск")

        # Поля поиска
        frame1 = ttk.Frame(frame)
        frame1.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(frame1, text="Стиль:").pack(side=tk.LEFT)
        self.search_style_entry = ttk.Entry(frame1, width=20)
        self.search_style_entry.pack(side=tk.LEFT, padx=10)

        ttk.Label(frame1, text="Бренд:").pack(side=tk.LEFT)
        self.search_brand_entry = ttk.Entry(frame1, width=20)
        self.search_brand_entry.pack(side=tk.LEFT, padx=10)

        ttk.Button(frame1, text="Найти", command=self._do_search).pack(side=tk.LEFT, padx=10)

        # Результаты поиска
        self.search_tree = ttk.Treeview(frame, columns=("Название", "Бренд", "Стиль", "Цена", "Наличие"),
                                        show="headings")
        for col in ("Название", "Бренд", "Стиль", "Цена", "Наличие"):
            self.search_tree.heading(col, text=col)
        self.search_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _load_sample_data(self):
        # Продавцы
        self.sellers = {
            1: Seller(1, "Иван Петров", "ivan@mail.ru"),
            2: Seller(2, "Мария Смирнова", "maria@mail.ru"),
            3: Seller(3, "Алексей Козлов", "alex@mail.ru"),
            4: Seller(4, "Елена Васнецова", "elena@mail.ru")
        }

        # Покупатели
        self.customers = {
            1: Customer(1, "Анна Иванова", "anna@mail.ru"),
            2: Customer(2, "Петр Кузнецов", "petr@mail.ru"),
            3: Customer(3, "Сергей Соколов", "sergey@mail.ru"),
            4: Customer(4, "Ольга Морозова", "olga@mail.ru"),
            5: Customer(5, "Дмитрий Волков", "dmitry@mail.ru")
        }

        # Товары
        items_data = [
            (1, "Гитара Fender Stratocaster", "Fender", "Fender USA", "дерево", "рок,блюз", 45000.0, 5),
            (2, "Фортепиано Yamaha", "Yamaha", "Yamaha Japan", "дерево", "классика,джаз", 120000.0, 2),
            (3, "Бас-гитара Ibanez", "Ibanez", "Ibanez", "дерево", "рок,метал", 35000.0, 3),
            (4, "Саксофон Yamaha", "Yamaha", "Yamaha", "металл", "джаз", 80000.0, 1),
            (5, "Гитара акустическая Martin", "Martin", "Martin", "дерево", "фолк", 25000.0, 4),
            (6, "Синтезатор Korg", "Korg", "Korg Japan", "пластик", "электроника,поп", 65000.0, 3),
            (7, "Ударная установка Pearl", "Pearl", "Pearl", "металл,пластик", "рок,поп", 89000.0, 2),
            (8, "Скрипка Stradivarius", "Stradivarius", "Stradivarius", "дерево", "классика", 150000.0, 1),
        ]

        for data in items_data:
            self.db.add_item(MusicalInstrument(*data))

        self._refresh_all()
        self._update_comboboxes()

    def _update_comboboxes(self):
        # Продавцы
        self.seller_combo['values'] = [s.name for s in self.sellers.values()]
        if self.seller_combo['values']:
            self.seller_combo.current(0)

        # Покупатели
        self.customer_combo['values'] = [c.name for c in self.customers.values()]
        if self.customer_combo['values']:
            self.customer_combo.current(0)

        # Покупатели для возврата
        self.return_customer_combo['values'] = [c.name for c in self.customers.values()]
        if self.return_customer_combo['values']:
            self.return_customer_combo.current(0)

    def _refresh_all(self):
        """Обновить все таблицы"""
        self._refresh_stock()
        self._show_all_genres()
        self._refresh_returns_list()

    def _refresh_stock(self):
        """Обновить таблицы товаров"""
        for tree in [self.stock_tree, self.sale_tree]:
            for i in tree.get_children():
                tree.delete(i)

        for item in self.db.items:
            self.stock_tree.insert("", "end", values=(
                item.id, item.name, item.brand, f"{item.price:.0f}", item.quantity_in_stock))
            self.sale_tree.insert("", "end", values=(
                item.id, item.name, f"{item.price:.0f}", item.quantity_in_stock))

    def _show_all_genres(self):
        """Показать все товары в разделе жанров"""
        for i in self.genre_tree.get_children():
            self.genre_tree.delete(i)

        for instr in self.db.items:
            self.genre_tree.insert("", "end", values=(
                instr.id,
                instr.name,
                instr.brand,
                f"{instr.price:.0f}",
                instr.style,
                instr.quantity_in_stock
            ))

    def _filter_by_genre(self):
        """Фильтр по жанру"""
        genre = self.genre_var.get()

        for i in self.genre_tree.get_children():
            self.genre_tree.delete(i)

        for instr in self.db.items:
            if genre == "Все" or genre.lower() in instr.style.lower():
                self.genre_tree.insert("", "end", values=(
                    instr.id,
                    instr.name,
                    instr.brand,
                    f"{instr.price:.0f}",
                    instr.style,
                    instr.quantity_in_stock
                ))

    def _on_item_selected(self, event):
        """Обработка выбора товара в продаже"""
        selected = self.sale_tree.selection()
        if selected:
            item_id = self.sale_tree.item(selected[0])['values'][0]
            item = next((i for i in self.db.items if i.id == item_id), None)
            if item:
                self.quantity_spinbox.config(to=item.quantity_in_stock)
                current_value = int(self.quantity_var.get())
                if current_value > item.quantity_in_stock:
                    self.quantity_var.set(str(item.quantity_in_stock))

    def _add_item(self):
        """Добавить товар на склад"""
        try:
            item = MusicalInstrument(
                len(self.db.items) + 1,
                self.entry_vars["Название"].get(),
                self.entry_vars["Бренд"].get(),
                "",
                self.entry_vars["Материал"].get(),
                self.entry_vars["Стиль"].get(),
                float(self.entry_vars["Цена"].get()),
                int(self.entry_vars["Количество"].get())
            )
            self.db.add_item(item)
            self._refresh_all()
            messagebox.showinfo("✅", "Товар добавлен!")

            # Очистка полей
            for entry in self.entry_vars.values():
                entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("❌", "Проверьте поля! Цена и количество должны быть числами.")

    def _remove_item(self):
        """Удалить товар со склада"""
        selected = self.stock_tree.selection()
        if selected:
            item_id = self.stock_tree.item(selected[0])['values'][0]
            item = next((i for i in self.db.items if i.id == item_id), None)
            if item:
                self.db.remove_item(item)
                self._refresh_all()
                messagebox.showinfo("✅", "Товар удалён!")

    def _create_sale(self):
        """Создать новую продажу"""
        seller_name = self.seller_var.get()
        customer_name = self.customer_var.get()

        if not seller_name or not customer_name:
            messagebox.showerror("❌", "Выберите продавца и покупателя!")
            return

        seller = next((s for s in self.sellers.values() if s.name == seller_name), None)
        customer = next((c for c in self.customers.values() if c.name == customer_name), None)

        if seller and customer:
            self.current_sale = Sale(self.sale_id_counter, customer, seller, date.today())
            self.sale_id_counter += 1
            self.sale_listbox.delete(0, tk.END)
            messagebox.showinfo("✅", f"Продажа #{self.current_sale.id} создана!")
        else:
            messagebox.showerror("❌", "Продавец или покупатель не найден!")

    def _add_to_sale(self):
        """Добавить товар в текущую продажу"""
        if not self.current_sale:
            messagebox.showwarning("⚠️", "Сначала создайте продажу!")
            return

        selected = self.sale_tree.selection()
        if not selected:
            messagebox.showwarning("⚠️", "Выберите товар!")
            return

        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showerror("❌", "Количество должно быть больше 0!")
                return
        except ValueError:
            messagebox.showerror("❌", "Введите корректное количество!")
            return

        item_id = self.sale_tree.item(selected[0])['values'][0]
        item = next((i for i in self.db.items if i.id == item_id), None)

        if not item:
            messagebox.showerror("❌", "Товар не найден!")
            return

        if item.quantity_in_stock < quantity:
            messagebox.showerror("❌", f"Недостаточно товара на складе! Доступно: {item.quantity_in_stock}")
            return

        try:
            self.current_sale.add_item(item, quantity)
            self.sale_listbox.insert(tk.END, f"{item.name} × {quantity} = {item.price * quantity:,.0f} руб.")
            self._refresh_stock()
            messagebox.showinfo("✅", f"Добавлено {quantity} шт. товара!\nОстаток на складе: {item.quantity_in_stock}")
        except ValueError as e:
            messagebox.showerror("❌", str(e))

    def _remove_from_sale(self):
        """Удалить товар из текущей продажи"""
        if not self.current_sale:
            messagebox.showwarning("⚠️", "Нет активной продажи!")
            return

        selected = self.sale_listbox.curselection()
        if not selected:
            messagebox.showwarning("⚠️", "Выберите товар!")
            return

        index = selected[-1]
        item_text = self.sale_listbox.get(index)
        item_name = item_text.split(" × ")[0]

        for item, quantity in self.current_sale.items:
            if item.name == item_name:
                self.current_sale.remove_item(item)
                self.sale_listbox.delete(index)
                self._refresh_stock()
                messagebox.showinfo("✅", f"Товар удален из продажи!\nОстаток на складе: {item.quantity_in_stock}")
                return

    def _complete_sale(self):
        """Завершить продажу"""
        if not self.current_sale or not self.current_sale.items:
            messagebox.showwarning("⚠️", "Нет товаров в продаже!")
            return

        items_list = "\n".join([f"  • {item.name} × {quantity} = {item.price * quantity:,.0f} руб."
                                for item, quantity in self.current_sale.items])

        messagebox.showinfo("✅",
                            f"Продажа #{self.current_sale.id} завершена!\n"
                            f"Продавец: {self.current_sale.seller.name}\n"
                            f"Покупатель: {self.current_sale.customer.name}\n"
                            f"Дата: {self.current_sale.sale_date}\n"
                            f"Товары:\n{items_list}\n"
                            f"Итого: {self.current_sale.total_amount:,.0f} руб.")

        self.current_sale = None
        self.sale_listbox.delete(0, tk.END)

    def _create_return(self):
        """Создать возврат"""
        customer_name = self.return_customer_var.get()
        reason = self.reason_entry.get().strip()

        if not customer_name:
            messagebox.showerror("❌", "Выберите покупателя!")
            return

        if not reason:
            reason = "Не указана"

        customer = next((c for c in self.customers.values() if c.name == customer_name), None)

        if customer:
            # Создаем новый возврат
            new_return = Return(
                self.return_id_counter,
                customer,
                date.today(),
                reason,
                self.has_receipt_var.get()
            )

            # Добавляем в список возвратов
            self.returns.append(new_return)
            self.return_id_counter += 1

            # Очищаем поля формы
            self.reason_entry.delete(0, tk.END)

            # Отображаем информацию о созданном возврате
            self._display_return_info(new_return)

            # Обновляем список возвратов
            self._refresh_returns_list()

            messagebox.showinfo("✅", f"Возврат #{new_return.id} создан для {customer.name}")
        else:
            messagebox.showerror("❌", "Покупатель не найден!")

    def _display_return_info(self, return_obj):
        """Отобразить информацию о возврате"""
        self.return_info_text.delete(1.0, tk.END)
        info = return_obj.get_info()
        self.return_info_text.insert(1.0, info)

        # Добавляем статистику
        self.return_info_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.return_info_text.insert(tk.END, f"Всего возвратов: {len(self.returns)}\n")

    def _refresh_returns_list(self):
        """Обновить список возвратов"""
        for item in self.returns_tree.get_children():
            self.returns_tree.delete(item)

        for return_obj in self.returns:
            self.returns_tree.insert("", "end", values=(
                return_obj.id,
                return_obj.customer.name,
                return_obj.return_date.strftime("%d.%m.%Y"),
                return_obj.reason,
                "Да" if return_obj.has_receipt else "Нет"
            ))

    def _show_return_details(self):
        """Показать детали возврата"""
        selected = self.returns_tree.selection()
        if not selected:
            messagebox.showwarning("⚠️", "Выберите возврат из списка!")
            return

        return_id = self.returns_tree.item(selected[0])['values'][0]
        return_obj = next((r for r in self.returns if r.id == return_id), None)

        if return_obj:
            self._display_return_info(return_obj)
            # Переключаемся на вкладку с возвратами
            self.notebook.select(3)  # Индекс вкладки "Создать возврат"

    def _do_search(self):
        """Выполнить поиск товаров"""
        style = self.search_style_entry.get()
        brand = self.search_brand_entry.get()
        results = self.db.find(style, brand)

        for i in self.search_tree.get_children():
            self.search_tree.delete(i)

        for item in results:
            self.search_tree.insert("", "end", values=(
                item.name, item.brand, item.style, f"{item.price:.0f}", item.quantity_in_stock))


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicShop(root)
    root.mainloop()