from django.db import models
from customers.models import Customer
from employees.models import Employee
from rooms.models import Room


# Bảng đặt phòng
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Chờ xác nhận'
        CONFIRMED = 'confirmed', 'Đã xác nhận' #nhân viên chấp nhận và khoá phòng
        CHECKED_IN = 'checked_in', 'Đang ở' # cập nhật thông tin lưu trú và chuyển đến awaiting payment
        CHECKED_OUT = 'checked_out', 'Đã trả phòng' #nhận tiền và set thành công chuyển phòng về trạng thái act
        CANCELLED = 'cancelled', 'Đã hủy'
        NO_SHOW = 'no_show', 'Không đến'
        AWAITING_PAYMENT = 'awaiting_payment', 'Đang chờ thanh toán'
        SUCCESSFUL = 'successful', 'Đã thanh toán'
        REFUNDED = 'refunded', 'Đã hoàn tiền'
        AMENDED = 'amended', 'Đã sửa đổi'
        FAILED = 'failed', 'Thất bại'

    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    # Cho phép customer là tùy chọn để đặt phòng cho khách vãng lai
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    guest_firstname = models.CharField(max_length=255, blank=True, null=True)  # Tên khách vãng lai
    guest_lastname = models.CharField(max_length=255, blank=True, null=True)  # Tên khách vãng lai
    guest_email = models.EmailField(blank=True, null=True)  # Email khách vãng lai
    guest_phone = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại khách vãng lai
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    stay_price = models.FloatField(blank=True, null=True, default=0)
    surcharge_price = models.FloatField(blank=True, null=True, default=0)
    services_price = models.FloatField(blank=True, null=True, default=0)
    promotion_price = models.FloatField(blank=True, null=True, default=0)
    total_price = models.FloatField(blank=True, null=True, default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    payment_info = models.TextField(blank=True, null=True)  # Thông tin thanh toán
    cancellation_reason = models.TextField(blank=True, null=True)  # Lý do hủy
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Chi phí bổ sung
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Số tiền hoàn lại
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.customer:
            return f"Booking {self.id} for {self.customer}"
        return f"Guest Booking {self.id} for {self.guest_name}"

    def save(self, *args, **kwargs):
        if self.check_out_date <= self.check_in_date:
            raise ValueError("Ngày trả phòng phải sau ngày nhận phòng.")

        # Tính toán tổng giá trị
        self.total_price = (
                (self.stay_price or 0) +
                (self.surcharge_price or 0) +
                (self.services_price or 0) -
                (self.promotion_price or 0) +
                (self.additional_charges or 0)
        )

        super().save(*args, **kwargs)