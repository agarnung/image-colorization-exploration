import cv2
import numpy as np
import threading
import PySimpleGUI as sg

class MaskAnnotator:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")

        self.height, self.width, _ = self.image.shape
        self.mask = np.zeros_like(self.image)
        self.brush_color = (255, 0, 0)  # BGR
        self.brush_size = 5
        self.drawing_active = False
        self.prev_x, self.prev_y = -1, -1
        self.running = True

        # Configuración de ventanas
        cv2.namedWindow('Annotator', cv2.WINDOW_GUI_NORMAL)
        cv2.setMouseCallback('Annotator', self.annotate)
        
        # Ventana de configuración de color
        self.color_window_size = (300, 150)
        cv2.namedWindow('Color Settings', cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow('Color Settings', *self.color_window_size)
        cv2.createTrackbar('R', 'Color Settings', self.brush_color[2], 255, self.update_color)
        cv2.createTrackbar('G', 'Color Settings', self.brush_color[1], 255, self.update_color)
        cv2.createTrackbar('B', 'Color Settings', self.brush_color[0], 255, self.update_color)
        self.update_color_preview()

        # Estados del teclado
        self.key_states = {
            'r': False,
            'c': False,
            '+': False,
            '-': False,
            'h': False,
            's': False
        }

    def update_color(self, x):
        r = cv2.getTrackbarPos('R', 'Color Settings')
        g = cv2.getTrackbarPos('G', 'Color Settings')
        b = cv2.getTrackbarPos('B', 'Color Settings')
        self.brush_color = (b, g, r)
        self.update_color_preview()

    def update_color_preview(self):
        # Crear imagen de preview del color
        self.color_preview = np.zeros((100, 300, 3), dtype=np.uint8)
        self.color_preview[:] = self.brush_color
        cv2.imshow('Color Settings', self.color_preview)

    def annotate(self, event, x, y, flags, param):
        if self.drawing_active:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.prev_x, self.prev_y = x, y
                cv2.circle(self.mask, (x, y), self.brush_size, self.brush_color, -1)
            
            elif event == cv2.EVENT_MOUSEMOVE and self.prev_x != -1:
                cv2.line(self.mask, (self.prev_x, self.prev_y), (x, y), self.brush_color, self.brush_size)
                self.prev_x, self.prev_y = x, y
            
            elif event == cv2.EVENT_LBUTTONUP:
                self.prev_x, self.prev_y = -1, -1

    def process_keys(self, key):
        new_states = {k: False for k in self.key_states}
        
        if key != -1:
            c = chr(key).lower()
            if c in self.key_states:
                new_states[c] = True

        # Manejar estado de 'R' para dibujo continuo
        self.drawing_active = new_states['r']
        
        # Resetear posición anterior al soltar 'R'
        if self.key_states['r'] and not new_states['r']:
            self.prev_x, self.prev_y = -1, -1

        # Manejar eventos únicos
        if new_states['c'] and not self.key_states['c']:
            cv2.namedWindow('Color Settings', cv2.WINDOW_NORMAL)
        
        if new_states['+'] and not self.key_states['+']:
            self.brush_size = min(50, self.brush_size + 1)
        
        if new_states['-'] and not self.key_states['-']:
            self.brush_size = max(1, self.brush_size - 1)
        
        if new_states['h'] and not self.key_states['h']:
            self.show_help()
        
        if new_states['s'] and not self.key_states['s']:
            self.save_mask()

        self.key_states = new_states

    def show_help(self):
        help_text = """
        Controles:
        - Mantén 'R' para dibujar
        - 'C': Mostrar controles de color
        - '+/-': Cambiar grosor
        - 'S': Guardar máscara
        - 'H': Mostrar ayuda
        - ESC: Salir
        """
        print(help_text)

    def save_mask(self):
        def save_async():
            file_path = sg.popup_get_file('Guardar', save_as=True, default_extension='.png', file_types=(('PNG', '*.png'),))
            if file_path:
                cv2.imwrite(file_path, self.mask)
                print(f"Máscara guardada en: {file_path}")
        threading.Thread(target=save_async, daemon=True).start()

    def run(self):
        while self.running:
            combined = cv2.addWeighted(self.image, 1, self.mask, 0.5, 0)
            cv2.imshow('Annotator', combined)
            
            key = cv2.waitKey(1) & 0xFF
            self.process_keys(key)

            if key == 27 or cv2.getWindowProperty('Annotator', cv2.WND_PROP_VISIBLE) < 1:
                self.running = False

        cv2.destroyAllWindows()

if __name__ == "__main__":
    annotator = MaskAnnotator("ruta/a/tu/imagen.png")
    annotator.run()