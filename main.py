import requests
import json
import datetime
from datetime import datetime

url1= 'https://api.slangapp.com/challenges/v1/activities'
url2= 'https://api.slangapp.com/challenges/v1/activities/sessions'
header = {'Content-Type': 'application/json', 'Authorization': 'Basic Njg6M2tmQnFRTmNDb3lHc2hHNzlOZFBBR3J3YllrZzFldFVMN0hhNVVER2trTT0='}

activities_response = requests.get(url1, headers=header)
print(activities_response.url)

if activities_response.status_code == 200:
    print('Success!')
    activities_response_json = json.loads(activities_response.text)
    print(activities_response_json)

    #Group by user_id
    groupid = {}
    for activities in activities_response_json: # Iterate through activities
        user_id = activities['user_id'] # Get user_id
        if user_id not in groupid:
            groupid[user_id] = [] # Create new list for user_id
        groupid[user_id].append(activities) # Append activities to list
    print("Group by user_id:", groupid)

    for user_id in groupid:
        activities_ids = []
        for activities in groupid[user_id]:
            activities_ids.append(activities['id'])
        groupid[user_id] = activities_ids


    #Dictionary of activities_ids
    groupid_activitiesids = {}
    for user_id in groupid:
        groupid_activitiesids[user_id] = {}
        for activities_id in groupid[user_id]:
            groupid_activitiesids[user_id][activities_id] = {}
            for activities in activities_response_json:
                if activities['id'] == activities_id:
                    groupid_activitiesids[user_id][activities_id] = activities

    # the list of activitiess ids in each groupid_activitiesids
    for user_id in groupid_activitiesids: #Iterate
        activities_ids = [] # Create new list
        for activities_id in groupid_activitiesids[user_id]: #Iterare through activities_ids
            activities_ids.append(activities_id) # Append activities_id to list
        groupid_activitiesids[user_id]['activities_ids'] = activities_ids # Add list to dictionary
    print("With activities id:", groupid_activitiesids)

    started_at = {}

    #Started_at is the first_seen_at of the first activities of each user_id
    for user_id in groupid_activitiesids: #Iterate through user_id
        started_at[user_id] = groupid_activitiesids[user_id][groupid_activitiesids[user_id]['activities_ids'][0]]['first_seen_at'] #Get first_seen_at of first activities
    print(started_at)

    ended_at = {}

    #Ended_at is the answered_at of the last activities of each user_id
    for user_id in groupid_activitiesids:
        ended_at[user_id] = groupid_activitiesids[user_id][groupid_activitiesids[user_id]['activities_ids'][-1]]['answered_at']
    print(ended_at)

    #Dictionary with started at and ended at
    groupid_activitiesids_started_ended = {}
    for user_id in groupid_activitiesids:
        groupid_activitiesids_started_ended[user_id] = {}
        groupid_activitiesids_started_ended[user_id]['activities_ids'] = groupid_activitiesids[user_id]['activities_ids']
        groupid_activitiesids_started_ended[user_id]['started_at'] = started_at[user_id]
        groupid_activitiesids_started_ended[user_id]['ended_at'] = ended_at[user_id]
    print("With ended and started at:", groupid_activitiesids_started_ended)

    duration = {}

    #Duration is the difference between the first_seen_at and answered_at of each user_id
    for user_id in groupid_activitiesids_started_ended:
        duration[user_id] = groupid_activitiesids_started_ended[user_id]['ended_at'] - groupid_activitiesids_started_ended[user_id]['started_at']
    print(duration)

    requests.post(url2, headers=header, json=groupid_activitiesids_started_ended)












