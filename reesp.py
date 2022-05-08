import datetime

import vk_api
LOGIN, PASSWORD = '89298661993', '1598753246Лдфцф'

def unixtime_to_time(unix):
    value = datetime.datetime.fromtimestamp(unix)
    return value.strftime('date: %Y-%m-%d, time: %H:%M:%S')


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    response = vk.wall.get(count=5, offset=1)
    if response['items']:
        for item in response['items']:
            print(f'{item["text"]};\n{unixtime_to_time(item["date"])}')


if __name__ == '__main__':
    main()
