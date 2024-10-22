from rest_framework.views import APIView
from datetime import datetime
import random
import string
from rest_framework import viewsets, status
from rest_framework.response import Response
from twilio.rest import Client
from django.conf import settings
from .models import Booking, Room
from .serializers import BookingSerializer
from users.models import OTP


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def generate_otp(self, length=6):
        """Tạo mã OTP ngẫu nhiên có độ dài được chỉ định."""
        return ''.join(random.choices(string.digits, k=length))

    def send_sms(self, to_phone_number, message):
        """Gửi tin nhắn SMS chứa mã OTP."""
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=to_phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message
        )

    def create(self, request, *args, **kwargs):
        """Tạo mã OTP và gửi SMS đến số điện thoại đã cung cấp."""
        phone_number = request.data.get('phone_number')
        otp = self.generate_otp()

        # Lưu OTP vào cơ sở dữ liệu
        OTP.objects.create(phone_number=phone_number, otp=otp)

        # Gửi OTP qua SMS
        message = f'Your OTP code is: {otp}'
        self.send_sms(phone_number, message)

        # Trả về thông báo yêu cầu người dùng nhập OTP
        return Response({"message": "OTP sent to your phone number. Please enter the OTP to proceed."},
                        status=status.HTTP_200_OK)

    def complete_booking(self, request):
        """Xác thực mã OTP và hoàn tất đặt phòng."""
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        # Xác thực OTP
        if not self.verify_otp(phone_number, otp):
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # Chuyển đổi định dạng ngày tháng từ 'dd-mm-yyyy' sang 'YYYY-MM-DD'
        if 'check_in_date' in request.data:
            request.data['check_in_date'] = datetime.strptime(request.data['check_in_date'], '%d-%m-%Y').strftime(
                '%Y-%m-%dT00:00:00')
        if 'check_out_date' in request.data:
            request.data['check_out_date'] = datetime.strptime(request.data['check_out_date'], '%d-%m-%Y').strftime(
                '%Y-%m-%dT00:00:00')

        # Lưu thông tin đặt phòng
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()

        # Cập nhật trạng thái phòng
        room_code = serializer.validated_data['room'].name
        room = Room.objects.get(name=room_code)
        room.is_available = False
        room.save()

        # Xóa bản ghi OTP sau khi xác thực thành công (tuỳ chọn)
        OTP.objects.filter(phone_number=phone_number).delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def verify_otp(self, phone_number, otp):
        """Xác thực mã OTP."""
        try:
            otp_record = OTP.objects.get(phone_number=phone_number, otp=otp)
            if (timezone.now() - otp_record.created_at).total_seconds() > 300:  # OTP hợp lệ trong 5 phút
                return False
            return True
        except OTP.DoesNotExist:
            return False

    def update(self, request, *args, **kwargs):
        """Cập nhật thông tin đặt phòng, bao gồm cả cập nhật trạng thái và thông tin hủy."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Chuyển đổi ngày tháng từ định dạng dd-mm-yyyy sang định dạng mà Django có thể xử lý
        check_in_date_str = request.data.get('check_in_date')
        check_out_date_str = request.data.get('check_out_date')

        if check_in_date_str:
            request.data['check_in_date'] = datetime.strptime(check_in_date_str, "%d-%m-%Y")
        if check_out_date_str:
            request.data['check_out_date'] = datetime.strptime(check_out_date_str, "%d-%m-%Y")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Hủy đặt phòng, có thể chỉ định lý do hủy nếu cần."""
        instance = self.get_object()
        instance.status = Booking.Status.CANCELLED
        if 'cancellation_reason' in request.data:
            instance.cancellation_reason = request.data['cancellation_reason']
        instance.save()

        return Response({"detail": "Đặt phòng đã được hủy."}, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')

        booking_viewset = BookingViewSet()
        response = booking_viewset.complete_booking(request, otp)

        return response


from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone


class DailyRevenueView(APIView):
    def get(self, request):
        # Lấy ngày hiện tại theo múi giờ địa phương
        today = timezone.localtime(timezone.now()).date()

        # Lọc theo ngày hiện tại với trạng thái 'successful'
        daily_revenue = Booking.objects.filter(
            created_at__date=today,
            status='successful'
        ).aggregate(total_revenue=Sum('total_price'))

        return Response(daily_revenue)

class MonthlyRevenueView(APIView):
    def get(self, request):
        today = timezone.now().date()
        # Lọc theo tháng, năm hiện tại và status='successful'
        monthly_revenue = Booking.objects.filter(
            created_at__month=today.month,
            created_at__year=today.year,
            status='successful'
        ).aggregate(total_revenue=Sum('total_price'))

        return Response(monthly_revenue)


class AnnualRevenueView(APIView):
    def get(self, request):
        today = timezone.now().date()
        # Lọc theo năm hiện tại và status='successful'
        annual_revenue = Booking.objects.filter(
            created_at__year=today.year,
            status='successful'
        ).aggregate(total_revenue=Sum('total_price'))

        return Response(annual_revenue)


class RevenueSummaryView(APIView):
    def get(self, request):
        # Lọc tất cả các booking có status='successful'
        total_revenue = Booking.objects.filter(
            status='successful'
        ).aggregate(total_revenue=Sum('total_price'))

        return Response(total_revenue)
