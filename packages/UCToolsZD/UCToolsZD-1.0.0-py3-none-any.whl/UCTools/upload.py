import requests

url = "http://192.168.3.146:48080/admin-api/content/device-screenshoot-api/upload/file"  # 服务器地址
headers = {"Authorization": "Bearer fe7765196d774071853a480a713d4b3b"}
# 元组列表形式
files = [('files', open("D:/image/cxk.jpg", 'rb')), ('files', open("D:/image/zh.webp", 'rb'))]
print(files)
response = requests.post(url, headers=headers, files=files)
print(response.text)



