import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font, colorchooser


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.dark_mode = False
        self.current_font = "Arial"
        self.font_size = 12
        self.text_color = "black"
        self.current_file = None
        self.setup_ui()

    def setup_ui(self):
        self.custom_font = font.Font(family=self.current_font, size=self.font_size)

        # Главный контейнер
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Панель инструментов
        self.toolbar = ttk.Frame(self.main_frame)
        self.toolbar.pack(side="top", fill="x")
        self.create_toolbar_buttons()

        # Текстовая область
        self.text_area, self.line_numbers = self.create_text_area()

        # Статус бар
        self.status_bar = ttk.Label(self.root, text="Готово | Цвет: Чёрный", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

        # Меню и горячие клавиши
        self.create_menus()
        self.bind_shortcuts()

    def create_toolbar_buttons(self):
        # Кнопки выравнивания
        ttk.Button(self.toolbar, text="◀", command=lambda: self.set_alignment("left")).pack(side="left", padx=2)
        ttk.Button(self.toolbar, text="●", command=lambda: self.set_alignment("center")).pack(side="left", padx=2)
        ttk.Button(self.toolbar, text="▶", command=lambda: self.set_alignment("right")).pack(side="left", padx=2)

        ttk.Separator(self.toolbar, orient="vertical").pack(side="left", fill="y", padx=5)

        # Кнопки стиля текста
        self.bold_btn = ttk.Button(self.toolbar, text="B", command=self.toggle_bold)
        self.italic_btn = ttk.Button(self.toolbar, text="I", command=self.toggle_italic)
        self.bold_btn.pack(side="left", padx=2)
        self.italic_btn.pack(side="left", padx=2)

        # Кнопка цвета текста
        ttk.Button(self.toolbar, text="🎨", command=self.change_text_color).pack(side="left", padx=5)

        # Выбор шрифта
        self.font_var = tk.StringVar()
        self.font_combobox = ttk.Combobox(self.toolbar, textvariable=self.font_var,
                                          values=["Arial", "Times New Roman", "Courier New", "Verdana"])
        self.font_combobox.set(self.current_font)
        self.font_combobox.bind("<<ComboboxSelected>>", self.change_font)
        self.font_combobox.pack(side="left", padx=5)

    def create_text_area(self):
        # Контейнер для текста
        text_frame = ttk.Frame(self.main_frame)
        text_frame.pack(fill="both", expand=True)

        # Нумерация строк
        self.line_numbers = tk.Text(text_frame, width=4, padx=5, state="disabled", bg="#f0f0f0")
        self.line_numbers.pack(side="left", fill="y")

        # Основная текстовая область
        self.text_area = tk.Text(text_frame, wrap="word", undo=True, font=self.custom_font,
                                 padx=5, pady=5, insertbackground="black")
        self.text_area.pack(side="right", fill="both", expand=True)

        # Привязка событий
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)

        return self.text_area, self.line_numbers

    def create_menus(self):
        # Создание меню
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Меню Файл
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.destroy)

        # Меню Правка
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторить", command=self.text_area.edit_redo, accelerator="Ctrl+Y")

        # Меню Вид
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Темная тема", command=self.toggle_theme)

    def bind_shortcuts(self):
        self.root.bind_all("<Control-n>", lambda e: self.new_file())
        self.root.bind_all("<Control-o>", lambda e: self.open_file())
        self.root.bind_all("<Control-s>", lambda e: self.save_file())
        self.root.bind_all("<Control-z>", lambda e: self.text_area.edit_undo())
        self.root.bind_all("<Control-y>", lambda e: self.text_area.edit_redo())

    def set_alignment(self, align):
        try:
            start = self.text_area.index("sel.first")
            end = self.text_area.index("sel.last")
        except tk.TclError:
            start = "1.0"
            end = "end"

        for tag in ["left", "center", "right"]:
            self.text_area.tag_remove(tag, start, end)

        self.text_area.tag_configure(align, justify=align)
        self.text_area.tag_add(align, start, end)
        self.status_bar.config(text=f"Выравнивание: {align.capitalize()}")

    def toggle_bold(self):
        try:
            start = self.text_area.index("sel.first")
            end = self.text_area.index("sel.last")
            if "bold" in self.text_area.tag_names("sel.first"):
                self.text_area.tag_remove("bold", start, end)
            else:
                self.text_area.tag_add("bold", start, end)
                self.text_area.tag_configure("bold", font=self.custom_font)
            self.apply_font_style()
        except tk.TclError:
            pass

    def toggle_italic(self):
        try:
            start = self.text_area.index("sel.first")
            end = self.text_area.index("sel.last")
            if "italic" in self.text_area.tag_names("sel.first"):
                self.text_area.tag_remove("italic", start, end)
            else:
                self.text_area.tag_add("italic", start, end)
                self.text_area.tag_configure("italic", font=self.custom_font)
            self.apply_font_style()
        except tk.TclError:
            pass

    def change_font(self, event=None):
        self.current_font = self.font_var.get()
        self.custom_font.configure(family=self.current_font)
        self.apply_font_style()

    def apply_font_style(self):
        weight = "bold" if "bold" in self.text_area.tag_names("sel.first") else "normal"
        slant = "italic" if "italic" in self.text_area.tag_names("sel.first") else "roman"
        self.custom_font.configure(
            family=self.current_font,
            size=self.font_size,
            weight=weight,
            slant=slant
        )
        self.text_area.configure(font=self.custom_font)

    def change_text_color(self):
        color = colorchooser.askcolor(title="Выберите цвет текста")[1]
        if color:
            self.text_color = color
            try:
                start = self.text_area.index("sel.first")
                end = self.text_area.index("sel.last")
                self.text_area.tag_add("color", start, end)
                self.text_area.tag_configure("color", foreground=color)
            except tk.TclError:
                self.text_area.configure(fg=color)
            self.status_bar.config(text=f"Готово | Цвет: {color}")

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")

        lines = self.text_area.get("1.0", "end-1c").split("\n")
        line_numbers_text = "\n".join(str(i) for i in range(1, len(lines) + 1))

        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")
        self.text_area.yview_moveto(self.line_numbers.yview()[0])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#2E2E2E" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"

        self.text_area.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.line_numbers.config(bg="#404040" if self.dark_mode else "#f0f0f0", fg=fg_color)

    def new_file(self):
        self.text_area.delete("1.0", "end")
        self.current_file = None
        self.update_title()

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete("1.0", "end")
                    self.text_area.insert("1.0", file.read())
                self.current_file = file_path
                self.update_title()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    file.write(self.text_area.get("1.0", "end-1c"))
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_area.get("1.0", "end-1c"))
                self.current_file = file_path
                self.update_title()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")

    def update_title(self):
        name = "Безымянный" if not self.current_file else self.current_file.split("/")[-1]
        self.root.title(f"{name} - Text Editor")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    style = ttk.Style()
    style.theme_use("clam")
    editor = TextEditor(root)
    root.mainloop()