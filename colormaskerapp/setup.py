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
        'numpy',         
        'opencv-python',  
        'PySimpleGUI'
    ],
    entry_points={
        'console_scripts': [
            'colormaskerapp=colormaskerapp.cli:main', 
        ],
    },
    setup_requires=[
        'setuptools>=42', 
    ],
    python_requires='>=3.6',
)
