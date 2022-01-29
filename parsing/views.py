import subprocess

from django.shortcuts import redirect, render
from loguru import logger

parser_process: subprocess = None


def index(request):
    status = False
    global parser_process
    if parser_process:
        status = True
    context = {"status": status}
    return render(request, "index.html", context)


def main(request):
    global parser_process
    if not parser_process:
        parser_process = subprocess.Popen(
            "python manage.py polling", stdout=subprocess.PIPE, shell=True
        )
    else:
        logger.debug(f"Ping {parser_process.pid}")
        subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=parser_process.pid))
        parser_process = False
    return redirect("index")
