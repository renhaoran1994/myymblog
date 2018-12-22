from urllib.parse import urlparse,urljoin
from flask import request,url_for,redirect,current_app

def is_safe_url(target):
    ret_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and ret_url.netloc == test_url.netloc

def redirect_back(defalut='blog.index',**kwargs):
    for tagrt in request.args.get('next'),request.referrer:
        if not tagrt:
            continue
        if is_safe_url(tagrt):
            return redirect(tagrt)
    return redirect(url_for(defalut,**kwargs))

def allowflie(filename):
    return '.'in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']