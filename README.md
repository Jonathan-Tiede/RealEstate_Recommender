# RealEstate_Recommender
## What is it?
This project will take a county/state pair (in this case, Brevard County FL) and recommend which currently-available houses should be considered for purchase.

## Why do this?
This project serves two purposes for me. First, I am looking to move and so this tool could be useful when that time comes. Second, I need to build out a data science portfolio and I came up with this as my first project.

## What is the main question being asked?
What are the top X homes I should consider buying given the state/county pair? I am looking for undervalued, single family homes currently listed "For Sale" on Zillow.

## What will this project cover?
This project will start by scraping Zillow's website for all recently sold and currently available single family homes and putting all relevant data into a database (postgreSQL) or dataframe. Next, the data will be cleaned and organized for further investigation and model training. Initial insights will be discovered on the data. Finally, it will predict fair market value of each available home, make a recommendation on the top X to consider based on user criteria and finally map the suggested homes. A final report will be generated on the market in question and the model's findings.
