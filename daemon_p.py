import os
import sys
from time import sleep

pid = os.fork()
if pid != 0:
    sys.exit(0)

os.chdir("~")
os.setsid()
os.umask(0)
sys.stderr.flush()
sys.stdout.flush()

os.mkfifo("~/namedpipe")
input = os.open("~/namedpipe", os.O_RDONLY)
output = os.open("~/daemon_logfile.log", os.O_WRONLY)
err = os.open("~/daemin_logfile.log", os.O_WRONLY)
os.dup2(input, sys.stdin.fileno())
os.dup2(output, sys.stdout.fileno())
os.dup2(err, sys.stderr.fileno())

while True:
    sleep(2)
    input_data = sys.stdin.read()
    if input_data.isdigit():

        ...


os.unlink("/namedpipe")