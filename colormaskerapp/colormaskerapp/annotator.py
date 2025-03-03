import cv2
import numpy as np
import tkinter as tk
from tkinter.colorchooser import askcolor

class MaskAnnotator:
    def __init__(self, image_path):
        # Cargar la imagen en color
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")

        self.height, self.width, _ = self.image.shape
        self.mask = np.zeros_like(self.image)  # Crear una máscara inicializada en negro
        self.brush_color = (255, 0, 0)  # Color inicial (rojo)
        self.brush_size = 5  # Grosor inicial del pincel
        self.drawing_active = False  # Si la tecla 'R' está presionada, se activa el modo de dibujo
        self.prev_x, self.prev_y = -1, -1  # Posiciones anteriores del ratón para trazos continuos

        # Crear la ventana de OpenCV
        cv2.namedWindow('Annotator', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('Annotator', self.annotate)

    def choose_color(self):
        # Función para elegir un color usando Tkinter
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        color = askcolor()[1]  # Devuelve el color como un código hexadecimal
        if color:
            # Convertir el color hexadecimal a RGB
            rgb_color = self.hex_to_rgb(color)
            self.brush_color = rgb_color
            print(f"Color de pincel cambiado a: {self.brush_color}")

    def hex_to_rgb(self, hex_color):
        # Convertir color hexadecimal a RGB
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def annotate(self, event, x, y, flags, param):
        # Función para manejar eventos de mouse
        if self.drawing_active:
            if event == cv2.EVENT_MOUSEMOVE:
                if self.prev_x != -1 and self.prev_y != -1:
                    # Dibujar línea desde la posición anterior
                    cv2.line(self.mask, (self.prev_x, self.prev_y), (x, y), self.brush_color, self.brush_size)
                else:
                    # Primera posición, dibujar un círculo
                    cv2.circle(self.mask, (x, y), self.brush_size, self.brush_color, -1)
                self.prev_x, self.prev_y = x, y
            elif event == cv2.EVENT_LBUTTONDOWN:
                # Opción adicional: iniciar dibujo con clic (opcional)
                cv2.circle(self.mask, (x, y), self.brush_size, self.brush_color, -1)
                self.prev_x, self.prev_y = x, y
        else:
            self.prev_x, self.prev_y = -1, -1

    def handle_keypress(self, k):
        # Manejar las teclas de acción
        if k == ord('c'):
            # Seleccionar el color del pincel
            self.choose_color()
        elif k == ord('h'):
            # Mostrar la ventana de ayuda
            self.show_help()
        elif k == ord('+'):
            self.brush_size = min(50, self.brush_size + 1)
            print(f"Grosor del pincel aumentado a {self.brush_size}")
        elif k == ord('-'):
            self.brush_size = max(1, self.brush_size - 1)
            print(f"Grosor del pincel reducido a {self.brush_size}")

    def show_help(self):
        # Función para mostrar la ventana de ayuda usando Tkinter
        help_text = """
        Controles:
        - 'R': Mantener presionado para activar el modo de dibujo
        - 'C': Seleccionar color del pincel
        - 'B': Alternar entre lápiz y goma
        - Tecla '+' o '-': Cambiar grosor del pincel
        - Tecla 'H': Mostrar esta ventana de ayuda
        - Tecla 'S': Guardar máscara y salir
        - ESC: Salir sin guardar
        """
        help_window = tk.Tk()
        help_window.title("Ayuda - ColormaskerApp")
        label = tk.Label(help_window, text=help_text, padx=10, pady=10)
        label.pack()
        close_button = tk.Button(help_window, text="Cerrar", command=help_window.destroy)
        close_button.pack(pady=10)
        help_window.mainloop()

    def run(self):
        # Bucle principal de OpenCV para dibujar sobre la imagen
        while True:
            combined = cv2.addWeighted(self.image, 1, self.mask, 0.5, 0)
            cv2.imshow('Annotator', combined)

            k = cv2.waitKey(1) & 0xFF
            self.drawing_active = (k == ord('r'))  # Activar dibujo solo si 'R' está presionada
            self.handle_keypress(k)

            if k == ord('s'):
                output_path = "output_mask.png"
                cv2.imwrite(output_path, self.mask)
                print(f"Máscara guardada en {output_path}")
                break
            elif k == 27:  # Tecla ESC para salir
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    annotator = MaskAnnotator("path/to/your/image.png")  # Reemplaza con la ruta de tu imagen
    annotator.run()