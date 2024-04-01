# Real Estate Market Predictions
## Objective
Florida remains one of the fastest growing regions in the United States with places like Miami having some of the highest single-family home prices. This same effect is felt throughout the coastal cities along both east and west coasts. On my street alone, there have been six new homes built in the past three years!

Home prices have continued to rise (even if slowly, lately) and new homes (and a great many apartment complexes) are constantly under construction. I have spent the last 15 years in Florida and it is fast approaching the right time to make a move back home; back to the great Pacific Northwest! As such, I am very interested in what to do with my current home. Should I sell or should I rent? When is the best time to sell in my area? Since I've never sold a home before, I would also like to know how long I could expect the house to be on the market. And most importantly, what would be the ideal price to list at? 

Enter this project. It is my goal to answer these questions and more. I will be narrowing the scope to that of my county and will only consider homes that have recently sold (<1yr) and are currently listed. I will pull data from Zillow using an API, clean and prep the data for modeling, explore what it has to say about the market in my area, and finally determine how to price my house based on Zillow's Zestimate.
## Project Plan
### Data Collection
It was my initial plan to build a web scraper. After spending a few days making no progress on **not** being identified as a bot, I decided to move forward with a well-regarded, paid, [API](https://rapidapi.com/s.mahmoud97/api/zillow56) found on RapidAPI.

There are two particular API calls made, each wrapped in its own function:
1. zillowAPISearch - This is necessarily the first call to make. The input parameters are location, price ranges, home status (for sale, recently sold, etc.), home type and page number on Zillow. From this call, information such as address, bed/bath, list price, zestimate, ZPID, and zip code is collected.
2. zillowPropertyDetails - Using the ZPID from the first search, each property is further searched and over 600 features are pull. Unfortunately, a fair amount of these features are duplicates and/or triplicates, but we will deal with that in the next section.

These two functions are each called for homes that were recently listed and homes that are currently listed. In my county, over 6500 homes have sold in the past year and over 2800 are currently listed. 

We are now ready to clean, organize, and otherwise prepare the data for exploration and model training!
### Data Wrangling
To tackle this monster of data, we go through all features and create a down-selected list to begin working with. To start, we will narrow down the feature set to 22 items. 

From here, each feature is dealt with individually. Property areas are universally converted to square feet, measures of time are all set to 'days,' missing boolean values are appropriately set to true/false, and all samples with n/a's found on critical features (such as price, living area space, and zip code) are dropped.

Due to the relatively small feature set, and each of the categorical variables do not require the ordinal relationship be maintained, we will apply one-hot encoding to all categorial variables.

At this point, features are cleaned and encoded appropriately. Now is the time to consider inter-feature relationships by checking for multicollinearity. Using Pandas, this is very straight forward.

```
corrmat = df_recentlySold_trunc[numCols].corr()
fig, ax = plt.subplots(figsize=(15, 10))
sns.heatmap(corrmat, vmax=.8, square=True, cbar=False)
```

Here, we want to maintain all features with strong correlation to the target but consider dropping any feature that is very strongly correlated with another feature. As the target variable is price, we must be care not to include any feature such as Zestimate or price/sq-ft as these will over-optimistically inform the model and cause unrealistically high performance.

Next, we will make sure the target variable is normally distributed. Since we are training a linear model as our baseline, it is important to ensure normal distribution which can lead to a more stable and reliable parameter estimates. For tree models (random forest, XGBoost, etc.), this is not necessary as the models partition features to reduce impurity measures (such as Gini Impurity or entropy).

And finally, since our feature space is relatively small, each feature will be plotted against the price and outliers removed manually by a similar approach to:

```
df_forSale_trunc = df_forSale_trunc
.drop(df_forSale_trunc[df_forSale_trunc['livingAreaValue']>5000]
.index)
.reset_index(drop=True)
```
### Data Exploration
Data exploration is important for the following reasons: 
1. **Understanding the Data**: EDA helps gain a deeper understanding of the dataset. This includes understanding the structure of the data, the types of variables present, and any patterns or trends that may exist.
2. **Data Cleaning**: EDA often reveals inconsistencies, missing values, or outliers in the data. Identifying and addressing these issues is essential for preparing the data for further analysis. Data cleaning tasks such as imputation of missing values or outlier treatment typically arise during EDA.
3. **Feature Selection and Engineering**: EDA can inform feature selection and engineering decisions by identifying which features are most relevant or informative for the predictive modeling task at hand. It may involve examining correlations between variables, identifying redundant features, or creating new features based on existing ones.
4. **Model Assumptions**: EDA helps ensure that the assumptions of the chosen modeling techniques are met. For example, linear regression assumes linearity, independence of errors, and homoscedasticity. EDA can reveal whether these assumptions hold true and guide adjustments if necessary.
5. **Identifying Relationships**: EDA uncovers relationships and interactions between variables, which can provide insights into the underlying mechanisms of the phenomenon being studied. This understanding can guide the selection of appropriate modeling techniques and improve model interpretability.
6. **Visualization and Communication**: Visualizations generated during EDA facilitate communication of findings to stakeholders who may not be familiar with the technical aspects of data science. Visualizations help tell a story about the data, making complex patterns and relationships more accessible and understandable.
7. **Detecting Anomalies and Outliers**: EDA helps identify anomalies or outliers in the data that may represent errors, anomalies, or interesting phenomena worthy of further investigation. Understanding the nature of these outliers can inform subsequent modeling decisions.
8. **Risk Assessment**: EDA can reveal potential risks associated with the data, such as biases, sampling issues, or data quality problems. Understanding these risks is essential for making informed decisions and mitigating potential problems downstream in the analysis process.
### Model Building and Price Predictions
Data cleaned. Exploration complete. Next, let's predict some home prices.
#### Modelling Flow
1. Import data cleaned data from the previous steps
2. Split data into training and testing sets. Here it is vital the data be split before doing any scaling. 
3. Scale the data. For this run, `RobutScalar()` is used as it is more capable of dealing with outliers. Further, the scalar was fit on the training data set **only** and then later used to transform both the test data set and all of the for sale data. Also, it is important to make sure that any scaling done to the target variable or feature variables in previous steps do not inject data leakage. The only scaling performed prior to this step was on the target variable using the `nlog1p()` function from numpy. Here, there is no data leakage as each call of nlog1p() is independent of the other samples.
4. Each of the three models are then trained on the recently sold training set and evaluated on the test set. 
	1. Repeated K-Fold cross validation is used primarily due to the relatively small data set (~6000 samples total) and should help reduce any potential overfitting. 
	2. Next, we need to tune the hyper-parameters for each model. For the linear model, this is very straight forward process: calculate the fit intercept or not; basically a check on if the data is centered. For the remaining models, there can be quite a few hyper-parameters and going through them manually would take a very long time. Enter `GridSearchCV()`. This will ensure the model is trained as many times as necessary to use each combination of hyper-parameters. It will keep track of the model performance during training and automatically select the best-performing one.
5. Now its time to evaluate the model on the remaining, unseen data from the recently sold collection. One output from `GridSearchCV()` is the collection of best parameters found for the model. Apply the model along with the best parameters to the test data set and report out the performance metrics.
6. For real estate price predictions, its advisable to use loss-functions such as MSE, MAE, and MAPE.
	1. For our case, we will consider the mean absolute error (MAE). Before I removed most outliers from the data sets, the target variable was heavily skewed to the right. As such I chose the loss-function that is more useful against skewness and outliers. Since then, the target variable has been normalized and the more common MSE could be used instead.
8. At long last, lets take a look at how the models performed on the recently sold data (predicted vs. sold price) and the for sale data (predicted vs list price). Since our goal is to predict the best list price for the available listings, it is not necessarily a negative indicator if the errors are "large" as this could be a sign of under-/over-valued homes... which is precisely what we are looking for.

==<> Table: Training/Testing/Deployment Results <>==
#### Results
==<> Table: Results Summary <>==
## Execution
Project consists of four files that should be run in the following order:

1. Data collection
2. Data wrangling
3. Data exploration (EDA)
4. Data prediction

Once complete, the file *final_forSale_data.csv* will be created which contains each model's price predictions and difference from list price.
## Next Steps
In its current state, the project will take pull housing data from Zillow for both current listings and recently sold single family homes. From there, the data will be cleaned (semi-autonomously) and have any outliers removed (manual process). Next, the local market will be explored to help focus model(s) creation. Finally, a set of models are trained on the recently sold data and deployed on the current listings with an output table created with the predicted prices for use in listing valuation.

Some key additions I will plan to add in a future update will be:
- Increase useful features by building a web scraper to collect data for listings from other websites such as Realtor.com or Propstream.com
- Seasonality metrics (months) to both data sets to hopefully capture hot and cold cycles in the market. 
	- This will likely require more data than just the previous 12 months (recently sold limits).
- Interactive Folium (or similar) map showing all currently listed homes the model(s) consider undervalued by x%.
	- Interactivity would show key stats (price, sqft, bd, ba) when hovering over property and when clicked would open the Zillow listing.
	- It would also be great to include community based metrics (say, by zip code) showing information such as:
		- Number of homes listed
		- Number of homes recently sold
		- Average time on market
		- Average home age
- Build separate models for homes in various price or square footage ranges, or based on neighborhoods/zip codes .
	- Increased model performance to be expected if each model is applied to a more focused group.
	- Due to scarcity, would need to implement bootstrapping or equivalent model resampling for homes in the more expensive and/or larger ranges. 
- Implement additional modeling techniques (ie. model stacking, weighted ensembles, etc.) to further refine predictive capability.
- Possibly extend this analysis to rental properties.
- Build a basic website to host all the above findings
## Skills Gained
- Version control using Git/GitHub.
- Web data collection using paid **API** available on **RapidAPI**
- **Pandas** library for data manipulation: imputation, cleaning, plotting, model training
- **Seaborn** and **Matplotlib** for visualizing feature and target variables for outlier detection and data distributions
- **Numpy** for removing skewness and kurtosis