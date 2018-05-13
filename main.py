import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui
import design  # Это наш конвертированный файл дизайна


class RecognitionApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.post_ui_setup()

    def post_ui_setup(self):
        self.loadImage.clicked.connect(self.choose_file)

    def choose_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Choose fingerprint source file",
                                                                directory="fingerprint-db",
                                                                filter="Image Files (*.png *.jpg *.bmp)")
        self.load_pic_to_window(directory[0])

    def load_pic_to_window(self, path_to_file):
        file_pixmap = QtGui.QPixmap(path_to_file)
        self.sourceImgLabel.setScaledContents(True)
        self.sourceImgLabel.setPixmap(file_pixmap)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = RecognitionApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()