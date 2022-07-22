import json
import requests
from secrets import spotify_user_id, discover_weekly_playlist_id
from datetime import date
from refresh import Refresh


class Save_songs:
    def __init__(self):
        self.user_id = spotify_user_id
        self.spotify_token = ""
        self.discover_weekly_playlist_id = discover_weekly_playlist_id
        self.tracks = ""
        self.new_playlist_id = ""

    def get_songs(self):
        # iterate over playlist and add tracks to a list

        print("getting songs from discover weekly...")
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            discover_weekly_playlist_id)

        response = requests.get(query, headers={
            "Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        for item in response_json["items"]:
            self.tracks += (item["track"]["uri"] + ",")
        # remove the last comma
        self.tracks = self.tracks[:-1]

        self.add_songs_to_playlist()

    def create_new_playlist(self):
        # create new playlist with discover weekly songs

        print("trying to create playlist...")

        today = date.today()
        date_formatted = today.strftime("%m/%d/%Y")

        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            spotify_user_id)

        request = json.dumps({
            "name": date_formatted + " discover weekly!!", "description": "no fear, the bot is here! (to save your discover weekly playlist from dissappearing)", "public": False
        })

        response = requests.post(query, data=request, headers={
            "Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

        response_json = response.json()

        return response_json["id"]

    def add_songs_to_playlist(self):
      # add all songs to new playlist

        print("addings songs to playlist...")

        self.new_playlist_id = self.create_new_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.new_playlist_id, self.tracks)

        response = requests.post(query, headers={
            "Content-Type": "application/json", "Authorization": "Bearer {}".format(self.spotify_token)})

    def call_refresh_token(self):

        print("refreshing token...")

        call_refresh = Refresh()
        self.spotify_token = call_refresh.refresh_auth_token()

        self.get_songs()


a = Save_songs()
a.call_refresh_token()
