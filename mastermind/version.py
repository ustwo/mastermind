IVERSION = (0, 9, 0, 'b0')
VERSION = ".".join(str(i) for i in IVERSION)
MINORVERSION = ".".join(str(i) for i in IVERSION[:2])

if __name__ == '__main__':
    print(VERSION)
