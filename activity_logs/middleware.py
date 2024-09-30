from django.utils.deprecation import MiddlewareMixin
from .models import ActivityLog  # Đảm bảo import đúng model ActivityLog
import user_agents

class UserAgentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent_string = request.META.get('HTTP_USER_AGENT', '')
        user_agent = user_agents.parse(user_agent_string)
        request.user_os = user_agent.os.family

        # Ghi lại hoạt động chỉ khi người dùng đã xác thực
        if request.user.is_authenticated:
            ActivityLog.objects.create(
                user=request.user,
                os=request.user_os,
                path=request.path,
                ip=request.META.get('REMOTE_ADDR', ''),
            )
