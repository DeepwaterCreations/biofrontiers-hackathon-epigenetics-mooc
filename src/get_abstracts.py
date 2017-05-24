#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    filename = sys.argv[1]
    tree = ET.parse(filename)
    abstracts = tree.getroot().findall(".//AbstractText")
    for abstract in abstracts:
        for text in abstract.itertext():
            print(text)
