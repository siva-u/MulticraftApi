#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2013 Chinacraft <admin@chinacraft.cc>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

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
import sys
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
    funclen = [1 for i in __method[func]
            if not (isinstance(i,dict) and "default" in i)]
    funclen = reduce(int.__add__, funclen) if funclen else 0
    if len(args) < funclen:
        #print len(__method[func]),__method[func]
        print "This method usage: "
        print str(_multicraftapi__method[func])
        raise TypeError("Not enough arguments. (%d < %d)%s" % (len(args),len(__method[func]),__method[func]))
    elif len(args) > len(__method[func]):
        print "This method usage: "
        print str(_multicraftapi__method[func])
        raise TypeError("Too many arguments. (%d > %d) %s" % (len(args),len(__method[func]),__method[func]))
    fparams = OrderedDict()
    for i in xrange(len(__method[func])):
        if isinstance(__method[func][i],str):
            fparams[__method[func][i]] = args[i]
        else:
            if "type" in __method[func][i]: # arrays
                assert isinstance(args[i],(list,tuple)),"arg %d is not 'arrays'" % i
                fparams[__method[func][i]["name"]] = args[i]
            else: # default option
                fparams[__method[func][i]["name"]] = __method[func][i]["default"]
    key = self.key
    for k,i in fparams.items():
        if isinstance(i,(tuple,list)):
            i = fparams[k] = self.strarray(i)
        key += i if isinstance(i,str) else str(i)
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

def search(method):
    print "You maybe want that:"
    [sys.stdout.write(x + "\n")
        for x in sorted(_multicraftapi__method.keys())
            if x.lower().find(method.lower()) != -1]


def main():
    import pprint
    api = multicraftapi('http://example.com/multicraft/api.php', 'demo', '57ce2b0285bd3c5568e0')
    method = 'findUsers'
    params = (["name","email"], ["test","@example.com"])
    result = api(method,*params)
    assert result['success'], "It seem somethings wrong => %r" % result['errors']
    #print sys.argv
    if len(sys.argv) < 2:
        c = 0
        print "Method list:"
        for x in sorted(_multicraftapi__method.keys()):
            c += 1
            sys.stdout.write(x + ("\n","\t")[bool(c % 3)])
        print "usage: \npython2 multicraftapi.py findUsers -a name email -a test @example.com"
        print "python2 multicraftapi.py findCommands 101 -a name -a command"
        return
    method = sys.argv[1]
    # elif len(sys.argv) == 2 and method in _multicraftapi__method:
    #     print "usage: ",
    #     print str(_multicraftapi__method[method])
    #     return
    lstmode = 0
    params = []
    for x in sys.argv[2:]:
        if x == "-a":
            lstmode = 1
            params.append([])
            continue
        if lstmode:
            params[-1].append(x)
        else:
            params.append(x)
    try:
        pprint.pprint(api(method,*params))
    except ValueError as e:
        print e
        search(method)


if __name__ == "__main__":
    main()


