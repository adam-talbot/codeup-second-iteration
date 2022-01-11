####### IMPORTS #######

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")
# viz settings
plt.rc('figure', figsize=(13, 7))
plt.rc('font', size=16)
plt.style.use('seaborn-darkgrid')

####### ACQUIRE #######

df = pd.read_csv('filename.csv', index_col=0) # read in data from .csv file and keep index from file instead of adding pandas index
df = pd.read_sql(sql_query, get_connection('database_name')) # create function for get_connection

####### PREPARE #######

df = df.drop_duplicates() # drop any duplicate rows
df = df.dropna() # drop all rows with null values
df = df.drop(columns=[cols_to_drop]) # drop columns from df you don’t need
df = df.rename(columns={old_name : new_name}) # rename columns as needed
df.column = np.where(df.column == True, 'Yes', 'No') # change from bool to Yes or No
df.column = df.column.apply(lambda x: x if x in top_list else 'Other') # group all others as 'Other'
df['column'] = df.column.astype(dtype) # can pass in a dictionary here if doing multiple columns at once

# Impute
df.column = df.column.fillna(value=imputation_value) # fill all missing values with one value for the column
# Imputation_value could be mean/median for column
df.column.mean()

# Split
def split_60(df):
    '''
    This function takes in a df and splits it into train, validate, and test dfs
    final proportions will be 60/20/20 for train/validate/test
    '''
    train_validate, test = train_test_split(df, test_size=0.2, random_state=527)
    train, validate = train_test_split(train_validate, test_size=.25, random_state=527)
    train_prop = train.shape[0] / df.shape[0]
    val_prop = validate.shape[0] / df.shape[0]
    test_prop = test.shape[0]/df.shape[0]
    print(f'Train Proportion: {train_prop:.2f} ({train.shape[0]} rows)\nValidate Proportion: {val_prop:.2f} ({validate.shape[0]} rows)\
    \nTest Proportion: {test_prop:.2f} ({test.shape[0]} rows)')
    return train, validate, test

# Scale
def scale(train, validate, test, scaler, cols_to_scale):
    '''
    Returns dfs with indicated columns scaled using scaler passed and original columns dropped
    '''
    new_column_names = [col + '_scaled' for col in cols_to_scale]
    # Fit the scaler on the train
    scaler.fit(train[cols_to_scale])
    # transform train validate and test
    train = pd.concat([
        train,
        pd.DataFrame(scaler.transform(train[cols_to_scale]), columns=new_column_names, index=train.index),
    ], axis=1)
    validate = pd.concat([
        validate,
        pd.DataFrame(scaler.transform(validate[cols_to_scale]), columns=new_column_names, index=validate.index),
    ], axis=1)
    test = pd.concat([
        test,
        pd.DataFrame(scaler.transform(test[cols_to_scale]), columns=new_column_names, index=test.index),
    ], axis=1)
    # drop scaled columns
    train = train.drop(columns=cols_to_scale)
    validate = validate.drop(columns=cols_to_scale)
    test = test.drop(columns=cols_to_scale)
    return train, validate, test

# remove outliers
def remove_outliers(train, validate, test, cols, k):
    '''
    Removes outliers that are outside of k*IQR using train to get bounds and then applying to all splits
    '''
     # make copies of passed splits so originals aren't modified
    train = train.copy()
    validate = validate.copy()
    test = test.copy()
    # remove outliers
    for col in cols:
        # get bounds from train
        Q1 = np.percentile(train[col], 25, interpolation='midpoint')
        Q3 = np.percentile(train[col], 75, interpolation='midpoint')
        IQR = Q3 - Q1
        UB = Q3 + (k * IQR)
        LB = Q1 - (k * IQR)
        # apply bounds to train to eliminate outliers
        train = train[(train[col] <= UB) & (train[col] >= LB)]
        # apply bounds to validate to eliminate outliers
        validate = validate[(validate[col] <= UB) & (validate[col] >= LB)]
        # apply bounds to test to eliminate outliers
        test = test[(test[col] <= UB) & (test[col] >= LB)]
    return train, validate, test

# encode
cat_cols = df.select_dtypes('object').columns.tolist()
df_modeling = pd.get_dummies(data=df, columns=cat_cols)


####### EXPLORE #######

# RFE Feature Selection/Engineering
def show_rfe_feature_ranking(X, y):
    '''
    Takes in predictors and target and returns feature ranking based on RFE function
    '''
    rfe = RFE(estimator=LinearRegression(), n_features_to_select=1)
    rfe.fit(X, y)
    rankings = pd.Series(rfe.ranking_, index=X.columns)
    return rankings.sort_values()

# Get lists of num_cols and cat_cols
cat_cols = df.select_dtypes('object').columns.tolist()
num_cols = df.select_dtypes('number').columns.tolist()

# Look at distributions for num_cols
fig, axs = plt.subplots(6, 3, sharey=False, figsize=(25, 20)) # adjust dimensions and size based on number of num_cols
axe = axs.ravel()
for i, c in enumerate(num_cols):
    train_exp[c].plot.hist(ax=axe[i],title=c, ec='black', bins=15)
    plt.tight_layout()

# Look at countplots for each cat_col
fig, axs = plt.subplots(4, 2, sharey=False, figsize=(25, 25))
axe = axs.ravel()
for i, c in enumerate(cat_cols):
    sns.countplot(train_exp[c], ax=axe[i])
    plt.tight_layout()
    
####### MODEL #######

# For created model evaluation df for regression, see Used Cars Project, evaluate.py file

# split into X and y for all splits (keeping all features)
X_train = train_scaled.drop(columns='target')
y_train = train_scaled.target
X_validate = val_scaled.drop(columns='target')
y_validate = val_scaled.target
X_test = test_scaled.drop(columns='target')
y_test = test_scaled.target

# get appropriate baseline for type of modeling (mode for classification, mean for regression, etc.)

# make model
ols = LinearRegression(normalize=True)
tree = DecisionTreeClassifier(max_depth=5, random_state=527)

# fit model
ols.fit(X_train, y_train)
tree = tree.fit(X_train, y_train)

# Make prediction for train and validate
y_train_pred = ols.predict(X_train)
y_validate_pred = ols.predict(X_validate)

# evaluation example
rmse_test = mean_squared_error(y_test_actual, y_test_pred, squared=False)
r2_test = explained_variance_score(y_test_actual, y_test_pred)

in_sample_accuracy = tree.score(X_train, y_train)
out_of_sample_accuracy = tree.score(X_validate, y_validate)

