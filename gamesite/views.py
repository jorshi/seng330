"""
Gamesite Views
"""

from django.shortcuts import render, redirect
import django.contrib.staticfiles.views as static_server

def doxygen(request, path=None):
    """
    Hack to serve doxygen files
    """

    if not path:
        return static_server.serve(request, "doxygen/html/index.html")
    # Super hacky ... for some reason index.html doesn't work ??
    elif path == "index.html/":
        return redirect("/doxygen/")
    else:
        return static_server.serve(request, "doxygen/html/%s" % path)
