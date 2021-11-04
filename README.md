NGINX Syntetic Access Logs
==========================

This is a simple utility for generating synthetic access logs for NGINX.
You can tweak the random weights to inject different types of requests into your fake logs
and practice parsing or processing them to your heart's content

Usage
-----

```
Usage: generate_logs.py [options]

Options:
  -h, --help            show this help message and exit
  -l LINES, --lines=LINES
                        Number of log lines to generate.

```

*NOTE:* This tool uses the python `dataclasses` module, which is available starting in python 3.7.  If you have a lower version of python (or no python) installed at the system level, you can use the included Dockerfile (assuming you've got docker installed).