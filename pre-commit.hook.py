#!/usr/bin/env python3
"""
git hook to validating code style, installed via ./init

I use it in all my projects modifying amount of `steps` to needs.

This script has lax approach to variable scope, relying on semi-accidental
closures, for example 'fails' is accessed as if it was passed. Meant for
readability, this is *deliberate* and fine as long as you keep the script short.
"""
from argparse import ArgumentParser
from collections import namedtuple
import functools
import logging.config
import os
from pprint import pformat
import re
import subprocess
import sys

from binaryornot.check import is_binary
from flake8.main.git import find_modified_files

CMD_NOT_FOUND_MSG = 'No such file or directory'

CMD_NOT_FOUND_RC = -100


DEBUG = False
LINE = '█' * 70
Result = namedtuple('Result', ['out', 'rc'])

colours = {
    'RED': 41, 'GREEN': 42, 'YELLOW': 43,
    'blue': 94, 'magenta': 95, 'light_yellow': 93,
    'red': 31, 'green': 32, 'yellow': 33
}


def title(msg: str):
    sys.stdout.write(f'\n{LINE}\r\t {msg} \n')


def step(func):
    # collect step functions, run conditionally
    step.collect.append(func.__name__)

    def inner(*args_, **kwargs):
        # either of lists defined and contains or both empty
        if (skip and func.__name__ not in skip) or (only and func.__name__ in only) or (not skip and not only):
            title(func.__name__)
            fails.update(func(*args_, **kwargs))
        else:
            debug(func.__name__, 'skipped')
    return inner


step.collect = []


def set_logging():
    if DEBUG:
        # flake has nice logs, useful for getting setup.cfg right, isort doesn't have logs
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'color': {
                    '()': 'logging.Formatter',
                    'format': f'\033[{colours["light_yellow"]}m%(name)s %(message)s\033[0m',
                    'datefmt': '%H:%M:%S',
                },
            },
            'handlers': {'color': {'class': 'logging.StreamHandler', 'formatter': 'color'}},
            'loggers': {
                'flake8.options.config': {'handlers': ['color'], 'level': 'DEBUG', 'propagate': False},
                'binaryornot': {'handlers': ['color'], 'level': 'DEBUG', 'propagate': False},
            },
        })


def colour(colour_label: str, msg: str):
    sys.stdout.write(f'\033[{colours[colour_label]:d}m{msg}\033[0m\n')


def debug(*msgs, c='yellow'):
    # takes strings or callables to save time if not DEBUG
    if DEBUG:
        colour(c, ' '.join(str(x()) if callable(x) else str(x) for x in msgs))


def git_available():
    return os.path.exists('.git')


@functools.lru_cache()
def run(cmd: str, fine_if_command_not_found=False, doprint=False, **kwargs) -> Result:
    # pass shell=True to use bash globs, pipes and other builtins
    # TODO: fine_if_command_not_found logic is getting out of hand
    try:
        result = subprocess.run(
            cmd if kwargs.get('shell', False) else cmd.split(),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs
        )
        out, rc = result.stdout.decode('utf-8'), result.returncode
    except Exception as e:
        # won't raise if shell=True
        out, rc = str(e), CMD_NOT_FOUND_RC
        if fine_if_command_not_found and CMD_NOT_FOUND_MSG in str(e):
            rc = 0
    if CMD_NOT_FOUND_MSG in str(out):
        rc = CMD_NOT_FOUND_RC
        if fine_if_command_not_found:
            rc = 0

    debug('run', cmd, kwargs, out.strip(), rc, c='blue')
    if doprint:
        sys.stdout.write(out)
    return Result(out, rc)


def generic_debug_info():
    debug('in:', __file__, c='magenta')
    debug('repo exists:', lambda: git_available())
    debug('cwd:', lambda: os.getcwd())
    debug('last commit:', lambda: run('git rev-parse --short=8 HEAD~1').out)
    debug('branch_name:', lambda: repr(run('git rev-parse --abbrev-ref HEAD').out.rstrip()))


# hook specific
fails = {}


@step
def frontend_lint() -> dict:
    lint = run('yarn lint', cwd='frontend', fine_if_command_not_found=True)
    sys.stdout.write(lint.out)
    return {'frontend_lint': lint.rc}


@step
def backend_flake8_isort() -> dict:
    from flake8.main.git import hook as flake8_hook
    from isort.hooks import git_hook as isort_hook
    return {
        'isort': isort_hook(strict=True),
        'flake8': flake8_hook(strict=True),
    }


@step
def backend_tests():
    tests = run('pytest backend --create-db')
    if tests.rc != 0:
        sys.stdout.write(tests.out)
    return {
        'backend_tests': tests.rc
    }


@step
def yamllint():
    lint = run(
        'find -name \*yml -not -path "./frontend/node_modules/*" 2>/dev/null | xargs yamllint',
        fine_if_command_not_found=True,
        shell=True,
    )
    if CMD_NOT_FOUND_MSG in lint.out:
        return {}
    ret = 0
    out = lint.out.rstrip()
    if out:
        sys.stdout.write(lint.out)
        ret = len([line for line in out.split('\n') if ":" in line])
    return {
        'yamllint': ret
    }


prod = [line.rstrip() for line in open('backend/requirements.txt').readlines() if not line.startswith('#')]
dev = [line.rstrip() for line in open('backend/requirements_dev.txt').readlines() if not line.startswith('#')]


@step
def make_sure_dev_requirements_contain_prod_ones():
    # this is often important for CI
    debug('prod', pformat(prod))
    debug('dev', pformat(dev))
    debug('not in prod', set(dev) - set(prod))
    debug('not in dev', pformat(set(prod) - set(dev)))
    prod_requirements_in_dev = int(not set(dev).issuperset(set(prod)))
    if prod_requirements_in_dev:
        sys.stdout.write('not in prod or dev: %s' % pformat(set(prod) - set(dev)))

    return {'prod_requirements_in_dev': prod_requirements_in_dev}


INVALID_PATTERNS = re.compile(
    '\n([^#].*'
    '('
    '<<<<<<< '  # noqa
    '|======= '  # noqa
    '|=======\n'
    '|>>>>>>> '  # noqa
    '|[\n ]print\('
    '|dupa'  # noqa
    '|kurwa'  # noqa
    '|fuck'  # noqa
    '|shit'  # noqa
    '|#, fuzzy'  # noqa
    '|console.log'  # noqa
    ').*'
    ')'
)


@step
def detect_invalid_patterns(modified_files):
    debug('modified_files', modified_files)
    count = 0
    for filename in modified_files:
        if is_binary(filename):
            continue
        with open(filename, 'r', encoding='utf-8') as inputfile:
            read = inputfile.read()
            for m in INVALID_PATTERNS.finditer(read):
                line, pattern = m.groups()
                if '# noqa' in line:
                    continue
                count += 1
                line_no = read[:m.start()].count('\n') + 2
                sys.stdout.write('%s:%s :\n' % (filename, line_no))
                sys.stdout.write(f'\033[0;33m{pattern}\033[0m'.join(line.split(pattern)).replace('\n', '') + '\n')
    return {'invalid_patterns': count}


@step
def requirements_are_pinned():
    prod_not_pinned = [l for l in prod if not l.startswith('#') and '==' not in l and l]
    dev_not_pinned = [l for l in dev if not l.startswith('#') and '==' not in l and l]
    if prod_not_pinned:
        sys.stdout.write('prod_not_pinned %r\n' % prod_not_pinned)
    debug('prod_not_pinned', prod_not_pinned)
    debug('dev_not_pinned', dev_not_pinned)
    return {
        'requirements_pinned_prod': len(prod_not_pinned),
    }


@step
def find_markers():
    # find patterns and highlight separately
    # https://stackoverflow.com/a/981831/1472229
    run(
        '''
        egrep -Irn \
        --exclude-dir=node_modules --exclude-dir=build --exclude-dir=.git --exclude-dir=.idea \
        --exclude-dir=dist \
        --exclude=\*pyc -e "TODO|HACK|EXPLAIN|REMOVE|THINK|@[A-Z][a-z]+: " 2>/dev/null |
        GREP_COLORS='mt=01;33' egrep --color=always "TODO|$" |
        GREP_COLORS='mt=01;31' egrep --color=always "HACK|$" |
        GREP_COLORS='mt=01;32' egrep --color=always "EXPLAIN|$" |
        GREP_COLORS='mt=01;34' egrep --color=always "REMOVE|$" |
        GREP_COLORS='mt=01;35' egrep --color=always "THINK|$" |
        GREP_COLORS='mt=01;36' egrep --color=always "@[A-Z][a-z]+: |$" |
        egrep -v "egrep|exclude|title\("
        ''',
        doprint=True,
        shell=True,
    )
    return {}


def hook():
    generic_debug_info()
    debug('all_files', all_files)

    frontend_lint()
    backend_flake8_isort()
    backend_tests()
    yamllint()
    make_sure_dev_requirements_contain_prod_ones()
    modified_files = set(find_modified_files(True))
    detect_invalid_patterns(modified_files)
    requirements_are_pinned()
    find_markers()

    any_fails = sum(fails.values())
    if any_fails:
        colour('RED', pformat(fails))
    debug('fails', fails)
    return any_fails


parser = ArgumentParser()
parser.add_argument(
    '-a', '--all-files',
    help='Run on all files rather on git "Changes to be committed", the default.',
    action='store_true'
)
parser.add_argument(
    '-d', '--debug',
    action='store_true'
)
parser.add_argument(
    '-s', '--skip',
    help='Functions to skip',
    default=[],
    choices=step.collect
)
parser.add_argument(
    '-o', '--only',
    help='Only run these functions',
    default=[],
    choices=step.collect
)

args = parser.parse_args()
assert not all((args.only, args.skip)), '--skip and --only are mutually exclusive.'
if args.debug:
    DEBUG = True
debug('argparse', args)
all_files = args.all_files
skip = args.skip
only = args.only
set_logging()
sys.exit(hook())
