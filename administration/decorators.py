from django.http import HttpResponse
from django.shortcuts import redirect, render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('staff_index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_roles=[], allowed_position=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            user_type = None
            staff_type = None
            

            if request.user.type == "LIBRARY_STAFF":
                user_type = "LIBRARY_STAFF"

                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)

                if request.user.librarystaffmoreinfo.position == "STAFF":
                    # print("pasok sa staff")
                    staff_type = "STAFF"
            else:
                return HttpResponse("you are not authorize in this page!1")

            
            if user_type in allowed_roles:
                # print(staff_type,"staff type toh")
                if staff_type is not None:
                    if staff_type in allowed_position:
                        return view_func(request, *args, **kwargs)
                    # if staff_type == "STAFF":
                    #     return view_func(request, *args, **kwargs)
                    else:
                        return HttpResponse("you are not authorize in this page!3")
                else:
                    return view_func(request, *args, **kwargs)
                # return view_func(request,*args, **kwargs)
            else:
                return HttpResponse("you are not authorize in this page!2")
        return wrapper_func

    return decorator



