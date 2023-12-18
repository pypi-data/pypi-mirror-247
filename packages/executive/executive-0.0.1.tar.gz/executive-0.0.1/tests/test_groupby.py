#!/usr/bin/env python

def test_groupby():

    import os
    import textwrap

    desired = textwrap.dedent("""
    9591818c07e900db7e1e0bc4b884c945e6a61b24	tests/data/groupby/2.txt	tests/data/groupby/4.txt
    f572d396fae9206628714fb2ce00f72e94f2258f	tests/data/groupby/1.txt	tests/data/groupby/3.txt
    """).strip()

    output = os.popen("""
        find tests/data/groupby/ -type f | sort | xargs sha1sum | sort | groupby
    """).read().strip()

    assert output == desired
