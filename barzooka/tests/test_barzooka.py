import pytest
import os
from .. import barzooka

b = barzooka.Barzooka()
    
import pathlib
if os.name == 'nt':
    pathlib.PosixPath = pathlib.WindowsPath

def test_barzooka_screen_img():
    assert b.predict_from_img("barzooka/examples/img/text1.jpg") == [['text']]
    assert b.predict_from_img("barzooka/examples/img/violin1.jpg") == [['violin']]
    assert b.predict_from_img("barzooka/examples/img/box1.jpg") == [['box']]
    assert b.predict_from_img("barzooka/examples/img/boxdot1.jpg") == [['box', 'dot']]
    assert b.predict_from_img("barzooka/examples/img/dot1.jpg") == [['dot']]

def test_barzooka_screen_img_folder():
    screening_results = b.predict_from_img_folder("barzooka/examples/img")
    #make sure that screening results are given in right order
    #should this code be included in the predict function?s
    screening_results_sorted = [category for file,category in 
                                sorted(zip(screening_results[0],screening_results[1]))]

    assert screening_results_sorted == [['box'], ['box', 'dot'], ['box', 'dot'], ['dot'], ['dot'], ['text'], ['violin']]

def test_barzooka_screen_pdf():
    screening_results = b.predict_from_file("barzooka/examples/pdf/text.pdf")
    assert screening_results == {'approp': 0,
                                 'bar': 0,
                                 'bardot': 0,
                                 'box': 0,
                                 'dot': 0,
                                 'flowno': 0,
                                 'flowyes': 0,
                                 'hist': 0,
                                 'other': 0,
                                 'pie': 0,
                                 'text': 1,
                                 'violin': 0,
                                 'paper_id': 'text'}

    screening_results = b.predict_from_file("barzooka/examples/pdf/doc.pdf")
    assert screening_results == {'approp': 0,
                                 'bar': 0,
                                 'bardot': 0,
                                 'box': 3,
                                 'dot': 4,
                                 'flowno': 0,
                                 'flowyes': 0,
                                 'hist': 0,
                                 'other': 0,
                                 'pie': 0,
                                 'text': 1,
                                 'violin': 1,
                                 'paper_id': 'doc'}

    screening_results = b.predict_from_file("barzooka/examples/pdf/doc.pdf", pagewise = True)
    #make sure that screening results are given in right order
    #should this code be included in the predict function?s
    screening_results_sorted = [category for file,category in 
                                sorted(zip(screening_results[0],screening_results[1]))]
    assert screening_results_sorted == [['box'],
                                 ['box', 'dot'],
                                 ['box', 'dot'],
                                 ['dot'],
                                 ['dot'],
                                 ['text'],
                                 ['violin']]

                                 