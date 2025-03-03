from setuptools import setup, find_packages

setup(
    name='colormaskerapp',
    version='0.1',
    description='CLI tool for creating RGB masks on grayscale images using PyQt',
    author='agarnung',
    url='https://github.com/agarnung/image-colorization-exploration',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'tk'
    ],
    entry_points={
        'console_scripts': [
            'colormaskerapp=colormaskerapp.cli:main',
        ],
    },
    # Add system dependencies as part of the setup metadata
    setup_requires=[
        'setuptools>=42',  # Ensure setuptools is up-to-date
    ],
    python_requires='>=3.6',  # Specify Python version compatibility
)
