NGINX Syntetic Access Logs
==========================

This is a simple utility for generating synthetic access logs for NGINX.
You can tweak the random weights to inject different types of requests into your fake logs
and practice parsing or processing them to your heart's content

Usage
-----

This tool uses the python `dataclasses` module, which is available starting in python 3.7.

If you have python 3.7 or higher in your system, you can just run:

`./generate_logs.py`

If you have a lower version of python (or no python, I guess), you can use the included Dockerfile.