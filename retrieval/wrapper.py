# coding:utf-8

from functools import wraps
import random
from django.conf import settings
from django.utils.decorators import available_attrs
import hashlib

if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange
_MAX_CSRF_KEY = 18446744073709551616L  # 2 << 63


def _get_new_submit_key():
    return hashlib.md5("%s%s" % (randrange(0, _MAX_CSRF_KEY), settings.SECRET_KEY)).hexdigest()


def anti_resubmit(page_key=''):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'GET':
                request.session['%s_submit' % page_key] = _get_new_submit_key()
                print 'session:' + request.session.get('%s_submit' % page_key)
            elif request.method == 'POST':
                old_key = request.session.get('%s_submit' % page_key, '')
                if old_key == '':
                    from django.http import HttpResponseRedirect
                    return HttpResponseRedirect('/home')
                request.session['%s_submit' % page_key] = ''
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


