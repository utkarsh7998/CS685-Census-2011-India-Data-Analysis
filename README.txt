Language Used : Python 3.8

Python Libraries used:
numpy
pandas
xlrd
scipy
openpyxl
warnings

Prerequisites: 

1. The above language and all the mentioned libraries must be installed in your local machine before proceeding further.
2. A little bit of patience because sometimes it takes a bit longer than usual to complete execution.


Datasets/ Input Files

DDW_PCA0000_2011_Indiastatedist.xlsx
DDW-C18-0000.xlsx
DDW-C19-0000.xlsx
https://censusindia.gov.in/2011census/C-series/C08.html
http://censusindia.gov.in/2011census/C-17.html
https://censusindia.gov.in/2011census/C-series/C-14.html


Instructions to run:-

Step 1: Extract 21111063-assign2.zip in your local machine

Step 2: Open Terminal in Ubuntu by pressing 'Ctrl + Shift + T'

Step 3: Navigate to the folder where your files are extracted
        For example: cd path/21111063-assign2/

Step 4: Type the following command to give permission to the sh file to be executed
        chmod +x ./assign2.sh
            
Step 5: Type the following command to run the file. This command will run all the files one by one automatically.
        After a few minutes you will see a number of output files generated in the same directory. 
        ./assign2.sh



Output Files:-

For Question_1 : percent-india.csv

For Question_2 : gender-india-a.csv
		 gender-india-b.csv
		 gender-india-c.csv

For Question_3 : geography-india-a.csv
                 geography-india-b.csv
                 geography-india-c.csv

For Question_4 : 3-to-2-ratio.csv
                 2-to-1-ratio.csv
                 
For Question_5 : age-india.csv

For Question_6 : literacy-india.csv

For Question_7 : region-india-a.csv
                 region-india-b.csv

For Question_8 : age-gender-a.csv                 
		 age-gender-b.csv
                 age-gender-c.csv

For Question_9 : literacy-gender-a.csv
		 literacy-gender-b.csv
		 literacy-gender-c.csv


NOTE: 

    1. Statistical Tests Used: I have used one sample ttest for statistical test analysis and reporting pvalue.
    2. Please use either VS Code or Notepad to open the output csv files. MS Excel has some issues, like for age group: 5-9, gets displayed as 5th September


