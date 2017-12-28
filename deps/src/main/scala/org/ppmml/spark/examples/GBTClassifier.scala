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

import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.{GBTClassifier, OneVsRest}
import org.apache.spark.ml.feature.{StringIndexer, VectorAssembler}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.IntegerType

/**
  * GBTClassifier currently only supports binary classification
  * org.apache.spark.ml.classification.OneVsRestModel is not supported by jpmml
  */
object GBTClassifier extends TrainingUtils {
  override val spark = SparkSession.builder()
    .master("local[*]").appName(this.getClass.getCanonicalName).getOrCreate()

  def train(outputBase: String) = {
    val data = loadIris()
    val transformedData = data.withColumn("label", (col("y") === "Iris-setosa").cast(IntegerType))
    val Array(trainData, testData) = transformedData.randomSplit(Array(0.8, 0.2))
    // preprocessing
    val vectorAssembler = new VectorAssembler()
      .setInputCols(Array("x1", "x2", "x3", "x4")).setOutputCol("features")
    val classifier = new GBTClassifier()
      .setMaxIter(10)
      .setMaxDepth(3)
      .setStepSize(0.1)
      .setLabelCol("label")
      .setFeaturesCol("features")
    val pipeline = new Pipeline().setStages(Array(vectorAssembler, classifier))
    val model = pipeline.fit(trainData)
    // Save model and schema
    println(s"saving model to ${outputBase}")
    model.write.overwrite().save(s"${outputBase}/gbt_classifier_model")
    saveSchema(trainData.schema, s"${outputBase}/gbt_classifier.json")
  }

  def main(args: Array[String]): Unit = {
    val outputBasePath = if (args.length >= 1) {
      args(0)
    } else {
      "./spark-models"
    }
    train(outputBasePath)
  }

}
