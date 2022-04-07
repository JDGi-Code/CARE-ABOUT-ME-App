class AuthService:

    def user_is_logged_in(self, request):
        return request.user.is_authenticated
