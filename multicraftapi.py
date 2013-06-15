#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright 2013 Chinacraft
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

_multicraftapi__method = {
    #User functions
'listUsers' : (),
'findUsers' : ({'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'getUser' : ('id'),
'updateUser' : ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}, {'name': 'send_mail', 'default': 0}),
'createUser' : ('name', 'email', 'password', {'name': 'lang', 'default': ''}, {'name': 'send_mail', 'default': 0}),
'deleteUser' : ('id'),
'getUserRole' : ('user_id', 'server_id'),
'setUserRole' : ('user_id', 'server_id', 'role'),
'getUserFtpAccess' : ('user_id', 'server_id'),
'setUserFtpAccess' : ('user_id', 'server_id', 'mode'),
'getUserId' : ('name'),
#Player functions
'listPlayers' : ('server_id'),
'findPlayers' : ('server_id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'getPlayer' : ('id'),
'updatePlayer' : ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'createPlayer' : ('server_id', 'name'),
'deletePlayer' : ('id'),
'assignPlayerToUser' : ('player_id', 'user_id'),
#Command functions
'listCommands' : ('server_id'),
'findCommands' : ('server_id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'getCommand' : ('id'),
'updateCommand' : ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'createCommand' : ('server_id', 'name', 'role', 'chat', 'response', 'run'),
'deleteCommand' : ('id'),
#Server functions
'listServers' : (),
'findServers' : ({'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'listServersByConnection' : ('connection_id'),
'listServersByOwner' : ('user_id'),
'getServer' : ('id'),
'updateServer' : ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'createServerOn' : ({'name': 'daemon_id', 'default': 0}, {'name': 'no_commands', 'default': 0}, {'name': 'no_setup_script', 'default': 0}),
'createServer' : ({'name': 'name', 'default': ''}, {'name': 'port', 'default': 0}, {'name': 'base', 'default': ''}, {'name': 'players', 'default': 0}, {'name': 'no_commands', 'default': 0}, {'name': 'no_setup_script', 'default': 0}),
'suspendServer' : ('id', {'name': 'stop', 'default': 1}),
'resumeServer' : ('id', {'name': 'start', 'default': 1}),
'deleteServer' : ('id', {'name': 'delete_dir', 'default': 'no'}),
'getServerStatus' : ('id', {'name': 'player_list', 'default': 0}),
'getServerOwner' : ('server_id'),
'setServerOwner' : ('server_id', 'user_id', {'name': 'send_mail', 'default': 0}),
'getServerConfig' : ('id'),
'updateServerConfig' : ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'startServerBackup' : ('id'),
'getServerBackupStatus' : ('id'),
'startServer' : ('id'),
'stopServer' : ('id'),
'restartServer' : ('id'),
'startAllServers' : (),
'stopAllServers' : (),
'restartAllServers' : (),
'sendConsoleCommand' : ('server_id', 'command'),
'sendAllConsoleCommand' : ('command'),
'runCommand' : ('server_id', 'command_id', {'name': 'run_for', 'default': 0}),
'getServerLog' : ('id'),
'clearServerLog' : ('id'),
'getServerChat' : ('id'),
'clearServerChat' : ('id'),
'sendServerControl' : ('id', 'command'),
#Daemon functions
'listConnections' : (),
'findConnections' : ({'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'getConnection' : ('id'),
'removeConnection' : ('id'),
'getConnectionStatus' : ('id'),
'getConnectionMemory' : ('id', {'name': 'include_suspended', 'default': 0}),
#Settings functions
'listSettings' : (),
'getSetting' : ('key'),
'setSetting' : ('key', 'value'),
'deleteSetting' : ('key'),
#Schedule functions
'listSchedules' : ('server_id'),
'findSchedules' : ('server_id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'getSchedule' : ('id'),
'updateSchedule' : ('id', {'name': 'field', 'type': 'array'}, {'name': 'value', 'type': 'array'}),
'createSchedule' : ('server_id', 'name', 'ts', 'interval', 'cmd', 'status', 'for'),
'deleteSchedule' : ('id')
}

import requests
import hashlib
from collections import OrderedDict

class multicraftapi(object):
  def __init__(self,url,user,key):
    self.url = url
    self.user = user
    self.key = key

  def strarray(self,lst):
    s = "["
    for i in lst:
        s += '"%s",' % i
    else:
        s = s[:-1] + "]"
    return s
  def __call__(self,func,*args):
    if func not in __method:
        raise ValueError("The function not exist. (%r)" % func)
    if isinstance(__method[func],str):
        __method[func] = (__method[func],)
    if len(args) < len(__method[func]):
        raise ValueError("Not enough arguments. (%d < %d)" % (len(args),len(__method[func])))
    elif len(args) > len(__method[func]):
        raise ValueError("Too many arguments.")
    fparams = OrderedDict()
    for i in xrange(len(__method[func])):
        if isinstance(i,str):
            fparams[__method[func][i]] = args[i]
        else:
            if "type" in __method[func][i]: # arrays
                assert isinstance(args[i],(list,tuple)),"arg %d is not 'arrays'" % i
                fparams[__method[func][i]["name"]] = args[i]
            elif len(args) <= len(__method[func]): # default option
                fparams[__method[func][i]["name"]] = __method[func][i]["default"]
    key = self.key
    for k,i in fparams.items():
        if isinstance(i,(tuple,list)):
            i = fparams[k] = self.strarray(i)
        key += i
    key += func + self.user
    fparams.update((
        ("_MulticraftAPIMethod",func),
        ("_MulticraftAPIUser",self.user),
        ("_MulticraftAPIKey", hashlib.md5(key).hexdigest()))
    )
    r = requests.get(self.url,params=fparams)
    data = r.json()
    # print key
    # print r.url
    return data

def main():
    api = multicraftapi('http://example.com/multicraft/api.php', 'demo', '57ce2b0285bd3c5568e0')
    method = 'findUsers'
    params = (["name","email"], ["test","@example.com"])
    assert api(method,*params)['success'], "It seem somethings wrong."
    api()

if __name__ == "__main__":
    main()


