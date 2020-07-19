import requests
import sys
from interpreter import *

CREATE = 1
JOIN = 2
START = 3
COMMANDS = 4

# commands
ACCELERATE = 0
DETONATE = 1
SHOOT = 2

API_POINT = '/aliens/send'


def send(base_url, data) -> list:
    url = base_url + API_POINT
    print(url, data)

    res = requests.post(url, data=data)
    if res.status_code == 302:
        print('HTTP code:', res.status_code)
    elif res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
    else:
        print('Server response:', res.text)

    dem = Demodulate([[int(c) for c in res.text]])
    res: list = dem()
    print(res)
    return res


def makeJoinRequest(player_key: str) -> str:
    print('makeJoinRequest')
    req = Modulate([[JOIN, int(player_key), []]])
    return ''.join([str(c) for c in req()])


def makeStartRequest(player_key, gameResponse):
    print('makeStartRequest')
    # https://message-from-space.readthedocs.io/en/latest/game.html#start
    xs = [1, 2, 3, 4]  # initial ship parameters
    assert xs[3] != 0

    req = Modulate([[START, int(player_key), xs]])
    return ''.join([str(c) for c in req()])


def makeCommandsRequest(player_key, gameResponse):
    print('makeCommandsRequest')
    # https://message-from-space.readthedocs.io/en/latest/game.html#commands
    commands = []
    req = Modulate([[COMMANDS, int(player_key), commands]])
    return ''.join([str(c) for c in req()])


def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    # make valid JOIN request using the provided player_key
    joinRequest = makeJoinRequest(player_key)

    # send it to aliens and get the GameResponse
    gameResponse = send(server_url, joinRequest)

    # make valid START request using the provided player_key and gameResponse returned from JOIN
    startRequest = makeStartRequest(player_key, gameResponse)

    # send it to aliens and get the updated GameResponse
    gameResponse = send(server_url, startRequest)

    # todo: you MAY detect somehow that game is finished using gameResponse
    while True:
        # make valid COMMANDS request using the provided player_key and gameResponse returned from START or previous COMMANDS
        commandsRequest = makeCommandsRequest(player_key, gameResponse)

        # send it to aliens and get the updated GameResponse
        gameResponse = send(server_url, commandsRequest)
        if gameResponse == [0]:
            exit()


if __name__ == '__main__':
    main()
