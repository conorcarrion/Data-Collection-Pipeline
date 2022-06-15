import requests
import json

stack_exchange = ('https://api.stackexchange.com')
current_search = '/2.3/posts?page=1&pagesize=10&fromdate=1654473600&todate=1654560000&order=desc&sort=votes&site=stackoverflow&filter=!1zI.IAi9PDysp4LGgMVQz'

# function to list users and post score
def top_upvoted(site, field):
    response = requests.get(site+field)
    content = response.content

    # Decode UTF-8 bytes to Unicode
    decoded_content = content.decode('utf8')

    # Load to a Python list
    data = json.loads(decoded_content)
    # print(data)

    for i in data.get("items"):
        owner = i.get('owner')
        display_name = owner.get('display_name')
        score = i.get('score')
        print(f'{display_name} made a posts with score of {score}')

top_upvoted(stack_exchange, current_search)