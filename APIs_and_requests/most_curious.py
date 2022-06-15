import pandas as pd
import requests
import json


# Function to get usernames of the 5 users with the most questions posted in the last 2 days. (actually between 6th and 8th June but whatever)
def most_curious(filename='most_curious.json'):
    stack_exchange = ('https://api.stackexchange.com')
    
    final_data = {}
    i = 0
    while True:
        i += 1
        next_page = f'/2.3/questions?page={i}&pagesize=30&fromdate=1654560000&todate=1654732800&order=asc&sort=creation&site=stackoverflow&filter=!9RRSCypBf'
        response = requests.get(stack_exchange+next_page)
       
        content = response.content
        decoded_content = content.decode('utf8').replace("'", '"')
        data = json.loads(decoded_content)
        final_data.update(data)
        
        if i == 25:
            break
            
    # Dump to json file formatted
    with open(filename, 'w') as outfile:
        json.dump(final_data, outfile, indent=4, sort_keys=True)

most_curious()




