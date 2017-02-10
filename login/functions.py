from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


'''
    Decorators explained:

    For each view used after logging in, there is a decorater declared on its url config.
    A decorator is a function that takes a function as an argument, as you can see below.
    Within the decorator function, there is another function declared.
    This function wraps the passed in function (the view function) in itself.
    Within the wrapper function there is code that will run before the passed in function is run
    The wrapper function is then returned to the original caller (the as_view() function call in the url config)
'''

def signed_in_only(function):
    def signed_in_only_view_function_wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            # use reverse and the url config names instead of hardcoding the url
            return HttpResponseRedirect(reverse("login:login"))

        return function(request, *args, **kwargs)

    return signed_in_only_view_function_wrapper
