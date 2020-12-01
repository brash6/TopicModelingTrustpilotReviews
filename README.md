# Topics analysis in UK train companies reviews 

What are the topics discussed in UK train companies reviews on Trustpilot ?

What could UK train companies learn from this to improve their services ?

## Description

This project consists in the analysis of topics discussed in UK train companies reviews from Trustpilot.

The goal of this project is to understand the evolution of discussed topics over time in order to give insights to UK train companies so they can improve their services.

## Configuration
To run this project on your machine, you can create a virtual environment using the <code>okra_env.yml</code> file.

## Data

We use reviews scraped from Trustpilot on 17 UK train companies. For each review, we extract : 
- date
- train company
- rating (number of stars)
- title
- body

To run the code, please unzip the data files in the data folder


Data can be found in the data folder.

## Scripts 

### Scraping

The script <code>trustpilot_scraping.py</code> used to scrap Trustpilot reviews is in the scraping folder. 

### Analysis

You will find the visualizations and results in the <code>TopicsAnalysisReviewsClean.ipynb</code> file.
To just look at results and viz, you can open <code>TopicsAnalysisReviewsClean.html</code>

Some visualizations (PyLDAvis) need to be launch in a web browser. These visualizations are in the <code>viz</code> folder

In order to make this notebook clean, functions are written in separated files. 

In the <code>constants.py</code> file, you will find all the constants used in this project.

In the <code>data_cleaning.py</code> file, you will find all the cleaning functions.
These functions clean the dataframe in order to make it ready for Latent Dirichlet Allocation.

In the <code>visualizations.py</code> file, you will find all the visualizations functions.

In the <code>modelization.py</code> file, you will find all the modelization functions.

## Advices to UK train companies based on topics analysis

- Keep working on the reliability of your train schedules 
- If not done already, develop efficient social media services for booking, refund, information on the journey, etc. (Whatsapp, Facebook and Twitter)
- Improve the effectiveness of your website especially for tickets refund, tickets change and railcard unsubscription
- Give the choice between voucher and refund when a train is deleted
- Deliver significantly higher quality services for first class passengers (cleanness, seat, drink, lounge, more accessible carriage, etc.)
- Emphasize helpfulness and kindness as key behaviours in your staff management, especially those in station and on board 
- If not done already, modernize your trains 
    - Smartphones outlets 
    - Space to work with a laptop, wifi
    - Space for bikes
    - Special places for the disabled