# -*- coding: utf-8 -*-
"""
title:        LogElasticStack
description:  Envia as mensagens de log para o ElasticStack
author:       Jones Vieira
email:        jones.vieira@tivit.com.br
copyright:    TIVIT
version:      2023-05-15 15:49:02
"""
# ---------------------------------------------------------------------------- #
# MODULES                                                                      #
# ---------------------------------------------------------------------------- #
import time
import json
import threading
import requests
# Ajuste para suprimir warnings do urllib
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# ---------------------------------------------------------------------------- #
# CLASS                                                                        #
# ---------------------------------------------------------------------------- #
class Logger(object):
    """
    Envia as mensagens de log para o LogELK
    """
    def __init__(self, env, hostname, app, space, url):
        self.__headers = {
            'content-type': "application/json",
            'charset': "UTF-8"
        }
        self.url = url
        self.space = space
        self.hostname = hostname
        self.env = env
        self.app = app
        self.meta = ''
        self.fixed_tags = []
        self._stdout = False

    @property
    def stdout(self):
        return self._stdout

    @stdout.setter
    def stdout(self, stdout):
        if isinstance(stdout, bool):
            if stdout is True:
                self._stdout = True
            else:
                self._stdout = False
        else:
            raise TypeError('The stdout value need be True or False')

    def critical(self, message, *tags):
        '''
        Grava as mensagens do level CRITICAL
        '''
        threading.Thread(target=self.__post, args=('CRITICAL', message, tags,)).start()

    def error(self, message, *tags):
        '''
        Grava as mensagens do level ERROR
        '''
        threading.Thread(target=self.__post, args=('ERROR', message, tags,)).start()

    def warning(self, message, *tags):
        '''
        Grava as mensagens do level WARNING
        '''
        threading.Thread(target=self.__post, args=('WARNING', message, tags,)).start()

    def info(self, message, *tags):
        '''
        Grava as mensagens do level INFO
        '''
        threading.Thread(target=self.__post, args=('INFO', message, tags,)).start()

    def debug(self, message, *tags):
        '''
        Grava as mensagens do level DEBUG
        '''
        threading.Thread(target=self.__post, args=('DEBUG', message, tags,)).start()

    def trace(self, message, *tags):
        '''
        Grava as mensagens do level TRACE
        '''
        threading.Thread(target=self.__post, args=('TRACE', message, tags,)).start()

    def __post(self, level, message, tags):
        '''
        Envia o post para o LogELK
        '''
        tags = [*self.fixed_tags, *tags]
        if 'message-delivery' in self.url:
            params = {
                'hostname': self.hostname,
                'tags': tags
            }
            data = {
                'lines': [
                    {
                        'timestamp': time.time(),
                        'line': message, 
                        'app': self.app,
                        'level': level,
                        'env': self.env,
                        'meta': self.meta
                    }
                ]
            }
        else:
            params = {}
            data = {
                'aplicacao': self.space,
                'data-log': int(time.time()),
                'message': message,
                'app': self.app,
                'level': level,
                'env': self.env,
                'hostname': self.hostname,
                'meta': json.dumps(self.meta, default=str),
                'tags-log': tags
            }

        attempts = 3
        while attempts > 0:
            try:
                response = requests.post(
                    self.url,
                    headers = self.__headers,
                    params = params,
                    data = json.dumps(data),
                    verify = False,
                    timeout = 5
                )

                if self._stdout:
                    data['status'] = response.status_code
                    data['content'] = response.content.decode('utf-8')
                    print(json.dumps(data, indent = 2, sort_keys = True, default=str))
                self.meta = {}
                attempts = 0
                return True
            except Exception as err:
                print(str(err))
                print(json.dumps(data, indent = 2, sort_keys = True, default=str))
                attempts -= 1
                time.sleep(1)
        return False
