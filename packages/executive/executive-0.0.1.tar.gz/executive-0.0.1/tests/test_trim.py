import os

def test_trim_left():
    assert os.popen("echo '@cake@' | trim -l @").read().strip() == 'cake@'

def test_trim_right():
    assert os.popen("echo '@cake@' | trim -r @").read().strip() == '@cake'

def test_trim():
    assert os.popen("echo '@cake@' | trim @").read().strip() == 'cake'
