# Push Junos Telemetry Interface native sensors data to InfluxDB

[jti-to-influxdb.py](https://github.com/tonusoo/jti-to-influxdb/blob/master/jti-to-influxdb.py) is a small script for lab usage which reads [Junos Telemetry Interface native sensors](https://www.juniper.net/documentation/en_US/junos/topics/concept/junos-telemetry-interface-export-format-understanding.html)(JTI) data and writes results to InfluxDB time series database.


## Overview

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
martin@lab-svr:~$ tshark -c 1 -Vn -i ge-0.0.2-PE1 -f "host 10.7.7.2 and udp port 21111"                        
Capturing on 'ge-0.0.2-PE1'
Frame 1: 488 bytes on wire (3904 bits), 488 bytes captured (3904 bits) on interface 0
    Interface id: 0 (ge-0.0.2-PE1)
        Interface name: ge-0.0.2-PE1
    Encapsulation type: Ethernet (1)
    Arrival Time: Mar 13, 2020 11:30:39.502920068 EET
    [Time shift for this packet: 0.000000000 seconds]
    Epoch Time: 1584091839.502920068 seconds
    [Time delta from previous captured frame: 0.000000000 seconds]
    [Time delta from previous displayed frame: 0.000000000 seconds]
    [Time since reference or first frame: 0.000000000 seconds]
    Frame Number: 1
    Frame Length: 488 bytes (3904 bits)
    Capture Length: 488 bytes (3904 bits)
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
    Total Length: 474
    Identification: 0x025c (604)
    Flags: 0x0000
        0... .... .... .... = Reserved bit: Not set
        .0.. .... .... .... = Don't fragment: Not set
        ..0. .... .... .... = More fragments: Not set
        ...0 0000 0000 0000 = Fragment offset: 0
    Time to live: 255
    Protocol: UDP (17)
    Header checksum: 0x95a6 [validation disabled]
    [Header checksum status: Unverified]
    Source: 10.7.7.2
    Destination: 10.7.7.1
User Datagram Protocol, Src Port: 21111, Dst Port: 8091
    Source Port: 21111
    Destination Port: 8091
    Length: 454
    [Checksum: [missing]]
    [Checksum Status: Not present]
    [Stream index: 0]
Data (446 bytes)

0000  0a 09 3a 31 30 2e 37 2e 37 2e 32 10 00 22 6c 67   ..:10.7.7.2.."lg
0010  65 2d 70 6f 72 74 73 3a 2f 6a 75 6e 6f 73 2f 73   e-ports:/junos/s
0020  79 73 74 65 6d 2f 6c 69 6e 65 63 61 72 64 2f 69   ystem/linecard/i
0030  6e 74 65 72 66 61 63 65 2f 6c 6f 67 69 63 61 6c   nterface/logical
0040  2f 75 73 61 67 65 2f 3a 2f 6a 75 6e 6f 73 2f 73   /usage/:/junos/s
0050  79 73 74 65 6d 2f 6c 69 6e 65 63 61 72 64 2f 69   ystem/linecard/i
0060  6e 74 65 72 66 61 63 65 2f 6c 6f 67 69 63 61 6c   nterface/logical
0070  2f 75 73 61 67 65 2f 3a 50 46 45 28 bb 8f 02 30   /usage/:PFE(...0
0080  bf a5 ec 99 8d 2e 38 01 40 01 aa 06 b0 02 e2 a4   ......8.@.......
0090  01 ab 02 3a a8 02 0a 41 0a 0a 67 65 2d 30 2f 30   ...:...A..ge-0/0
00a0  2f 30 2e 30 10 db f9 f8 f2 05 18 99 04 2a 12 08   /0.0.........*..
00b0  e8 d0 44 10 b7 ff f3 b9 02 18 d9 db 32 20 8f f5   ..D.........2 ..
00c0  11 32 10 08 fe cf 25 10 ee ea fa a8 02 18 fe cf   .2....%.........
00d0  25 20 00 3a 04 0a 02 75 70 0a 40 0a 0b 67 65 2d   % .:...up.@..ge-
00e0  30 2f 30 2f 31 2e 38 38 10 b4 9b 83 f3 05 18 9a   0/0/1.88........
00f0  04 2a 10 08 c5 db 1d 10 84 a6 f5 bb 02 18 c5 db   .*..............
0100  1d 20 00 32 10 08 f5 ec 19 10 f6 fd 83 9d 02 18   . .2............
0110  f5 ec 19 20 00 3a 04 0a 02 75 70 0a 2b 0a 0e 67   ... .:...up.+..g
0120  65 2d 30 2f 30 2f 31 2e 33 32 37 36 37 10 bc c0   e-0/0/1.32767...
0130  f9 f2 05 18 9b 04 2a 04 08 00 10 00 32 04 08 00   ......*.....2...
0140  10 00 3a 04 0a 02 75 70 0a 32 0a 0a 67 65 2d 30   ..:...up.2..ge-0
0150  2f 30 2f 33 2e 30 10 da a3 88 f3 05 18 9e 04 2a   /0/3.0.........*
0160  0f 08 e3 ce 02 10 c2 9a f0 03 18 e3 ce 02 20 00   .............. .
0170  32 04 08 00 10 00 3a 04 0a 02 75 70 0a 40 0a 0a   2.....:...up.@..
0180  67 65 2d 30 2f 30 2f 32 2e 30 10 88 c6 98 f3 05   ge-0/0/2.0......
0190  18 a0 04 2a 11 08 d1 8c 25 10 93 dc d7 dc 02 18   ...*....%.......
01a0  86 b4 24 20 cb 58 32 10 08 87 d7 21 10 c7 97 96   ..$ .X2....!....
01b0  b1 02 18 87 d7 21 20 00 3a 04 0a 02 75 70         .....! .:...up
    Data: 0a093a31302e372e372e321000226c67652d706f7274733a...
    [Length: 446]

1 packet captured
martin@lab-svr:~$ 
```

[jti-to-influxdb.py](https://github.com/tonusoo/jti-to-influxdb/blob/master/jti-to-influxdb.py) binds to UDP socket 10.7.7.1:8091, reads the incoming datagrams, decodes the Protocol Buffers data and writes results to InfluxDB.


## Installation

```
(jti-to-influxdb) martin@lab-svr:~/jti-to-influxdb$ git clone https://github.com/Juniper/telemetry -q
(jti-to-influxdb) martin@lab-svr:~/jti-to-influxdb$ sudo apt-get install libprotobuf-dev -qq
Selecting previously unselected package libprotobuf-dev:amd64.
(Reading database ... 185095 files and directories currently installed.)
Preparing to unpack .../libprotobuf-dev_2.6.1-1.3_amd64.deb ...
Unpacking libprotobuf-dev:amd64 (2.6.1-1.3) ...
Setting up libprotobuf-dev:amd64 (2.6.1-1.3) ...
(jti-to-influxdb) martin@lab-svr:~/jti-to-influxdb$ cp -r /usr/include/google telemetry/19.4/19.4R1/protos/
(jti-to-influxdb) martin@lab-svr:~/jti-to-influxdb$ protoc --python_out ~/jti-to-influxdb/ --proto_path ~/jti-to-influxdb/telemetry/19.4/19.4R1/protos/ ~/jti-to-influxdb/telemetry/19.4/19.4R1/protos/logical_port.proto
(jti-to-influxdb) martin@lab-svr:~/jti-to-influxdb$ protoc --python_out ~/jti-to-influxdb/ --proto_path ~/jti-to-influxdb/telemetry/19.4/19.4R1/protos/ ~/jti-to-influxdb/telemetry/19.4/19.4R1/protos/telemetry_top.proto
(jti-to-influxdb) martin@lab-svr:~/jti-to-influxdb$ pip3 install protobuf influxdb -q
(jti-to-influxdb) martin@lab-svr:~/jti-to-influxdb$ ./jti-to-influxdb.py
```

`jti-to-influxdb.py` will populate the InfluxDB `intstats` database `octets` measurement with `i_octets` and `o_octets` field values:

```
martin@lab-svr:~$ influx -database="intstats" -execute "SELECT * FROM octets WHERE \"ifl\"='ge-0/0/1.88' AND time > now() - 20s"
name: octets
time                i_octets  ifl         o_octets
----                --------  ---         --------
1584101655000000000 733572730 ge-0/0/1.88 668732108
1584101658000000000 733587190 ge-0/0/1.88 668746568
1584101660000000000 733603096 ge-0/0/1.88 668762474
1584101662000000000 733617556 ge-0/0/1.88 668776934
1584101664000000000 733632016 ge-0/0/1.88 668791394
1584101666000000000 733647968 ge-0/0/1.88 668807346
1584101669000000000 733662428 ge-0/0/1.88 668821806
1584101671000000000 733676888 ge-0/0/1.88 668836266
martin@lab-svr:~$ 
```

One can easily link Grafana to InfluxDB. Example:
![Grafana bps graph](https://github.com/tonusoo/jti-to-influxdb/blob/master/grafana_bps_graph.png)
