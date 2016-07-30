#  Copyright 2016 Florian Eich, florian.eich@gmail.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import sys
import time
import datetime as dt
import configparser

import certificates.spreadhandler as sh
import certificates.datahandler as dh
import certificates.certhandler as ch


class Core:
    '''Core class for the certificate generator.

    Reads configuration, instantiates connection, starts generator thread.'''
    def __init__(self, debug):
        self.debug = debug

        self.confpath = os.path.expanduser('~/.config/certificates/')
        if not os.path.exists(self.confpath):
            os.makedirs(self.confpath)

        self.msgfile = open(self.confpath + 'msgfile.log', 'w+')

        self.conffile = self.confpath + 'certificates.cfg'
        self.config = configparser.ConfigParser()

        if not os.path.exists(self.conffile):
            self.msglog('INFO', self.conffile + ' not found')
            self.config['DEFAULT']['timeout'] = 30
            self.config['DEFAULT']['gapi_key'] = 'certkey.json'
            self.config['DEFAULT']['source'] = '~/.config/certificates/'
            self.config['DEFAULT']['destination'] = '~/certificates/'
            self.config['WIKI']['user'] = 'munich.motorsport'
            self.config['WIKI']['pass'] = 'MiaMengsBoarisch!'
            with open(self.conffile, 'w') as f:
                self.config.write(f)
            self.msglog('INFO', 'default configfile generated in place')

        self.config.read(self.conffile)

        try:
            self.timeout = self.config['DEFAULT']['timeout']
            self.gapi_key = self.config['DEFAULT']['gapi_key']
            self.tmpl_src = self.config['DEFAULT']['source']
            self.cert_dest = self.config['DEFAULT']['destination']
            self.wiki_user = self.config['WIKI']['user']
            self.wiki_pass = self.config['WIKI']['pass']
            self.msglog('INFO', 'config read')
        except KeyError:
            self.msglog('FATAL', 'config file faulty')

        self.spreadh = sh.SpreadHandler(self, self.confpath, self.gapi_key)
        self.datah = dh.DataHandler(self, self.wiki_user, self.wiki_pass)
        self.certh = ch.CertHandler(self, self.tmpl_src, self.cert_dest)

        self.handlers = [self.spreadh, self.datah, self.certh]

    def run(self):
        try:
            while True:
                time.sleep(self.timeout)
                synctime = time.perf_counter()
                for handler in self.handlers:
                    handler.sync(synctime)
        except KeyboardInterrupt:
            self.msglog('INFO', 'keyboard interrupt received, exiting')
            sys.exit(0)

    def msglog(self, type, message):
        log = dt.datetime.now(dt.timezone.utc).astimezone().isoformat() + ' # '
        log += type + '\t\t# '
        log += message

        print(log, file=self.msgfile, flush=True)

        if self.debug:
            print('msglog: ### ' + log)

        if type == 'FATAL':
            self.msgfile.close()
            sys.exit(-1)
