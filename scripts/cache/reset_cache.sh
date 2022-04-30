#!/bin/bash
# ©2022 TickSy
# TickSy development memcached cache reset script
# Prerequisites
# Ubuntu 20.04+
# memcached service active

echo 'flush_all' | nc localhost 11211 | exit