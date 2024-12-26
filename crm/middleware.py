from django.shortcuts import redirect

class PreventBackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Redirect logged-out users trying to access cached pages
        if not request.user.is_authenticated and request.path != '/final/':
            return redirect('final')
        return self.get_response(request)
