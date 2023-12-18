#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""comment here"""
import sub2txt
import vtt2text
from pathlib import Path


def entry():
    root_directory = Path(".")
    for path_object in root_directory.glob('**/*'):
        if path_object.is_file() and path_object.suffix == '.vtt':
            outfile_path = path_object.stem + '_parsed.txt'
            # get clean content
            content = vtt2text.clean(path_object)
            # save clean content to text file
            f = open(outfile_path, "w")
            f.write(content)
            f.close()

            print(f"{path_object} -> {outfile_path}")

    print("Done.")
