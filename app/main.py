import requests
import sys


def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    # res = requests.post(server_url, data=player_key)
    # if res.status_code != 200:
    #     print('Unexpected server response:')
    #     print('HTTP code:', res.status_code)
    #     print('Response body:', res.text)
    #     exit(2)
    # print('Server response:', res.text)

    aliens_api = server_url + '/aliens/send/'
    params = {
        "apiKey": player_key
    }
    data = "string"
    url = aliens_api
    print('URL:', url)
    res = requests.post(url, data=data)
    if res.status_code == 302:
        print('HTTP code:', res.status_code)
    elif res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
        print('Server response:', res.text)


if __name__ == '__main__':
    main()
