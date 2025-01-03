# README
Repo to share and store code, data, and project proposal for Scrapy Party's Data in the Wild Project. This repo collects and analyses data concerning IT University of Copenhagen's research publication with a particular focus on trends in international Collaboration in the past two decades.

Collaborators: Tonio Ermakoff, Markus Leonard Brenken, Mikas Jankeliunas, Daria Damian, and Antonia-Bianca Zserai.


The repo is organized as follows:

-/Data
-/Code
	-/Annotation Task 
	-/Time Series Visualization
	-/Scraping
-/Proposal


Below is a brief description of each folder as well as basic instructions to reproduce our results.

- /Proposal
  - Contains a draft for our original project proposal
- /Data
  - The data collected from the scraping scripts is found here. Publications.csv describes all the publications scraped. Addresses.csv contains the addresses of each institution that collaborated with ITU in the past twenty years.
- /Code
  - Contains the python scripts and ipynb files used to scrape, clean the data, carry out our project analysis, and produce visualizations.
  - /Scaping
     - Changes in ITU departments in the year 2025 might make these scripts obsolete. To collect data on ITU's publications, run the three python scripts starting with 'Scraping_'. Afterwards, running Address_Scraping_for_Institutions.py will retrive the addresses of each instituion that collaborated with ITU.
  - /Annotation Task
     - Contains the code use to obtain a sample dataset for our annotators. Annotated scores of 120 reside in annotation.csv. Running agreement.ipynb executes the analysis carried out on the annotation score. 
  - /Time Series Visualizations
     - To recreate the Visualizations of the report, run the Jupyter-Notebook "Time Series Visualizations/Final Visualizations.ipynb". Detailed instructions can be found inside the notebook.
  





