import pytest
from mastermind.networksetup import *

def test_service_map():
    mock_service_order = """An asterisk (*) denotes that a network service is disabled.
(1) Bluetooth DUN
(Hardware Port: Bluetooth DUN, Device: Bluetooth-Modem)

(2) Thunderbolt Ethernet
(Hardware Port: Thunderbolt Ethernet, Device: en3)

(3) VPN (PPTP)
(Hardware Port: PPTP, Device: )

(4) Wi-Fi
(Hardware Port: Wi-Fi, Device: en0)

(5) AirCard 782S
(Hardware Port: AirCard 782S, Device: en5)

(6) Bluetooth PAN
(Hardware Port: Bluetooth PAN, Device: en4)

(7) Thunderbolt Bridge
(Hardware Port: Thunderbolt Bridge, Device: bridge0)

(8) VPN LDN
(Hardware Port: L2TP, Device: )

(9) VPN LDN 1
(Hardware Port: L2TP, Device: )

(10) frootvpn (us)
(Hardware Port: PPTP, Device: )"""

    assert service_map(mock_service_order) == [('Bluetooth DUN', 'Bluetooth-Modem'),
                                               ('Thunderbolt Ethernet', 'en3'),
                                               ('Wi-Fi', 'en0'),
                                               ('AirCard 782S', 'en5'),
                                               ('Bluetooth PAN', 'en4'),
                                               ('Thunderbolt Bridge', 'bridge0')]


def test_webproxy_record():
    mock_raw_record = """Enabled: No
Server: 127.0.0.1
Port: 8080
Authenticated Proxy Enabled: 0"""

    assert webproxy_record(mock_raw_record) == {'Authenticated Proxy Enabled': '0',
                                                'Enabled': 'No',
                                                'Port': '8080',
                                                'Server': '127.0.0.1'}

def test_is_proxy_enabled():
    mock_record_disabled = {'Authenticated Proxy Enabled': '0',
                            'Enabled': 'No',
                            'Port': '8080',
                            'Server': '127.0.0.1'}
    mock_record_enabled = {'Authenticated Proxy Enabled': '0',
                           'Enabled': 'Yes',
                           'Port': '8080',
                           'Server': '127.0.0.1'}
    assert is_proxy_enabled(mock_record_disabled) == False
    assert is_proxy_enabled(mock_record_enabled) == True
