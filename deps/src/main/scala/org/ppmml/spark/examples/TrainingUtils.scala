/*
 * Copyright (c) 2017 the ppmml authors. All Rights Reserved
 * ppmml is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * ppmml is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * You should have received a copy of the GNU Affero General Public License
 * along with ppmml. If not, see <http://www.gnu.org/licenses/>.
 */
package org.ppmml.spark.examples

import java.io.{File, FileOutputStream, PrintWriter}
import javax.xml.transform.stream.StreamResult

import org.apache.spark.ml.evaluation.BinaryClassificationEvaluator
import org.apache.spark.ml.{Pipeline, PipelineModel}
import org.apache.spark.ml.feature.{StringIndexer, VectorAssembler}
import org.apache.spark.sql.{DataFrame, Dataset, SparkSession}
import org.apache.spark.sql.types.StructType
import org.jpmml.model.JAXBUtil
import org.jpmml.sparkml.ConverterUtil

import scala.io.Source


trait TrainingUtils {
  val spark: SparkSession

  // data format is: https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data
  def loadIris() = {
    import spark.implicits._
    val dataStream = DecisionTree.getClass.getResourceAsStream("/iris.csv")
    val data = Source.fromInputStream(dataStream).getLines().toList
    val rddData: Dataset[String] = spark.sparkContext.parallelize(data).toDS()
    val dataSet = spark.read
      .option("inferSchema", "true")
      .option("header", "false")
      .csv(rddData)
    val res = dataSet.toDF("x1", "x2", "x3", "x4", "y")
    res.show()
    res
  }

  def preprocessing(irisDF: DataFrame) = {
    val indexer = new StringIndexer().setInputCol("y").setOutputCol("label")
    val vectorAssembler = new VectorAssembler()
      .setInputCols(Array("x1", "x2", "x3", "x4")).setOutputCol("features")
    val pipeline = new Pipeline().setStages(Array(indexer, vectorAssembler))
    val data = pipeline.fit(irisDF).transform(irisDF)
    data
  }

  def loadProcessedIris(): DataFrame = {
    val data = loadIris()
    preprocessing(data)
  }

  def toPmml(model: PipelineModel, schema: StructType, filePath: String) = {
    println(s"Write PMML to path ${filePath}")
    val pmml = ConverterUtil.toPMML(schema, model)
    var outputStream: FileOutputStream = null
    try {
      outputStream = new FileOutputStream(new File(filePath))
      JAXBUtil.marshalPMML(pmml, new StreamResult(outputStream))
    } finally {
      outputStream.close()
    }
  }

  def saveSchema(schema: StructType, fileOutput: String) = {
    val out = new PrintWriter(new FileOutputStream(fileOutput, false)) // overwrite
    out.println(schema.prettyJson)
    out.close()
  }

  def withTime(message: String)(fn: => Any): Any = {
    val startTime = System.currentTimeMillis()
    val res = fn
    println(s"Processing $message, duration ${System.currentTimeMillis() - startTime}ms")
    res
  }

  def doEvaluate(model: PipelineModel, testData: DataFrame) = {
    // validate
    val predictions = model.transform(testData)
    predictions.show()
    val evaluator = new BinaryClassificationEvaluator()
      .setMetricName("areaUnderROC")
      .setRawPredictionCol("rawPrediction")
      .setLabelCol("label")
    println("AUC = " + evaluator.evaluate(predictions))
    println(s"Model params: ${model.explainParams()}")
  }
}
