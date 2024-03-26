# RealEstate_Recommender
## What is it?
This project will take a county/state pair (in this case, Brevard County FL) and recommend which currently-available houses should be considered for purchase.

## Why do this?
This project serves two purposes for me. First, I am looking to move and so this tool could be useful when that time comes. Second, I need to build out a data science portfolio and I came up with this as my first project.

## What is the main question being asked?
What are the top X homes I should consider buying given the state/county pair? I am looking for undervalued, single family homes currently listed "For Sale" on Zillow.

## What will this project cover?
This project will start by scraping Zillow's website for all recently sold and currently available single family homes and putting all relevant data into a database (postgreSQL) or dataframe. Next, the data will be cleaned and organized for further investigation and model training. Initial insights will be discovered on the data. Finally, it will predict fair market value of each available home, make a recommendation on the top X to consider based on user criteria and finally map the suggested homes. A final report will be generated on the market in question and the model's findings.


# Real Estate Market Predictions
## Objective
- Predict housing prices on currently listed homes using recently (< 1yr) sold homes in the same area (Brevard County, FL)
- Find currently-listed, undervalued homes (based on list price and Zestimate)
- Find regional "hot-spots"

## Steps to Completion
### Data Collection
- {Corresponding code filename}
- Discuss original intent to build a webscraper but issues with bot detection stopped me
- Discuss API usage. Don't shy away from personal cost
- Discuss two major API calls, how they interact with one another and what data they pull

### Data Wrangling
- {Corresponding code filename}
- Discuss how missing values were handled (sample deletion, imputation, 0, etc.)
- Discuss how distributions were handled (nlog1p, boxcox1p)
- Discuss how outliers were detected and handled
    - Show some obvious plots with outliers present vs removed (box plots for bathroom/bedrooms)
- Discuss how only certain price range & living square-footage was considered and why
    - Why: rest were outliers. Models couldn't handle the wide variety and sparse data at the extremes
-  Show a few key plots: jointgrid plots (living area vs price; both before and after outlier removal)

### Data Exploration
- {Corresponding code filename}
- Show average age per zipcode (32909 youngest)
- Show average time on market (32909 near lowest)
- Show average price (32909 near lowest)
- Show number of homes on market (32909 has greatest)

### Model Building and Price Predictions
- {Corresponding code filename}
- Discuss the models chosen, their strengths and weaknesses in this use case
- Discuss the data prep for model training (feature scaling, train/test splits, hyperparameter tuning using gridsearch cross validation, etc.)
- Discuss metrics used to gauge relative and absolute performance
- Discuss feature importance based on Random Forest model and how that can/was used to downselect features
- Discuss steps taken to avoid/minimize overfitting
- Discuss final values/findings for model performance
- Discuss currently-listed housing price predictions vs. Zestimate/list price and if it makes sense.

### Final Reporting
- {Corresponding code filename}
- Not yet build
- This will almost entirely be the Plotly dashboard hosted on a website

## Next Steps
- Want to add: 
    - seasonality (cyclical months) to both data sets
    - interactive folium map that shows all homes currenlty undervalued by X%
    - website showing using plotly:
        - Top X best deals
        - Map of brevard with deals
        - Regional statistics (zipcode price inc., avg time on market, avg age, etc.)
    - More models and/or modeling techniques (ie. model stacking, weighted ensembles, etc.)
        - Instead of looking only at subset of data based on price/square footage, build multiple models based on price/square-footage
            - If sample size low (ie. price > $1 million), do some bootstrap resampling??
    - More features (would need to scrape from other sources) such as quality, property features, etc.