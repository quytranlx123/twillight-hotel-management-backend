import random
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import hmac
import hashlib
import json
import requests
from django.http import JsonResponse
from django.views import View


class ZaloPayCreateOrderView(APIView):
    config = {
        "app_id": 2553,
        "key1": "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL",
        "key2": "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz",
        "endpoint": "https://sb-openapi.zalopay.vn/v2/create"
    }

    def post(self, request):
        transID = random.randrange(1000000)
        callback_url = "https://2b76-42-117-225-244.ngrok-free.app/api/payments/callback/"
        order = {
            "app_id": self.config["app_id"],
            "app_trans_id": "{:%y%m%d}_{}".format(timezone.now(), transID),
            "app_user": request.user.username,
            "app_time": int(round(timezone.now().timestamp() * 1000)),
            "embed_data": json.dumps({"callback_url": callback_url}),
            "item": json.dumps([{}]),
            "amount": 50000,
            "description": "Lazada - Payment for the order #" + str(transID),
            "bank_code": "",
            "callback_url": callback_url,
        }

        # app_id|app_trans_id|app_user|amount|apptime|embed_data|item
        data = "{}|{}|{}|{}|{}|{}|{}".format(
            order["app_id"],
            order["app_trans_id"],
            order["app_user"],
            order["amount"],
            order["app_time"],
            order["embed_data"],
            order["item"]
        )

        order["mac"] = hmac.new(self.config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

        # Gửi yêu cầu đến ZaloPay với requests
        try:
            response = requests.post(self.config["endpoint"], data=order, verify=False)
            result = response.json()
            print(order["app_trans_id"])
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse(result)


class ZaloPayCallbackView(APIView):
    config = {
        'key2': 'kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz'
    }

    def post(self, request):
        result = {}
        try:
            cbdata = request.data
            # Tạo mã MAC để kiểm tra tính hợp lệ của callback
            mac = hmac.new(self.config['key2'].encode(), cbdata['data'].encode(), hashlib.sha256).hexdigest()

            # Kiểm tra callback hợp lệ (đến từ ZaloPay server)
            if mac != cbdata['mac']:
                # Callback không hợp lệ
                result['return_code'] = -1
                result['return_message'] = 'mac not equal'
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                result['return_code'] = 1
                result['return_message'] = 'success'
                result['data'] = {
                    'message': 'Đặt phòng thành công!'
                }
                print(mac, cbdata['mac'])
        except KeyError as e:
            result['return_code'] = 0
            result['return_message'] = f'Missing key: {str(e)}'
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result['return_code'] = 0  # ZaloPay server sẽ callback lại (tối đa 3 lần)
            result['return_message'] = str(e)
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Thông báo kết quả cho ZaloPay server
        return Response(result, status=status.HTTP_200_OK)


class ZaloPayQueryTransactionView(View):
    def get(self, request, app_trans_id):
        config = {
            "app_id": 2553,
            "key1": "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL",
            "endpoint": "https://sb-openapi.zalopay.vn/v2/query"
        }

        # Tạo tham số cho truy vấn
        params = {
            "app_id": config["app_id"],
            "app_trans_id": app_trans_id  # Sử dụng app_trans_id đã truyền vào
        }

        # Tạo mã MAC để kiểm tra tính hợp lệ
        data = "{}|{}|{}".format(config["app_id"], params["app_trans_id"], config["key1"])
        params["mac"] = hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()

        # Gửi yêu cầu POST đến API của ZaloPay
        response = requests.post(config["endpoint"], data=params)

        # Xử lý phản hồi từ ZaloPay
        if response.status_code == 200:
            result = response.json()
        else:
            result = {"error": "Không thể kết nối đến ZaloPay"}

        return JsonResponse(result)
