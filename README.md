# Python pipeline for evaluation of MOOC student answers
## Biomedical natural language processing (BioNLP) and neural network analysis

Writing assignments in Massive Open Online Courses (MOOCs) don't just provide students with grades: they contain data useful for assessing student learning.

This pipeline analyzes the effectiveness of human learning in a highly abstract scientific domain, epigenetics, and is based on data from the Coursera course “Epigenetic Control of Gene Expression” (https://www.coursera.org/learn/epigenetics) by the University of Melbourne.

This pipeline extracts each student’s answer and associated scores from the HTML data from the coursera website for natural language processing and neural network analysis.

![pipeline](https://biof-git.colorado.edu/hackathon/epigenetics_mooc/blob/ada932bd749486f035e9f8fce19177d46642ac0b/Epigenetics_MOOC_5_24_17_pipeline.png)


# What it does

placeholder

# How it works

placeholder

# Installation

put installation info here

## Dependencies
* python 3+

* pandas

* numpy

* tensorflow

* tflearn

* spacy

## Required input data

* Student answer and score data in JSON format

OR

* Student answer and score data in HTML format

## Optional input data

* outside vocabulary or word corpus

# Table of contents:

resources

* conda-env-epimook.yml: YAML file for conda ML/NLP environment

src/notebooks	

* load_json.py: processes data in json format into python lists for input into spaCy and TFlearn (Epigenetics-Answer-Classifier.ipynb)

* output_csv.py: processes data in json format into human-interpretable csv file of answers and scores

* Epigenetics-Answer-Classifier.ipynb: spaCy and TFlearn python notebook for vectorization and neural network analysis



# To-do:
Final git repo location TBD
 