from VARS import * #Create file VARS.py and add variables: CLIENT_ID, CLIENT_SECRET, AUTH_TOKEN and PLAYLIST_ID
import base64
import requests
import json
import os 
from PIL import Image

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

def make_collage(images, filename, width, init_height):
    if not images:
        print('No images for collage found!')
        return False

    margin_size = 2
    # run until a suitable arrangement of images is found
    while True:
        # copy images to images_list
        images_list = images[:]
        coefs_lines = []
        images_line = []
        x = 0
        while images_list:
            # get first image and resize to `init_height`
            img_path = images_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, init_height))
            # when `x` will go beyond the `width`, start the next line
            if x > width:
                coefs_lines.append((float(x) / width, images_line))
                images_line = []
                x = 0
            x += img.size[0] + margin_size
            images_line.append(img_path)
        # finally add the last line with images
        coefs_lines.append((float(x) / width, images_line))

        # compact the lines, by reducing the `init_height`, if any with one or less images
        if len(coefs_lines) <= 1:
            break
        if any(map(lambda c: len(c[1]) <= 1, coefs_lines)):
            # reduce `init_height`
            init_height -= 10
        else:
            break

    # get output height
    out_height = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            out_height += int(init_height / coef) + margin_size
    if not out_height:
        print('Height of collage could not be 0!')
        return False

    collage_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
    # put images to the collage
    y = 0
    for coef, imgs_line in coefs_lines:
        if imgs_line:
            x = 0
            for img_path in imgs_line:
                img = Image.open(img_path)
                # if need to enlarge an image - use `resize`, otherwise use `thumbnail`, it's faster
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                if collage_image:
                    collage_image.paste(img, (int(x), int(y)))
                x += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size
    collage_image.save(filename)
    return True

def create_collage(path, aspectRatio):
    finalNumImages = aspectRatio[1][0]*aspectRatio[1][1]

    # get images
    files = [os.path.join(path, fn) for fn in os.listdir(path)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() == '.png']
    if not images:
        print('No images for making collage! Please select other directory with images!')
        exit(1)

    # shuffle images
    random.shuffle(images)

    # Pad list until it has enough images
    while len(images) < finalNumImages:
        images.insert(random.randrange(len(images) + 1), random.choice(images))
    
    print('Making collage...')
    res = make_collage(images[:finalNumImages], "collage.jpg", aspectRatio[0], aspectRatio[0]/aspectRatio[1][0])
    if not res:
        print('Failed to create collage!')
        exit(1)
    print('Collage is ready!')

def main():
    aspectRatio = (1920, (16, 9)) # (width, (w, h)) 
    #Final collage will be 'width' wide and have w*h images

    authToken = AUTH_TOKEN  #getAuthToken()
    print ("Token: " + authToken)
    albums, playlistName = getPlaylistAlbums(PLAYLIST_ID)
    path = downloadAlbums(albums, playlistName)
    squareImages(path)
    create_collage(path, aspectRatio)


if __name__ == "__main__":
    try:
        #getAuthToken()
        main()
    except Exception as e :
        print("rip")
        print(e)