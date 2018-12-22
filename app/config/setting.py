"""
author : Ger-Rr
"""
import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BLOG_POST_PER_PAGE=10
BLUE_BLOG_THEME = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan','journal':'journal','sketchy':'sketchy'}
ADMIN_POST_PER_PAGE = 10
BLUELOG_COMMENT_PER_PAGE = 10
BLUELOG_ALLOWED_IMAGE_EXTENSIONS =['jpg','png','jpeg','gif','svg','psd','cdr']
BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')