Gitlab table of contents:
 
 doc	
    Project notes as of 5/23/17 lunchtime
 
 resources
    YAML file for conda ML/NLP environment
 
 src/notebooks	
    Epigenetics-Answer-Classifier.ipynb
    load_json.py	Fix dumb slicing error

 
 Still need to determine final location of git and materials
 
 Project info:
 
Massive Open Online Courses (MOOCs) have exploded over the past few years and brought college and professional-level education to students throughout the world. One of the benefits of MOOCs also presents challenges: the number of students participating in the course. Because courses often include thousands to tens of thousands of students, many MOOCs draw upon their students not only for vibrant discussion but for peer grading of written assignments. Peer grading serves as an additional learning opportunity for students and provides a wealth of data on student learning. Because MOOCs are both popular and new, educators need to assess how well students learn during these courses in order to improve them.

Our goal was to develop a pipeline to analyze the effectiveness of human learning in a highly abstract scientific domain. Epigenetics is one such abstract scientific subject: because of the scale at which epigenetics acts, it is challenging to understand from human experience; understanding requires both biological knowledge and critical thinking. In order to investigate abstract scientific learning in a MOOC, this study utilized data from the Coursera course “Epigenetic Control of Gene Expression” (https://www.coursera.org/learn/epigenetics) by the University of Melbourne. The data set consists of student answers to the final writing assignment for three sections of the course as well as peer assessments of those answers. This writing assignment required students to read a scientific paper, a popular press article, and integrate details of those articles with their broader knowledge from the class in order to include particular ideas in their answers. Peers assessed how completely and clearly each answer addressed the required ideas. The data set contains about 7,000 answers, with about 4 peer assessments each, a rich resource for biological natural language processing.

This pipeline extracts each student’s answer and associated scores from the HTML data from the coursera website for natural language processing and neural network analysis. While this pipeline takes advantage of shallow semantics to identify answer features, it provides a framework that can be adapted to deeper semantics which represent models of student knowledge.