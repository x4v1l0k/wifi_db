import os
# import sqlite3
import unittest
# from database_utils import *
from utils import database_utils
from utils import oui
from utils import update
from utils import wifi_db_aircrack
import wifi_db
from unittest.mock import patch, MagicMock
import json


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        self.database_name = 'test_database.db'
        self.database = database_utils.connectDatabase(self.database_name,
                                                       self.verbose)
        database_utils.createDatabase(self.database, self.verbose)
        database_utils.createViews(self.database, self.verbose)
        self.c = self.database.cursor()
        self.bssid = "00:11:22:33:44:55"
        self.mac = "55:44:33:22:11:00"
        self.test_database_name = 'test_database.db'
        self.test_database_conn = None

    def tearDown(self):
        self.database.close()
        os.remove(self.database_name)
        if self.test_database_conn:
            self.test_database_conn.close()
        if os.path.exists(self.test_database_name):
            os.remove(self.test_database_name)

    def test_connectDatabase(self):
        self.assertIsNotNone(self.database)

    def test_createDatabase(self):
        self.test_database_conn = database_utils.connectDatabase(self.test_database_name, False)
        database_utils.createDatabase(self.test_database_conn, self.verbose)
        cursor = self.test_database_conn.cursor()
        # Verify that the tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        expected_tables = [('AP',), ('Client',), ('SeenClient',), ('Connected',), ('WPS',), ('SeenAp',), ('Probe',), ('Handshake',), ('Identity',), ('Files',)]  # Replace with actual expected tables
        self.assertEqual(tables, expected_tables)

    def test_createViews(self):
        self.test_database_conn = database_utils.connectDatabase(self.test_database_name, False)
        database_utils.createDatabase(self.test_database_conn, False)  # Create tables first
        database_utils.createViews(self.test_database_conn, self.verbose)
        cursor = self.test_database_conn.cursor()
        # Verify that the views were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
        views = cursor.fetchall()
        expected_views = [('ProbeClients',), ('ConnectedAP',), ('ProbeClientsConnected',), ('HandshakeAP',), ('HandshakeAPUnique',), ('IdentityAP',), ('SummaryAP',)]  # Replace with actual expected views
        self.assertEqual(views, expected_views)

    def test_insertAP(self):
        essid = "Test_AP"
        manuf = "Test_Manufacturer"
        channel = "6"
        freqmhz = "2437"
        carrier = "test"
        encryption = "WPA2"
        packets_total = "10"
        lat = "37.7749"
        lon = "-122.4194"
        cloaked = 'False'
        mfpc = 'False'
        mfpr = 'False'
        # Insert new AP
        result = database_utils.insertAP(self.c, self.verbose, self.bssid,
                                         essid, manuf, channel, freqmhz,
                                         carrier, encryption, packets_total,
                                         lat, lon, cloaked, mfpc, mfpr, 0)

        self.assertEqual(result, 0)
        # TODO  Insert existing AP with new values
        # manuf = "Updated_Manufacturer"
        # result = insertAP(self.c, False, bssid, essid, manuf, channel,
        #                   freqmhz, carrier,
        # encryption, packets_total, lat, lon, cloaked)
        # self.assertEqual(result, 0)
        # self.c.execute("SELECT * FROM AP WHERE bssid=?", (bssid,))
        # rows = self.c.fetchall()
        # self.assertEqual(len(rows), 1)
        # self.assertEqual(rows[0][3], "Updated_Manufacturer")

    def test_insertClients(self):
        ssid = "Test_AP"
        manuf = "Test_Manufacturer"
        packets_total = "10"
        power = "-70"
        # Insert new client
        result = database_utils.insertClients(self.c, self.verbose, self.mac,
                                              ssid, manuf, packets_total,
                                              power, "Misc", 0)

        self.assertEqual(result, 0)
        # TODO Insert existing client with new values
        # manuf = "Updated_Manufacturer"
        # result = insertClients(self.c, False, mac, ssid, manuf,
        #                        packets_total, power, "Misc")
        # self.assertEqual(result, 0)
        # self.c.execute("SELECT * FROM CLIENT WHERE mac=?", (mac,))
        # rows = self.c.fetchall()
        # self.assertEqual(len(rows), 1)
        # self.assertEqual(rows[0][2], "Updated_Manufacturer")

    def test_insertWPS(self):
        # Define WPS parameters
        wlan_ssid = "Test_SSID"
        wps_version = "1.0"
        wps_device_name = "Test_Device"
        wps_model_name = "Test_Model"
        wps_model_number = "12345"
        wps_config_methods = "1234"
        wps_config_methods_keypad = True

        # Insert new WPS
        result = database_utils.insertWPS(self.c, self.verbose, self.bssid,
                                          wlan_ssid, wps_version,
                                          wps_device_name, wps_model_name,
                                          wps_model_number,
                                          wps_config_methods,
                                          wps_config_methods_keypad)
        self.assertEqual(result, 0)

        # TODO Insert existing WPS with new values
        # wps_device_name = "Updated_Device"
        # result = insertWPS(self.c, self.verbose, bssid, wlan_ssid,
        # wps_version,
        # wps_device_name, wps_model_name, wps_model_number,
        # wps_config_methods, wps_config_methods_keypad)
        # self.assertEqual(result, 0)
        # self.c.execute("SELECT * FROM WPS WHERE wlan_ssid=?", (wlan_ssid,))
        # rows = self.c.fetchall()
        # self.assertEqual(len(rows), 1)
        # self.assertEqual(rows[0][3], "Updated_Device")

    def test_insertConnected(self):
        # add needed data
        essid = "Test_AP"
        manuf = "Test_Manufacturer"
        channel = "6"
        freqmhz = "2437"
        carrier = "test"
        encryption = "WPA2"
        packets_total = "10"
        lat = "37.7749"
        lon = "-122.4194"
        cloaked = False
        mfpc = 'False'
        mfpr = 'False'
        # Insert new AP
        result = database_utils.insertAP(self.c, self.verbose, self.bssid,
                                         essid, manuf, channel, freqmhz,
                                         carrier, encryption, packets_total,
                                         lat, lon, cloaked, mfpc, mfpr, 0)

        self.assertEqual(result, 0)

        ssid = ""
        manuf = "Test_Manufacturer"
        packets_total = "10"
        power = "-70"
        # Insert new client
        result = database_utils.insertClients(self.c, self.verbose, self.mac,
                                              ssid, manuf, packets_total,
                                              power, "Misc", 0)

        self.assertEqual(result, 0)

        # Insert new connected device
        result = database_utils.insertConnected(self.c, self.verbose,
                                                self.bssid, self.mac)
        self.assertEqual(result, 0)

    def test_inserFile(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        path = script_path+"/README.md"

        result = database_utils.insertFile(self.c, self.verbose, path)
        self.assertEqual(result, 0)

    def test_insertHandshake(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        path = script_path+"/README.md"

        result = database_utils.insertHandshake(self.c, self.verbose,
                                                self.bssid, self.mac, path)
        self.assertEqual(result, 0)

        self.c.execute("SELECT * FROM handshake WHERE bssid=?", (self.bssid,))
        rows = self.c.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][2], path)

    def test_insertIdentity(self):
        identity = "DOMAIN\\username"
        method = "EAP-PEAP"
        result = database_utils.insertIdentity(self.c, self.verbose,
                                               self.bssid, self.mac, identity,
                                               method)
        self.assertEqual(result, 0)
        self.c.execute("SELECT identity FROM Identity WHERE mac=?",
                       (self.mac,))
        row = self.c.fetchone()
        self.assertEqual(row[0], identity)

    def test_insertSeenClient(self):
        # add needed data
        ssid = ""
        manuf = "Test_Manufacturer"
        packets_total = "10"
        power = "-70"
        # Insert new client
        result = database_utils.insertClients(self.c, self.verbose, self.mac,
                                              ssid, manuf, packets_total,
                                              power, "Misc", 0)

        # Insert seenClient
        # station = "Test_Station"
        time = "2022-02-23 10:00:00"
        tool = "aircrack-ng"
        power = -50
        lat = "37.7749"
        lon = "-122.4194"
        alt = "10000"
        result = database_utils.insertSeenClient(self.c, self.verbose,
                                                 self.mac, time, tool, power,
                                                 lat, lon, alt)
        self.assertEqual(result, 0)
        self.c.execute("SELECT * FROM SeenClient WHERE mac=?", (self.mac,))
        row = self.c.fetchone()
        self.assertEqual(row[1], time)
        self.assertEqual(row[2], tool)
        self.assertEqual(row[3], power)

    def test_insertSeenAP(self):
        # add needed data
        essid = "Test_AP"
        manuf = "Test_Manufacturer"
        channel = "6"
        freqmhz = "2437"
        carrier = "test"
        encryption = "WPA2"
        packets_total = "10"
        lat = "37.7749"
        lon = "-122.4194"
        cloaked = False
        mfpc = 'False'
        mfpr = 'False'
        # Insert new AP
        result = database_utils.insertAP(self.c, self.verbose, self.bssid,
                                         essid, manuf, channel, freqmhz,
                                         carrier, encryption, packets_total,
                                         lat, lon, cloaked, mfpc, mfpr, 0)

        self.assertEqual(result, 0)

        # Insert SeenAP
        time = "2032-02-23 10:00:00"
        tool = "aircrack-ng"
        signal_rsi = "-70"
        lat = "37.7749"
        lon = "-122.4194"
        alt = "10000"
        bsstimestamp = "2032-02-23 10:00:00"
        result = database_utils.insertSeenAP(self.c, self.verbose, self.bssid,
                                             time, tool, signal_rsi, lat, lon,
                                             alt, bsstimestamp)
        self.assertEqual(result, 0)
        self.c.execute("SELECT * FROM SeenAP WHERE bssid=?", (self.bssid,))
        row = self.c.fetchone()
        self.assertEqual(row[1], time)
        self.assertEqual(row[2], tool)

    def test_setHashcat(self):
        # add needed data
        essid = "Test_AP"
        manuf = "Test_Manufacturer"
        channel = "6"
        freqmhz = "2437"
        carrier = "test"
        encryption = "WPA2"
        packets_total = "10"
        lat = "37.7749"
        lon = "-122.4194"
        cloaked = False
        mfpc = 'False'
        mfpr = 'False'
        # Insert new AP
        result = database_utils.insertAP(self.c, self.verbose, self.bssid,
                                         essid, manuf, channel, freqmhz,
                                         carrier, encryption, packets_total,
                                         lat, lon, cloaked, mfpc, mfpr, 0)

        self.assertEqual(result, 0)

        ssid = ""
        manuf = "Test_Manufacturer"
        packets_total = "10"
        power = "-70"
        # Insert new client
        result = database_utils.insertClients(self.c, self.verbose, self.mac,
                                              ssid, manuf, packets_total,
                                              power, "Misc", 0)

        self.assertEqual(result, 0)

        # insert Handshake
        script_path = os.path.dirname(os.path.abspath(__file__))
        path = script_path+"/README.md"

        result = database_utils.insertHandshake(self.c, self.verbose,
                                                self.bssid, self.mac, path)
        self.assertEqual(result, 0)

        # Insert hashcat HASH
        script_path = os.path.dirname(os.path.abspath(__file__))
        path = script_path+"/README.md"
        test_hashcat = "aa:bb:cc:dd:ee:ff:11:22:33:44:55:66:77"
        result = database_utils.setHashcat(self.c, self.verbose, self.bssid,
                                           self.mac, path, test_hashcat)
        self.assertEqual(result, 0)
        self.c.execute("SELECT * FROM handshake WHERE bssid=?", (self.bssid,))
        rows = self.c.fetchall()
        self.assertEqual(rows[0][2], path)

    def test_obfuscateDB(self):
        # add needed data
        essid = "Test_AP"
        manufAP = "Test_Manufacturer_AP"
        channel = "6"
        freqmhz = "2437"
        carrier = "test"
        encryption = "WPA2"
        packets_total = "10"
        lat = "37.7749"
        lon = "-122.4194"
        cloaked = False
        mfpc = 'False'
        mfpr = 'False'
        # Insert new AP
        result = database_utils.insertAP(self.c, self.verbose, self.bssid,
                                         essid, manufAP, channel, freqmhz,
                                         carrier, encryption, packets_total,
                                         lat, lon, cloaked, mfpc, mfpr, 0)

        self.assertEqual(result, 0)

        ssid = "null_ssid"
        manufClient = "Test_Manufacturer_Client"
        packets_total = "10"
        power = "-70"
        # Insert new client
        result = database_utils.insertClients(self.c, self.verbose, self.mac,
                                              ssid, manufClient, packets_total,
                                              power, "Misc", 0)

        self.assertEqual(result, 0)

        # insert Handshake
        script_path = os.path.dirname(os.path.abspath(__file__))
        path = script_path+"/README.md"

        result = database_utils.insertHandshake(self.c, self.verbose,
                                                self.bssid, self.mac, path)
        self.assertEqual(result, 0)

        # obfuscateDB
        result = database_utils.obfuscateDB(self.database, self.verbose)
        self.assertEqual(result, 0)

        # self.c.execute("SELECT * FROM handshake WHERE bssid=?",
        #                (self.bssid,))
        self.c.execute("SELECT * FROM AP WHERE ssid=?", (essid,))
        rows = self.c.fetchall()
        # Same ESSID but different BSSID
        self.assertEqual(rows[0][1], essid)
        self.assertEqual(rows[0][3], manufAP)
        self.assertEqual(rows[0][4], int(channel))
        self.assertNotEqual(rows[0][0], self.bssid)

        self.c.execute("SELECT * FROM CLIENT WHERE ssid=?", (ssid,))
        rows = self.c.fetchall()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], ssid)
        self.assertEqual(rows[0][2], manufClient)
        self.assertEqual(rows[0][3], packets_total)


class MyModuleTestCase(unittest.TestCase):

    def test_load_vendors(self):
        ouiAux = oui.load_vendors()
        vendor = oui.get_vendor(ouiAux, '00:00:00:00:00:01')
        self.assertEqual(vendor, 'XEROX CORPORATION')

    def test_get_vendor(self):
        ouiAux = {'000000': 'company1',
                  'FFFFFF': 'company2'}
        vendor = oui.get_vendor(ouiAux, '00:00:00:00:00:01')
        self.assertEqual(vendor, 'company1')


if __name__ == '__main__':
    unittest.main()
