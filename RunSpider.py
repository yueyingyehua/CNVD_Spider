#config:UTF8

import sys
sys.path.append('/path/to/your/module')
import CNVDSpider
import os

if __name__ == "__main__":
    CNVDSpider.getCNVD().spiderAll()
    os.system("pause")
    input("Press <enter>")