import csv

def search_nzpocs(search_text, search_in_text):
    global matches
    nomatchlist = ['blood','urine','post','group','serum','plasma','specimen','by','in','test', '','.']
    for text in search_text:
        # leave loop if text in nomatch list
        if text.lower() in nomatchlist:
            return False
        for search in search_in_text:
            if text.lower() in search.lower():
                # Add the matching code, test, and short description to the list
                # print('search: ' + search + ' text: ' + text)
                matches+=1
                return True
    # couldn't find match, return false
    return False

# Open the first CSV file containing the codeset
with open('c:/dev/Warren/nzpocs-observation-code-set-1-October-2022.csv', newline='', encoding='utf-8') as csvfile1:
    nzpocs = csv.DictReader(csvfile1)
    
    # Open the second CSV file containing the test groups
    with open('c:/dev/delphic/listestinfo/testmaster.csv', newline='', encoding='utf-8') as csvfile2:
        paltests = csv.DictReader(csvfile2)
        
        # Initialize a list to hold the matching codes, tests, and short descriptions
        matching_data = []
        
        # Loop through each row in the test groups CSV file
        for paltest in paltests:
            # Extract the text to search for from the relevant columns
            search_text = [paltest['short_desc'],paltest['text']]
            matches = 0
            #print(search_text)
            # Loop through each row in the codeset CSV file
            for nzpoc in nzpocs:
                # Extract the text to search within from the relevant columns
                search_in_text = [nzpoc['COMPONENT']]
                #print(search_in_text)
                if search_nzpocs(search_text,search_in_text):
                    matching_data.append((paltest['test'], paltest['short_desc'],paltest['text'], nzpoc['CODE'],nzpoc['NZ_SHORT_NAME'],nzpoc['COMPONENT'],matches))
                # Reset the codeset CSV reader to the beginning of the file
            if matches == 0:
                matching_data.append((paltest['test'], paltest['short_desc'],paltest['text'],'','','','0'))
            
            csvfile1.seek(0)
            nzpocs = csv.DictReader(csvfile1)
                    
        # Print the list of matching data
        with open('C:/dev/warren/matching_testmaster2.csv','w', newline='', encoding='utf-8') as csvfilew:
            matchwriter = csv.writer(csvfilew, dialect='excel')
            matchwriter.writerow(['TEST','SHORT_DESC','TEXT','"Potential LOINC CODE"','NZ_SHORT_NAME','COMPONENT'])
            matchwriter.writerows(matching_data)

        #for data in matching_data:
        #    print(data)
