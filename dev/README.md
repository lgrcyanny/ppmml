# Run unit tests

## Requirement:
+ python packages
```
pip install xgboost,lightgbm,tensorflow,sklearn
```

+ sun-java8

## Run all tests:
```
sh run_test.sh
```

## Run single unit test
1. *test a module*
```
sh run_test.sh --module sklearn_test
```

2. *test a method*
```
sh run_test.sh --module sklearn_test.SklearnConverterTest --method test_decision_tree
```

3. more info
```
sh run_test.sh -h
```

### Notes:
+ `python -m unittest discover -s ppmml/tests -p *_test.py` must be called under project base path, in case of model not found exception