## lib_managed
Libraries that hasn't been published to maven yet, they will be deploy to ppmml/resources as python lib resources
+ jpmml-tensorflow-1.0
+ jpmml-r-1.2
+ pmml-evaluator-example-1.3

# Notes
+ jpmml-converter-1.2.5 is needed by jpmml-sparkml, If use the version 1.2.6, it will report java.lang.ClassNotFoundException: org.jpmml.converter.ModelEncoder

+ jpmml-example-1.3-SNAPSHOT.jar is a shaded packaged compiled from jpmml-evaluator
jpmml-evaluator-example is not published to maven. In order to avoid exception, such as **java.lang.NoSuchMethodError: org.dmg.pmml.MiningField.getInvalidValueReplacement**, we get the whole shaded package(40MB)

pull and compile jpmml-evaluator as follows:
```
git pull git@github.com:jpmml/jpmml-evaluator.git
mvn clean package -DskipTests
cp pmml-evaluator-example/target/example-1.3-SNAPSHOT.jar lib_managed/
# rename the jar
mv example-1.3-SNAPSHOT.jar jpmml-evaluator-example-1.3-SNAPSHOT.jar
```
the evaluator version will changed in future, please do these operations manually.
please ensure the prefix of the jar name is "jpmml-evaluator-example", since evaluator will include the jar by name.