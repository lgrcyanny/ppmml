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

import org.apache.spark.ml.{Pipeline, PipelineModel}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{DataType, StructType}

import scala.io.Source

/**
  * Created by lgrcyanny on 17/12/19.
  */
object TestConverterUtil {

  val spark = SparkSession.builder().master("local[*]").appName(this.getClass.getName).getOrCreate()

  def main(args: Array[String]): Unit = {
    val basePath = "/Users/lgrcyanny/Codecookies" +
      "/machine-learning-workspace/pmml-wp/pmml-lab/notebooks/pmml-models/spark/spark-models"
    val schemaPath = s"$basePath/decision_tree.json"
    val modelPath = s"$basePath/logistic_regression_model"
    val jsonString = Source.fromFile(schemaPath).toString()
    println(jsonString)
//    val schemaDF = DataType.fromJson(Source.fromFile(schemaPath).toString()).asInstanceOf[StructType]

    val model = PipelineModel.load(modelPath)
    val testDataPath = "/Users/lgrcyanny/Codecookies/machine-learning-workspace/datasets/iris/iris.data"
    val testDF = spark.read.format("csv")
      .option("inferSchema", "true")
      .option("header", "false").load(testDataPath).toDF("x1", "x2", "x3", "x4", "y")
    testDF.printSchema()
    testDF.show()
    val predictions = model.transform(testDF)
    println("predictions")
    predictions.show()
  }
}
