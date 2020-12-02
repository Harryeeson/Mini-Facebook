"""Custom topology example
Two directly connected switches plus a host for each switch:
   host --- switch --- switch --- host
Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    print("Simple topology example.")

    def __init__( self ):
        print("Create custom topo.")

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'c1' )
        rightHost = self.addHost( 's1' )
        leftHost2 = self.addHost( 'c2' )
        leftHost3 = self.addHost( 'c3' )
        leftSwitch = self.addSwitch( 'sw1' )
        rightSwitch = self.addSwitch( 'sw2' )

        # TODO: Add all the other links similar to one given below 
        self.addLink( leftHost, leftSwitch )        # C1 connects to sw1
        self.addLink( leftHost2, leftSwitch )       # C2 connects to sw1
        self.addLink( leftHost3, leftSwitch )       # C3 connects to sw1
        self.addLink( leftSwitch, rightSwitch )     # sw1 connects to sw2
        self.addLink( rightSwitch, rightHost )      # sw2 connects to s1

topos = { 'mytopo': ( lambda: MyTopo() ) }