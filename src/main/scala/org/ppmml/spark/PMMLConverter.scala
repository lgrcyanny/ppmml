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
package org.ppmml.spark

import org.apache.spark.sql.SparkSession

/**
  * It's a wrapper of org.jpmml.spark.Main
  * Since it will init SparkContext with exception A master URL must be set in your configuration
  * To fix the exception, this wrapper creates a SparkSession with master local
  */
object PMMLConverter {
  val spark = SparkSession.builder()
    .appName("PMMLConverter")
    .config("spark.ui.port", "0")
    .master("local[*]").getOrCreate()
  def main(args: Array[String]): Unit = {
    org.jpmml.sparkml.Main.main(args: _*)
  }
}
