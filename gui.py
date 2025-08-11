from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QStackedWidget
)
from PySide6.QtCore import QDate
from tracker import add_expense, delete_selected_expense, get_expenses, modify
from pages import create_expense_page, create_home_page, create_insight_page,create_monthly_expense,create_daily_expense,create_monthly_analysis


class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 500, 600)

        # Stacked widget to switch pages
        self.stack = QStackedWidget()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)   
        self.setLayout(main_layout)

        # Create pages (pass main_window as argument so pages can access it)
        self.home_page = create_home_page(main_window=self)
        self.expense_page = create_expense_page(main_window=self)
        self.insight_page = create_insight_page(main_window=self)
        self.monthly_expense = create_monthly_expense(main_window=self)
        self.daily_expense= create_daily_expense(main_window=self)
        self.monthly_analysis=create_monthly_analysis(main_window=self)
        
        # Add pages to stack
        self.stack.addWidget(self.home_page)     # index 0
        self.stack.addWidget(self.expense_page)  # index 1
        self.stack.addWidget(self.insight_page)  # index 2
        self.stack.addWidget(self.monthly_expense)#index 3
        self.stack.addWidget(self.daily_expense)#index 4
        self.stack.addWidget(self.monthly_analysis)#index 5
        # Show home page first
        self.stack.setCurrentIndex(0)