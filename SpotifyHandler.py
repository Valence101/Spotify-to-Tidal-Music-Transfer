import base64
import json
import requests

# Spotify Handler


def login(client_id, client_secret):
    #API Authentication 
    auth_header = f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    header={"Authorization": auth_header}
    token_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(
        token_url,
        headers=header,
        data={"grant_type": "client_credentials"}
    )
    access_token = auth_response.json()["access_token"]

    print("Completed Authenticating, access_token: ", access_token)


    access_token = {
    "Authorization": f"Bearer {access_token}"
    }

    return access_token



def request_all_playlist(access_token, user_id):
    #Gets All of the playlist of a given user
    """
    Attempt at building auto user id functionality, not sure how to make an API request for a single user.

    user_url = "https://api.spotify.com/v1/me"
    user_json = requests.get(user_url, headers=access_token)

    user_json = user_json.json()
    user_id = user_json["id"]
    """

    playlists_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    playlists = {}

    limit = 20 # Max is 50 per spotify
    offset = 0  # Start at the beginning

    while True:
        params = {
            'limit': limit,
            'offset': offset
        }
        response = requests.get(playlists_url, headers=access_token, params=params)
        response_json = response.json()

        # Extract playlists from the current page
        for item in response_json["items"]:
            playlists[item["name"]] = item["id"]

        # Check if there are more playlists to fetch
        if len(response_json["items"]) < limit:
            break

        # Update the offset for the next batch
        offset += limit

    return playlists






def request_tracks(access_token, playlist_id, offset = 0 ):
    #Returns up to 100 tracks from a given playlist in the form of a json.
    params = {
    "limit": 100,
    "offset": offset   # Index of the first track to return
    }
 
    tracks_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    tracks_response = requests.get(tracks_url, params=params ,headers=access_token)
    tracks = tracks_response.json()

  
    return tracks




