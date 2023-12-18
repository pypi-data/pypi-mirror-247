import requests

url = "http://192.168.3.146:48080/admin-api/content/device-screenshoot-api/upload/file"  # 服务器地址
headers = {"Authorization": "Bearer 966cdc03431f410887dd44ba1c9b5435"}
file_path = "D:/image/cxk.jpg"  # 待上传的文件路径
with open(file_path, "rb") as file:
    files = {"file": file}
    response = requests.post(url, headers=headers, files=files)
    print(response.text)