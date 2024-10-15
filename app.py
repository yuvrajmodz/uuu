from flask import Flask, request, jsonify
import requests
import gzip
from io import BytesIO
import os  # Import the os module

app = Flask(__name__)

cache = {}

@app.route('/api', methods=['GET'])
def api():
    uid = request.args.get('uid')
    if uid:
        if uid in cache:
            return cache[uid]
        api_url = 'https://shop.garena.sg/api/auth/player_id_login'
        headers = {
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Origin': 'https://shop.garena.sg',
            'Referer': 'https://shop.garena.sg/app/100067/idlogin',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Accept': 'application/json',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'x-datadome-clientid': 'Jmho2Ii8HPbH7oYogHAaf7~jJkrnuoe2Vf7oUk3zBadjqUWaFOuWF6JcUJ9dm0QiVzX_17vUBG4uw9rn8tiFe7oy0Spb6Mf4wJF7DjToYhK3MeHVRgpmGGxRezIKvMP8',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36'
        }

        data = {
            'app_id': 100067,
            'login_id': uid,
            'app_server_id': 0
        }

        try:
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()

            if response.headers.get('Content-Encoding') == 'gzip':
                try:
                    buf = BytesIO(response.content)
                    with gzip.GzipFile(fileobj=buf) as f:
                        response_content = f.read().decode('utf-8')
                except gzip.BadGzipFile:
                    response_content = response.text  # Fallback to plain text
            else:
                response_content = response.text

            parsed_response = response.json()

            if 'nickname' in parsed_response:
                result = parsed_response['nickname']
            elif 'url' in parsed_response:
                result = 'captcha'
            else:
                result = 'invalid_uid'

            # Save result to cache
            cache[uid] = result

            return result
        except requests.RequestException as e:
            return f'Error: {str(e)}'
    else:
        return 'developed by: @YuvrajMODZ'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
