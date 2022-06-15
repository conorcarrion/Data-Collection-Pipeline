import requests
import json

stack_exchange = ('https://api.stackexchange.com')
badge_search = '/2.3/badges?page=1&pagesize=3&order=asc&max=named&sort=type&site=stackoverflow&filter=!-)8(vv2ceDvU'

# function
def get_badges(site, field):
    response = requests.get(site+field)
    content = response.content

    # Decode UTF-8 bytes to Unicode
    decoded_content = content.decode('utf8')

    # Load to a Python list
    data = json.loads(decoded_content)
    # print(data)

    for badge in data.get('items'):
        badge_name = badge.get('name')
        badge_id = badge.get('badge_id')
        print(f'{badge_id} - {badge_name}' )


get_badges(stack_exchange, badge_search)

def get_recent_badge_winners(badge_id_list):
    badge_winners = []
    for badge_id in badge_id_list:
        site = ('https://api.stackexchange.com')
        field = f'/2.3/badges/{badge_id}/recipients?page=1&pagesize=1&site=stackoverflow&filter=!SV_dAhIj9dh2URJ2-z'
        response = requests.get(site+field)
        content = response.content

        # Decode UTF-8 bytes to Unicode
        decoded_content = content.decode('utf8')

        # Load to a Python list
        data = json.loads(decoded_content)
        # print(data)
        badge_winner = data.get('items')[0]
        badge_winners.append(badge_winner)
    return badge_winners

get_recent_badge_winners(['222', '1306', '260'])