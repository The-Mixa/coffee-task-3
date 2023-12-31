import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QLabel, QLineEdit
from PyQt5 import QtCore
from main_design import Ui_Form_Main
from addEditCoffeeForm import Ui_Form


class Coffee(QMainWindow, Ui_Form_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.load_table()
        self.addButton.clicked.connect(self.add_coffee_click)
        self.tableWidget.cellChanged.connect(self.cell_canged)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Coffee!"))
        self.addButton.setText(_translate("Form", "Добавить"))

    def load_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"Select * from Coffee").fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        titles = ['id', 'название', 'степень обжарки', 'молотый/в зёрнах', 'описание вкуса', 'цена', 'объём']
        self.tableWidget.setHorizontalHeaderLabels(titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def add_coffee_click(self):
        self.add_form = AddWidget(self)
        self.add_form.show()

    def add_coffee(self, data):
        cur = self.con.cursor()
        i = self.tableWidget.rowCount() + 1
        data = [i] + data
        data = tuple(data)
        cur.execute(f'INSERT INTO coffee VALUES {data}')
        self.con.commit()

        self.tableWidget.setRowCount(i)
        for j, val in enumerate(data):
            self.tableWidget.setItem(i - 1, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def cell_canged(self, row, col):
        data = [self.tableWidget.item(row, j).text() for j in range(7)]
        data = [int(data[i]) if i in [0, 2, 5, 6] else data[i] for i in range(7)]
        data = tuple(data)

        cur = self.con.cursor()
        cur.execute(f'Delete from coffee where id = {data[0]}')
        cur.execute(f'Insert into coffee values {data}')
        self.con.commit()


class AddWidget(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.doneButton.clicked.connect(self.done)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить элемент"))
        self.label.setText(_translate("Form", "Название"))
        self.label_2.setText(_translate("Form", "Степень обжарки"))
        self.label_3.setText(_translate("Form", "Молотый или нет"))
        self.label_4.setText(_translate("Form", "Описание вкуса"))
        self.label_5.setText(_translate("Form", "Цена"))
        self.label_6.setText(_translate("Form", "Объём"))
        self.doneButton.setText(_translate("Form", "Добавить"))

    def done(self):
        title = self.title.text()
        roastinglevel = self.roastingLevel.text()
        ground = self.ground.text()
        taste_desk = self.tasteDescription.text()
        price = self.price.text()
        volume = self.volume.text()

        data = [title, roastinglevel, ground, taste_desk, price, volume]
        self.parent().add_coffee(data)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())