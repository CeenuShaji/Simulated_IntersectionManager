This folder contains a dataset of total 193 FPGAs measured over a period of one year. The first phase of measurement includes 125 FPGAs measured in 2010. The second phase includes 68 additional FPGAs measured in 2011. Therefore, the total number of measured FPGAs is 193. This folder contains data from both 2010 and 2011.

The data is stored in comma-separated value (csv) format for easy export/import across applications. There are 193 files in total; one for each of the 193 FPGAs. The filenames have the format < ChipID >.csv where < ChipID > is the serial number of each board measured. 

In each file, there are 512 lines for 512 ROs. Each of the line contains 100 RO frequencies separated by comma. These are 100 samples of the corresponding RO. 

It is important to describe the spatial location of the ROs. The 2-D RO array has 32 rows and 16 columns. The first RO (first line in the csv file) is located at the CLB location X10Y8 (SLICE_X18Y14:SLICE_X19Y15), and the 16th RO (16th line in the csv file) is located at CLB X25Y8 (SLICE_X48Y14:SLICE_X49Y15). The intermediate 14 ROs are located across CLB location X11Y8 to CLB location X24Y8. 

Similarly, the second row starts with the 17th RO (17th line in the csv file) at CLB location X10Y9 and ends with the 32nd RO (32nd line in the csv file) at the CLB location X25Y10. Likewise, the 512th RO (the last line in the csv file) is located at the CLB location X25Y39.
