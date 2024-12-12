mkdir data

wget https://databank.worldbank.org/data/download/WDI_CSV.zip

unzip WDI_CSV.zip 

rm WDIcountry-series.csv && rm WDIseries-time.csv && rm WDIfootnote.csv

mv WDICSV.csv data/Data.csv

python3 transform_CSV.py

mv Countries.csv data/Countries.csv && mv Indicators.csv data/Indicators.csv

rm WDICountry.csv && rm WDISeries.csv && rm WDI_CSV.zip