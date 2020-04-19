#!/usr/bin/env python3

# Title               : jti-to-influxdb.py
# Last modified date  : 20.04.2020
# Author              : Martin Tonusoo
# Description         : Script reads Junos Telemetry Interface native sensors
#                       data and writes results to InfluxDB time series
#                       database.
# Options             : None
# Notes               : Requires protobuf Python package and Junos
#                       Telemetry Interface data model .proto files available
#                       for registered users from Juniper Downloads portal or
#                       from https://github.com/Juniper/telemetry

import sys
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


def main():
    with sock:
        sock.bind(("0.0.0.0", 8091))

        while True:

            data = sock.recv(65536)
            nt = telemetry_top_pb2.TelemetryStream()
            nt.ParseFromString(data)

            jnpr_ext = nt.enterprise.Extensions[telemetry_top_pb2.juniperNetworks]
            ports = jnpr_ext.Extensions[logical_port_pb2.jnprLogicalInterfaceExt]

            current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            # On vMX running Junos 18.2R1.9 the router requires a reboot for
            # new host-name to take effect. Ip is the "local-address" configured
            # under telemetry export profile and this changes immediately after
            # the commit.
            hostname, ip = nt.system_id.split(":")

            json_body = []
            for port in ports.interface_info:
                json_body += [
                    {
                        "measurement": "octets",
                        "tags": {
                            "ifl": port.if_name,
                            "hostname": hostname,
                            "ip": ip,
                        },
                        "time": current_time,
                        "fields": {
                            "i_octets": port.ingress_stats.if_octets,
                            "o_octets": port.egress_stats.if_octets
                        }
                    }
                ]

            client.write_points(json_body)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
