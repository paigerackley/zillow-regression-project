# <center><a name="top"></a>Regression Project: Zillow Property Values
![](https://github.com/paigerackley/zillow-regression-project/blob/main/images/house%20clip%20art.png)

by: Paige Rackley </center>

<p>
  <a href="https://github.com/paigerackley" target="_blank">
    <img alt="Paige" src="https://img.shields.io/github/followers/paigerackley?label=Follow_Paige&style=social" />
  </a>

 * * *  
[[Project Description](#project_description)]
[[Project Planning](#planning)]
[[Data Dictionary](#dictionary)]
[[Data Acquire and Prep](#wrangle)]
[[Data Exploration](#explore)]
[[Modeling](#model)]
[[Conclusion](#conclusion)]
___



## <a name="project_description"></a>Project Description:

We are wanting to gather data to create a new model to predict property values. We have one currently that we would like to improve upon and use our data as a tool to help us find trends that can help our predictions. At Zillow, this data is important because our customers need to be able to trust that we can give them accurate predictions for value.

-> 1. Construct a Regression model that can properly predict the estimated property value of <b> Single Family Properties </b>.
    
    
-> 2. Present a report to team that shows my processes and how I came to my conclusions.


-> 3. Make recommendations on what are attributes to consider when predicting property value.
  
***
## <a name="planning"></a>Project Planning:
  
  
 ### Business Goals: 
 > - As a junior Data Scientist, my goals are to use the data I have to create a ML Regression model that beats our current model on predicting property value. I want to be able to zero in on potential factors that I find correlate most to predicting these values, as it is very important to our company to be trustworthy with the information we provide our customers. 

 ### Audience:
> - My audience is the Zillow data science team. 
  
  
 ### Deliverables:
> - A final report notebook
> - A final report notebook presentation
> - Workbooks that were used while going through the steps to create my model

###  Executive Summary: 
Evidence from stats tests and visualizations supports the claim that these square feet, bathrooms count and bedroom count are a few of the major features that can help predict property tax value. My recommendation is to focus on square feet, bathroom and bedroom count when trying to predict property value. I also found that the zip codes had big differences in property value for many of the features tested, so to get accurate results, it would be best to focus on each zip code one at a time. 
  
        
### Initial Hypothesis/Questions: 
 > - Does bathroom and bedroom count help predict the property value?
 > - Why do some properties relatively close to eachother value differently? What are the other attributes to this?
 > - Is there a relationship between the year built and property value?
 > - Does the county dictate property value?


[[Back to top](#top)]


## <a name="dictionary"></a>Data Dictionary  
[[Back to top](#top)]

### Data Used

Target|Datatype|Definition|
|:-------|:--------|:----------|
| taxvaluedollarcnt | int64 | final home estimated price |

|Feature|Datatype|Definition|
|:-------|:--------|:----------|
| bedroomcnt       | int64 |    number of bedrooms |
| bathroomcnt        | float64 |    number of bathrooms |
| square_feet       | int64 |    total square feet of home |
| year_built        | int64 |    year home was built |
| taxamount       | float64 |    tax amount |
| fips_name        | int64 |    name of county home is in |
| propertylandusetypeid | int64 | property land use id |
| parcelid | int64 | parcel id

***

## <a name="wrangle"></a>Data Acquisition and Preparation
  
 ## Acquire

In this step, I used SQL queries to pull what I wanted from Zillows tables.
I went with pulling bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, regionidzip as zipcode, fips from properties 2017 table.
I renamed regionidzip to zipcode right away for readability. I then joined propertylandusetype and predictions_2017 to get all the data I wanted in one place.

  
## Prepare
In this step, I created multiple functions that were meant to help me prepare my data for both exploration and modeling.


Functions created:

<b><font color='green'> train_validate_test_split </font></b> : This function splits the data into the 3 sets needed for exploring and statistical tests.
<b><font color='green'> scale_split_data </font></b> : This function scales the the 3 split data sets. 

<b><font color='green'> wrangle_zillow </font></b> : This function has the acquire function nested inside of it, but also starts to sort through the data. This function is also only intended to be used during my exploration phase, as it is not scaled or split yet.

Steps implemented: 
  - Dropped all nulls by row (The amount of data loss that happens here is less than 1%, it is worth it)
  - Converted columns to integers (fips, yearbuilt, bedroomcnt, taxvalluedollarcnt, calculatedfinishedsquarefeet)
  - Renamed calculatedsquarefeet to something easier and smaller = square_feet
  - I decided to narrow down my search and get rid of outliers by adding in criteria

          -> Square feet was narrowed down to between 400 and 100,00
      
          -> Taxvalluedollarcount narrowed to 10,000 - 2,000,000
      
          -> Taxamount to 300 - 300,000
      
          -> Bathroom and bedroom count to 7 or less
      
          -> Made sure that any values that were either null or 0 for bedroom/bathroom to be taken out.
      
  - Converted fips to fips_name and named the zip codes (6037, 'Los Angeles', 6059, 'Orange','Ventura')

### The Big One...

<b><font color='green'> wrangle_split_scale </font></b> : This function is meant to take all prior functions and put them all in one. It wrangles, splits and scales the data meant to be used for modeling.
  
[[Back to top](#top)]


  
## <a name="explore"></a>Data Exploration:
  ###  Explore

 ## The Big Question: How do we determine home value?

Our target variable is taxvalluedollarcnt, so we will be comparing the fips_name, bathroomcnt, bedroomcnt, square_feet ad year_built columns to this to determine our goal. 
  
   
 
[[Back to top](#top)]

### Takeaways from exploration:
Exploration using visuals and statistical tests prove that all variables are associated with higher property values. We will move forward with our modeling using square_feet, year_built, bedroomcnt, and bathroomcnt.

## <a name="model"></a>Modeling:
  
For Regression, we want to decide if we need to use mean or median baseline, so we will compare the model testing results to both.

LassoLars did well and beat both median and mean baselines.
The Linnear Regression model beats both mean and median baselines and is extremely close to results of LassoLars.

  
The Polynomial Regression model not only beat both baselines, but beats the LassoLars and Linear as well. Polynomial is our best peforming model and will be moved into our test phase.
 
After testing Polynomial using test, we get a result of Test:  436046.3117047775, which is even better than our train and validate sets.
  
[[Back to top](#top)]



## <a name="conclusion"></a>Conclusion:
  
 # Conclusion:
### After our testing, we were able to prove that the major features in predicting property tax were bathroom count, bedroom count and square feet. 

#### Out of all of the models tested, Polynomial did the best and beat both the mean and median baseline.
#### Although the LassoLars and Linear Regression models couldn't beat Polynomial, they still both beat the baseline mean and median as well.
  
### With more time:

- I would like to delve into the zip codes/counties deeper. There were some big difference is tax values and a common theme was that Los Angeles tended to have a higher tax value in all the features explored.

- Bring in new features that weren't used this time around such as room count, pool count and size, fireplace, and fire place count. I feel that these features could definitely play into higher property tax value.

- Look into the years built a little further. Are houses from a certain time period or before/after a certain time period tending to have higher property tax values?

- Possibly bringing in newer datasets for property value would be smart, as the data set used was 5 years old and a Pandemic happened since this was taken. Property value will have more than likely changed.

## Recomendations: 
####


### Recommendations:

- Focus on the square feet, bedroom and bathroom count when attempting to predict property value.

- When attempting to predict, because the zip codes seem to have big differences in overall tax value, it may be best to focus on one zip at a time.

[[Back to top](#top)]
  
  
  **How to Reproduce**
- [x] Read this README.md
- [ ] 
- [ ] Have fun doing your own exploring, modeling, and more! 
