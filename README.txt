To run the model:

1. Execute run_model.bat. This will generate the input files, run the model on those input files,
and then format the data into CW_trimmed.csv and LRG_trimmed.csv.

2. Open CW_trimmed.csv and LRG_trimmed.csv in Microsoft Excel and save them as .xlsx files.

3. Run testplotter.m in MATLAB, once with

    fname = "./CW_trimmed"

and once with

    fname = "./LRG_trimmed".

Comment and uncomment the appropriate lines at the bottom of the file to save the plots
as .png's or .eps files for better publication quality.