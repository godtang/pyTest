# -*- coding: utf-8 -*-
# !/usr/bin/env python


import py_eureka_client.eureka_client as eureka_client

my_eureka_url = 'http://192.168.3.27:8500'

your_rest_server_port = 8080
# The flowing code will register your server to eureka server and also start to send heartbeat every 30 seconds
eureka_client.init(eureka_server=my_eureka_url,
                   app_name="your_app_name",
                   instance_port=your_rest_server_port)

