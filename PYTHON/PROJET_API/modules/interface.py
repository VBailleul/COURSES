from PyQt5.QtWidgets import (QMainWindow, QApplication, QLineEdit, QPushButton,
                             QFileDialog, QTextBrowser)
import sys
import os


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        _height, _width = 360, 520
        self.response = "No file selected"
        self.save_file = ""
        self.texte = ""
        self.setFixedSize(_height, _width)
        self.set_file()
        self.genes_browser()
        self.launch()

    def set_file(self):
        file_launcher = QPushButton("Select your file", self)
        file_launcher.setGeometry(20, 20, 150, 50)
        self.file_viewer = QLineEdit(self.response, self)
        self.file_viewer.setGeometry(190, 20, 150, 50)
        file_launcher.clicked.connect(self.get_file)
        file_launcher.clicked.connect(self.file_opener)

    def genes_browser(self):
        self.query_list = QTextBrowser(self)
        self.query_list.setGeometry(20, 90, 320, 340)

    def launch(self):
        self.launch_button = QPushButton("Launch your analysis", self)
        self.launch_button.setGeometry(20, 450, 320, 50)
        self.launch_button.clicked.connect(self.action_button_save_file)
        self.launch_button.clicked.connect(self.close)

    def get_file(self):
        file_filter = 'Text files(*.txt)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter
        )
        self.file_viewer.setText(response[0].split("/")[-1])
        self.response = response[0]

    def action_button_save_file(self):
        file_filter = 'HTML files(*.html)'
        response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a data file',
            directory='Data File.dat',
            filter=file_filter,
            initialFilter='HTML files(*.html)'
        )
        self.save_file = response[0]

    def get_save_file(self):
        return self.save_file

    def file_opener(self):
        with open(self.response, "r") as f:
            self.texte = [i.rstrip() for i in f.readlines()]
            self.query_list.setText("\n".join(self.texte))

    def get_text(self):
        return self.texte


def main():
    app = QApplication(sys.argv)
    launcher = Window()
    launcher.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
