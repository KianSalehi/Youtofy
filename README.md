# Youtofy

Converts Youtube playlist/songs to a spotify playlist

## Installation

Use the package manager pip to install google-api-python-client, google-auth-oauthlib, youtube_dl, and requests. Youtube Data API v3, Spotify Web API were used in production of this script.

User id and OAuth Token from Spotify developer are needed in the "API_Info!
client_secret.json holds the client secret information from google cloud which can be downloaded in the credential section of Youtube API.

Run the file 'makePlaylist.py'

Please note Spotify Oauth token expires and it needs to be renewed.
```bash
pip install requests
```

## Usage

```python
 import requests
 request.get({}) # returns info about a search (API)
 request.post({}) # makes a playlist and returns the link to the playlist
 ```
```python
youtube_url = "https://www.youtube.com/watch?v={}".format("id") # searches 'id' on youtube to download the directed content

youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)   # downloads information with youtube_dl
```

Project inspired by https://www.youtube.com/watch?v=7J_qcttfnJA
