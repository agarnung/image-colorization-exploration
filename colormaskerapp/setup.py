from setuptools import setup, find_packages

setup(
    name='colormaskerapp',
    version='0.1',
    description='CLI tool for creating RGB masks on grayscale images using OpenCV and PySimpleGUI',
    author='agarnung',
    url='https://github.com/agarnung/image-colorization-exploration',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',           # Para manejo de arrays y operaciones numéricas
        'opencv-python',   # Para procesamiento de imágenes
    ],
    entry_points={
        'console_scripts': [
            'colormaskerapp=colormaskerapp.cli:main',  # Punto de entrada para la CLI
        ],
    },
    setup_requires=[
        'setuptools>=42',  # Asegura que setuptools esté actualizado
    ],
    python_requires='>=3.6',  # Compatibilidad con Python 3.6 o superior
)
