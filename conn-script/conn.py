#!/usr/bin/env python3
import sys
import gi
import uuid
import socket
import threading
gi.require_version('NM', '1.0')
from gi.repository import NM

client = NM.Client.new(None)

def AddConnectionFinish(client, result, _data):
    threading.Thread(target=client.add_connection_finish, args=(result,), daemon=True).run()

def AddConnection():
    interface = "eth4242"
    dns = ["8.8.8.8"]
    print("Adding a new cell-modem connection...")
    conSettings = NM.SettingConnection.new()
    conSettings.set_property("id", "myidyyy")
    conSettings.set_property("interface_name", interface)
    conSettings.set_property("uuid", str(uuid.uuid4()))
    conSettings.set_property("type", "gsm")
    conSettings.set_property("metered", NM.Metered.YES)
    conSettings.set_property("interface_name", interface)
    gsmSettings = NM.SettingGsm.new()
    #gsmSettings.set_property("auto_config", True)
    #gsmSettings.set_property("apn", "internet")
    ip4Settings = NM.SettingIP4Config.new()
    ip4Settings.set_property(NM.SETTING_IP_CONFIG_METHOD, "auto")
    ip4Settings.add_address(NM.IPAddress.new(socket.AF_INET, "10.10.10.12", 24))
    for d in dns: ip4Settings.add_dns(d)
    ip6Settings = NM.SettingIP6Config.new()
    ip6Settings.set_property("method", "auto")
    connection = NM.SimpleConnection.new()
    connection.add_setting(conSettings)
    connection.add_setting(ip4Settings)
    connection.add_setting(ip6Settings)
    connection.add_setting(gsmSettings)
    print("Verifying connection parameters...")
    connection.verify()
    print("Saving connection...")
    client.add_connection_async(
        connection,
        False, # Make the connection persistent
        None,
        AddConnectionFinish,
        None
    )
    #self._connection = connection

AddConnection()
