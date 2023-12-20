from setuptools import setup
import setuptools

setup(
    name='Face_Mash',
    version='1.1.1.0',
    description='drowsiness detection model',
    author='Murali && Monica',
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
        'tensorflow>=2.13.0'
    ]
)
