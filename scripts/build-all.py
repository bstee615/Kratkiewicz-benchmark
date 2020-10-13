MANIFEST_FILE = './manifest-89-2Ekjh3.xml'

with open(MANIFEST_FILE, 'r') as f:
    text = f.read()

from logging import log
import xmltodict
root = xmltodict.parse(text)
testcases = root['container']['testcase']

import subprocess
from pathlib import Path
import shutil
import logging
logging.basicConfig(level=logging.INFO)

tmp = Path('tmp')
tmp.mkdir(exist_ok=True)

for tc in testcases:
    logging.info('Building testcase %s', tc['@id'])

    srcfile = Path(tc['file']['@path'])
    assert(srcfile.exists())
    build_dir = tmp / tc['@id']

    aout = Path(build_dir / 'a.out')
    if aout.exists():
        logging.info('Skipping testcase %s because it is already built', tc['@id'])
        continue

    build_dir.mkdir(exist_ok=True)
    try:
        shutil.copy(srcfile, build_dir)
    except FileExistsError:
        pass
    process = subprocess.Popen(['gcc', srcfile.name], cwd=build_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = process.communicate()
    logging.debug(out.decode('utf-8').strip())
    
    logging.info('Done building testcase %s', tc['@id'])