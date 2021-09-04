from optparse import OptionParser

usage = "Usage: %prog [discover | test] url [OPTIONS]"
parser = OptionParser(usage=usage)

# custom auth
parser.add_option("--custom-auth", dest="auth", metavar="STRING")

# common words
parser.add_option("--common-words", dest="words", metavar="FILE")
