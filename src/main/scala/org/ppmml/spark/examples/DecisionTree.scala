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

import org.apache.spark.ml.{Pipeline}
import org.apache.spark.ml.classification.DecisionTreeClassifier
import org.apache.spark.ml.feature.{StringIndexer, VectorAssembler}
import org.apache.spark.sql.SparkSession

/**
  * Generating spark decision tree models and schema
  */
object DecisionTree extends TrainingUtils {
  override val spark: SparkSession = SparkSession.builder()
    .master("local[*]").appName(this.getClass.getCanonicalName).getOrCreate()

  def train() = {
    val data = loadIris()
    val Array(trainData, testData) = data.randomSplit(Array(0.8, 0.2))
    // preprocessing
    val indexer = new StringIndexer().setInputCol("y").setOutputCol("label")
    val vectorAssembler = new VectorAssembler()
      .setInputCols(Array("x1", "x2", "x3", "x4")).setOutputCol("features")
    // set classifier
    val classifier = new DecisionTreeClassifier()
      .setLabelCol("label").setMaxDepth(6).setMaxBins(50).setFeaturesCol("features")
    val pipeline = new Pipeline().setStages(Array(indexer, vectorAssembler, classifier))
    val model = pipeline.fit(trainData)
    // Save model and schema
    model.write.overwrite().save("./spark-models/decision_tree_model")
    saveSchema(trainData.schema, "./spark-models/decision_tree.json")
    doEvaluate(model, testData)
  }

  def main(args: Array[String]): Unit = {
    train()
  }
}
