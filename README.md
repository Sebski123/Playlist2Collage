# Playlist2Collage
Converts album covers from Spotify playlist to a Google Chrome "new tab" background


## Setup
1. Go to https://developer.spotify.com/dashboard and create a new app
1. Replace values CLIENT_ID and CLIENT_SECRET in VARS.py with values from app
1. Uncomment line 209 and comment line 110 in main.py. It should look like [this](https://i.imgur.com/DnO9zsZ.png)
1. Run main.py eg. `python main.py` it should look like [this](https://i.imgur.com/L7gfJZ3.png)
1. Copy 'access_token' from step 4 and add it to AUTH_TOKEN in VARS.py
1. Reverse what you did in step 3, it should now look like [this](https://i.imgur.com/rkkjD7o.png)
1. Add Spotify playlist ID to PLAYLIST_ID in VARS.py. Get playlist ID by right-clicking it in spotify and going Share>Copy Spotify URI and the pasting the part after "spotify:playlist:"
1. VARS.py should now look like [this](https://i.imgur.com/0kBXzRo.png)
1. Change the value of "ChromeLocation" in main.py to the location of background.jpg
1. Run main.py eg. `python main.py`
1. Output should look like [this](https://i.imgur.com/P2CSgcN.png)


## Troubleshooting
If you get an error like this: 

![error](https://i.imgur.com/uvElPWC.png)

Repeat step 3-6 from Setup and try again
