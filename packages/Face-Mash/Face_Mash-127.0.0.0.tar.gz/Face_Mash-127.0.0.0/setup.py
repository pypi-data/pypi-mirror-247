from setuptools import setup
import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='Face_Mash',
    version='127.0.0.0',
    description='Deep Learning model for fatigue detection',
    author='Murali,Monica',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    keywords=['deep learning', 'drowsiness detection', 'fatigue analysis'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['Face_Mash'],
    package_data={'Face_Mash': ['model.h5']},
    install_requires=[
        'keras>=2.6.0',
        'opencv-python>=4.5.3',
        'numpy>=1.19.5',
        'tensorflow>=2.13.0',
        'gdown>=4.7.1'
    ]
)
