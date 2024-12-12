def transform_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        content = infile.read()
    cleaned_content = content.replace('\n', '')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        outfile.write(cleaned_content)


input_file = 'WDICountry.csv'   
output_file = 'Countries.csv' 
transform_csv(input_file, output_file)

input_file = 'WDISeries.csv'   
output_file = 'Indicators.csv' 
transform_csv(input_file, output_file)