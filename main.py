import sys
from PySide6.QtWidgets import (QApplication,QStackedWidget) 
from gui import ExpenseTracker

if __name__ == "__main__":
    app = QApplication(sys.argv)#to take inputs
    window = ExpenseTracker() 
    window.show()
    sys.exit(app.exec())#Ensures a clean exit when the application is closed.
        