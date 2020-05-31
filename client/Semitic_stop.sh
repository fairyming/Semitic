#!/bin/bash
ps -aux | grep suricata | awk '{print $2}'|xargs kill -9
ps -aux | grep senteve | awk '{print($2)}'| xargs kill -9