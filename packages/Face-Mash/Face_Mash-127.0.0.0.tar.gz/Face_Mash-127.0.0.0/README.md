# Deep learning model for fatigue detection

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   


##  Meta Information 

- Trained on open source dataset from kaggle
- Following are the predictable classes
- Closed(eyes)
- Open(eyes)
- no_yawn
- yawn


## Usage

- Make sure you have Python installed in your system.
- Model file will be saved locally in root directory.
- Model training info will be explained in medium blog soon.


## Example

 ```
from Face_Mash import Face_Mash
model_path = 'path/of/model.h5'
img_path   = 'path/of/img_file'
prediction = Face_Mash(img_path,model_path)

  ```
