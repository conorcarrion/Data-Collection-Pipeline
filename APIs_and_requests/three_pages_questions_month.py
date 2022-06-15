import requests
import json

# function
def three_pages_questions_month():
    stack_exchange = ('https://api.stackexchange.com')
    combined_dict_results = {}
    # for page in range(1,10+1):
    question_search = f'/2.3/questions?page=1&pagesize=10&fromdate=1654041600&todate=1654732800&order=asc&sort=creation&site=stackoverflow&filter=!-)8(vv2ceDvU'
    response = requests.get(stack_exchange+question_search)
    content = response.content

    # Decode UTF-8 bytes to Unicode
    decoded_content = content.decode('utf8').replace("'", '"')

    # Load to a Python list
    data = json.loads(decoded_content)
    combined_dict_results.update(data)
    return combined_dict_results

instanceof3pqm= three_pages_questions_month()

def write_to_file(sample_json):
    with open('three_pages_questions_month.json', 'w') as outfile:
        json.dump(sample_json, outfile, indent=4, sort_keys=True)

write_to_file(instanceof3pqm)
