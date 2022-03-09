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

If not pre-installed, install the poppler library that is used to convert the PDF files to images for screening
```
conda install poppler
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

The algorithm was trained on a set of 37,784 pages derived from a set of biomedical open access publication from PubMed Central and eLife. The number of examples per class range from 837 (flowno) to 8615 (other). For internal validation, a set of 3812 pages gathered from the same sources that were not used for training were used. Additional, two separate validation datasets with 1107 bioRxiv preprints and 1000 publications of authors affiliated with Charité Universitätsmedizin – Berlin (only for flow & pie charts) were used.

Performance internal validation dataset:

| Class | Manually labeled cases | False positives | precision | recall | F1 score |
|-------|-------|-------|-------|-------|-------|
| Bar graph of counts or proportions (appropriate) | 407 65 | 0.84 | 0.86 | 0.85 |
| Bar graph of continuous data (inappropriate) | 671 | 35 | 0.95 | 0.91 | 0.93 |
| Bar graph with dot plot | 149 | 10 | 0.93 | 0.91 | 0.92 |
| Dot plot | 393 | 33 | 0.91 | 0.85 | 0.88 |
| Box plot | 368 | 29 | 0.92 | 0.88 | 0.90 |
| Violin plot | 340 | 13 | 0.96 | 0.96 | 0.95 |
| Histogram | 238 | 32 | 0.86 | 0.86 | 0.83 |
| Flow chart | 276 | 32 | 0.89 | 0.91 | 0.90 |
| Pie chart | 160 | 5 | 0.97 | 0.92 | 0.94 |

Performance bioRxiv validation dataset:

| Class | Manually labeled cases | False positives | precision | recall | F1 score |
|-------|-------|-------|-------|-------|-------|
| Bar graph of counts or proportions (appropriate) | 345 | 60 | 0.82 | 0.81 | 0.82 |
| Bar graph of continuous data (inappropriate) | 405 | 25 | 0.94 | 0.92 | 0.93 |
| Bar graph with dot plot | 74 | 37 | 0.63 | 0.86 | 0.73 |
| Dot plot | 257 | 51 | 0.80 | 0.80 | 0.80 |
| Box plot | 255 | 36 | 0.87 | 0.91 | 0.89 |
| Violin plot | 57 | 27 | 0.65 | 0.89 | 0.76 |
| Histogram | 198 | 66 | 0.72 | 0.85 | 0.78 |
| Flow chart | 20 | 26 | 0.40 | 0.85 | 0.54 |
| Pie chart | 71 | 12 | 0.83 | 0.85 | 0.84 |

Performance Charité validation dataset:

| Class | Manually labeled cases | False positives | precision | recall | F1 score |
|-------|-------|-------|-------|-------|-------|
| Flow chart | 123 | 20 | 0.84 | 0.87 | 0.86 |
| Pie chart | 38 | 4 | 0.89 | 0.87 | 0.88 |

