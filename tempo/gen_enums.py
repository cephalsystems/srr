import sys

with open(sys.argv[1], "rt") as src:
    for line in src:
        gps = line.strip().split()
        if len(gps) > 0:
            if gps[0] == "#define" and len(gps) > 1:
                sline = gps[1]
            else:
                sline = gps[0]
            print('addIntConstant(dest, "%s", %s);' % (sline,sline))