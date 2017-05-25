# Python pipeline for evaluation of MOOC student answers
## Biomedical natural language processing (BioNLP) and neural network analysis

Writing assignments in Massive Open Online Courses (MOOCs) don't just provide students with grades: they contain data useful for assessing student learning.

This pipeline analyzes the effectiveness of human learning in a highly abstract scientific domain, epigenetics, and is based on data from the Coursera course “Epigenetic Control of Gene Expression” (https://www.coursera.org/learn/epigenetics) by the University of Melbourne.

This pipeline extracts each student’s answer and associated scores from the HTML data from the coursera website for natural language processing and neural network analysis.

![pipeline](https://biof-git.colorado.edu/hackathon/epigenetics_mooc/blob/ada932bd749486f035e9f8fce19177d46642ac0b/Epigenetics_MOOC_5_24_17_pipeline.png)


## What it does

This pipeline uses a python script and jupyter notebook to transform student answers and scores into python lists, generate a vocabulary from those answers for Natural Language Processing, transform the answers into vectors for analysis, and use a neural network to correlate answer vector features with scores. The neural network output includes loss, to represent the efficiency of neural network training, and mean-squared-error.

## How it works

This pipeline requires two scripts to run. First, load_json.py loads student answer and score data already in JSON format. The script outputs a python list of sublists, where each sublist is a student's answer to one question followed by the averages of the scores given to that question by the student's reviewers. This script separates the answer and score data for each question into separate lists, removes reviewer comments associated with a student’s answer, cleans up leftover HTML code, and normalizes the scores for each answer and returns scores between 0 and 1 for analysis. 

Next, the Epigenetics-Answer-Classifier.ipynb notebook runs a python notebook that takes a python list of answers and scores as input. This notebook first uses spaCy for natural language processing with the built-in standard english language model. SpaCy tokenizes the input data, and creates a vocabulary from the 10,000 most frequent words in the dataset. The vector representing each answer contains the count of each vocabulary word and the normalized score for that answer.

Using the Neural Network software TensorFlow (TFlearn API), the dataset is split into training, test, and validation sets (80%, 10%, and 10% respectively for this analysis). The neural network contains two hidden layers with 100 nodes and 10 nodes respectively and utilizes the ReLU activation function, trains for 1,000 to 30,000 steps.

## Required input data

* Student answer and score data in JSON format (start with load_json.py)

OR

* Student answer and score data in HTML format (processing script for HTML data available upon request)

## Optional input data

* outside vocabulary or word corpus

# Installation

put installation info here

## Dependencies
* python 3+

* pandas

* numpy

* tensorflow

* tflearn

* spacy


# Table of (code) contents:

resources

* conda-env-epimook.yml: YAML file for conda ML/NLP environment

src

* get_abstracts.py: Read abstracts from multiple PubMed xml files in parallel. Can be used to generate custom vocabulary and corpora.

* gen_dummy_data.py: Generates dummy/test data for pipeline tests and optimization.

src/notebooks	

* load_json.py: processes json data from preprocess.py into feature and target lists for input into spaCy and TFlearn (Epigenetics-Answer-Classifier.ipynb)

* output_csv.py: processes json data from preprocess.py into csv file of student ids, answers, and scores

* Epigenetics-Answer-Classifier.ipynb: spaCy and TFlearn python notebook for vectorization and neural network analysis

src/preprocess

* preprocess.py: preprocess data from .html files from Coursera or other online source into json format for analysis



# To-do:
Final git repo location TBD
 
