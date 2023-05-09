little program to try and find nzpocs codes based on a dump from the 
Delphic LIS testmaster table. 

To run, dump the testmaster table to a csv file or dump the obscode table from eclair 
specify the filename and type in an argument 

nzpocs.py -f <inputfilename> -o <outputfilename> -s lis|eclair

it should dump a file with each local test and potential LOINC code matches