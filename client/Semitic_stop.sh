#!/bin/bash
ps -aux | grep suricata | awk '{print $2}'|xargs kill -9