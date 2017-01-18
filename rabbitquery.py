#!/usr/bin/env /usr/bin/python
#Alexandre D Amato abril/2016
import urllib, json, urllib2
import pprint
import sys
import json
import optparse
import socket
import urllib2
import subprocess
import tempfile
import os
import logging

class RabbitMQ(object):
    """docstring for RabbitMQ"""
    def __init__(self, user_name='guest', password='guest', host_name='localhost',
                 protocol='http', port=15672):
        super(RabbitMQ, self).__init__()
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.protocol = protocol
        self.port = port

    def vhost(self):
        url = '{0}://{1}:{2}/api/queues'.format(self.protocol, self.host_name, self.port)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, "zabbix", "zabbix")
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        data=json.loads(urllib2.build_opener(handler).open(url).read())
        lista= []
        for i in data:
            lista.append(i['vhost'])
        ulista = list(set(lista))
        return ulista

    def filas(self,path):
        self.path=path
        url = '{0}://{1}:{2}/api/queues/{3}'.format(self.protocol, self.host_name, self.port, self.path)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, "zabbix", "zabbix")
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        data=json.loads(urllib2.build_opener(handler).open(url).read())
        filaslista=[]
        primeira=0
        for i in data:
            if i["durable"] == True :
                if primeira == 0:
                    primeira=1
                    filaslista=[i["name"]]
                else:
                    filaslista.append(i["name"])
        return filaslista

    def status(self,path,metrica):
        self.metrica=metrica
        self.path=path
        url = '{0}://{1}:{2}/api/queues/{3}'.format(self.protocol, self.host_name, self.port, self.path)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, "zabbix", "zabbix")
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        data=json.loads(urllib2.build_opener(handler).open(url).read())
        '''pp = pprint.PrettyPrinter(depth=6)
        filaStatus={}
        filaStatus['data']=[{"consumers": data["consumers"]},
                            {"deliveries": data["deliveries"]},
                            {"idle_since":data["idle_since"]},
                            {"messages": data["messages"]},
                            {"messages_ready": data["messages_ready"]},
                            {"messages_unacknowledged": data["messages_unacknowledged"]},
                            {"state": data["state"]},
                            {"vhost": data["vhost"]},
                            {"name": data["name"]},
                            {"message_bytes": data["message_bytes"]},
                            {"memory": data["memory"]},
                            ]
        pp.pprint(filaStatus)'''
        print(data[self.metrica])

def main():
    parser = optparse.OptionParser()
    parser.add_option('--u', help='RabbitMQ API username',
                      default='guest')
    parser.add_option('--pwd', help='RabbitMQ API password',
                      default='guest')
    parser.add_option('--h', help='RabbitMQ API host',
                      default="loalhost")
    parser.add_option('--proto', help='RabbitMQ API protocol (http or https)',
                      default='http')
    parser.add_option('--p', help='RabbitMQ API port', type='int',
                      default=15672)
    parser.add_option('--q', help='RabbitMQ API port',
                      default="teste")
    parser.add_option('--v', help='RabbitMQ API port',
                      default="teste")
    parser.add_option('--m', help='RabbitMQ API port',
                      default="teste")
    (options, args) = parser.parse_args()
    api = RabbitMQ(user_name=options.u, password=options.p,
                      host_name=options.h, protocol=options.proto, port=options.p)
    if options.q == "descobrir":
        listaVhosts=[]
        listaFilas=[]
        listadiscovery={"data":[]}
        ## listadiscovery={}
        ## listadiscovery["data"] = []
        listaVhosts=api.vhost()
        primeira = 0
        for i in listaVhosts:
            if primeira == 0:
                primeira=1
                listaFilas=api.filas(i)
                pprimeira=0
                for f in listaFilas:
                    if pprimeira == 0:
                        pprimeira=1
                        listadiscovery["data"]=[{"{#VHOST}":i,"{#FILA}": f}]
                    else:
                        listadiscovery["data"].append({"{#VHOST}":i,"{#FILA}": f})
            else:
                listaFilas=api.filas(i)
                for f in listaFilas:
                    listadiscovery["data"].append({"{#VHOST}":i,"{#FILA}": f})
        pp = pprint.PrettyPrinter(depth=6)
        pp.pprint(listadiscovery)
    elif options.q == "coletar":
        #print("coletar")
        api.status(options.v,options.m)
    else:
        print("Erro")

main()
