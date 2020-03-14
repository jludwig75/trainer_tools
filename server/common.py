from subprocess import run
import shlex

def running_on_rpi():
    try:
        import RPi.GPIO
        return True
    except:
        return False

def run_cmd(cmd):
    p = run(shlex.split(cmd), check=True, capture_output=True)
    return p.stdout.decode("utf-8")