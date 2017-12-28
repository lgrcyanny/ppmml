# ppmml
ppmml is a python library for converting machine learning models to pmml file. ppmml wraps jpmml libraries and provides clean interface.

# Geting Started
```python
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
import ppmml
# load data and train iris datasets
(X, y) = load_iris(True)
lr = LogisticRegression(tol=1e-5)
lr.fit(X, y)
joblib.dump(lr, "lr.pkl.z", compress = 9)

# to pmml file
ppmml.to_pmml("lr.pkl.z", "lr.pmml", model_type='sklearn')

# prepare test data
df = pd.DataFrame(X)
df.columns = ['x1', 'x2', 'x3', 'x4']
df.to_csv('test.csv', header=True, index=False)
# predit with pmml file, a simple predict API based on jpmml-evaluator
ppmml.predict('lr.pmml', 'test.csv', 'predict.csv')
```

*More examples*
- [sklearn models to pmml file](https://github.com/lgrcyanny/ppmml/blob/master/examples/notebooks/ppmml_sklearn_examples.ipynb)
- [xgboost model to pmml file](https://github.com/lgrcyanny/ppmml/blob/master/examples/notebooks/ppmml_sklearn_examples.ipynb)
- [lightgbm model to pmml file](https://github.com/lgrcyanny/ppmml/blob/master/examples/notebooks/ppmml_lightgbm_example.ipynb)
- [tensorflow model to pmml file](https://github.com/lgrcyanny/ppmml/blob/master/examples/notebooks/ppmml_tensorflow_example.ipynb)
- [r model to pmml file](https://github.com/lgrcyanny/ppmml/blob/master/examples/notebooks/ppmml_r_example.ipynb)

# Algorithm Features
All algorithm supported by jpmml is support by pmml. In summary:
## sklearn estimators

### Supervised Learning
* GLM: Linear, Logistic Regression, Lasso, ElasticNet, Ridge, SGD
* Naive Bayes: GaussianNB, but no support for multinomial naive Bayes, Bernoulli naive Bayes
* Nearest Neighbors
* Neural Network
* SVM
* DecisionTree
* All EM Method
* LinearDiscriminantAnalysis

### Unsupervised Learning
* Custering: KMeans, no support for LDA and DBSCAN
* PCA

### feature algorithms
* feature selection
* feature extraction, no support for FeatureHasher
* feature selection
* feature preprocessing

[jpmml-sklearn](https://github.com/jpmml/jpmml-sklearn )

## xgboost classifier and regressor
[jpmml-xgboost](https://github.com/jpmml/jpmml-xgboost)

## lightgbm classifier and regressor
[jpmml-lightgbm](https://github.com/jpmml/jpmml-lightgbm)

## tensorflow
Only support DNNClassifier, DNNRegressor, Linear Classifier, Linear Regressor, one_hot_column, real_valued_column
sparse_column_with_keys
[jpmml-tensorflow](https://github.com/jpmml/jpmml-tensorflow)

## spark ml
[jpmml-sparkml](https://github.com/jpmml/jpmml-sparkml) is better than spark mllib's pmml transformation. it support 35 algorithms now.
- Feature extractors, transformers and selectors. But no support for BucketedRandomProjectionLSH,DCT, ElementWiseProduct, LSH, MinHashLSH, Normalizer, PolynomialExpansion
- Classification: LR, GBT, DecisionTree, NN, RandomForest. But no support for SVM，Naive Bayes.
- Regression: Linear, GBT, DecisionTree, RandomForest, GLR. But no support for Survival regression, Isotonic regression
- Clustering: KMeans. But no support for GMM, LDA

## R models
ppmml integrates [jpmml-r](https://github.com/jpmml/jpmml-r)
### Preprocessing
* range, center, scale, medianImpute

### R Algorithms
* glm - Generalized linear (GLM) regression and classification
* kmeans - K-Means clustering
* lm - Linear (LM) regression
* XGBoost, GBM
* Random Forest
* SVM Classifier and Regression
* Scorecard regression
* earth - Multivariate Adaptive Regression Spline (MARS) regression
* elmNN - Extreme Learning Machine (ELM) regression
* iForest - Isolation Forest (IF) anomaly detection
* mvr - Multivariate Regression (MVR) regression
* lrm - Binary Logistic Regression (LR) classification
* ols - Ordinary Least Squares (OLS) regression

# Requirements
- python 2.7
- jdk 1.8+

# How to build from source
```shell
sh build.sh clean package
```
the output egg package will be palced in dist directory

# Project Structure
- ppmml: ppmml python libraries
- deps:  jar dependencies, including jpmml-sklearn, jpmml-tensorflow, jpmml-r, jpmml-spark, jpmml-xgboost, jpmml-lightgbm and jpmml-evaluator.
- examples: ppmml example notebooks

# Run unit tests
please refer to [dev guide](https://github.com/lgrcyanny/ppmml/tree/master/dev)

All unit tests are passed with these versions:
- tensorflow 1.4
- xgboost 0.6a2
- scikit-learn 0.19
- lightgbm 2.0.11
- spark 2.2, 2.3
- R 3.4.2
- jpmml-model 1.3.8

# Notes
## Notes for Users
- pmml converters only support run in locally, especially spark converter will new a local SparkSession
- Users care about the input path and pmml output path

## Notes for developers
- jpmml-tensorflow hasn't been publish to maven, please pull the code and compile the jar manually
(https://github.com/lgrcyanny/jpmml-tensorflow/tree/fix-building)
The forked version has fixed compile error of jpmml-tensorflow
