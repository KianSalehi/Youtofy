import json
from API_Info import user_id, oToken
import requests
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl


class MakePlaylist:
    def __init__(self):
        self.spotify_user_id = user_id
        self.spotify_token = oToken
        self.youtube_user = self.get_youtube_user()
        self.all_songs = {}

    # Function to log into Youtube
    def get_youtube_user(self):
        # Code copied from youtube's api service
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        # from the Youtube DATA API
        youtube_user = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        return youtube_user

    # Function to get videos and store the info of songs in a dictionary
    def get_video(self):
        request = self.youtube_user.videos().list(
            part="snippet,contentDetails,statistics",
            alt="json",
            myRating="like"
        )
        response = request.execute()

        # getting videos and important info
        for item in response["items"]:
            videoTitle = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # getting name of the artist and song with youtube_dl
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]

            # storing the info
            self.all_songs[videoTitle] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,

                # spotify search song
                "spotify_search": self.search_song(song_name, artist)

            }

    # Function to create a new playlist
    def create_playlist(self):
        request_body = json.dumps({
            "name": "New Playlist",
            "description": "New playlist description",
            "public": False}
        )
        endpoint = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_user_id)
        response = requests.post(
            endpoint,
            data=request_body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        )
        res_json = response.json()

        # playlist id
        return res_json["id"]

    # Function to search for a song on spotify
    def search_song(self, song_name, artist):
        endpoint = "https://api.spotify.com/v1/search?q={} {}&type=track%2Cartist&limit=20".format(
            song_name,
            artist
        )
        response = requests.get(
            endpoint,
            headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)

                    }
        )
        res_json = response.json()
        song = res_json["tracks"]["items"]
        songuri = song[0]["uri"]
        return songuri

    # Function to add the song to the playlist
    def add_song(self):
        # adding songs to the dictionary
        self.get_video()
        # getting all the song searches
        uri = []
        for song, info in self.all_songs.items():
            uri.append(info["spotify_search"])

        # create a new playlist
        playlist_id = self.create_playlist()

        # add all songs into new playlist created

        request_data = json.dumps(uri)
        endpoint = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            endpoint,
            data=request_data,
            headers={"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)}

        )
        response_json = response.json()
        return response_json


if __name__ == '__main__':
    MakePlaylist().add_song()
