from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QInputDialog, QLabel
from PyQt5.QtCore import QSize
import sys
import webbrowser
import os
from image_combiner import cut_images, combine_images

class App(QWidget):
    # Inicialización de la aplicación
    def __init__(self):
        super().__init__()
        self.title = 'TheKDT_ Cortar y Unir'
        self.initUI()

    # Configuración de la interfaz de usuario
    def initUI(self):
        # Configuración del título y el icono de la ventana
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icono.ico'))
        
        # Configuración del layout principal
        self.layout = QVBoxLayout()

        # Etiqueta con instrucciones para el usuario
        self.label = QLabel("Selecciona una opción", self)
        self.layout.addWidget(self.label)

        # Botón para cortar imágenes
        self.button_cut = QPushButton('Cortar', self)
        self.button_cut.clicked.connect(self.cut_images_action)
        self.layout.addWidget(self.button_cut)

        # Botón para unir imágenes
        self.button_join = QPushButton('Unir', self)
        self.button_join.clicked.connect(self.join_images)
        self.layout.addWidget(self.button_join)

        # Botón para realizar donaciones
        self.button_donate = QPushButton('Donación', self)
        self.button_donate.clicked.connect(self.open_donation_link)
        self.layout.addWidget(self.button_donate)

        # Establecimiento del layout en la ventana
        self.setLayout(self.layout)

        self.button_cut.setStyleSheet("""
    QPushButton {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        padding: 6px 12px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        -webkit-transition-duration: 0.4s; /* Safari */
        transition-duration: 0.4s;
        cursor: pointer;
    }
    QPushButton:hover {
        background-color: #0056b3;
        color: white;
    }
""")

        self.button_join.setStyleSheet("""
    QPushButton {
        background-color: #28a745;
        color: white;
        border-radius: 10px;
        padding: 6px 12px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        -webkit-transition-duration: 0.4s; /* Safari */
        transition-duration: 0.4s;
        cursor: pointer;
    }
    QPushButton:hover {
        background-color: #218838;
        color: white;
    }
""")

        self.button_donate.setStyleSheet("""
    QPushButton {
        background-color: #FAFAFA;  # Un color de fondo que coincida con el de tu imagen para transiciones suaves
        color: white;
        border-radius: 15px;
        padding: 10px 20px;
        text-align: center;
        font-size: 16px;
        margin-top: 50px;  # Aumenta la separación del botón 'Donar' con respecto a los otros botones
        border: none;
    }
    QPushButton:hover {
        background-color: #E1E1E1;  # Un color ligeramente diferente para el efecto hover
    }
""")
        self.button_donate.setIcon(QIcon('path_to_your_icon.png'))
        self.button_donate.setIconSize(QSize(24, 24))

    # Acción para cortar imágenes
    def cut_images_action(self):
        # Se abre un diálogo para que el usuario seleccione una carpeta
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta para Cortar")
        if folder_path:
            # Se crea una subcarpeta donde se guardará el resultado del corte
            output_directory = os.path.join(folder_path, "Corte")
            os.makedirs(output_directory, exist_ok=True)
            
            # Se solicita al usuario el número de partes para cortar las imágenes
            parts, ok = QInputDialog.getInt(self, "Número de Partes", "¿En cuántas partes deseas cortar las imágenes?", 5, 1, 100)
            if ok:
                # Se procede a cortar las imágenes y se informa al usuario del éxito de la operación
                cut_images(folder_path, parts, output_directory)
                QMessageBox.information(self, "Éxito", "Las imágenes han sido cortadas correctamente y guardadas en el directorio seleccionado.")

    # Acción para unir imágenes
    def join_images(self):
        # Se abre un diálogo para que el usuario seleccione una carpeta
        folder_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta para Unir")
        if folder_path:
            # Se procede a unir las imágenes y se informa al usuario del éxito de la operación
            combine_images(folder_path, 'JPEG', folder_path)
            QMessageBox.information(self, "Éxito", "Las imágenes han sido unidas y guardadas correctamente en el directorio seleccionado.")

    # Acción para abrir una URL de donación
    def open_donation_link(self):
        # Se abre el navegador web por defecto en la URL de donación
        paypal_url = "https://www.paypal.me/thekdt12"
        webbrowser.open(paypal_url)

# Punto de entrada principal de la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())