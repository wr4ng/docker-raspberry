#!/usr/bin/env python3

import datetime
import speedtest
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "grafana"
ifpass = "password"
ifdb   = "maindb"
ifhost = "influxdb"
ifport = 8086
measurement_name = "speedtest"

# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# run a single-threaded speedtest using default server
s = speedtest.Speedtest()
s.get_best_server()
s.download()
s.upload()
res = s.results.dict()

# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": time,
        "fields": {
            "download": res["download"],
            "upload": res["upload"],
            "ping": res["ping"]
        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
ifclient.write_points(body)