import sys
from datetime import datetime
from mylib import Foo

def main():

    fi = sys.argv[1]
    fo = sys.argv[2]

    newlines = []
    with open(fi) as f:
        for line in f.readlines():
            newlines.append(line.strip())

    newlines.append(datetime.now().isoformat(' '))

    val = Foo().get_foo()
    newlines.append(str(val))

    with open(fo, 'w') as f:
        f.write('\n'.join(newlines))


if __name__ == '__main__':
    main()
