from rest_framework import viewsets, status
from .models import Room
from .serializers import BookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
from django.db.models import Q


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        # Chuyển đổi định dạng ngày tháng từ 'dd-mm-yyyy' sang 'YYYY-MM-DD'
        if 'check_in_date' in request.data:
            request.data['check_in_date'] = datetime.strptime(request.data['check_in_date'], '%d-%m-%Y').strftime(
                '%Y-%m-%dT00:00:00')
        if 'check_out_date' in request.data:
            request.data['check_out_date'] = datetime.strptime(request.data['check_out_date'], '%d-%m-%Y').strftime(
                '%Y-%m-%dT00:00:00')

        serializer = BookingSerializer(data=request.data)  # Sử dụng BookingSerializer
        serializer.is_valid(raise_exception=True)

        # Lưu thông tin đặt phòng
        booking = serializer.save()  # Lưu và trả về instance đặt phòng

        # Cập nhật trạng thái phòng
        room_code = serializer.validated_data['room'].name  # Lấy mã phòng từ validated_data
        room = Room.objects.get(name=room_code)  # Tìm phòng dựa trên mã phòng
        room.is_available = False  # Đánh dấu phòng là không còn khả dụng
        room.save()  # Lưu thay đổi

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Cập nhật thông tin đặt phòng, bao gồm cả cập nhật trạng thái và thông tin hủy.
        """
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
        """
        Hủy đặt phòng, có thể chỉ định lý do hủy nếu cần.
        """
        instance = self.get_object()
        instance.status = Booking.Status.CANCELLED
        if 'cancellation_reason' in request.data:
            instance.cancellation_reason = request.data['cancellation_reason']
        instance.save()

        return Response({"detail": "Đặt phòng đã được hủy."}, status=status.HTTP_200_OK)


class DailyRevenueView(APIView):
    def get(self, request):
        today = timezone.now().date()
        status = "successful"
        daily_revenue = Booking.objects.filter(
            Q(check_in_date=today) & Q(status=status)
        ).aggregate(total_revenue=Sum('total_price'))
        return Response(daily_revenue)


class MonthlyRevenueView(APIView):
    def get(self, request):
        today = timezone.now().date()
        # Lọc theo tháng, năm hiện tại và status='successful'
        monthly_revenue = Booking.objects.filter(
            check_in_date__month=today.month,
            check_in_date__year=today.year,
            status='successful'  # Thêm điều kiện lọc
        ).aggregate(total_revenue=Sum('total_price'))  # Sửa tên trường thành 'total_price'
        return Response(monthly_revenue)


class AnnualRevenueView(APIView):
    def get(self, request):
        today = timezone.now().date()
        # Lọc theo năm hiện tại và status='successful'
        annual_revenue = Booking.objects.filter(
            check_in_date__year=today.year,
            status='successful'  # Thêm điều kiện lọc
        ).aggregate(total_revenue=Sum('total_price'))  # Sửa tên trường thành 'total_price'
        return Response(annual_revenue)


# class RevenueSummaryView(APIView):
#     def get(self, request):
#         # Lọc tất cả các booking có status='successful'
#         total_revenue = Booking.objects.filter(
#             status='successful'  # Thêm điều kiện lọc
#         ).aggregate(total_revenue=Sum('total_price'))  # Sửa tên trường thành 'total_price'
#         return Response(total_revenue)


class RevenueSummaryView(APIView):
    def get(self, request):
        # Lọc tất cả các booking có status='successful'
        total_revenue = Booking.objects.filter(
            status='awaiting_payment'  # Thêm điều kiện lọc
        ).aggregate(total_revenue=Sum('stay_price'))  # Sửa tên trường thành 'total_price'
        return Response(total_revenue)
