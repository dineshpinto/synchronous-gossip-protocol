"""
Usage:
  test.py [--no-header] [--debug] [-r n] [-p p] [-b B]
  test.py (-h | --help)

Options:
  -h --help    Show this text.
  --no-header  Skip JSONL headers.
  --debug      Show time taken for simulations.
  -r n         No. of repeats [default: 50]
  -p p         Prob of links. [default: 1.0,0.001,0.05,0.01,0.1,0.5,0.9,0.99]
  -b B         No. of evil nodes [default: 10,20,30,40,50]
"""

import itertools
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor

from docopt import docopt

import synchronous_gossip_protocol


def dump(k):
    print(json.dumps(k))


N = 100
K = 25
t = 2000


def run_simulation(params):
    return synchronous_gossip_protocol.run(*params)


def generate_conditions(repeats, probs, n_evil):
    for p in probs:
        for B in n_evil:
            yield (p, B, 1 if p == 1.0 else repeats)


def main(args):
    debug = args['--debug']
    show_header = not args['--no-header']
    if show_header:
        dump(['p', 'B', 'immediate', 'ok'])

    repeats = int(args['-r'])
    probs = [float(n) for n in args['-p'].split(',')]
    n_evil = [int(n) for n in args['-b'].split(',')]
    conditions = generate_conditions(repeats, probs, n_evil)

    with ProcessPoolExecutor() as exe:
        for p, B, repeats in conditions:
            start = time.time()
            results = exe.map(run_simulation, itertools.repeat(
                (N, K, B, p, t),
                repeats,
            ))
            for is_immediate, ok in results:
                dump([p, B, is_immediate, ok])
            if debug:
                end = time.time()
                dt = end - start
                sys.stderr.write('p=%r B=%r t=%r\n' % (p, B, dt))
                sys.stderr.flush()


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
