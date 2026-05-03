import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# ======================== КОНФИГУРАЦИЯ ========================
CONFIG_FILE = "multiplication_config.json"

def load_last_n():
    """Загружает последнее использованное число N из JSON."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("last_n", 5)
        except:
            return 5
    return 5

def save_last_n(n):
    """Сохраняет число N в JSON-файл."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_n": n}, f, ensure_ascii=False, indent=4)
    except:
        pass

class MultiplicationTableApp:
    """Класс приложения для генерации таблицы умножения."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Генератор таблицы умножения | Matrix Pro 🔢")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1f2c")
        
        # Переменные
        self.current_n = load_last_n()
        self.table_frame = None
        
        # Создаём интерфейс
        self.create_widgets()
        
        # Загружаем таблицу для последнего N
        self.generate_table()
    
    def create_widgets(self):
        """Создаёт все элементы интерфейса."""
        # ========== Верхняя панель с вводом ==========
        top_frame = tk.Frame(self.root, bg="#1e1f2c")
        top_frame.pack(pady=20, padx=20, fill="x")
        
        # Заголовок
        title_label = tk.Label(
            top_frame,
            text="📐 ТАБЛИЦА УМНОЖЕНИЯ PRO 📐",
            font=("Segoe UI", 20, "bold"),
            bg="#1e1f2c",
            fg="#f1c40f"
        )
        title_label.pack(pady=(0, 15))
        
        # Рамка для ввода
        input_frame = tk.Frame(top_frame, bg="#2c2e3e", relief="groove", bd=2)
        input_frame.pack(pady=10, padx=50, fill="x")
        
        label_n = tk.Label(
            input_frame,
            text="Введите число N (1-20):",
            font=("Segoe UI", 12),
            bg="#2c2e3e",
            fg="#ffffff"
        )
        label_n.pack(side="left", padx=(20, 10), pady=15)
        
        self.entry_n = tk.Entry(
            input_frame,
            font=("Segoe UI", 14),
            width=8,
            bg="#1e1f2c",
            fg="#2ecc71",
            insertbackground="white",
            justify="center"
        )
        self.entry_n.insert(0, str(self.current_n))
        self.entry_n.pack(side="left", padx=10, pady=15)
        
        btn_generate = tk.Button(
            input_frame,
            text="🚀 ПОСТРОИТЬ ТАБЛИЦУ",
            command=self.generate_table,
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2",
            relief="flat",
            padx=15
        )
        btn_generate.pack(side="right", padx=20, pady=10)
        
        # Привязываем Enter
        self.entry_n.bind("<Return>", lambda event: self.generate_table())
        
        # ========== Область для таблицы ==========
        # Создаём Canvas + Scrollbar для прокрутки (на случай больших таблиц)
        canvas = tk.Canvas(self.root, bg="#1e1f2c", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Внутренний фрейм для таблицы (всё, что внутри Canvas)
        self.table_container = tk.Frame(canvas, bg="#1e1f2c")
        canvas.create_window((0, 0), window=self.table_container, anchor="nw", width=canvas.winfo_reqwidth())
        
        self.table_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(1, width=e.width))
        
        self.canvas = canvas
        self.table_container.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
    def clear_table(self):
        """Удаляет старую таблицу (если есть)."""
        if self.table_container:
            for widget in self.table_container.winfo_children():
                widget.destroy()
    
    def generate_table(self):
        """Главная функция: генерирует и отображает таблицу умножения."""
        # ========== ВАЛИДАЦИЯ ВВОДА ==========
        input_text = self.entry_n.get().strip()
        
        if input_text == "":
            messagebox.showerror("Ошибка", "Поле ввода пустое!\nВведите число от 1 до 20.")
            return
        
        if not input_text.lstrip('-').isdigit():
            messagebox.showerror("Ошибка", f"'{input_text}' — это не число!\nВведите целое число от 1 до 20.")
            return
        
        n = int(input_text)
        
        if n < 1:
            messagebox.showerror("Ошибка", "Число должно быть положительным (от 1 и выше).")
            return
        
        if n > 20:
            if not messagebox.askyesno("Предупреждение", f"Таблица {n}×{n} будет очень большой!\nПродолжить?"):
                return
        
        # ========== СОХРАНЯЕМ В JSON ==========
        self.current_n = n
        save_last_n(n)
        
        # ========== ОТРИСОВЫВАЕМ ТАБЛИЦУ ==========
        self.clear_table()
        
        # Создаём заголовки (первая строка и первый столбец)
        # Стили
        header_bg = "#3498db"
        cell_bg_odd = "#2c2e3e"
        cell_bg_even = "#232536"
        
        # Размер ячейки
        cell_width = 70
        cell_height = 40
        
        # ===== Заголовок строки "×" в левом верхнем углу =====
        corner_label = tk.Label(
            self.table_container,
            text="×",
            font=("Segoe UI", 14, "bold"),
            bg=header_bg,
            fg="white",
            width=8,
            height=2,
            relief="ridge",
            bd=1
        )
        corner_label.grid(row=0, column=0, padx=1, pady=1, sticky="nsew")
        
        # ===== Заголовки столбцов (1, 2, 3, ..., n) =====
        for j in range(1, n + 1):
            col_header = tk.Label(
                self.table_container,
                text=str(j),
                font=("Segoe UI", 12, "bold"),
                bg=header_bg,
                fg="white",
                width=8,
                height=2,
                relief="ridge",
                bd=1
            )
            col_header.grid(row=0, column=j, padx=1, pady=1, sticky="nsew")
        
        # ===== Заголовки строк (1, 2, 3, ..., n) и ячейки =====
        for i in range(1, n + 1):
            # Заголовок строки (первая колонка)
            row_header = tk.Label(
                self.table_container,
                text=str(i),
                font=("Segoe UI", 12, "bold"),
                bg=header_bg,
                fg="white",
                width=8,
                height=2,
                relief="ridge",
                bd=1
            )
            row_header.grid(row=i, column=0, padx=1, pady=1, sticky="nsew")
            
            # Ячейки с произведениями
            for j in range(1, n + 1):
                result = i * j
                # Чередуем цвета для удобства чтения
                bg_color = cell_bg_odd if (i + j) % 2 == 0 else cell_bg_even
                
                cell = tk.Label(
                    self.table_container,
                    text=str(result),
                    font=("Segoe UI", 11),
                    bg=bg_color,
                    fg="#ffffff",
                    width=8,
                    height=2,
                    relief="ridge",
                    bd=1
                )
                cell.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")
        
        # ===== Настройка весов столбцов и строк для адаптивности =====
        for j in range(n + 1):
            self.table_container.grid_columnconfigure(j, weight=1, minsize=60)
        for i in range(n + 1):
            self.table_container.grid_rowconfigure(i, weight=1, minsize=35)
        
        # Обновляем область прокрутки
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Показываем сообщение об успехе
        messagebox.showinfo("Готово", f"✅ Таблица умножения {n}×{n} построена!\n📁 Файл config.json обновлён.")

# ======================== ЗАПУСК ========================
if __name__ == "__main__":
    root = tk.Tk()
    app = MultiplicationTableApp(root)
    root.mainloop()