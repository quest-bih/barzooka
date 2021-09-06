# Barzooka

Barzooka screens publication and detects different graph types. The following graph types can be detected:

- bar graphs for continuous data
- bar graphs for count data
- bar graphs with dots
- pie charts
- dot plots
- box plots
- histograms
- violin plots
- flow charts


## Description

Barzooka is based on a deep convolutional network trained using the fastai python package (https://docs.fast.ai/). It screens a publication on the page level and can detect multiple graph types per page.

## Installation

It is recommended to set up a separate environment first, e.g. using conda: 
```
conda create -n env_name python 3.9
conda activate env_name
```

Then run the following command from the package folder
``` python
python setup.py install
```

## Usage

Barzooka consist of a model file (.pkl) that stores the trained network parameters and a python class file with a simple interface. As Barzooka is trained using fastai, make sure you have installed fastai.

Create Barzooka object and load model file:
``` python
import barzooka
b = barzooka.Barzooka()
```


Predict from single image:
``` python
b.predict_from_img('./barzooka/examples/img/box1.jpg')
```

Returns a list of all classes detectected in the image.


Predict from image folder:
``` python
b.predict_from_img_folder('./barzooka/examples/img/')
```
Use this function if you have a folder with images of individual pages. This returns the filenames and the detected classes per filename.


Predict from PDF file:
``` python
b.predict_from_file('./barzooka/examples/pdf/doc.pdf')
```

Returns a dict with the number of successfully detected pages for each class.


Predict from PDF folder:
``` python
b.predict_from_folder('./barzooka/examples/pdf/', 'results.csv', tmp_folder='./tmp/')
```
Use this function if you have a folder with PDFs. Each PDF is temporarily converted to page images (into the tpm_folder, which is created if it is not existing) and the prediction results for all pages of the PDF are combined. The results are saved in csv format under save_filename. The tmp images are deleted afterwards. For the PDF conversion the command line tool pdftocairo is used - please make sure that this is installed on your system.

The result files use the following encoding for the different classes:

| class label | description |
|-------------|-------------|
| approp | Bar graph for count data |
| bar | Bar graph for continuous data |
| bardot | Bar graph with dots |
| box | Box plot |
| dot | Dot plot |
| flowno | Flow chart without numbers |
| flowyes | Flow chart with numbers |
| hist | Histogram |
| other | Other non-text pages that do not fit any of the other graph types |
| pie | Pie chart |
| text | Pages with only text |
| violin | Violin plot |


In case of the following error on Windows machines

``` python
raise NotImplementedError("cannot instantiate %r on your system")
NotImplementedError: cannot instantiate 'PosixPath' on your system
```

try to first execute the following lines to redirect the path:

``` python
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
```

## Performance

...
