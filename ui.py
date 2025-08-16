# ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from data import get_transactions, save_income_ui, save_expense_ui, delete_transaction, clear_all_transactions, get_summary, get_expense_summary
from tips import get_ai_tip
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

APP_BG = "#eff6ff"
TITLE_COLOR = "#1e3a8a"
SUBTITLE_COLOR = "#4b5563"
BTN_PRIMARY = "#1e40af"
BTN_SUCCESS = "#15803d"
BTN_DANGER = "#b91c1c"
FONT_TITLE = ("Arial", 20, "bold")
FONT_SUB = ("Arial", 12)
FONT_BTN = ("Arial", 12, "bold")

class UIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Personal Budget Tracker")
        self.root.geometry("960x640")
        self.root.configure(bg=APP_BG)

        self.container = tk.Frame(root, bg=APP_BG)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for Page in (MainMenuPage, AddIncomePage, AddExpensePage, TransactionsPage, SummaryPage, TipsPage):
            page = Page(parent=self.container, controller=self)
            self.frames[Page] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page(MainMenuPage)

    def show_page(self, page_class):
        page = self.frames[page_class]
        page.tkraise()
        if hasattr(page, "on_show"):
            page.on_show()

class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)
        self.controller = controller
        self._build()

    def _build(self):
        tk.Label(self, text="Smart Personal Budget Tracker", font=FONT_TITLE, bg=APP_BG, fg=TITLE_COLOR).pack(pady=20)
        tk.Button(self, text="Add Income", bg=BTN_SUCCESS, fg="white", font=FONT_BTN,
                  command=lambda: self.controller.show_page(AddIncomePage)).pack(pady=5)
        tk.Button(self, text="Add Expense", bg=BTN_DANGER, fg="white", font=FONT_BTN,
                  command=lambda: self.controller.show_page(AddExpensePage)).pack(pady=5)
        tk.Button(self, text="View Transactions", bg=BTN_PRIMARY, fg="white", font=FONT_BTN,
                  command=lambda: self.controller.show_page(TransactionsPage)).pack(pady=5)
        tk.Button(self, text="View Summary", bg="#6d28d9", fg="white", font=FONT_BTN,
                  command=lambda: self.controller.show_page(SummaryPage)).pack(pady=5)
        tk.Button(self, text="AI Tips", bg="#b45309", fg="white", font=FONT_BTN,
                  command=lambda: self.controller.show_page(TipsPage)).pack(pady=5)
        tk.Button(self, text="Exit", bg="#374151", fg="white", font=FONT_BTN,
                  command=self.controller.root.quit).pack(pady=5)

class AddIncomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)
        self.controller = controller
        self._build()  # Keep this call

    def _build(self):  # <--- my replacement starts here
        tk.Label(self, text="Add Income", font=FONT_TITLE, bg=APP_BG, fg=TITLE_COLOR).pack(pady=20)
        form = tk.Frame(self, bg=APP_BG)
        form.pack()

        # Amount
        tk.Label(form, text="Amount (RM)", font=FONT_SUB, bg=APP_BG).grid(row=0, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(form, font=FONT_SUB)
        self.amount_entry.grid(row=0, column=1, pady=5)

        # Source dropdown
        tk.Label(form, text="Source", font=FONT_SUB, bg=APP_BG).grid(row=1, column=0, sticky="w", pady=5)
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(form, textvariable=self.source_var, font=FONT_SUB,
                                         values=["Parents", "Salary", "Gift", "Business", "Other"])
        self.source_combo.grid(row=1, column=1, pady=5)
        self.source_combo.set("Parents")  # default

        # Notes
        tk.Label(form, text="Notes", font=FONT_SUB, bg=APP_BG).grid(row=2, column=0, sticky="w", pady=5)
        self.notes_entry = tk.Entry(form, font=FONT_SUB)
        self.notes_entry.grid(row=2, column=1, pady=5)

        tk.Button(self, text="Save", bg=BTN_SUCCESS, fg="white", font=FONT_BTN, command=self.save_income).pack(pady=10)
        tk.Button(self, text="Back", bg="#e5e7eb", fg="#111827", font=FONT_BTN,
                  command=lambda: self.controller.show_page(MainMenuPage)).pack()

    def save_income(self):  # <--- my replacement continues here
        try:
            amount = float(self.amount_entry.get())
            source = self.source_var.get()
            notes = self.notes_entry.get()
            save_income_ui(amount, source, notes)
            messagebox.showinfo("Saved", f"Income of RM {amount:.2f} added successfully.")
            self.amount_entry.delete(0, tk.END)
            self.source_combo.set("Parents")
            self.notes_entry.delete(0, tk.END)
            self.controller.show_page(MainMenuPage)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for amount.")



class AddExpensePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)
        self.controller = controller
        self._build()

    def _build(self):  # <--- replacement starts here
        tk.Label(self, text="Add Expense", font=FONT_TITLE, bg=APP_BG, fg=TITLE_COLOR).pack(pady=20)
        form = tk.Frame(self, bg=APP_BG)
        form.pack()

        # Amount
        tk.Label(form, text="Amount (RM)", font=FONT_SUB, bg=APP_BG).grid(row=0, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(form, font=FONT_SUB)
        self.amount_entry.grid(row=0, column=1, pady=5)

        # Category dropdown
        tk.Label(form, text="Category", font=FONT_SUB, bg=APP_BG).grid(row=1, column=0, sticky="w", pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form, textvariable=self.category_var, font=FONT_SUB,
                                           values=["Rent", "Food", "Transport", "Entertainment", "Bills", "Other"])
        self.category_combo.grid(row=1, column=1, pady=5)
        self.category_combo.set("Food")  # default

        # Notes
        tk.Label(form, text="Notes", font=FONT_SUB, bg=APP_BG).grid(row=2, column=0, sticky="w", pady=5)
        self.notes_entry = tk.Entry(form, font=FONT_SUB)
        self.notes_entry.grid(row=2, column=1, pady=5)

        tk.Button(self, text="Save", bg=BTN_DANGER, fg="white", font=FONT_BTN, command=self.save_expense).pack(pady=10)
        tk.Button(self, text="Back", bg="#e5e7eb", fg="#111827", font=FONT_BTN,
                  command=lambda: self.controller.show_page(MainMenuPage)).pack()

    def save_expense(self):  # <--- replacement continues here
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            notes = self.notes_entry.get()
            save_expense_ui(amount, category, notes)
            messagebox.showinfo("Saved", f"Expense of RM {amount:.2f} added successfully.")
            self.amount_entry.delete(0, tk.END)
            self.category_combo.set("Food")
            self.notes_entry.delete(0, tk.END)
            self.controller.show_page(MainMenuPage)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number for amount.")



class TransactionsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)
        self.controller = controller
        self._build()

    def _build(self):
        tk.Label(self, text="All Transactions", font=FONT_TITLE, bg=APP_BG, fg=TITLE_COLOR).pack(pady=20)
        self.tree_frame = tk.Frame(self, bg=APP_BG)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("date", "type", "category/source", "amount", "notes")
        self.tree = ttk.Treeview(self.tree_frame, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="center")
        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=APP_BG)
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Delete Selected", bg=BTN_DANGER, fg="white", font=FONT_BTN,
                  command=self.delete_selected).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Clear All", bg="#b45309", fg="white", font=FONT_BTN,
                  command=self.clear_all).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Back to Menu", bg=BTN_PRIMARY, fg="white", font=FONT_BTN,
                  command=lambda: self.controller.show_page(MainMenuPage)).pack(side="left", padx=8)

    def on_show(self):
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        txs = get_transactions()
        if not txs:
            self.tree.insert("", "end", values=("—", "—", "—", "—", "No transactions"))
            return

        for t in reversed(txs):
            date = t.get("date", "—")
            ttype = t.get("type", "").capitalize()
            cat_or_src = t.get("category", t.get("source", "—"))
            amt = f"+RM{t['amount']:.2f}" if t.get("type") == "income" else f"-RM{t['amount']:.2f}"
            notes = t.get("notes", "")
            self.tree.insert("", "end", values=(date, ttype, cat_or_src, amt, notes))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a transaction to delete.")
            return
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected transaction?"):
            index = len(get_transactions()) - self.tree.index(selected[0]) - 1
            delete_transaction(index)
            self.refresh_table()

    def clear_all(self):
        if messagebox.askyesno("Confirm Clear All", "Are you sure you want to delete ALL transactions?"):
            clear_all_transactions()
            self.refresh_table()

class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)
        self.controller = controller

        # Title
        tk.Label(self, text="Summary", font=FONT_TITLE, bg=APP_BG, fg=TITLE_COLOR)\
            .pack(pady=10)

        # Summary text
        self.summary_label = tk.Label(self, text="", font=FONT_SUB, bg=APP_BG, justify="left")
        self.summary_label.pack(pady=(10, 5))

        # Chart frame
        self.chart_frame = tk.Frame(self, bg=APP_BG)
        self.chart_frame.pack(pady=(5, 50))  # extra bottom padding to make room for button

        # Back button (always at bottom with enough gap)
        self.back_btn = tk.Button(self, text="Back to Menu", bg=BTN_PRIMARY, fg="white", font=FONT_BTN,
                                  command=lambda: self.controller.show_page(MainMenuPage))
        self.back_btn.pack(side="bottom", pady=40)  # push button up

    def on_show(self):
        # Update summary text
        self.summary_label.config(text=get_summary())

        # Clear old chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        # Create pie chart if data exists
        expense_data = get_expense_summary()
        if expense_data:
            fig, ax = plt.subplots(figsize=(2.5, 2.5))  # smaller chart
            ax.pie(expense_data.values(), labels=expense_data.keys(), autopct="%1.1f%%")
            ax.set_title("Expense Breakdown", fontsize=12)
            chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().pack()




class TipsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)
        self.controller = controller
        self._build()

    def _build(self):
        # Title
        tk.Label(self, text="AI Budgeting Tip", font=FONT_TITLE, bg=APP_BG, fg=TITLE_COLOR)\
            .pack(pady=20)

        # Frame for scrollable tip area
        tip_frame = tk.Frame(self, bg=APP_BG)
        tip_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Scrollbar (vertical only)
        scrollbar = tk.Scrollbar(tip_frame)
        scrollbar.pack(side="right", fill="y")

        # Text widget with word wrapping
        self.tip_box = tk.Text(
            tip_frame, font=FONT_SUB, bg=APP_BG, fg=SUBTITLE_COLOR,
            wrap="word", yscrollcommand=scrollbar.set, relief="flat"
        )
        self.tip_box.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tip_box.yview)

        # Make text read-only
        self.tip_box.config(state="disabled")

        # Buttons frame (fixed at bottom)
        btn_frame = tk.Frame(self, bg=APP_BG)
        btn_frame.pack(side="bottom", pady=10)

        # Generate tip button
        tk.Button(
            btn_frame, text="Generate AI Tip", bg=BTN_PRIMARY, fg="white", font=FONT_BTN,
            command=self.show_tip
        ).pack(side="left", padx=8)

        # Back button
        tk.Button(
            btn_frame, text="Back to Menu", bg="#e5e7eb", fg="#111827", font=FONT_BTN,
            command=lambda: self.controller.show_page(MainMenuPage)
        ).pack(side="left", padx=8)

    def show_tip(self):
        """Fetch and display AI-generated tip with loading state."""
        # Enable editing to update content
        self.tip_box.config(state="normal")
        self.tip_box.delete("1.0", tk.END)
        self.tip_box.insert(tk.END, "Loading tip... Please wait.")
        self.tip_box.config(state="disabled")
        self.update_idletasks()

        try:
            tip = get_ai_tip()
            self.tip_box.config(state="normal")
            self.tip_box.delete("1.0", tk.END)
            self.tip_box.insert(tk.END, tip)
            self.tip_box.config(state="disabled")
        except Exception as e:
            self.tip_box.config(state="normal")
            self.tip_box.delete("1.0", tk.END)
            self.tip_box.insert(tk.END, f"Error: {e}")
            self.tip_box.config(state="disabled")
