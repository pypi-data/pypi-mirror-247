# Median housing value prediction

The housing data can be downloaded from https://github.com/ageron/handson-ml/blob/master/. The script has codes to download the data. We have
modelled the median house value on given housing data.

The following techniques have been used:

 - Linear regression
 - Decision Tree
 - Random Forest

## Steps performed
 - We prepare and clean the data. We check and impute for missing values.
 - Features are generated and the variables are checked for correlation.
 - Multiple sampling techinuqies are evaluated. The data set is split into train and test.
 - All the above said modelling techniques are tried and evaluated. The final metric used to evaluate is mean squared error.
 -performed the tests

##sklearn pypi acount recreation 
-added the functional tests and unit tests
-performed test_training and tets_installation tests in functional testings
-performed test_data_ingestion test in unit testing


## To excute the script
python src/score.py

##To Excute the distribution file
unzip dist/housing_library_5515-0.1-py3-none-any.whl -d wheel_contents
 cd wheel_contents
python3 house_price_prediction/score.py


##To activate the environment
conda activate mle-dev
##To export the environment
conda env export > environment.yml
##To import the environment
 conda env create -f environment.yml
##LICENSE
This project is licensed under the MIT license - see the (LICENSE) file for details
