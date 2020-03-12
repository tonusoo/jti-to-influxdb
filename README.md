## Push [Junos Telemetry Interface native sensors](https://www.juniper.net/documentation/en_US/junos/topics/concept/junos-telemetry-interface-export-format-understanding.html) data to InfluxDB

Small script for lab usage which reads [Junos Telemetry Interface native sensors](https://www.juniper.net/documentation/en_US/junos/topics/concept/junos-telemetry-interface-export-format-understanding.html) data and writes results to InfluxDB time series database.

Junos configuration example:

```
martin@PE1> show configuration services analytics 
streaming-server native-jti-collector {
    remote-address 10.7.7.1;
    remote-port 8091;
}
export-profile export-parameters {
    local-address 10.7.7.2;
    local-port 21111;
    reporting-rate 1;
    format gpb;
    transport udp;
}
sensor ge-ports {
    server-name native-jti-collector;
    export-name export-parameters;
    resource /junos/system/linecard/interface/logical/usage/;
    resource-filter ge-*;
}

martin@PE1> 
```

With configuration above JTI collector server at `10.7.7.1` receives following datagrams:
```
Frame 1: 483 bytes on wire (3864 bits), 483 bytes captured (3864 bits) on interface 0
    Interface id: 0 (ge-0.0.2-PE1)
        Interface name: ge-0.0.2-PE1
    Encapsulation type: Ethernet (1)
    Arrival Time: Mar 12, 2020 14:22:58.688637971 EET
    [Time shift for this packet: 0.000000000 seconds]
    Epoch Time: 1584015778.688637971 seconds
    [Time delta from previous captured frame: 0.000000000 seconds]
    [Time delta from previous displayed frame: 0.000000000 seconds]
    [Time since reference or first frame: 0.000000000 seconds]
    Frame Number: 1
    Frame Length: 483 bytes (3864 bits)
    Capture Length: 483 bytes (3864 bits)
    [Frame is marked: False]
    [Frame is ignored: False]
    [Protocols in frame: eth:ethertype:ip:udp:data]
Ethernet II, Src: 02:06:dd:02:ff:f2, Dst: fe:06:dd:02:ff:f2
    Destination: fe:06:dd:02:ff:f2
        Address: fe:06:dd:02:ff:f2
        .... ..1. .... .... .... .... = LG bit: Locally administered address (this is NOT the factory default)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
    Source: 02:06:dd:02:ff:f2
        Address: 02:06:dd:02:ff:f2
        .... ..1. .... .... .... .... = LG bit: Locally administered address (this is NOT the factory default)
        .... ...0 .... .... .... .... = IG bit: Individual address (unicast)
    Type: IPv4 (0x0800)
Internet Protocol Version 4, Src: 10.7.7.2, Dst: 10.7.7.1
    0100 .... = Version: 4
    .... 0101 = Header Length: 20 bytes (5)
    Differentiated Services Field: 0x00 (DSCP: CS0, ECN: Not-ECT)
        0000 00.. = Differentiated Services Codepoint: Default (0)
        .... ..00 = Explicit Congestion Notification: Not ECN-Capable Transport (0)
    Total Length: 469
    Identification: 0x0257 (599)
    Flags: 0x0000
        0... .... .... .... = Reserved bit: Not set
        .0.. .... .... .... = Don't fragment: Not set
        ..0. .... .... .... = More fragments: Not set
        ...0 0000 0000 0000 = Fragment offset: 0
    Time to live: 255
    Protocol: UDP (17)
    Header checksum: 0x95b0 [validation disabled]
    [Header checksum status: Unverified]
    Source: 10.7.7.2
    Destination: 10.7.7.1
User Datagram Protocol, Src Port: 21111, Dst Port: 8091
    Source Port: 21111
    Destination Port: 8091
    Length: 449
    [Checksum: [missing]]
    [Checksum Status: Not present]
    [Stream index: 0]
Data (441 bytes)

0000  0a 09 3a 31 30 2e 37 2e 37 2e 32 10 00 22 6c 67   ..:10.7.7.2.."lg
0010  65 2d 70 6f 72 74 73 3a 2f 6a 75 6e 6f 73 2f 73   e-ports:/junos/s
0020  79 73 74 65 6d 2f 6c 69 6e 65 63 61 72 64 2f 69   ystem/linecard/i
0030  6e 74 65 72 66 61 63 65 2f 6c 6f 67 69 63 61 6c   nterface/logical
0040  2f 75 73 61 67 65 2f 3a 2f 6a 75 6e 6f 73 2f 73   /usage/:/junos/s
0050  79 73 74 65 6d 2f 6c 69 6e 65 63 61 72 64 2f 69   ystem/linecard/i
0060  6e 74 65 72 66 61 63 65 2f 6c 6f 67 69 63 61 6c   nterface/logical
0070  2f 75 73 61 67 65 2f 3a 50 46 45 28 b6 02 30 df   /usage/:PFE(..0.
0080  f7 c9 f5 8c 2e 38 01 40 01 aa 06 ac 02 e2 a4 01   .....8.@........
0090  a7 02 3a a4 02 0a 3f 0a 0a 67 65 2d 30 2f 30 2f   ..:...?..ge-0/0/
00a0  30 2e 30 10 db f9 f8 f2 05 18 99 04 2a 11 08 ed   0.0.........*...
00b0  a8 2a 10 f0 93 bb 30 18 df 80 1a 20 8e a8 10 32   .*....0.... ...2
00c0  0f 08 97 8f 0e 10 a0 ea d9 21 18 97 8f 0e 20 00   .........!.... .
00d0  3a 04 0a 02 75 70 0a 3e 0a 0b 67 65 2d 30 2f 30   :...up.>..ge-0/0
00e0  2f 31 2e 38 38 10 b4 9b 83 f3 05 18 9a 04 2a 0f   /1.88.........*.
00f0  08 de 9a 06 10 d2 a8 b2 35 18 de 9a 06 20 00 32   ........5.... .2
0100  0f 08 f6 bf 02 10 e4 e8 e1 16 18 f6 bf 02 20 00   .............. .
0110  3a 04 0a 02 75 70 0a 2b 0a 0e 67 65 2d 30 2f 30   :...up.+..ge-0/0
0120  2f 31 2e 33 32 37 36 37 10 bc c0 f9 f2 05 18 9b   /1.32767........
0130  04 2a 04 08 00 10 00 32 04 08 00 10 00 3a 04 0a   .*.....2.....:..
0140  02 75 70 0a 32 0a 0a 67 65 2d 30 2f 30 2f 33 2e   .up.2..ge-0/0/3.
0150  30 10 da a3 88 f3 05 18 9e 04 2a 0f 08 8e ac 02   0.........*.....
0160  10 ec b2 b4 03 18 8e ac 02 20 00 32 04 08 00 10   ......... .2....
0170  00 3a 04 0a 02 75 70 0a 40 0a 0a 67 65 2d 30 2f   .:...up.@..ge-0/
0180  30 2f 32 2e 30 10 88 c6 98 f3 05 18 a0 04 2a 11   0/2.0.........*.
0190  08 f5 cf 22 10 c4 8f 8e d4 02 18 92 8b 22 20 e3   ..."........." .
01a0  44 32 10 08 82 ca 1f 10 f9 d9 b5 a9 02 18 82 ca   D2..............
01b0  1f 20 00 3a 04 0a 02 75 70                        . .:...up
    Data: 0a093a31302e372e372e321000226c67652d706f7274733a...
    [Length: 441]
```

[jti-to-influxdb.py](https://github.com/tonusoo/jti-to-influxdb/blob/master/jti-to-influxdb.py) binds to UDP socket 10.7.7.1:8091, reads the incoming datagrams, decodes the protocol buffers data and writes results to InfluxDB.


## Installation

