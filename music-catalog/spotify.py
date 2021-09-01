from os import name
import requests

class Playlist:

    AUTH_URL = 'https://accounts.spotify.com/api/token'
    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    headers = {}
    
    snapshot_id = 0
    tracks = []


    def __init__(self, client_id, client_secret, playlist_id):
        try:
            # Spotify API authentication
            auth_response = requests.post(self.AUTH_URL,{
                'grant_type': 'client_credentials',
                'client_id' : client_id,
                'client_secret' : client_secret,
            })

            # convert the response to JSON
            auth_response_data = auth_response.json()

            # save the access token
            access_token = auth_response_data['access_token']

            self.headers = {
                'Authorization': 'Bearer {token}'.format(token=access_token)
            }

            # Retrieve the playlist content and keep only the interesting fields
            response = self.get_playlist_items(playlist_id)

            self.snapshot_id = response['snapshot_id']

            # Fill the list of Track objects
            for track in response['tracks']['items']:
                self.tracks.append(Track(track))

        except Exception:
            print("There was a problem trying to authenticate")

    
    def __get(self, URL):
        return requests.get(URL, headers=self.headers)


    def get_playlist_items(self, playlist_id):
        # URL endpoint for playlists: https://api.spotify.com/v1/playlists/{playlistId}/tracks
        URL = self.BASE_URL + 'playlists/' + playlist_id + '/tracks'
        return self.__get(URL).json()


class Track:

    def __init__(self, data):
        
        # id
        self.href = data['track']['href']
        self.name = data['track']['name']
        self.album = data['track']['album']['name']
        self.artist = data['track']['artists'][0]['name']
        self.duration_ms = data['track']['duration_ms']
        # popularity?
        self.track_number = data['track']['track_number']
