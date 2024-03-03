from django.shortcuts import redirect

def doctor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type!='doctor':
            return redirect('home') 
        return view_func(request, *args, **kwargs)
    return _wrapped_view