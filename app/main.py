import requests
import sys


def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    params = {
        "apiKey": "fcec2a485b1a4a89898fd2021b88fbd8"
    }

    # res = requests.post(server_url, data=player_key, params=params)
    # if res.status_code != 200:
    #     print('Unexpected server response:')
    #     print('HTTP code:', res.status_code)
    #     print('Response body:', res.text)
    #     exit(2)
    # print('Server response:', res.text)

    aliens_api = server_url + '/aliens/send'
    data = "string"
    url = aliens_api
    print('URL:', url)
    res = requests.post(url, data=data, params=params)
    if res.status_code == 302:
        print('HTTP code:', res.status_code)
    elif res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
        print('Server response:', res.text)
    else:
        print('Server response:', res.text)


if __name__ == '__main__':
    main()
