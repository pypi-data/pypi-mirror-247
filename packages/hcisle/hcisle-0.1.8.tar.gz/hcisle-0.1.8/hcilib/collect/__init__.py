# The MIT License (MIT)
#
# Copyright (c) 2021-2022 Thorsten Simons (sw@snomis.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Sos of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyrighftware without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copiet notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import subprocess
from sys import exit
from os import environ
from os.path import join as pjoin
from logging import getLogger

from hcilib.collect.hcidetails import Hci

def collect(installdir: str, logdir: str) -> str:
    """
    Collect logs for 24 hours.

    :param installdir:  the HCI installation folder
    :param logdir:      the folder where the collected log is to be stored
    :returns:           the filename of the collected log package
    """
    log = getLogger('hcisle.' + __name__)

    # Collect required data from HCI
    log.debug('Requesting HCI version and enabled services')
    try:
        hci = Hci(host=environ['HCISLE_HOST'],
                  user=environ['HCISLE_USER'],
                  password=environ['HCISLE_PASSWORD'],
                  realm=environ['HCISLE_REALM'])
    except KeyError as e:
        log.error(f'required environment variable not set: {e}')
        exit(f'Fatal: missing required environment variable!')
        raise
    hciVersion = hci.getHciVersion()['productVersion']
    log.info(f'HCI version {hciVersion}')
    hciServices = hci.getHciServices()
    log.info(f'enabled services: {", ".join(hciServices)}')

    # request log package download
    # -> select wanted services if they are enabled, only!
    _services = ' '.join([x.replace(' ', '\\\\ ') for x in ['Search-App', 'Index', 'Solr 8 Index'] if x in hciServices])

    cmd = f'{pjoin(installdir, "bin/log_download")} -l -o {logdir} --services {_services}'
    log.debug(f'running command: "{cmd}"')
    try:
        ret = subprocess.run(cmd, shell=True, check=True, cwd=installdir,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        log.error('Failed to collect logs!')
        log.error(f'returncode: {e.returncode}')
        log.error(f'stdout: {e.stdout}')
        log.error(f'stderr: {e.stderr}')
        raise
    else:
        # stdout look like this:
        # Log information written to: /opt/hci/logs_1634209645495.zip
        logpkg = ret.stdout.split()[4].decode(encoding="utf-8", errors="ignore")
        return logpkg

