#!/bin/bash
#Alexandre D Amato abril/2016
USUARIO=zabbix
SENHA=zabbix
PROTOCOLO=http
PORTA=15672
HOST=
#curl -i -u zabbix:zabbix http://rabbitmq.rocko83.com.br:15672/api/queues/teste/teste01
#Métricas a serem monitoradas
#messages=tamanho da fila
#messages_ready=tamanho da fila que ninguém pegou
#state
#idle_since
function ajuda() {
	echo \# $0 descobrir
	echo \# $0 coletar vhost fila metrica
}
case $# in
	0)
		ajuda
		exit 1
		;;
	1)
		case $1 in
			descobrir)
				./rabbitquery.py --u=$USUARIO --pwd=$SENHA --h=$HOST --proto=$PROTOCOLO --p=$PORTA --q=descobrir
				;;
			*)
				ajuda
				exit 1
				;;
		esac
		;;
	4)
		case $1 in
			coletar)
				./rabbitquery.py --u=$USUARIO --pwd=$SENHA --h=$HOST --proto=$PROTOCOLO --p=$PORTA --q=coletar --v=$2/$3 --m=$4
				;;
			*)
				ajuda
				exit 1
				;;
		esac
		;;
	*)
		ajuda
		exit 1
		;;
esac
