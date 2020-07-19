import requests
import sys


def makeJoinRequest(player_key: str) -> str:
    return ''


def makeStartRequest(player_key, gameResponse):
    return ''


def makeCommandsRequest(player_key, gameResponse):
    return ''


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
