import subprocess
import os

def is_program_installed(program):
    """
    Check if a program is installed by trying to call it.
    """

    # Use a null device to suppress the output of the program
    null_device = open(os.devnull, 'w')

    try:
        # Try to execute the program and get its version
        subprocess.run([program, '--version'], stdout=null_device, stderr=null_device)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    finally:
        null_device.close()

def check_invalid_cmdlet(response : bytes):
    if b"invalid cmdlet" in response:
        return True
    if b"is not recognized as an internal or external command" in response:
        return True
    return False
