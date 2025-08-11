from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox,QHBoxLayout,QTextEdit,QSizePolicy,
)
from PySide6.QtCore import (QDate,Qt)
from tracker import add_expense, delete_selected_expense, get_expenses, modify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

def create_expense_page(main_window):
    page = QWidget()
    layout = QVBoxLayout()
   
    main_window.setStyleSheet("""
    QWidget {
        background-color: #f4f6f8;
        color: #2d2d2d;
        font-family: 'Segoe UI';
        font-size: 14px;
    }

    QLabel {
        font-weight: 500;
        color: #2d2d2d;
        margin-bottom: 4px;
    }

    QLineEdit, QTextEdit, QDateEdit {
        background-color: #ffffff;
        color: #2d2d2d;
        border: 1px solid #d0d5da;
        border-radius: 6px;
        padding: 8px;
    }

    QPushButton {
        background-color: #0078d7;
        color: white;
        font-weight: 600;
        font-size: 14px;
        padding: 5px 10px;
        border: none;
        border-radius: 3px;
        margin-top: 4px;
    }

    QPushButton:hover {
        background-color: #005fa3;
    }

    QTableWidget {
        background-color: #ffffff;
        gridline-color: #d0d5da;
        border-radius: 6px;
        padding: 5px;
        color: #2d2d2d;
    }

    QHeaderView::section {
        background-color: #e2e6ea;
        color: #2d2d2d;
        font-weight: bold;
        padding: 6px;
        border: none;
    }

    QScrollBar:vertical {
        background: #f4f6f8;
        width: 12px;
        margin: 0px;
    }

    QScrollBar::handle:vertical {
        background: #cccccc;
        border-radius: 5px;
        min-height: 20px;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        background: none;
    }
""")



    # Amount
    layout.addWidget(QLabel("Amount:"))
    main_window.amount_entry = QLineEdit()
    layout.addWidget(main_window.amount_entry)

    # Description
    layout.addWidget(QLabel("Description:"))
    main_window.description_entry = QLineEdit()
    layout.addWidget(main_window.description_entry)

    # Date
    layout.addWidget(QLabel("Date:"))
    main_window.date_entry = QDateEdit()
    main_window.date_entry.setDate(QDate.currentDate())
    layout.addWidget(main_window.date_entry)

    # Add Button
    add_button = QPushButton("Add Expense")
    add_button.clicked.connect(lambda: handle_add_expense(main_window))
    layout.addWidget(add_button)

    # Expense Table
    main_window.expense_list = QTableWidget()
    main_window.expense_list.setColumnCount(3)
    main_window.expense_list.setHorizontalHeaderLabels(["Amount", "Description", "Date"])
    main_window.expense_list.setSelectionBehavior(QTableWidget.SelectRows)
    layout.addWidget(main_window.expense_list)

    # Delete Button
    delete_button = QPushButton("Delete Expense")
    delete_button.clicked.connect(lambda: delete_expense(main_window))
    layout.addWidget(delete_button)

    # Modify Button
    modify_button = QPushButton("Modify Expense")
    modify_button.clicked.connect(lambda: modify_expense(main_window))
    layout.addWidget(modify_button)

    # Back Button
    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: main_window.stack.setCurrentIndex(0))
    layout.addWidget(back_button)

    page.setLayout(layout)
    load_expenses(main_window)
    return page


def handle_add_expense(main_window):
    amount = main_window.amount_entry.text().strip()
    description = main_window.description_entry.text().strip()
    date = main_window.date_entry.date().toString("dd-MM-yyyy")

    if not amount.isdigit():
        QMessageBox.warning(main_window, "Invalid Input", "Amount should be a number.")
        return

    if not description:
        QMessageBox.warning(main_window, "Invalid Input", "Description cannot be empty.")
        return

    add_expense(amount, description, date)
    row = main_window.expense_list.rowCount()
    main_window.expense_list.insertRow(row)
    main_window.expense_list.setItem(row, 0, QTableWidgetItem(amount))
    main_window.expense_list.setItem(row, 1, QTableWidgetItem(description))
    main_window.expense_list.setItem(row, 2, QTableWidgetItem(date))

    main_window.amount_entry.clear()
    main_window.description_entry.clear()


def delete_expense(main_window):
    selected = main_window.expense_list.selectedItems()
    if not selected:
        return
    row = main_window.expense_list.row(selected[0])
    selected_text = [item.text() for item in selected]
    delete_selected_expense(selected_text)
    main_window.expense_list.removeRow(row)


def modify_expense(main_window):
    selected = main_window.expense_list.selectedItems()
    if not selected:
        return

    row = main_window.expense_list.row(selected[0])
    selected_text = [item.text() for item in selected]
    modify(selected_text)

    amount = main_window.expense_list.item(row, 0).text()
    description = main_window.expense_list.item(row, 1).text()
    date = main_window.expense_list.item(row, 2).text()

    main_window.amount_entry.setText(amount)
    main_window.description_entry.setText(description)
    main_window.date_entry.setDate(QDate.fromString(date, "dd-MM-yyyy"))

    main_window.expense_list.removeRow(row)


def load_expenses(main_window):
    expenses = get_expenses()  # Should return a list of [amount, description, date]
    for expense in expenses:
        if len(expense) < 3:
            continue

        amount, description, date = expense[:3]

        row = main_window.expense_list.rowCount()
        main_window.expense_list.insertRow(row)
        main_window.expense_list.setItem(row, 0, QTableWidgetItem(amount))
        main_window.expense_list.setItem(row, 1, QTableWidgetItem(description))
        main_window.expense_list.setItem(row, 2, QTableWidgetItem(date))


def create_home_page(main_window):
    home = QWidget()
    layout = QVBoxLayout()

    welcome_label = QLabel("🏠 Welcome to Expense Tracker!")
    welcome_label.setStyleSheet("""
    font-size: 24px;
    font-weight: bold;
    color: #ffffff;
    background-color: #3c3f41;
    padding: 10px;
    border-radius: 8px;
""")

    layout.addWidget(welcome_label)

    start_button = QPushButton("➡ Go to Expense Manager")
    insights_button = QPushButton("➡ Insights")

    start_button.clicked.connect(lambda: main_window.stack.setCurrentIndex(1))
    insights_button.clicked.connect(lambda: main_window.stack.setCurrentIndex(2))

    layout.addWidget(start_button)
    layout.addWidget(insights_button)

    home.setLayout(layout)
    return home


def create_insight_page(main_window):
    page_2 = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(QLabel("WELCOME TO INSIGHTS PAGE"))
    summary=QPushButton("MONTHLY EXPENSES")# it will give detail analysis of how much amount of money is spend into what
    summary.clicked.connect(lambda: main_window.stack.setCurrentIndex(3))
    layout.addWidget(summary)
    
    daily=QPushButton("DAILY EXPENSES")
    layout.addWidget(daily)
    daily.clicked.connect(lambda:main_window.stack.setCurrentIndex(4))
    
    bar=QPushButton("MONTHLY ANALYSIS")
    layout.addWidget(bar)
    bar.clicked.connect(lambda:main_window.stack.setCurrentIndex(5))
    

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: main_window.stack.setCurrentIndex(0))
    layout.addWidget(back_button)

    page_2.setLayout(layout)
    return page_2

def create_monthly_expense(main_window):
    page_3 = QWidget()
    layout = QVBoxLayout()

    # Row for month and year
    date_row = QHBoxLayout()
    main_window.daily_graph_layout_1 = layout
    date_row.addWidget(QLabel("Month:"))
    main_window.month_entry = QLineEdit()
    main_window.month_entry.setPlaceholderText("e.g., 07")
    main_window.month_entry.setFixedWidth(80)
    date_row.addWidget(main_window.month_entry)

    date_row.addSpacing(20)

    date_row.addWidget(QLabel("Year:"))
    main_window.year_entry = QLineEdit()
    main_window.year_entry.setPlaceholderText("e.g., 2025")
    main_window.year_entry.setFixedWidth(100)
    date_row.addWidget(main_window.year_entry)

    layout.addLayout(date_row)

    # Search button
    search = QPushButton("Search")
    search.clicked.connect(lambda: filter_expense(main_window))
    layout.addWidget(search)

    # Analysis section
    layout.addWidget(QLabel("ANALYSIS:"))
    main_window.analysis_entry = QTextEdit()
    main_window.analysis_entry.setReadOnly(True)
    main_window.analysis_entry.setFixedWidth(450)
    layout.addWidget(main_window.analysis_entry)

    # Back button
    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: main_window.stack.setCurrentIndex(2))
    layout.addWidget(back_button)

    # Finalize
    page_3.setLayout(layout)
    return page_3

def filter_expense(main_window):
    # Step 1: Get user input
    month_input = main_window.month_entry.text().strip().zfill(2)  # pad "7" → "07"
    year_input = main_window.year_entry.text().strip()

    # Step 2: Get all expenses
    expenses = get_expenses()  # [["200", "Groceries", "2025-07-09"], ["150", "Books", "2025-06-01"]]

    # Step 3: Filter by month & year
    filtered_expenses = []
    for expense in expenses:
        if len(expense) < 3:
            continue  # skip invalid rows

        amount, description, date = expense[:3]
        _,m,y= date.split("-")

        if m == month_input and y == year_input:
            filtered_expenses.append(expense)

    # Step 4: Category-wise sorting
    food_keywords = ["food", "groceries", "restaurant", "snack"]
    transport_keywords = ["transport", "bus", "uber", "auto", "cab", "fuel"]
    lifestyle_keywords = ["shopping", "clothes", "entertainment", "lifestyle"]

    food = []
    transport = []
    lifestyle = []
    other = []

    for exp in filtered_expenses:
        amount, description, date = exp[:3]
        desc_lower = description.lower()

        if any(keyword in desc_lower for keyword in food_keywords):
            food.append(exp)
        elif any(keyword in desc_lower for keyword in transport_keywords):
            transport.append(exp)
        elif any(keyword in desc_lower for keyword in lifestyle_keywords):
            lifestyle.append(exp)
        else:
            other.append(exp)

    # Step 5: Calculate total
    def calc_total(exp_list):
        total=0
        for e in exp_list:
            total= total+int(e[0])
        return total
    total = calc_total(filtered_expenses)
    food_total = calc_total(food)
    transport_total = calc_total(transport)
    lifestyle_total = calc_total(lifestyle)
    other_total = calc_total(other)

    # Step 6: Print or show breakdown
    print(f"\n--- Monthly Breakdown ({month_input}-{year_input}) ---")
    print("Food:", food_total)
    print("Transport:", transport_total)
    print("Lifestyle:", lifestyle_total)
    print("Other:", other_total)
    print("Total:", total)

    breakdown_text = (
        f"Monthly Breakdown ({month_input}-{year_input}):\n"
        f"🧁 Food: ₹{food_total}\n"
        f"🚌 Transport: ₹{transport_total}\n"
        f"🛍️ Lifestyle: ₹{lifestyle_total}\n"
        f"📦 Other: ₹{other_total}\n"
        f"💰 Total: ₹{total}"
    )

    # Step 7: Update GUI
    main_window.analysis_entry.setText(breakdown_text)
    canvas = MatplotlibCanvas(main_window, width=5, height=4, dpi=100)

    categories = ['Food', 'Rent', 'Entertainment', 'Transport']
    expenses = [food_total,lifestyle_total, other_total,transport_total]

    canvas.axes.clear()
    canvas.axes.pie(expenses, labels=categories, autopct='%1.1f%%')
    canvas.axes.set_title("Expense Breakdown")
    canvas.draw()
    main_window.daily_graph_layout_1.addWidget(canvas)


    

    # Optional: Show filtered expenses in the table (you can uncomment this if UI is ready)
    # main_window.expense_list.setRowCount(0)
    # for row_data in filtered_expenses:
    #     row_index = main_window.expense_list.rowCount()
    #     main_window.expense_list.insertRow(row_index)
    #     for col, value in enumerate(row_data):
    #         item = QTableWidgetItem(str(value))
    #         main_window.expense_list.setItem(row_index, col, item)

    

def create_daily_expense(main_window):
    page_4 = QWidget()
    layout = QVBoxLayout()
    date_row = QHBoxLayout()
    main_window.daily_graph_layout = layout
    
    date_row.addWidget(QLabel("date:"))
    main_window.daily_date_entry = QLineEdit()
    main_window.daily_date_entry.setPlaceholderText("e.g., 31")
    main_window.daily_date_entry.setFixedWidth(80)
    date_row.addWidget(main_window.daily_date_entry)

    date_row.addSpacing(20)

    date_row.addWidget(QLabel("Month:"))
    main_window.daily_month_entry = QLineEdit()
    main_window.daily_month_entry.setPlaceholderText("e.g., 07")
    main_window.daily_month_entry.setFixedWidth(80)
    date_row.addWidget(main_window.daily_month_entry)

    date_row.addSpacing(20)

    date_row.addWidget(QLabel("Year:"))
    main_window.daily_year_entry = QLineEdit()
    main_window.daily_year_entry.setPlaceholderText("e.g., 2025")
    main_window.daily_year_entry.setFixedWidth(100)
    date_row.addWidget(main_window.daily_year_entry)

    layout.addLayout(date_row)

    # Search button
    search = QPushButton("Search")
    search.clicked.connect(lambda: filtering_expense(main_window))
    layout.addWidget(search)

    # Analysis section
    layout.addWidget(QLabel("ANALYSIS:"))
    main_window.daily_analysis_entry = QTextEdit()
    main_window.daily_analysis_entry.setReadOnly(True)
    main_window.daily_analysis_entry.setFixedWidth(450)
    layout.addWidget(main_window.daily_analysis_entry)

    # Back button
    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: main_window.stack.setCurrentIndex(2))
    layout.addWidget(back_button)

    # Finalize
    page_4.setLayout(layout)
    return page_4

def filtering_expense(main_window):
     # Step 1: Get user input
        date_input = main_window.daily_date_entry.text().strip().zfill(2)
        month_input = main_window.daily_month_entry.text().strip().zfill(2)  # pad "7" → "07"
        year_input = main_window.daily_year_entry.text().strip()

        # Step 2: Get all expenses
        expenses = get_expenses()  # [["200", "Groceries", "2025-07-09"], ["150", "Books", "2025-06-01"]]

        # Step 3: Filter by month & year
        filtered_expenses = []
        for expense in expenses:
            if len(expense) < 3:
                continue  # skip invalid rows

            amount, description, date = expense[:3]
            d,m,y= date.split("-")

            if   d==date_input and m == month_input and y == year_input:
                filtered_expenses.append(expense)

        # Step 4: Category-wise sorting
        food_keywords = ["food", "groceries", "restaurant", "snack"]
        transport_keywords = ["transport", "bus", "uber", "auto", "cab", "fuel"]
        lifestyle_keywords = ["shopping", "clothes", "entertainment", "lifestyle"]

        food = []
        transport = []
        lifestyle = []
        other = []

        for exp in filtered_expenses:
            amount, description, date = exp[:3]
            desc_lower = description.lower()

            if any(keyword in desc_lower for keyword in food_keywords):
                food.append(exp)
            elif any(keyword in desc_lower for keyword in transport_keywords):
                transport.append(exp)
            elif any(keyword in desc_lower for keyword in lifestyle_keywords):
                lifestyle.append(exp)
            else:
                other.append(exp)

        # Step 5: Calculate total
        def calc_total(exp_list):
            total=0
            for e in exp_list:
                total= total+int(e[0])
            return total
        total = calc_total(filtered_expenses)
        food_total = calc_total(food)
        transport_total = calc_total(transport)
        lifestyle_total = calc_total(lifestyle)
        other_total = calc_total(other)

        # Step 6: Print or show breakdown
        print(f"\n---Daily Breakdown ( {date_input}-{month_input}-{year_input}) ---")
        print("Food:", food_total)
        print("Transport:", transport_total)
        print("Lifestyle:", lifestyle_total)
        print("Other:", other_total)
        print("Total:", total)

        breakdown_text = (
            f"Daily Breakdown ( {date_input}-{month_input}-{year_input}):\n"
            f"🧁 Food: ₹{food_total}\n"
            f"🚌 Transport: ₹{transport_total}\n"
            f"🛍️ Lifestyle: ₹{lifestyle_total}\n"
            f"📦 Other: ₹{other_total}\n"
            f"💰 Total: ₹{total}"
        )

        # Step 7: Update GUI
        main_window.daily_analysis_entry.setText(breakdown_text)
        # categories = ['Food', 'Lifestyle', 'Other', 'Transport']
        # expenses = [food_total,lifestyle_total, other_total,transport_total]
        # plt.pie(expenses, labels=categories, autopct='%1.1f%%')
        # plt.title('Expense Breakdown by Category')
        # plt.show()
        canvas = MatplotlibCanvas(main_window, width=5, height=4, dpi=100)

        categories = ['Food', 'Rent', 'Entertainment', 'Transport']
        expenses = [food_total,lifestyle_total, other_total,transport_total]

        canvas.axes.clear()
        canvas.axes.pie(expenses, labels=categories, autopct='%1.1f%%')
        canvas.axes.set_title("Expense Breakdown")
        canvas.draw()
        main_window.daily_graph_layout.addWidget(canvas)

def create_monthly_analysis(main_window):
    page_5 = QWidget()
    layout = QVBoxLayout()
    title = QLabel("Monthly Expense Comparison")
    title.setStyleSheet("font-weight: bold; font-size: 16px")
    layout.addWidget(title)

    # Graph Layout Holder
    main_window.monthly_bar_layout = QVBoxLayout()
    layout.addLayout(main_window.monthly_bar_layout)
     # Back button
    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: main_window.stack.setCurrentIndex(2))
    layout.addWidget(back_button)

    # Finalize
    page_5.setLayout(layout)
    show_monthly_bar_graph(main_window)
    return page_5
def show_monthly_bar_graph(main_window):
    # Step 1: Collect and group expenses
    expenses = get_expenses()  # Format: [["200", "Food", "09-07-2025"], ...]

    monthly_totals = {}  # key: "07-2025", value: total_expense

    for exp in expenses:
            if len(exp) < 3:
                continue  # 💡 Prevent crash if data is bad

            amount, _, date = exp[:3]
            day, month, year = date.split("-")
            key = f"{month}-{year}"  # e.g., "07-2025"
            monthly_totals[key] = monthly_totals.get(key, 0) + int(amount)

    # Step 2: Sort months chronologically
    sorted_keys = sorted(monthly_totals.keys(), key=lambda x: (x.split("-")[1], x.split("-")[0]))
    totals = [monthly_totals[k] for k in sorted_keys]

    # Step 3: Create and show canvas
    canvas = MatplotlibCanvas(main_window, width=4, height=2.5, dpi=90)
    canvas.axes.clear()
    canvas.axes.bar(sorted_keys, totals, color="skyblue")
    canvas.axes.set_title("Total Monthly Expenses")
    canvas.axes.set_ylabel("Amount (₹)")
    canvas.axes.set_xlabel("Month-Year")
    canvas.axes.set_title("Monthly Expenses", fontsize=10)
    canvas.axes.set_ylabel("Amount (₹)", fontsize=9)
    canvas.axes.set_xlabel("Month-Year", fontsize=9)
    canvas.axes.tick_params(axis='x', labelsize=8, rotation=45)
    canvas.axes.tick_params(axis='y', labelsize=8)
    canvas.setMinimumHeight(int(main_window.height() * 0.5))  # Adjust this if you want more/less
    canvas.setMinimumWidth(int(main_window.width() * 0.75))
    canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    canvas.draw()

    # Clear old canvas if needed
    while main_window.monthly_bar_layout.count():
        item = main_window.monthly_bar_layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.setParent(None) 

    main_window.monthly_bar_layout.addWidget(canvas)
