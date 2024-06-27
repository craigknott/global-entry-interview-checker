import requests
import time
import os

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" sound name "Temple"'
              """.format(text, title))

notify("Title", "Heres a test alert")

def choose_locations():
    r = requests.get('https://ttp.cbp.dhs.gov/schedulerapi/locations/?inviteOnly=false&operational=true&serviceName=Global%20Entry')
    if r.status_code != 200:
        print(f'error fetching locations')
    name = input("Location name: ")
    locs = {}
    for x in r.json():
        if name.lower() in x['name'].lower():
            q = input(f"Found match: {x['name']}, do you want to include this (Y/N, default Y)?")
            if q in ['y', 'Y', '']:
                locs[x['name']] = x['id']
    return locs


def check_location(location_id):
    r = requests.get(f'https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId={location_id}&minimum=1')
    return r.json()


def main():
    locations = choose_locations()
    if len(locations) == 0:
        print("no locations found")
        return

    # test locations
    for _, l in locations.items():
        print(check_location(l))

    while True:
        time.sleep(5)
        for k, l in locations.items():
            r = check_location(l)
            if r != []:
                notify(f"TTP Availability @{k}", "TTP Availability Found")
                print(f'Found availability: {r}')

if __name__=='__main__':
    main()
