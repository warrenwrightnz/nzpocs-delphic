import csv
import argparse
import os 
import json

# parse an argument to define if operating on lis or eclair data and pass in the path for the input file
parser = argparse.ArgumentParser()
parser.add_argument("--inputfile", "-i", required=True)
parser.add_argument("--outputfile", "-o", required=True)
parser.add_argument("--source","-s", choices=['lis','eclair'])
parser.add_argument("--type","-t", default="csv", choices=['csv','json'])
parser.add_argument('--nomissmatches','-nm',action='store_true')
args = parser.parse_args()

def search_nzpocs(search_text, search_in_text):
    # print(search_text,search_in_text)
    
    nomatchlist = ['blood','urine','post','group','serum','plasma','specimen','by','in','test', '','.']
    for text in search_text:
        if text.lower() in nomatchlist:
            continue
        # leave loop if text in nomatch list
        for search in search_in_text:
            if search.lower in nomatchlist:
                continue
            if text.lower() in search.lower():
                # Add the matching code, test, and short description to the list
                #print( ' text:' + text + ' in: ' + search )
                return True
    # couldn't find match, return false
    return False

def main(): 
    test_nomatches = 0
    test_matches= 0
    # Open the CSV or json file containing the codeset relative to nzpocs folder
    if args.type == 'csv':
        pocsfname = 'nzpocs-observation-code-set-1-October-2022.csv'
    if args.type == 'json':
        pocsfname = 'nzhts-nzpocs.json'

    with open(pocsfname, newline='', encoding='utf-8') as nzpocsfile:
        if args.type == 'csv':
            nzpocs = csv.DictReader(nzpocsfile)
        if args.type == 'json':
            nzpocs = json.load(nzpocsfile)
        
        # Open the second CSV file containing the test groups from the passed in argument
        with open(os.path.abspath(args.inputfile), newline='', encoding='utf-8') as csvfile2:
            paltests = csv.DictReader(csvfile2)
            
            # Initialize a list to hold the matching codes, tests, and short descriptions
            matching_data = []
            matches = 0
            # Loop through each row in the test groups CSV file
            for paltest in paltests:
                # Extract the text to search for from the relevant columns
                if args.source == "lis":
                    search_text = [paltest['short_desc'],paltest['text']]
                else:
                    search_text = [paltest['OBSC_DESC']]
                matches = 0
                #print(search_text)
                # Loop through each row in the codeset CSV file
                if args.type == 'csv':
                    for nzpoc in nzpocs:
                        # Extract the text to search within from the relevant columns
                        search_in_text = [nzpoc['COMPONENT'],nzpoc['NZ_SHORT_NAME']]
                        #print(search_in_text)
                        if search_nzpocs(search_text,search_in_text):
                            matches+=1
                            if args.source == "lis":
                                matching_data.append((paltest['test'], paltest['short_desc'],paltest['text'], nzpoc['CODE'],nzpoc['NZ_SHORT_NAME'],nzpoc['COMPONENT'],matches))
                            else:
                                matching_data.append((paltest['OBSC_OBSID'], paltest['OBSC_DESC'],'', nzpoc['CODE'],nzpoc['NZ_SHORT_NAME'],nzpoc['COMPONENT'],matches))
                        # Reset the codeset CSV reader to the beginning of the file
                    if matches == 0:
                        test_nomatches +=1
                        if not args.nomissmatches:
                            if args.source == "lis":
                                matching_data.append((paltest['test'], paltest['short_desc'],paltest['text'],'','','','0'))
                            else:
                                matching_data.append((paltest['OBSC_OBSID'], paltest['OBSC_DESC'],'','','','','0'))
                    nzpocsfile.seek(0)
                    nzpocs = csv.DictReader(nzpocsfile)
                if args.type == 'json':
                    nzpocs_array = nzpocs['expansion']['contains']
                    #print(str(nzpocs_array))
                    for item in nzpocs_array:
                        for key,value in item.items():
                            if key == 'code':
                                curr_code = value
                            if key == 'display':
                                search_in_text = [value]
                        if search_nzpocs(search_text,search_in_text):
                            matches+=1
                            if args.source == "lis":
                                matching_data.append((paltest['test'], paltest['short_desc'],paltest['text'], curr_code,value,matches))
                            else:
                                matching_data.append((paltest['OBSC_OBSID'], paltest['OBSC_DESC'],'', curr_code,value,matches))
                    if matches == 0:
                        test_nomatches+=1
                        if not args.nomissmatches:
                            if args.source == "lis":
                                matching_data.append((paltest['test'], paltest['short_desc'],paltest['text'],'','','','0'))
                            else:
                                matching_data.append((paltest['OBSC_OBSID'], paltest['OBSC_DESC'],'','','','','0'))
                if matches != 0:
                    test_matches +=1
                                            
            # Print the list of matching data
            with open(os.path.abspath(args.outputfile),'w', newline='', encoding='utf-8') as csvfilew:
                matchwriter = csv.writer(csvfilew, dialect='excel')
                if args.source == "lis":
                    matchwriter.writerow(['TEST','SHORT_DESC','TEXT','"Potential LOINC CODE"','NZ_SHORT_NAME','COMPONENT'])
                else:
                    matchwriter.writerow(['OBSC_OBSID','OBSC_DESC','','"Potential LOINC CODE"','NZ_SHORT_NAME','COMPONENT'])
                matchwriter.writerows(matching_data)

            #for data in matching_data:
            #    print(data)
            total_tests = test_matches + test_nomatches
            print(f"Matched {test_matches} tests. Was not able to match {test_nomatches} tests out of {total_tests} tests")
main()