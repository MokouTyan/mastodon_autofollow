# coding = utf-8
import requests
import numpy as np
import telegram

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Authorization": "Bearer 1111111111",  # Bearer Token
}

wordList = [chr(i) for i in np.arange(97, 123)]
numList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
following_count = 0
baseUrl = 'https://2222222222'  # 实例地址
botName = '3333333333'  # 机器人用户名
openNotice = False  # 是否开启tg通知
tgbot_token = '4444444444'  # TG机器人Token
tg_id = '5555555555'  # chat_id(在@getmyid_bot中获取)


def getUserInfo(key):
    url = baseUrl + "/api/v2/search"
    params = {"q": key, "resolve": True, "limit": 80}
    response = requests.get(url=url, params=params, headers=headers).json()
    return response


def followingRequest(id):
    url = f"{baseUrl}/api/v1/accounts/{id}/follow"
    response = requests.post(url=url, headers=headers)
    return response.headers.get("X-RateLimit-Remaining")


def getFollowingList(id):
    print("正在获取关注列表...")
    ls = [i for i in range(1, following_count * 2, 39)]
    followingList = []
    for i in ls:
        url = f"{baseUrl}/api/v1/accounts/{id}/following"
        params = {"max_id": str(i + 40), "since_id": str(i - 1)}
        response = requests.get(url=url, params=params, headers=headers).json()
        for j in response:
            if j["id"] not in followingList:
                followingList.append(j["id"])
    print(f"关注列表共有{len(followingList)}人")
    return followingList


def followingAll(ls, botId):
    followingList = getFollowingList(botId)
    for k in ls:
        for i in k:
            userInfo = getUserInfo(i)
            for j in userInfo["accounts"]:
                if j["id"] not in followingList and not j["locked"]:
                    remaining = int(followingRequest(j["id"]))
                    print("发送关注" + j["id"] + "请求成功")
                    if remaining < 50:
                        print("请求次数已达上限,请5分钟后再试！")
                        return
            print("keyword:" + i + ",complete!")


def telegram_notice():
    bot = telegram.Bot(token=tgbot_token)
    bot.send_message(chat_id=tg_id, text='定时任务执行完成\n', parse_mode=telegram.ParseMode.HTML)


def main():
    global following_count
    print("正在获取机器人id...")
    botInfo = getUserInfo(f"{botName}@{baseUrl[8:]}")["accounts"][0]
    bot_id = botInfo["id"]
    following_count = botInfo["following_count"]
    print(f"机器人id:{bot_id}")
    followingAll([wordList, numList], bot_id)
    print("All Complete!")
    if openNotice:
        telegram_notice()


if __name__ == '__main__':
    main()
