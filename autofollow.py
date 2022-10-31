# coding = utf-8
import requests
import numpy as np

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Authorization": "Bearer 1111111111",  # Bearer Token
}

wordList = [chr(i) for i in np.arange(97, 123)]
numList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
baseUrl = 'https://2222222222'  # 实例地址
botName = '3333333333'  # 机器人用户名


def getUserInfo(key):
    url = baseUrl + "/api/v2/search"
    params = {"q": key, "resolve": True, "limit": 80}
    response = requests.get(url=url, params=params, headers=headers).json()
    return response


def followingRequest(id):
    url = f"{baseUrl}/api/v1/accounts/{id}/follow"
    requests.post(url=url, headers=headers)


def getFollowingList(id):
    print("正在获取关注列表...")
    ls = [40, 80, 120, 160, 200, 240, 280]
    followingList = []
    for i in ls:
        url = f"{baseUrl}/api/v1/accounts/{id}/following"
        params = {"max_id": str(i)}
        response = requests.get(url=url, params=params, headers=headers).json()
        for j in response:
            if j["id"] not in followingList:
                followingList.append(j["id"])
    print(f"关注列表共有{len(followingList)}人")
    return followingList


def followingAll(ls, botId):
    followingList = getFollowingList(botId)
    for i in ls:
        userInfo = getUserInfo(i)
        for j in userInfo["accounts"]:
            if j["id"] not in followingList:
                followingRequest(j["id"])
                print("发送关注" + j["id"] + "请求成功")
        print("keyword:" + i + ",complete!")


def main():
    print("正在获取机器人id...")
    botId = getUserInfo(f"{botName}@{baseUrl[8:]}")["accounts"][0]["id"]
    print(f"机器人id:{botId}")
    followingAll(wordList, botId)
    followingAll(numList, botId)
    print("All Complete!")


if __name__ == '__main__':
    main()
