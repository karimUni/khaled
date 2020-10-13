# decorators for role Authentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime

# admin decoration to check user role is Admin
def admin_role(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.role != "admin":
            # raise Http404
            return Response({"EError": "not authorized"})
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func


# Editor decoration to check user role is Editor
def editor_role(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.role != "editor":
            # raise Http404
            return Response({"EError": "not authorized"})
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func



