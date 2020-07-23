# -*- coding: utf-8 -*-
# !/usr/bin/env python


import consul

c = consul.Consul(host='192.168.3.27', port=8500, scheme='http')
c.agent.service.register(
            "test-tmj",
            "test-tmj",
            "192.168.3.80",
            18888,
            ["aaa","bbbb"],
            check=consul.Check().tcp("192.168.3.80", 18888, "5s", "30s", "30s"))
data = c.catalog.service('lxpay-gateway')
for value in data[1]:
    print("accountSrv addr: " + value['ServiceAddress'], value['ServicePort'])
