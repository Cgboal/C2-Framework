import os, urllib, pip, re


def install(package):
    pip.main(['install', package])


if __name__ == "__main__":
    install('wheel')

    try:
        os.mkdir('agent')
    except Exception, e:
        print e

    os.chdir('agent')
    url = "http://{{hostname}}/latest"
    filename = re.findall("filename=(.+)", urllib.urlopen(url).info().getheader("Content-Disposition"))[0]
    whl = urllib.urlretrieve(url, filename)
    install('./%s' % filename)
