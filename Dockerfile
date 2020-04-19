FROM debian:buster-slim

ENV REFRESHED_AT 20-04-2020

RUN apt-get update && apt-get install -y --no-install-recommends \
		ca-certificates \
		git \
		libprotobuf-dev \
		protobuf-compiler \
		python3 \
		python3-pip \
	&& rm -rf /var/lib/apt/lists/*

RUN pip3 install protobuf influxdb

RUN groupadd -r jtiuser \
	&& useradd --no-log-init -r -m -g jtiuser jtiuser
USER jtiuser
WORKDIR /home/jtiuser

RUN git clone https://github.com/Juniper/telemetry && \
	cp -r /usr/include/google telemetry/19.4/19.4R1/protos/

RUN mkdir jti-to-influxdb/ && \
	protoc --python_out jti-to-influxdb/ \
	--proto_path telemetry/19.4/19.4R1/protos/ \
	telemetry/19.4/19.4R1/protos/logical_port.proto && \
	protoc --python_out jti-to-influxdb/ \
	--proto_path telemetry/19.4/19.4R1/protos/ \
	telemetry/19.4/19.4R1/protos/telemetry_top.proto

COPY jti-to-influxdb.py jti-to-influxdb/

CMD [ "python3", "jti-to-influxdb/jti-to-influxdb.py" ]
