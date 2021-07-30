import os
import subprocess
import sys
import time
from time import sleep
FIFO = "./namedpipe"
STDOUT = "./logfile.log"
STDERR = "./logfile.err"
# TODO uncomment this
pid = os.fork()
if pid != 0:
    sys.exit(0)

os.setsid()
os.umask(0)
sys.stderr.flush()
sys.stdout.flush()
try:
    os.mkfifo(FIFO)
except OSError:
    pass

with open(FIFO) as fifo, open(STDOUT,"w+") as stdout, open(STDERR,"w+") as stderr:
    while True:
        input_data = fifo.read().strip("\n")
        if not input_data:
            sleep(3)
        # TODO uncomment
        sys.stderr = stderr
        sys.stdout = stdout
        if input_data.isdigit():
            # TODO Daemon shoud write to log the value of soft limit for "Max open files" of the PID
            command = f"cat /proc/{input_data}/limits | grep 'Max open files'"
            output = str(subprocess.check_output(['/bin/bash', '-c', command]))
            print(f"{time.time()} {output}")
        elif input_data == "PACKAGES":
            # TODO write top 5 packages installed in the system
            output = str(subprocess.check_output(['/bin/bash','-c',"""apt list --installed | tail -n 5 | tr "\n" " " """]))
            print(f"{time.time()} {output}")
        elif input_data.startswith("/dev/pts/"):
            # TODO WRITE "Hello Sender" to the terminal /dev/pts/<NUM>. And write 'Sent message to user' to logfile
            print(f"{time.time()} Message sent!")
            subprocess.run(["/bin/bash", "-c", f"echo 'Hello Sender\n' > {input_data}"])
        elif input_data == "CLOSE":
            # TODO Shut down daemon process with message "Shutting down" to log
            print(f"{time.time()} Shutting down")
            os.unlink("./namedpipe")
            sys.exit(1)
        sleep(3)