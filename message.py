import struct 

MESSAGE_FLAGS = {
        0: 'choke',
        1: 'unchoke',
        2: 'interested',
        3: 'uninterested',
        4: 'have',
        5: 'bitfield',
        6: 'request',
        7: 'piece',
        8: 'cancel'
        }

class MessageParser(object):
    def __init__(self, client, peer_id):
        this.peer_id = peer_id
        this.client = client 
        
    while len(buf) > 0:
        if check_for_handshake(buf):
            process_handshake
        msg_len, = struct.unpack('!I', buf[0:4])
        if msg_len == 0:
            this.client.update_timeout(this.peer_id)
            buf = buf[4:]
        if len(buf) < msg_len:
            this.client.wait_for_rest_of_message(this.peer_id, buf)
        msg_id = struct.unpack('!B', buf[4])
        #These four are a pseudo-block, and if one is true, need to update
        #buffer and go back to top of while loop
        if msg_len == 1:
            this.client.set_flag(this.peer_id, MESSAGE_FLAGS[msg_id])
        if msg_id == 4:
            this.client.update_pieces(this.peer_id, 
                    struct.unpack('!I', buf[5:9]))
        if msg_id == 5:
            this.client.update_bit_array(this.peer_id,
                    buf[5:5+msg_len - 1])
        if msg_id == 6:
            block_info = struct.unpack('!III', buf[5:17])
            this.client.add_to_queue(this.peer_id, block_info)
        if msg_id == 7:
            index, begin = struct.unpack('!II', buf[5:13])
            block = struct.unpack('!'+str(msg_len-9)+'B', buf[13:])
            this.client.add_block_to_piece(this.peer_id,
                    (index, begin, len(block)), block)
        if msg_id == 8:
            block_info = struct.unpack('!III', buf[5:17])
            remove_from_queue(this.peer_id, block_info)
        buf = buf[msg_len + 4:]

    
            
            



