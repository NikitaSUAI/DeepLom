# AUTHORS
# Jose PATINO, EURECOM, Sophia-Antipolis, France, 2019
# http://www.eurecom.fr/en/people/patino-jose
# Contact: patino[at]eurecom[dot]fr, josempatinovillar[at]gmail[dot]com

from pyBK import alon, as_service
import sys

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "service":
        as_service()
    else:
        alon()
