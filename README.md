import io
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from manga_ocr import MangaOcr
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR con manga_ocr")
        
        # Maximizar la ventana en modo ventana
        self.root.state('zoomed')

        self.manga_ocr = MangaOcr()
        self.image_path = ''
        self.img = None
        self.tkimg = None
        self.rect = None
        self.zoom_level = 1.0  # Factor de zoom inicial

        # Configurar PanedWindow para dividir la UI
        self.setup_ui()

        # Configurar eventos de teclado para el zoom
        self.root.bind("<Control-plus>", lambda event: self.adjust_zoom(1.1))
        self.root.bind("<Control-minus>", lambda event: self.adjust_zoom(0.9))

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<ButtonPress-3>", self.on_right_click)

        ruta_del_directorio = os.path.dirname(os.path.abspath(__file__))
        ruta_del_archivo = os.path.join(ruta_del_directorio, 'mall/assets/example.jpg')

    def setup_ui(self):
        self.paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Configurar el lado izquierdo (imagen)
        self.setup_left_frame()

        # Configurar el lado derecho (texto)
        self.setup_right_frame()

        # Configurar el menú
        self.setup_menu()

    def setup_left_frame(self):
        self.frame_left = tk.Frame(self.paned_window)
        self.canvas = tk.Canvas(self.frame_left, cursor="cross")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_x = tk.Scrollbar(self.frame_left, orient="horizontal", command=self.canvas.xview)
        self.scroll_y = tk.Scrollbar(self.frame_left, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")

        self.paned_window.add(self.frame_left)

    def setup_right_frame(self):
        self.frame_right = tk.Frame(self.paned_window)
        self.text_area = scrolledtext.ScrolledText(self.frame_right)
        self.save_button = tk.Button(self.frame_right, text="Guardar", command=self.save_text)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.save_button.pack(side=tk.BOTTOM, pady=10)
        self.paned_window.add(self.frame_right)

    def setup_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        fileMenu = tk.Menu(menu)
        menu.add_cascade(label="Archivo", menu=fileMenu)
        fileMenu.add_command(label="Abrir...", command=self.load_image)
        fileMenu.add_separator()
        fileMenu.add_command(label="Salir", command=self.root.quit)

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image_path = path
            self.img = Image.open(self.image_path)
            self.update_image()

    def update_image(self):
        if self.img:
            img_zoomed = self.img.resize((int(self.img.width * self.zoom_level), int(self.img.height * self.zoom_level)), Image.Resampling.LANCZOS)
            self.tkimg = ImageTk.PhotoImage(img_zoomed)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tkimg)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def adjust_zoom(self, factor):
        self.zoom_level *= factor
        self.update_image()

    def save_text(self):
        text_to_save = self.text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_to_save)
            messagebox.showinfo("Guardar", f"El texto ha sido guardado en '{file_path}'.")

    def on_button_press(self, event):
    # Calcula las coordenadas reales teniendo en cuenta el nivel de zoom
        scaled_x = (self.canvas.canvasx(event.x)) / self.zoom_level
        scaled_y = (self.canvas.canvasy(event.y)) / self.zoom_level
        self.selection_start = (scaled_x, scaled_y)
    # Dibuja el rectángulo inicial en el canvas
        self.rect = self.canvas.create_rectangle(scaled_x, scaled_y, scaled_x, scaled_y, outline='red')

    def on_move_press(self, event):
    # Escala las coordenadas actuales según el zoom
        scaled_x = (self.canvas.canvasx(event.x)) / self.zoom_level
        scaled_y = (self.canvas.canvasy(event.y)) / self.zoom_level
    # Actualiza las coordenadas del rectángulo para permitir la selección desde cualquier esquina
        self.canvas.coords(self.rect, self.selection_start[0] * self.zoom_level, self.selection_start[1] * self.zoom_level, scaled_x * self.zoom_level, scaled_y * self.zoom_level)


    def on_button_release(self, event):
    # Escala las coordenadas finales según el zoom
        scaled_x = (self.canvas.canvasx(event.x)) / self.zoom_level
        scaled_y = (self.canvas.canvasy(event.y)) / self.zoom_level
        self.selection_end = (scaled_x, scaled_y)

    # Asegura que las coordenadas de selección se guarden en el orden correcto
        x0, x1 = sorted([self.selection_start[0], self.selection_end[0]])
        y0, y1 = sorted([self.selection_start[1], self.selection_end[1]])
        self.selection = [x0, y0, x1, y1]

        self.extract_text()


    def on_right_click(self, event):
        # Deseleccionar y eliminar el rectángulo actual
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
            self.selection_start = None
            self.selection_end = None


    def extract_text(self):
        if self.img and self.selection:
            # Extraer el área seleccionada de la imagen
            area = (self.selection[0], self.selection[1], self.selection[2], self.selection[3])
            cropped_img = self.img.crop(area)

        # Convertir la imagen recortada a bytes
            img_byte_arr = io.BytesIO()
            cropped_img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)

        # Usar Manga-OCR para detectar texto en la imagen recortada
            text = self.manga_ocr(cropped_img)

        # Enviar el texto extraído al servidor mediante un socket
            self.text_area.insert(tk.END, text + "\n\n")

        # Mostrar un mensaje de información
            messagebox.showinfo("Texto Extraído", "El texto dentro del área seleccionada ha sido enviado.")
        else:
            messagebox.showinfo("Información", "Por favor, selecciona un área de la imagen primero.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()




set INCLUDE=C:\Mecab\sdk;%INCLUDE%
set LIB=C:\Mecab\sdk;%LIB%

pip install fire fugashi jaconv loguru numpy "Pillow>=10.0.0" pyperclip "torch>=1.0" "transformers>=4.25.0" unidic_lite


**Descripción del uso principal:**
Este código proporciona una interfaz de usuario (GUI) para dos funcionalidades principales: cortar y unir imágenes. Con la opción de "Cortar", el usuario puede seleccionar una carpeta que contiene imágenes y especificar en cuántas partes desea dividirlas. Las imágenes cortadas se guardarán en una subcarpeta dentro de la carpeta original. Con la opción de "Unir", el usuario puede seleccionar una carpeta que contiene imágenes ya divididas y estas se combinarán en una sola imagen verticalmente, guardándose en la misma carpeta.

**Descripción detallada de cómo usarlo y los factores a tener en cuenta:**

**► Cortar imágenes:**
- Al hacer clic en el botón "Cortar", se abrirá un diálogo para que el usuario seleccione una carpeta que contiene las imágenes que desea cortar.
- Después de seleccionar la carpeta, se solicitará al usuario que ingrese el número de partes en las que desea dividir las imágenes.
- Es importante tener en cuenta que el número de partes debe ser un número entero entre 1 y 100.
- Una vez que se completa el proceso de corte, las imágenes cortadas se guardarán en una subcarpeta llamada "Corte" dentro de la carpeta original.
- Se mostrará un mensaje de éxito informando al usuario que las imágenes han sido cortadas correctamente.

**► Unir imágenes:**
- Al hacer clic en el botón "Unir", se abrirá un diálogo para que el usuario seleccione una carpeta que contiene las imágenes que desea unir.
- Las imágenes seleccionadas serán combinadas en una sola imagen verticalmente.
- La imagen combinada se guardará en la misma carpeta donde se encuentran las imágenes originales.
- Se mostrará un mensaje de éxito informando al usuario que las imágenes han sido unidas y guardadas correctamente.

**Consideraciones adicionales:**
- Las imágenes deben estar en formato PNG, JPG o JPEG para poder ser procesadas correctamente.
- Se recomienda tener cuidado al seleccionar las carpetas y al ingresar el número de partes durante el proceso de corte para evitar errores o resultados inesperados.
- Es importante tener en cuenta que el proceso de unión de imágenes puede consumir una cantidad considerable de recursos, especialmente si las imágenes son de gran tamaño o hay muchas de ellas.
