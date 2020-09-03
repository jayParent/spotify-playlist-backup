import requests
import csv

client_id = ''
client_secret = ''
response_type = 'code'
scope = 'playlist-read-private'
redirect_uri = 'http://localhost:8888'


class Playlist:
    def __init__(self, name, id, trackList):
        self.name = name
        self.id = id
        self.trackList = trackList


def main():
    playlistsNamesAndIds = getPlaylists()
    playlists = getTracksFromPlaylists(playlistsNamesAndIds)
    # writeToCsv(playlists)


def getAuthorization():
    auth_url = 'https://accounts.spotify.com/authorize?client_id=' + client_id + \
        '&redirect_uri=' + redirect_uri + '&scope=' + \
        scope + '&response_type=' + response_type

    r = requests.get(auth_url)
    print(r)


def getAccessAndRefreshToken():
    grant_type = 'authorization_code'
    code = 'AQCLAnVXfOi--DMI_W48dCE9QplGDIJo1FqDFgx3TVoBlsRyWg0VkFZoZXTkpV-U2rbh-2pi-Gh7EpCpNqO1UxIhhXCqz0OVYGpwIRrlTI-XTX3k72GvRVkz92kh22C0akhfzumJ5571mkjUV3KU-Ur_-VJS8wc0uPIunSXcEToFVjGjZA78MALEV2_FrnWK'
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

    r = requests.get(url, headers=authorization)

    playlists = r.json()
    playlistsNamesAndIds = []

    for playlist in playlists['items']:
        pl = Playlist(playlist['name'], playlist['id'], '')
        playlistsNamesAndIds.append(pl)

    return playlistsNamesAndIds


def getTracksFromPlaylists(playlistsNamesAndIds):
    playlists = []
    access_token = getNewAccessToken()
    authorization = {'Authorization': 'Bearer ' + access_token}

    for playlist in playlistsNamesAndIds:
        url = 'https://api.spotify.com/v1/playlists/' + \
            playlist.id + '/tracks?fields=items(track(name))'
        r = requests.get(url, headers=authorization)
        trackList = r.json()
        print(type(trackList))

        pl = Playlist(playlist.name, playlist.id, trackList)
        playlists.append(pl)

    return playlists


def writeToCsv(playlists):
    for playlist in playlists:
        fileName = playlist.name + '.csv'
        trackList = playlist.trackList
        print(playlist.name, playlist.id)

        with open(fileName, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            for track in trackList['items']:
                writer.writerow([track['track']['name']])


if __name__ == "__main__":
    main()
