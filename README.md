little program to try and find nzpocs codes based on a dump from the 
Delphic LIS testmaster table. 

To run, dump the testmaster table to a csv file or dump the obscode table from eclair 
specify the filename and type in an argument 

nzpocs.py -i <inputfilename> -o <outputfilename> -s lis|eclair -t csv|json -nm

switches:
`--inputfile, -i "input file name"
`--outputfile, -o "output file name"
`--source, -s "lis"|"eclair" choose format of source csv file either lis or eclair
`--type, -t "csv"|"json" ok, a bit weird but choose the nzpocs source, either the excel spreadsheet converted to csv in nzpocs-observation-code-set-1-October-2022.csv or nzhts-nzpocs.json file as downloaded fron the nzhts fhir terminology service
`--nomissmatches, -nm a switch that suppress outputting tests that did not have a potential match 

Output will be local code, local description and a line for every potential match of a nzpocs code. 



