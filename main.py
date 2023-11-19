import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QPushButton, QLabel, QLineEdit
from PyQt5 import  QtCore


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI(self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.load_table()
        self.addButton.clicked.connect(self.add_coffee_click)
        self.tableWidget.cellChanged.connect(self.cell_canged)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(565, 415)
        self.tableWidget = QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(20, 40, 531, 381))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.addButton = QPushButton(Form)
        self.addButton.setGeometry(QtCore.QRect(20, 10, 75, 23))
        self.addButton.setObjectName("addButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Coffee!"))
        self.addButton.setText(_translate("Form", "Добавить"))

    def load_table(self):
        cur = self.con.cursor()
        result = cur.execute(f"Select * from Coffee").fetchall()

        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        titles = ['id', 'название', 'степень обжарки', 'молотый или нет', 'описание вкуса', 'цена', 'объём']
        self.tableWidget.setVerticalHeaderLabels(titles)
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


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.doneButton.clicked.connect(self.done)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 220)
        self.title = QLineEdit(Form)
        self.title.setGeometry(QtCore.QRect(120, 10, 271, 20))
        self.title.setObjectName("title")
        self.roastingLevel = QLineEdit(Form)
        self.roastingLevel.setGeometry(QtCore.QRect(120, 40, 271, 20))
        self.roastingLevel.setObjectName("roastingLevel")
        self.ground = QLineEdit(Form)
        self.ground.setGeometry(QtCore.QRect(120, 70, 271, 20))
        self.ground.setObjectName("ground")
        self.tasteDescription = QLineEdit(Form)
        self.tasteDescription.setGeometry(QtCore.QRect(120, 100, 271, 20))
        self.tasteDescription.setObjectName("tasteDescription")
        self.price = QLineEdit(Form)
        self.price.setGeometry(QtCore.QRect(120, 130, 271, 20))
        self.price.setObjectName("price")
        self.volume = QLineEdit(Form)
        self.volume.setGeometry(QtCore.QRect(120, 160, 271, 21))
        self.volume.setObjectName("volume")
        self.label = QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 20))
        self.label.setObjectName("label")
        self.label_2 = QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 101, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 101, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 101, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 101, 20))
        self.label_5.setObjectName("label_5")
        self.label_6 = QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 160, 101, 20))
        self.label_6.setObjectName("label_6")
        self.doneButton = QPushButton(Form)
        self.doneButton.setGeometry(QtCore.QRect(10, 190, 381, 23))
        self.doneButton.setObjectName("doneButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

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
