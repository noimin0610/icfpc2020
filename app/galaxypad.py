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


def send(a, b):
    print(a, b)


def makeJoinRequest(player_key: str) -> str:
    req = Modulate([[JOIN, int(player_key), []]])
    return [str(c) for c in req()]


def makeStartRequest(player_key, gameResponse):
    # https://message-from-space.readthedocs.io/en/latest/game.html#start
    xs = [1, 2, 3, 4]  # initial ship parameters
    assert xs[3] != 0

    req = Modulate([[START, int(player_key), xs]])
    return [str(c) for c in req()]


def makeCommandsRequest(player_key, gameResponse):
    # https://message-from-space.readthedocs.io/en/latest/game.html#commands
    commands = []
    req = Modulate([[COMMANDS, int(player_key), commands]])
    return [str(c) for c in req()]


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


if __name__ == '__main__':
    main()
