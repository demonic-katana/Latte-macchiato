import sqlite3
import sys
from addEditCoffeeForm import Ui_MainWindow
from diolog_window import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Капучино')
        self.setupUi(self)
        self.update_.clicked.connect(self.update)
        self.new_.clicked.connect(self.new)
        self.write()

    def update(self):
        global d
        if not d:
            d = DialogWindow('Редактировать', self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
            d.show()

    def new(self):
        global d
        if not d:
            d = DialogWindow('Новая запись')
            d.show()

    def write(self):
        self.con = sqlite3.connect("data/coffee.sqlite")
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM main").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах',
                                                    'Описание вкуса', 'Цена (руб.)', 'Объем упаковки (г.)'])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


class DialogWindow(QWidget, Ui_Form):
    def __init__(self, title, row=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(title)
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        self.close_.clicked.connect(self.close)
        self.run_.clicked.connect(self.run)
        self.row = row
        if self.row:
            res = cur.execute(f"""SELECT * FROM main WHERE id = {self.row}""").fetchone()
            n = 1
            for i in [self.variety_name, self.degree_of_roast, self.ground_or_in_grains, self.taste_description,
                      self.price, self.packing_volume]:
                i.setText(str(res[n]))
                n += 1
        con.close()

    def run(self):
        con = sqlite3.connect('data/coffee.sqlite')
        cur = con.cursor()
        if self.row:
            cur.execute(f"""Delete from main where id = {self.row}""").fetchall()
        cur.execute(f"""INSERT INTO main (variety_name, degree_of_roast, ground_or_in_grains, taste_description,
                    price, packing_volume) 
                    VALUES ('{self.variety_name.text()}', {self.degree_of_roast.text()},
                    '{self.ground_or_in_grains.text()}', '{self.taste_description.text()}', 
                    {self.price.text()}, {self.packing_volume.text()})""")
        con.commit()
        con.close()
        self.closeEvent(self)

    def close(self):
        self.closeEvent(self)

    def closeEvent(self, event):
        global d
        d = None
        ex.write()


def excepthook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = excepthook
    d = None
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
