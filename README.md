# A little program to try and find nzpocs codes based on a dump from the Delphic LIS testmaster table. 

To run, dump the testmaster table to a csv file or dump the obscode table from eclair 

Switches:
```
--inputfile, -i "input file name"
--outputfile, -o "output file name"
--source, -s "lis"|"eclair" choose format of source csv file either lis or eclair
--type, -t "csv"|"json" ok, a bit weird but choose the nzpocs source, either the excel spreadsheet converted to csv in nzpocs-observation-code-set-1-October-2022.csv or nzhts-nzpocs.json file as downloaded fron the nzhts fhir terminology service
--nomissmatches, -nm a switch that suppress outputting tests that did not have a potential match 
```

Examples:

`nzpocs.py -i testmaster.csv -o -nzpocs-out.csv -s lis -t csv`

This will use the nzpocs csv in this repo and parse a dump from a lis formatted test database. Basically assumes some field names based on the Delphic LIS

`nzpocs.py -i eclair-obscode.csv -o nzpocs-out.csv -s eclair -t json`

Will do the same but for a dump from the Eclair system, this will use the json file that has been extracted from the nzhts fhit terminology server.


Output will be local code, local description and a line for every potential match of a nzpocs code. 



