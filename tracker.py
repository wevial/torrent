import bencode as B
import hashlib as H
import requests
import urllib as U
import socket
import metadata
#import util
#url_encode the info_hash

class Tracker:
    def __init__(self, metadata):
        self.torrent = metadata.torrent
        self.tracker_url = metadata.data['announce']
        self.params_order = ['uploaded', 'compact', 'info_hash', 'event', 
                'downloaded', 'peer_id', 'port', 'left']
        self.params = {
            'uploaded': '0',
            'compact': '1',
            'info_hash': H.sha1(B.bencode(metadata.data['info'])).digest(),
            'event': 'started',
            'downloaded': '0',
            'peer_id': '-TZ-0000-00000000000',
            'port': '6881', 
            'left': str(metadata.data['info']['length']),
        }

    def construct_url(self):
        """ Construct the full URL for the torrent we're connecting to """ 
        params = '&'.join('%s=%s' % (key, U.quote(self.params[key])) for key in self.params_order)
        full_url = self.tracker_url + '?' +  params
        self.full_url = full_url
        return full_url

    def send_request(self):
        """ Returns bencoded request """
        return requests.get(url=self.full_url)

    def get_host_string(self, peer_byte_list):
        return '.'.join([str(val) for val in peer_byte_list[0:4]])

    def get_port(self, peer_byte_list):
        return 256 * peer_byte_list[4] + peer_byte_list[5]


    def peer_host_port_vals(self, peers):
        #Get values of all bytes in byte_string list of peers
        peer_host_port_values = []
        while len(peers) > 0:
            peer_host_port_values.append( [ ord(peer) for peer in peers[0:6] ] )
            peers = peers[6:]
        return peer_host_port_values

    def peers_to_ips(self, peer_bytes):
        byte_list = self.peer_host_port_vals(peer_bytes)
        return [(self.get_host_string(peer), self.get_port(peer)) for peer in byte_list]

    def parse_response(self, response):
        response_text = B.bdecode(response.text)
        self.peer_ips = self.peers_to_ips(response_text['peers'])
        
    #TO DO - make sure str methods are compatible with unicode crap


        
def build():
    m = metadata.Metadata()
    m.decode()
    t = Tracker(m)
    t.construct_url()
    return t