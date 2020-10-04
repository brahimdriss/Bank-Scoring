# Bank Credit Scoring Project
## Data Science  Project - 4th year of Computer Science Engineering
## Higher Private School of Engineering and Technology - Ecole Supérieure Privée d'Ingénierie et de Technologie



### Subject
Using 3 different bank datasets (Taiwan ,Usa, Germany) , our goal was to end up with an accurate scoring system by clustering and classifiying clients in order to help optimize the decision making process when it comes to handing out loans .

Since it's better for a bank to classify a good client as bad than classify a bad client as good , we choose as our evaluation metric the Precision Score of the models . In this NoteBook , we selected for each bank the best model along with some snippets of the data preprocessing and modeling .

# German Credit Dataset
### Clustering
We run almost every combination of Dimension reduction algorithms ( SVD / PCA / KPCA ) and Data rescaling methods to finally keep the best segmentation obtained , minimising the "Bad clients predicted good" ratio .

### Classification
After some exploratory data analysis , variables correlation with the target study (Chi2, Kendall , Anova ) and feature selection , we decided to drop some columns that gives no relevant information about our target variable .

We OneHotEncoded the remaining categorical variables , and scaled using Sickit-learn StandardScaler ( Gave us better results than other scalers ) before Train Test splitting and running the final joined data to our Models pipelines .

PCA was irrelevant in our case since it explained 80% with more than 30 column .


We used BayesianOptimization for XGBoost to select optimal values for some of our XGboost Classifier . Our target as explained above was Precision so the eval metric was precision score . Other models like KNN , Random Forest , LGBM (non optimised ) gave around ~70%-78% So we kept this one .

# American Credit Dataset

In this part, we have splitted the numeric and categorical data
- We logged the Label Encoder dictionnary of each categorical feature and the Dictionnary of the OneHotEncoder in order to use them for the new registered clients to predict them using the Models we generated so that we obtain maximum accuracy.
- to deal with missing valeus of the discrete variables, we proceeded with interpolating these variables to predict them.
- And for the missing categoricals values, the best method is to fill them with the most frequent modality for each feature.
- We capped/floored the outliers after detecting them with Tukey's method using the first and third quantile

### Clustering

Applyinh the Kmeans Algorithm after Scaling the Numeric Data with Standard Scaler and reducing the dimensions with KernellPCA method and filling the missing values with the median Value have shown the best Segmentation of our data.¶

### Classification

Before applying the Classification algorithms we need to deal with the missing values of the continious features.
- filling them with the median value of each feature or with the mean values have gave us the same performances so we proceeded with the median

- We run a Grid Search on the XGBoost Classifier in order to retrieve the best Hyper parameters for The XGB Classifier for the sake of giving the best possible results and Accuracy to our model.
- The parameters put below have gave us 90% Accuracy

# Bank Of Taiwan
### Clustering
### Classification

# Flask Application
We created a web based application using flask for model deployment and integration of a Dashboard for data analysis.
## Predictive model deployment
The interface contains a formular where we enter a new client's credentials and his previous interactions and transactions with the bank (behavior) in order to predict his eligibility for future loans application. 
![alt text](https://github.com/[username]/[reponame]/blob/[branch]/image.jpg?raw=true)
## Creation of an interactive Analytical Dashboard for Data visualization and data Analysis
In this interface, the user can visually track, analyze and display key performance indicators (KPI), metrics and key data points.


### Credits & Links : 
Template :
[Flask Dashboard Black](https://appseed.us/admin-dashboards/flask-dashboard-black) - provided by **AppSeed**
Two Dash dashboards merge :
https://github.com/eNMS-automation/eNMS
