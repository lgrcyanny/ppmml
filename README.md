# PPMML
Python library for converting machine learning models to pmml file. PPMML wraps jpmml libraries and provides clean interface for user.

# Features
- Clean interface for various machine learning models
- Support sklearn, tensorflow, xgboost, lightgbm, r, and sparkml

# How to build from source
```shell
sh build.sh clean package
```
the output egg package will under dist directory

# Project Structure
- ppmml: ppmml python libraries
- deps:  jar dependencies, including jpmml-sklearn, jpmml-tensorflow, jpmml-r, jpmml-spark, jpmml-xgboost, jpmml-lightgbm and jpmml-evaluator.
- examples: ppmml example notebooks

# Notes
## Notes for Users
- pmml converters only support run in locally, especially spark converter will new a local SparkSession
- Users care about the input path and pmml output path

## Notes for developers
- jpmml-tensorflow hasn't been publish to maven, please pull the code and compile the jar manually
(https://github.com/lgrcyanny/jpmml-tensorflow/tree/fix-building)
