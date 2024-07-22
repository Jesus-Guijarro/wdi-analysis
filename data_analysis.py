from pyspark.sql import SparkSession
import shutil
import os

def create_csv(df,category,topic,indicator):
    base_dir = "reports"
    category_dir = os.path.join(base_dir, category)
    topic_dir = os.path.join(category_dir, topic)
    
    os.makedirs(topic_dir, exist_ok=True)

    modified_indicator = indicator.replace(".","-")

    namefile = os.path.join(topic_dir, f"{category}_{topic}_{modified_indicator}.csv")

    temp_dir = os.path.join(base_dir, "temp_WDI_" + topic)

    df.coalesce(1).write.option("header", "true").csv(temp_dir)

    temp_file = [file for file in os.listdir(temp_dir) if file.startswith("part-")][0]

    shutil.move(os.path.join(temp_dir, temp_file), namefile)

    shutil.rmtree(temp_dir)

spark = SparkSession.builder \
    .appName("WDI Analysis") \
    .getOrCreate()

file_path = "data/Countries_Indicators.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Country Categories
innovative_countries = ["ESP", "USA", "CHE", "SWE", "GBR", "NLD"]
neighbour_countries = ["ESP","PRT","FRA","ITA","MAR","DZA"]
countries=[innovative_countries, neighbour_countries]

# Indicators by topic
economic_indicators = ["NY.GDP.MKTP.CD","NY.GDP.PCAP.CD","NY.GDP.MKTP.KD.ZG","NY.GNP.PCAP.CD","SI.POV.GINI","FP.CPI.TOTL.ZG","IC.BUS.EASE.XQ"]
education_indicators = ["SE.XPD.TOTL.GD.ZS","SE.SEC.ENRR","SE.TER.ENRR","SE.TER.CUAT.BA.ZS"]
energy_indicators = ["EG.USE.PCAP.KG.OE","EG.ELC.ACCS.ZS"]
research_dev_indicators = ["GB.XPD.RSDV.GD.ZS","SP.POP.SCIE.RD.P6","SP.POP.TECH.RD.P6","IP.PAT.RESD","IP.PAT.NRES","IP.JRN.ARTC.SC","IT.NET.USER.ZS","IT.CEL.SETS.P2","IT.NET.BBND.P2","IT.NET.SECR.P6","TX.VAL.TECH.MF.ZS","TX.VAL.TECH.CD"]
indicators=[economic_indicators, education_indicators, energy_indicators, research_dev_indicators]

#Columns select
years = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
fixed_columns = ["Country Name", "Country Code", "Indicator Name"]
selected_columns = fixed_columns + years

categories=["innovative","neighbour"]
topics=["economic","education","energy","research_dev"]

for i, category in enumerate(categories):
    for j, topic in enumerate(topics):
        for indicator in indicators[j]:
            df_filter = df.filter((df["Country Code"].isin(countries[i])) & (df["Indicator Code"] == indicator))
            df_select = df_filter.select(*selected_columns)

            create_csv(df_select,category,topic,indicator)
