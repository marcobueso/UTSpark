#!/bin/bash

sudo mkdir -p perf_data/l4/stat/nofilter perf_data/l4/stat/rbac

# Start envoy with no filter config
sudo ./setup_envoy_alone.sh
sudo ./setup_perf.sh
sudo ./start_envoy.sh envoy-demo.yaml 1 100 &
PID1=$!
sleep 5

# Test no filter with request rates of 500, 1000
sudo timeout 10 ./perf-l4-10ms.sh stat nofilter 500
sudo timeout 10 ./perf-l4-10ms.sh stat nofilter 1000
sudo kill $PID1

# Start envoy with RBAC network filter config
sudo ./start_envoy.sh envoy-l4-ip-filter.yaml 1 100 &
PID2=$!
sleep 5

# Test RBAC with request rates of 500, 1000
sudo timeout 10 ./perf-l4-10ms.sh stat rbac 500
sudo timeout 10 ./perf-l4-10ms.sh stat rbac 1000
sudo kill $PID2