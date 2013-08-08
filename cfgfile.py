import re
def parseconfig(configfile):
    settings = {}
    f = open(configfile)
    for line in f:
        # skip comment lines
        m = re.search('^\s*#', line)
        if m:
            continue
        # parse key=value lines
        m = re.search('^(\w+)\s*=\s*(\S.*)$', line)
        if m is None:
            continue
        settings[m.group(1)] = m.group(2)
    f.close()
    return settings
