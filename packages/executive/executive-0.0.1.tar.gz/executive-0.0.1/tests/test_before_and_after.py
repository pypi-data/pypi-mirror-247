#!/usr/bin/env python

import os

def test_before():
    output = os.popen("cat tests/data/before-and-after | before '#'").read().strip()
    assert output == 'hello'

def test_after():
    output = os.popen("cat tests/data/before-and-after | after '#'").read().strip()
    assert output == 'world'
