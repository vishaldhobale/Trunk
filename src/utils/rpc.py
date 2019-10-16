import os
import sys
import socket
import subprocess
import hashlib
from xmlrpc.server import SimpleXMLRPCServer

sys.path.append(os.getcwd())

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
server = SimpleXMLRPCServer((IP, 9000), logRequests=True, allow_none=True)

print(hostname)
print(IP)


@server.register_function
def test_hello():
    print("Hello...")


@server.register_function
# execute given command on command prompt in given directory(cwd)
def execute_command(command, cwd):
    """
    :param command:
    :param cwd:
    :return:
    """
    print("executing command " + command)
    try:
        out = subprocess.check_output(command, shell=True, cwd=cwd)
    except Exception as e:
        out = str(e)
    return out


@server.register_function
# calculate md5 checksum of given file
def get_md5(file_path):
    """
    :param file_path:
    :return:
    """
    BLOCKSIZE = 65536
    try:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buf = file.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(BLOCKSIZE)
        print(hasher.hexdigest())
        print(type(hasher.hexdigest()))
        return hasher.hexdigest()
    except Exception as e:
        print("error generating checksum: " + str(e))
        return str(e)


@server.register_function
# returns list of files present under given directory
def get_list(path):
    """
    :param path:
    :return:
    """
    lst = []
    for root, dirs, files in os.walk(path):
        lst.extend(files)
    return lst


# server.register_function(test_hello)
# server.register_function(get_md5)
# server.register_instance(add instance here)

try:
    print('Use Control-C to exit')
    server.serve_forever()
except KeyboardInterrupt as ki:
    print(str(ki))
    print('Exiting...')
