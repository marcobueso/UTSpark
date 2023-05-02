#!/bin/bash

sudo mkdir -p tls-results/

# Start envoy with no filter config
sudo ./setup_envoy_alone.sh
sudo ./setup_perf.sh

# Start envoy with RBAC network filter config
sudo ./start_envoy.sh envoy-l4-ip-filter.yaml 1 100 &
PID2=(ps -C "envoy" -o pid=)
sleep 5

# Test TLS with request rates of 1500, 3000
sudo timeout 10 ./perf-l4.sh stat tls 1500
sudo timeout 10 ./perf-l4.sh stat tls 3000
sudo kill $PID2