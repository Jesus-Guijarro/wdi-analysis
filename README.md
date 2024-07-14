# World Development Indicators Analysis

## 1. Installation and configuration

### Download data and extract files
```shell
mdkir data && cd data
```
```shell
wget https://databank.worldbank.org/data/download/WDI_CSV.zip
```
```shell
unzip WDI_CSV.zip && rm WDI_CSV.zip
```

### Project IntelliJ
Java SDK version: 11

```sbt
ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.13.10"

lazy val root = (project in file("."))
  .settings(
    name := "wdi-analysis",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % "3.5.1",
      "org.apache.spark" %% "spark-sql" % "3.5.1"
    )
  )
```
Check Spark version installed:
```shell
spark-shell --version
```





