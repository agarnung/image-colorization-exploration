import sys
import argparse
from .annotator import MaskAnnotator

def main():
    parser = argparse.ArgumentParser(description='Create a color mask on an image.')
    parser.add_argument('--input', type=str, required=True, help='Path to the image to be annotated')
    parser.add_argument('--output', type=str, required=True, help='Path to the mask to be generated')

    args = parser.parse_args()

    annotator = MaskAnnotator(args.input, args.output)

    annotator.run()

if __name__ == "__main__":
    main()
