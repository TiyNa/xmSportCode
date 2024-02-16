import re

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def xmSport():
    url = f"https://api-user.huami.com/registrations/+86{request.form.get('phoneNumber')}/tokens"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "MiFit/4.6.0 (iPhone; iOS 14.0.1; Scale/2.00)"
    }
    data = {
        "client_id": "HuaMi",
        "password": request.form.get('password'),
        "redirect_uri": "https://s3-us-west-2.amazonaws.com/hm-registration/successsignin.html",
        "token": "access"
    }
    response = requests.post(url, headers=headers, data=data, allow_redirects=False)
    body = {"status": False}

    try:
        print(response.headers)
        location = response.headers["Location"]
        match = re.search("(?<=access=).*?(?=&)", location)
        if match:
            body['status'] = True
            body['code'] = match.group()
        else:
            body['code'] = "请检查手机号码和登录密码"
    except IndexError:
            body['code'] = "请求失败，请稍后重试"

    return jsonify(body)


if __name__ == '__main__':
    app.run(port=3000)
