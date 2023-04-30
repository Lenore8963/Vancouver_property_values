# Calculate and rank the sales to assessment ratioes of Vancouver properties

This is the final project of the course: Intensive Foundations of Computer Science.

In this project, I am analyzing Vancouver property sales records for some interesting findings. 
The data I have chosen are from two sources:
1, Nonprofit organization Open Housing(https://openhousing.ca/)
VAN_PROPERTY_SALES_RECORDS_2016 = https://openhousing.ca/wp-content/uploads/2022/11/vanresales2016.csv
2, The City of Vancouver Open Data Portal
BC_PROPERTY_TAX_2016 = https://opendata.vancouver.ca/explore/dataset/property-tax-report-2016-2019/table/?refine.report_year=2016
BC_PROPERTY_TAX_2018 = https://opendata.vancouver.ca/explore/dataset/property-tax-report-2016-2019/table/?refine.report_year=2018

The main data I hope to get out of this project is the Sales to Assessment Ratio (SAR) of each property. Each year, the BC government releases an assessed value of each property and uses the Assessment to Sales Ratio (ASR) to measure of how accurate its assessment of a sold property is to market value. I am doing it the opposite way to locate the anomalous sales in Vancouver. Because the SAR is the sold price divided by the assessed value, if it is extremely high or low, there might be an interesting transaction behind it, such as property speculation or even money laundering or bribery through real estate sales. 

I decided to analyze the year 2016 because this is the year when the government slapped the foreign buyer tax.
The reason why I use the 2018 Property Tax data is that I need to exclude the possibility of new constructions or major improvements in the results, otherwise the majority of properties with exceptionally high SAR would be due to these two reasons. Furthermore, the government didn’t upload 2016’s “year built” and “big improvement” data until two years later.

The Property Identifier code PID is a unique ID for each property. I use this data as keys in the dictionaries and the first index in each list of the list of lists to match each property with its data in separate files.

Also, downloading the files takes time, causing some output to take a long time to appear.
