#!/usr/bin/env python3
import sys
import os
import glob
import xml.etree.ElementTree as ET
from threading import Thread

class XMLReadingThread(Thread):
    def __init__(self, filename):
        super(XMLReadingThread, self).__init__()
        self.filename = filename
        self.results = []

    def run(self):
        tree = ET.parse(self.filename)
        abstracts = tree.getroot().findall(".//AbstractText")
        abs = []
        for abstract in abstracts:
            for text in abstract.itertext():
                abs.append(text)
        self.results = abs

if __name__ == "__main__":
    filedesc = sys.argv[1]
    filelist = glob.glob(filedesc)
    threads = []
    for xml_file in filelist:
        t = XMLReadingThread(filename=xml_file)
        t.start()
        threads.append(t)

    full_results = []
    for t in threads:
        t.join()
        results = "\n".join(t.results)
        full_results.append(results)
    print("\n".join(full_results))
