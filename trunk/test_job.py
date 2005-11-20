# -*- coding: UTF-8 -*-
import time, sys
try:
    import psyco
    psyco.full()
except:
    print "psyco unavailable"

print sys.argv
if len(sys.argv) > 1:
    sys.stderr.write(sys.argv[1])
    time.sleep(int(sys.argv[1]))
else:
    sys.stderr.write("-1")
