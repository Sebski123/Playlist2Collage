from VARS import *
import base64
import requests
import json
import os 

def getAuthToken():
    code_payload = {
        'grant_type': 'client_credentials'
    }

    auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(b64_auth_str)
    }

    post_request = requests.post("https://accounts.spotify.com/api/token", data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)

    print(response_data)
    return response_data["access_token"]

def getPlaylistAlbums(playlist):
    requestUrl = "https://api.spotify.com/v1/playlists/{}".format(playlist)

    params = {
        'fields': 'tracks.items(limit, next, total, track(album(name,images))), name',
        'offset': 100,
        'limit' : 100
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(AUTH_TOKEN)
    }
    
    get_request = requests.get(requestUrl, headers=headers, params=params)
    response_data = json.loads(get_request.text)

    with open("data123.json", "w") as file:
        json.dump(response_data, file)

    albums = {}
    for track in response_data["tracks"]["items"]:
        albums[track["track"]["album"]["name"]] = track["track"]["album"]["images"]

    print(len(albums.keys()))
    return albums, response_data["name"]

def downloadAlbums(albums, playlistName):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    os.makedirs("{}\\{}".format(dir_path, playlistName.replace(" ", "_")), exist_ok=True)

    print(dir_path)

    for album in albums.keys():

        url = albums[album][1]["url"]
        filename = '{}\\{}\\{}.png'.format(dir_path, playlistName.replace(" ", "_"), url.split('/')[-1])
        r = requests.get(url, allow_redirects=True)
        with open(filename, 'wb') as handler:
            handler.write(r.content)

def main():
    authToken = AUTH_TOKEN  #getAuthToken()
    print ("Token: " + authToken)
    albums, playlistName = getPlaylistAlbums(PLAYLIST_ID)
    downloadAlbums(albums, playlistName)


if __name__ == "__main__":
    try:
        #getAuthToken()
        main()
    except Exception as e :
        print("rip")
        print(e)