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
import org.apache.spark.ml.classification.MultilayerPerceptronClassifier
import org.apache.spark.ml.feature.{StringIndexer, VectorAssembler}
import org.apache.spark.sql.SparkSession

object NeuralNetwork extends TrainingUtils {
  override val spark = SparkSession.builder().master("local[*]").appName(this.getClass.getCanonicalName).getOrCreate()

  def train() = {
    val data = loadIris()
    val Array(trainData, testData) = data.randomSplit(Array(0.8, 0.2))
    val layers = Array(4, 20, 20, 3)
    // preprocessing
    val indexer = new StringIndexer().setInputCol("y").setOutputCol("label")
    val vectorAssembler = new VectorAssembler()
      .setInputCols(Array("x1", "x2", "x3", "x4")).setOutputCol("features")
    val classifier = new MultilayerPerceptronClassifier()
      .setLayers(layers)
      .setLabelCol("label")
      .setBlockSize(128)
      .setSeed(1234L)
      .setMaxIter(100)
    // pipeline data
    val pipeline = new Pipeline().setStages(Array(indexer, vectorAssembler, classifier))
    val model: PipelineModel = pipeline.fit(trainData)

    // output spark model
    model.write.overwrite().save("./spark-models/neural_network_model")
    saveSchema(trainData.schema, "./spark-models/neural_network.json")

    // evaluate
    val predictions = model.transform(testData)
    predictions.show()
    println(s"Model params: ${model.explainParams()}")
  }

  def main(args: Array[String]): Unit = {
    train()
  }
}
