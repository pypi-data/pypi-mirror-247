# Generates a JSON trace that is compatible with the js/pytutor.ts frontend

import json
import sys
from optparse import OptionParser
from .json_tracer import JSONTracer

# To make regression tests work consistently across platforms,
# standardize display of floats to 3 significant figures
#
# Trick from:
# http://stackoverflow.com/questions/1447287/format-floats-with-standard-json-module
json.encoder.FLOAT_REPR = lambda f: ('%.3f' % f)


parser = OptionParser(usage="Generate JSON trace for pytutor")
parser.add_option('-c', '--cumulative', default=False, action='store_true',
                  help='output cumulative trace.')
parser.add_option('-p', '--heapPrimitives', default=False, action='store_true',
                  help='render primitives as heap objects.')
parser.add_option('--allmodules', default=False, action='store_true',
                  help='allow importing of all installed Python modules.')
parser.add_option("--code", dest="usercode", default=None,
                  help="Load user code from a string instead of a file and output compact JSON")
parser.add_option("--probe-exprs", dest="probe_exprs_json", default=None,
                  help="A JSON list of strings representing expressions whose values to probe at each step (advanced)")

(options, args) = parser.parse_args()

if options.usercode:
    INDENT_LEVEL = None

    probe_exprs = None
    if options.probe_exprs_json:
        probe_exprs = json.loads(options.probe_exprs_json)

    allow_all_modules = False
    if options.allmodules:
        allow_all_modules = True
    print(JSONTracer(options.cumulative,
                     options.heapPrimitives,
                     False,
                     probe_exprs=probe_exprs,
                     allow_all_modules=allow_all_modules).runscript(options.usercode))

else:
    fin = sys.stdin if args[0] == "-" else open(args[0])

    print(JSONTracer(options.cumulative,
                     options.heapPrimitives,
                     False).runscript(fin.read()))
