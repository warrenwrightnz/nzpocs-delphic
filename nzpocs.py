import csv
import argparse
import os 

# parse an argument to define if operating on lis or eclair data and pass in the path for the input file
parser = argparse.ArgumentParser()
parser.add_argument("--inputfile", "-f", required=True)
parser.add_argument("--outputfile", "-o", required=True)
parser.add_argument("--source","-s", choices=['lis','eclair'])
args = parser.parse_args()

def search_nzpocs(search_text, search_in_text):
    
    nomatchlist = ['blood','urine','post','group','serum','plasma','specimen','by','in','test', '','.']
    for text in search_text:
        # leave loop if text in nomatch list
        if text.lower() in nomatchlist:
            return False
        for search in search_in_text:
            if text.lower() in search.lower():
                # Add the matching code, test, and short description to the list
                # print('search: ' + search + ' text: ' + text)
                
                return True
    # couldn't find match, return false
    return False

def main(): 
    # Open the first CSV file containing the codeset relative to nzpocs folder
    with open('nzpocs-observation-code-set-1-October-2022.csv', newline='', encoding='utf-8') as csvfile1:
        nzpocs = csv.DictReader(csvfile1)
        
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
                    if args.source == "lis":
                        matching_data.append((paltest['test'], paltest['short_desc'],paltest['text'],'','','','0'))
                    else:
                        matching_data.append((paltest['OBSC_OBSID'], paltest['OBSC_DESC'],'','','','','0'))
                csvfile1.seek(0)
                nzpocs = csv.DictReader(csvfile1)
                        
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
main()