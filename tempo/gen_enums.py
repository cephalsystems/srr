with open("enumlist.txt", "rt") as src:
    for line in src:
        sline = line.strip()
        print('addIntConstant(dest, "%s", %s);' % (sline,sline))