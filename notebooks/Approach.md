# Approach
Before applying the machine learning model to the dataset, a set of challenges were identified:-
- The multiple datasets were to be merged and aggregated to create a machine learning consumable data.
- A few categorical variables had high cardinality.
- The target variable `is_click` was highly imbalanced.

## Data Aggregation
The dataset contained three files, with a brief description of each file as follow:-
1. trainset - contains the information of the all the ad impressions and the time it appeared, the user who interacted with that particular ad and whether he clicked or not. The file also has device information from which user interacted with like whether the device is 4G or not and what type of Operating System they used along with the type of app used.
2. view logs - contains the session related information and the item user interacted with.
3. Item master - contains all the information regarding a particular item like the product price, category it belonged to and the product type.

All of the above files were merged, keeping in mind the temporal nature of the dataset. The time component was necessary because each future interaction of the user is somewhat affected by the past activities. So, while aggregation of the data, those things were kept in check. The time in the datasets was mapped by two predictors, the `impression_time` in the trainset and `server_time` in the view_logs. Some of the examples of the features that captured time dependent relationship in the dataset were:-
- capturing mean of how many times user has clicked in the past from a particular app
- capturing how many times user has clicked the ad and what was the last time he had an impression

## Weight of Evidence
For the issue of **high cardinality**, we used weight of evidence. The weight of evidence tells the predictive power of an independent variable in relation to the dependent variable. It is calculated by taking the natural logarithm of division of % of non-events and % of events. 
> WOE = In(% of non-events ➗ % of events)

A big motivation to use WoE was it's performance is not hampered by imbalanaced data. A few other advantages of using Weight of Evidence are:-
- Handles missing values
- Handles outliers
- The transformation is based on logarithmic value of distributions. This is aligned with the logistic regression output function
- No need for dummy variables
- By using proper binning technique, it can establish monotonic relationship (either increase or decrease) between the independent and dependent variable

## Class Imbalance
The class imbalance occurs when one class dominates the data over other. A fairly common problem in the data science, there are too many techniques available for dealing with this problem. In this particular case, I tried three techniques, namely:-
1. Stratified K-Fold
2. Majority Under-Sampling, Minority Over-Sampling (implemented via SMOTE)
3. Hyperparameter tuning (in this case tuning `scale_pos_weight` hyperparameter of the XGBoost model)

Of all the above techniques, the third technique, i.e. tuning `scale_pos_weight` gave the best result.

## Result
The evaluation metric chosen was Recall. This is because True Positives, i.e. classifying people who will click on the advertisement correctly is much more important for us. Hence, it directly relates to identifying potential customer respectively. The final recall achieved in this problem was of **0.713**.
