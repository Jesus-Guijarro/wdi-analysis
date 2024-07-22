import org.apache.spark.sql.{DataFrame, SparkSession}
import java.io.File
import java.nio.file.{Files, Paths, StandardCopyOption}

object DataAnalysis {
  def createCSV(df: DataFrame, category: String, topic: String, indicator: String): Unit = {
    val baseDir = "reports"
    val categoryDir = Paths.get(baseDir, category).toString
    val topicDir = Paths.get(categoryDir, topic).toString

    new File(topicDir).mkdirs()

    val modifiedIndicator = indicator.replace(".", "-")
    val nameFile = Paths.get(topicDir, s"${category}_${topic}_${modifiedIndicator}.csv").toString

    val tempDir = Paths.get(baseDir, s"temp_WDI_$topic").toString

    df.coalesce(1).write.option("header", "true").csv(tempDir)

    val tempFile = new File(tempDir).listFiles().filter(_.getName.startsWith("part-")).head

    Files.move(tempFile.toPath, Paths.get(nameFile), StandardCopyOption.REPLACE_EXISTING)

    new File(tempDir).listFiles().foreach(_.delete())
    new File(tempDir).delete()
  }

  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder
      .appName("WDI Analysis")
      .config("spark.master", "local[*]")
      .getOrCreate()

    val filePath = "data/Countries_Indicators.csv"
    val df = spark.read.option("header", "true").option("inferSchema", "true").csv(filePath)

    // Country Categories
    val innovativeCountries = List("ESP", "USA", "CHE", "SWE", "GBR", "NLD")
    val neighbourCountries = List("ESP", "PRT", "FRA", "ITA", "MAR", "DZA")
    val countries = List(innovativeCountries, neighbourCountries)

    // Indicators by topic
    val economicIndicators = List("NY.GDP.MKTP.CD", "NY.GDP.PCAP.CD", "NY.GDP.MKTP.KD.ZG", "NY.GNP.PCAP.CD", "SI.POV.GINI", "FP.CPI.TOTL.ZG", "IC.BUS.EASE.XQ")
    val educationIndicators = List("SE.XPD.TOTL.GD.ZS", "SE.SEC.ENRR", "SE.TER.ENRR", "SE.TER.CUAT.BA.ZS")
    val energyIndicators = List("EG.USE.PCAP.KG.OE", "EG.ELC.ACCS.ZS")
    val researchDevIndicators = List("GB.XPD.RSDV.GD.ZS", "SP.POP.SCIE.RD.P6", "SP.POP.TECH.RD.P6", "IP.PAT.RESD", "IP.PAT.NRES", "IP.JRN.ARTC.SC", "IT.NET.USER.ZS", "IT.CEL.SETS.P2", "IT.NET.BBND.P2", "IT.NET.SECR.P6", "TX.VAL.TECH.MF.ZS", "TX.VAL.TECH.CD")
    val indicators = List(economicIndicators, educationIndicators, energyIndicators, researchDevIndicators)

    // Columns to select
    val years = (2001 to 2023).map(_.toString).toList
    val fixedColumns = List("Country Name", "Country Code", "Indicator Name")
    val selectedColumns = fixedColumns ++ years

    val categories = List("innovative", "neighbour")
    val topics = List("economic", "education", "energy", "research_dev")

    for ((category, i) <- categories.zipWithIndex) {
      for ((topic, j) <- topics.zipWithIndex) {
        for (indicator <- indicators(j)) {
          val dfFilter = df.filter(df("Country Code").isin(countries(i): _*) && df("Indicator Code") === indicator)
          val dfSelect = dfFilter.select(selectedColumns.head, selectedColumns.tail: _*)

          createCSV(dfSelect, category, topic, indicator)
        }
      }
    }
    spark.stop()
  }
}
