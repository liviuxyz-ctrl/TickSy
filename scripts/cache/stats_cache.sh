#!/bin/bash
# ©2022 TickSy
# TickSy development memcached cache stats script
# Prerequisites
# Ubuntu 20.04+
# memcached service installed/active

/usr/share/memcached/scripts/memcached-tool localhost:11211 stats
