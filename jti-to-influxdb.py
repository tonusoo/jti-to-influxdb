#!/usr/bin/env python3

# Title               : jti-to-influxdb.py
# Last modified date  : 12.03.2020
# Author              : Martin Tonusoo
# Description         : Script reads Junos Telemetry Interface native sensors
#                       data and writes results to InfluxDB time series
#                       database.
# Options             : None
# Notes               : Requires python3-protobuf Python package and Junos
#                       Telemetry Interface Data Model Files package.
#                       Latter is available for registered users from
#                       https://www.juniper.net/support/downloads/

import socket
import logical_port_pb2
import telemetry_top_pb2
from datetime import datetime
from influxdb import InfluxDBClient

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client = InfluxDBClient(host="localhost", port=8086, username="admin",
                                                     password="admin")
client.create_database("intstats")
client.switch_database("intstats")


with sock:
    sock.bind(("10.7.7.1", 8091))

    while True:

        data = sock.recv(65536)
        nt = telemetry_top_pb2.TelemetryStream()
        nt.ParseFromString(data)

        jnpr_ext = nt.enterprise.Extensions[telemetry_top_pb2.juniperNetworks]
        ports = jnpr_ext.Extensions[logical_port_pb2.jnprLogicalInterfaceExt]

        current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        json_body = []
        for port in ports.interface_info:
            json_body += [
                {
                    "measurement": "octets",
                    "tags": {
                        "ifl": port.if_name,
                    },
                    "time": current_time,
                    "fields": {
                        "i_octets": port.ingress_stats.if_octets,
                        "o_octets": port.egress_stats.if_octets
                    }
                }
            ]

        client.write_points(json_body)
