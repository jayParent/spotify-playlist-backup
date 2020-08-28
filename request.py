import requests
import csv

client_id = ''
client_secret = ''
response_type = 'code'
scope = 'playlist-read-private'
redirect_uri = 'http://localhost:8888'


def getAuthorization():
    auth_url = 'https://accounts.spotify.com/authorize?client_id=' + client_id + \
        '&redirect_uri=' + redirect_uri + '&scope=' + \
        scope + '&response_type=' + response_type

    r = requests.get(auth_url)
    print(r)


def getAccessAndRefreshToken():
    grant_type = 'authorization_code'
    code = ''
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'client_id': client_id, 'client_secret': client_secret,
               'grant_type': grant_type, 'code': code, 'redirect_uri': redirect_uri}

    r = requests.post(token_url, data=headers)
    print(r.text)


def getNewAccessToken():
    refresh_token = ''

    refresh_url = 'https://accounts.spotify.com/api/token'
    headers = {'grant_type': 'refresh_token', 'refresh_token': refresh_token,
               'client_id': client_id, 'client_secret': client_secret}
    r = requests.post(refresh_url, data=headers)
    jsonResponse = r.json()
    return jsonResponse["access_token"]


def getPlaylists():
    url = 'https://api.spotify.com/v1/me/playlists'
    access_token = getNewAccessToken()
    authorization = {'Authorization': 'Bearer ' + access_token}
    trance_PlaylistId = '4NGcaASBaU1elQauvK65Z1'

    url = 'https://api.spotify.com/v1/playlists/' + \
        trance_PlaylistId + '/tracks?fields=items(track(name))'
    r = requests.get(url, headers=authorization)
    jsonResponse = r.json()

    return jsonResponse

def writeToCsv(trackList):
    with open('trance_playlist.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)

        for track in trackList['items']:
            writer.writerow([track['track']['name']])
            print(track['track']['name'])


trackList = getPlaylists()
writeToCsv(trackList)
