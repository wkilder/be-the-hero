#!/usr/bin/python

"""
Cenario de Prova Pratica de Redes 2
Adaptacao do codigo de exemplo
linuxrouter.py: Example network with Linux IP router
~mininet/examples/linuxrouter.py
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
	"No com encaminhamento de pacotes habilitado."

	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		# Enable forwarding on the router
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
	# Topologia de rede usando seis subredes

	def build( self, **_opts ):


		r1 = self.addNode( 'r1', cls=LinuxRouter, ip='10.1.0.1/16' )
		r2 = self.addNode( 'r2', cls=LinuxRouter, ip='10.2.0.1/16' )
		r3 = self.addNode( 'r3', cls=LinuxRouter, ip='10.3.0.1/16' )
		r4 = self.addNode( 'r4', cls=LinuxRouter, ip='10.4.0.1/16' )

		s1, s12, s2, s23, s3, s34, s4 = [ self.addSwitch( s ) 
		                       for s in 's1', 's12', 's2', 's23', 's3', 's34', 's4' ]


		for switch_i, roteador_i, intfName, endereco_ip in [(s1 ,r1,'r1-eth0','10.1.0.1/16'),
		                                                    (s12,r1,'r1-eth1','10.12.0.1/16'),

		                                                    (s2  ,r2,'r2-eth0','10.2.0.1/16'),
		                                                    (s12 ,r2,'r2-eth1','10.12.0.2/16'),
		                                                    (s23 ,r2,'r2-eth2','10.23.0.1/16'),

		                                                    (s3  ,r3,'r3-eth0','10.3.0.1/16'),
		                                                    (s23 ,r3,'r3-eth1','10.23.0.2/16'),
		                                                    (s34 ,r3,'r3-eth2','10.34.0.1/16'),

		                                                    (s4  ,r4,'r4-eth0','10.4.0.1/16'),
		                                                    (s34 ,r4,'r4-eth1','10.34.0.2/16')
                                                         ]:
			self.addLink( switch_i, roteador_i, intfName2=intfName, params2={'ip' : endereco_ip} )


		h1_1 = self.addHost( 'h1_1', ip='10.1.0.2/16',
		                   defaultRoute='via 10.1.0.1' )
		h1_2 = self.addHost( 'h1_2', ip='10.1.0.3/16',
		                   defaultRoute='via 10.1.0.1' )

		h2_1 = self.addHost( 'h2_1', ip='10.2.0.2/16',
		                   defaultRoute='via 10.2.0.1' )
		h2_2 = self.addHost( 'h2_2', ip='10.2.0.3/16',
		                   defaultRoute='via 10.2.0.1' )

		h3_1 = self.addHost( 'h3_1', ip='10.3.0.2/16',
		                   defaultRoute='via 10.3.0.1' )

		h34_1 = self.addHost( 'h34_1', ip='10.34.0.99/16',
		                   defaultRoute='via 10.34.0.1' )

		h4_1 = self.addHost( 'h4_1', ip='10.4.0.2/16',
		                   defaultRoute='via 10.4.0.1' )
		h4_2 = self.addHost( 'h4_2', ip='10.4.0.3/16',
		                   defaultRoute='via 10.4.0.1' )

		# adiciona enlaces de comunicacao entre todos os hosts e
		# respectivos switches de suas redes
		for h, s in [(h1_1,s1),(h1_2,s1),(h2_1,s2),(h2_2,s2),(h3_1,s3),(h34_1,s34),(h4_1,s4),(h4_2,s4)]:
			self.addLink(h,s)

		
def run():
	topo = NetworkTopo()
	net = Mininet( topo=topo )
	net.start()
	net['r1'].cmd('route add default gw 10.12.0.2') 
	net['r2'].cmd('route add default gw 10.23.0.2')
	net['r3'].cmd('route add default gw 10.23.0.1')
	net['r4'].cmd('route add default gw 10.34.0.1')
	info( '*** Tabela de Roteamento do roteador r1:\n' )
	print net[ 'r1' ].cmd( 'route -n' )
	CLI( net )
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	run()
