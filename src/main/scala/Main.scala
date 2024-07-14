import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

object Main {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession
      .builder()
      .appName("Leyendo CSV con Spark")
      .config("spark.master", "local[*]")
      .getOrCreate()

    val filePath = "data/WDICSV.csv"

    spark.sparkContext.setLogLevel("ERROR")

    // From CSV to a DataFrame
    val df = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv(filePath)

    // Schema DataFrame
    df.printSchema()

    // First 20 rows
    df.show()

    spark.stop()
  }

}