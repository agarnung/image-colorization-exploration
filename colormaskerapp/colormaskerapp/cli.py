import sys
import argparse
from .annotator import MaskAnnotator

def main():
    # Configuración del parser para recibir el argumento de la imagen y el color
    parser = argparse.ArgumentParser(description='Create a color mask on an image.')
    parser.add_argument('--input', type=str, required=True, help='Path to the image to be annotated')
    parser.add_argument('--output', type=str, required=True, help='Path to the mask to be generated')

    args = parser.parse_args()

    # Crear una instancia de la clase MaskAnnotator con el color del pincel
    annotator = MaskAnnotator(args.input, args.output)

    # Ejecutar la aplicación de anotación
    annotator.run()

if __name__ == "__main__":
    main()
