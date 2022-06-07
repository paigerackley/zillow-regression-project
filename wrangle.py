import pandas as pd
import numpy as np
import os

from env import get_db_url

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

#### ACQUIRE ######

"""
USAGE: 
Use `from wrangle import wrangle_zillow` at the top of your notebook.
This 
"""
def get_zillow_data():
    """Seeks to read the cached zillow.csv first """
    filename = "zillow.csv"

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        return get_new_zillow_data()

def get_new_zillow_data():
    """Returns a dataframe of all 2017 properties that are Single Family Residential"""

    db_name = 'zillow'
    filename='zillow.csv'
    sql = """
    SELECT bedroomcnt,
        bathroomcnt, 
        calculatedfinishedsquarefeet, 
        taxvaluedollarcnt, 
        yearbuilt, 
        regionidzip as zipcode, 
        fips
    FROM properties_2017
        JOIN propertylandusetype USING(propertylandusetypeid)
        JOIN predictions_2017 USING(parcelid)
    WHERE propertylandusedesc = 'Single Family Residential' AND transactiondate LIKE '2017%%';
    """
    #Read SQL from file
    df = pd.read_sql(sql,get_db_url(db_name))
    #write to disk - writes index as col 0:
    df.to_csv(filename)
    return df

    ###########################


### SPLIT #####
def train_validate_test_split(df, seed=123):
    '''
    This function takes in a dataframe, the name of the target variable, and an integer for a setting a seed
    and splits the data into train, validate and test.
    Test is 20% of the original dataset, validate is .30*.80= 24% of the
    original dataset, and train is .70*.80= 56% of the original dataset.
    The function returns, in this order, train, validate and test dataframes.
    '''
    train_validate, test = train_test_split(df, test_size=0.2,
                                            random_state=seed)
    train, validate = train_test_split(train_validate, test_size=0.3,
                                       random_state=seed)
    return train, validate, test


#### Scale #####
def scale_data(train, 
               validate, 
               test, 
               columns_to_scale=['bedroomcnt', 'bathroomcnt', 'taxvaluedollarcnt', 'square_feet']):
    '''
    Scales the 3 data splits. 
    Takes in train, validate, and test data splits and returns their scaled counterparts.
    If return_scalar is True, the scaler object will be returned as well
    '''
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    scaler = MinMaxScaler()
    scaler.fit(train[columns_to_scale])
    
    train_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(train[columns_to_scale]),
                                                  columns=train[columns_to_scale].columns.values).set_index([train.index.values])
                                                  
    validate_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(validate[columns_to_scale]),
                                                  columns=validate[columns_to_scale].columns.values).set_index([validate.index.values])
    
    test_scaled[columns_to_scale] = pd.DataFrame(scaler.transform(test[columns_to_scale]),
                                                 columns=test[columns_to_scale].columns.values).set_index([test.index.values])
    

    return train_scaled, validate_scaled, test_scaled



def wrangle_zillow():
    """
    Acquires Zillow data
    Handles nulls
    optimizes or fixes data types
    handles outliers w/ manual logic
    returns a clean dataframe
    """ 
    
    # Acquire function 
    df = get_zillow_data()

    # Drop all nulls from dataset
    df = df.dropna()
    # Convert some columns to integers
    # fips, yearbuilt, and bedrooms can be integers
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)    
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)

    # readability
    df = df.rename(columns={'calculatedfinishedsquarefeet': 'square_feet'}) 

    # Eliminate the funky values
    df = df[df['square_feet'] > 400]
    df = df[df['square_feet'] < 100000]
    df = df[df['taxvaluedollarcnt'] > 10000]
    df = df[df['taxvaluedollarcnt'] < 20000000]
    df = df[df['taxamount'] > 100]
    df = df[df['taxamount'] < 300000]
    df = df[df['bathroomcnt'] > 0]
    df = df[df['bedroomcnt'] > 0]
    df = df[df['bathroomcnt'] < 7]
    df = df[df['bedroomcnt'] < 7]

     # Convert Fips to Names
    df['fips_name'] = np.where(df.fips == 6037, 'Los Angeles', np.where(df.fips == 6059, 'Orange','Ventura') )
    df = df.drop(columns = 'fips')

# Make dummies df for non-binary variables, fips_name is now an object
    dummy_df = pd.get_dummies(df[['fips_name']], dummy_na=False, \
                              drop_first=True)
    # Concat dummy to original
    df = pd.concat([df, dummy_df], axis=1)

    return df


###### All Together #######
def wrangle_split_scale():
    
    df = wrangle_zillow()
    train, validate, test = train_validate_test_split(df)
    train_scaled, validate_scaled, test_scaled = scale_data(train, validate, test)
    
    return train_scaled, validate_scaled, test_scaled