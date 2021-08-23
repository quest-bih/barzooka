import pytest
from .. import barzooka

import pathlib
pathlib.PosixPath = pathlib.WindowsPath

def test_barzooka_class_loads():
    b = barzooka.Barzooka("barzooka/barzooka.pkl")
    assert True

def test_barzooka_screen_img():
    b = barzooka.Barzooka("barzooka/barzooka.pkl")
    assert b.predict_from_img("barzooka/examples/img/text1.jpg") == [['text']]
    assert b.predict_from_img("barzooka/examples/img/violin1.jpg") == [['violin']]
    assert b.predict_from_img("barzooka/examples/img/box1.jpg") == [['box']]
    assert b.predict_from_img("barzooka/examples/img/boxdot1.jpg") == [['box', 'dot']]
    assert b.predict_from_img("barzooka/examples/img/dot1.jpg") == [['dot']]

def test_barzooka_screen_img_folder():
    b = barzooka.Barzooka("barzooka/barzooka.pkl")
    screening_results = b.predict_from_img_folder("barzooka/examples/img")
    assert screening_results[1] == [['box'], ['box', 'dot'], ['box', 'dot'], ['dot'], ['dot'], ['text'], ['violin']]

def test_barzooka_screen_pdf():
    b = barzooka.Barzooka("barzooka/barzooka.pkl")
    screening_results = b.predict_from_file("barzooka/examples/pdf/text.pdf")
    assert screening_results == {'approp': 0,
                                 'bar': 0,
                                 'pie': 0,
                                 'hist': 0,
                                 'bardot': 0,
                                 'box': 0,
                                 'dot': 0,
                                 'violin': 0,
                                 'flowyes': 0,
                                 'flowno': 0,
                                 'paper_id': 'text'}
    screening_results = b.predict_from_file("barzooka/examples/pdf/doc.pdf")
    assert screening_results == {'approp': 0,
                                 'bar': 0,
                                 'pie': 0,
                                 'hist': 0,
                                 'bardot': 0,
                                 'box': 3,
                                 'dot': 4,
                                 'violin': 1,
                                 'flowyes': 0,
                                 'flowno': 0,
                                 'paper_id': 'doc'}