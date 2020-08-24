import requests

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
    code = 'AQCLAnVXfOi--DMI_W48dCE9QplGDIJo1FqDFgx3TVoBlsRyWg0VkFZoZXTkpV-U2rbh-2pi-Gh7EpCpNqO1UxIhhXCqz0OVYGpwIRrlTI-XTX3k72GvRVkz92kh22C0akhfzumJ5571mkjUV3KU-Ur_-VJS8wc0uPIunSXcEToFVjGjZA78MALEV2_FrnWK'
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {'client_id': client_id, 'client_secret': client_secret,
               'grant_type': grant_type, 'code': code, 'redirect_uri': redirect_uri}

    r = requests.post(token_url, data=headers)
    print(r.text)


def getNewAccessToken():
    refresh_token = 'AQAUHKJsR94MppfljIzISyR09VqH8E1WrRsrSJVXPmEIuz0ue-btIGqjadHAPGoYAKVj76krF62JyQTkcqeEbeeSuAoG4ZWRx6uvfJklx-t2r6cCKrjpHv-I3rXhkotXqu8'

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

    # r = requests.get(url, headers=authorization)
    # jsonResponse = r.json()
    # print(jsonResponse)

    url = 'https://api.spotify.com/v1/playlists/4NGcaASBaU1elQauvK65Z1/tracks'
    r = requests.get(url, headers=authorization)
    print(r.text)


# getNewAccessToken()
getPlaylists()
