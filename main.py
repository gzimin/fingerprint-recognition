import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui
import design  # Это наш конвертированный файл дизайна
import recognition


class RecognitionApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    path_to_source_file = ''

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.post_ui_setup()

    def post_ui_setup(self):
        self.loadImage.clicked.connect(self.choose_file)
        self.processImage.clicked.connect(self.process_image)
        self.processImage_2.clicked.connect(self.process_image_with_another_method)

    def choose_file(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Choose fingerprint source file",
                                                                directory="fingerprint-db",
                                                                filter="Image Files (*.png *.jpg *.bmp)")
        self.path_to_source_file = directory[0]
        self.load_pic_to_window_left()

    def load_pic_to_window_left(self):
        file_pixmap = QtGui.QPixmap(self.path_to_source_file)
        self.sourceImgLabel.setScaledContents(True)
        self.sourceImgLabel.setPixmap(file_pixmap)

    def process_image(self):
        if self.path_to_source_file == '':
            return
        reconAlgorithm = recognition.Recognition(self.path_to_source_file)
        recon_image = reconAlgorithm.new_path
        found_image = reconAlgorithm.final_recon_path

        self.load_pic_to_window_right(recon_image)
        self.load_recon_image(found_image)
        self.load_text_to_recon_info(reconAlgorithm.result)

    def process_image_with_another_method(self):
        if self.path_to_source_file == '':
            return
        recAlg = recognition.RecognitionCompareMethod(
            self.path_to_source_file, 10)
        if not recAlg.path_to_recon_image:
            result = "Didn't found any matches"
            self.load_text_to_recon_info(result)
        else:
            self.load_recon_image(recAlg.path_to_recon_image)
            result = "We find it, it's - {}".format(recAlg.path_to_recon_image)
            self.load_text_to_recon_info(result)

    def load_pic_to_window_right(self, recon_image_path):
        file_pixmap = QtGui.QPixmap(recon_image_path)
        self.procImageLabel.setScaledContents(True)
        self.procImageLabel.setPixmap(file_pixmap)

    def load_recon_image(self, final_image_path):
        file_pixmap = QtGui.QPixmap(final_image_path)
        self.foundImageLabel.setScaledContents(True)
        self.foundImageLabel.setPixmap(file_pixmap)

    def load_text_to_recon_info(self, text_to_set):
        self.infoAboutImage.setPlainText(text_to_set)

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = RecognitionApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()