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
    requestUrl = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist)
    albums = {}

    params = {
        'fields': 'items(track(album(name,images))), limit, next, total',
        'offset': 0,
        'limit' : 100
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer {}'.format(AUTH_TOKEN)
    }
    
    playlistName = json.loads(requests.get(requestUrl.replace("/tracks", ""), headers=headers, params={'fields':'name'}).text)["name"]

    while True:
        get_request = requests.get(requestUrl, headers=headers, params=params)
        response_data = json.loads(get_request.text)

        with open("data123.json", "w") as file:
            json.dump(response_data, file)

        for track in response_data["items"]:
            albums[track["track"]["album"]["name"]] = track["track"]["album"]["images"]
        
        if response_data["next"] == None:
            break
        else:
            params["offset"] += 100


    print(len(albums.keys()), " album covers to download")
    return albums, playlistName

def downloadAlbums(albums, playlistName):

    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.isdir("{}\\{}".format(dir_path, playlistName.replace(" ", "_"))):
        os.makedirs("{}\\{}".format(dir_path, playlistName.replace(" ", "_")), exist_ok=True)
    else:
        print("Directory already exists, skipping download")
        return "{}\\{}".format(dir_path, playlistName.replace(" ", "_"))
    
    print("Downloading...")

    for album in albums.keys():

        url = albums[album][0]["url"]
        filename = '{}\\{}\\{}.png'.format(dir_path, playlistName.replace(" ", "_"), ''.join(e for e in album if e.isalnum()))
        r = requests.get(url, allow_redirects=True)
        with open(filename, 'wb') as handler:
            handler.write(r.content)
    
    return "{}\\{}".format(dir_path, playlistName.replace(" ", "_"))

def squareImages(path):
    images = [os.path.join(path, fn) for fn in os.listdir(path)]
    
    print("Resizing images...")

    for image in images:
        oldImg = Image.open(image)
        if oldImg.size != (640, 640):
            newImg = Image.new("RGB", (640, 640))
            newImg.paste(oldImg, ((640-oldImg.size[0])//2,(640-oldImg.size[1])//2))
            newImg.save(image)

def main():
    authToken = AUTH_TOKEN  #getAuthToken()
    print ("Token: " + authToken)
    albums, playlistName = getPlaylistAlbums(PLAYLIST_ID)
    path = downloadAlbums(albums, playlistName)
    squareImages(path)


if __name__ == "__main__":
    try:
        #getAuthToken()
        main()
    except Exception as e :
        print("rip")
        print(e)