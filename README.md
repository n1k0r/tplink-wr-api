# tplink-wr-api

[![Package Version](https://img.shields.io/pypi/v/tplink-wr-api?style=flat-square)](https://pypi.org/project/tplink-wr-api/)
[![Python Version](https://img.shields.io/pypi/pyversions/tplink-wr-api?style=flat-square)](https://pypi.org/project/tplink-wr-api/)
[![License](https://img.shields.io/github/license/n1k0r/tplink-wr-api?style=flat-square)](https://github.com/n1k0r/tplink-wr-api/blob/master/LICENSE)

Python API to some budget TP-Link routers.

## Supported devices

This library designed for budget models with firmware without API. Library interacts with router management interface like user (scrape HTML UI) so it may not work with others versions of firmware.

Tested with TL-WR840N v2 with firmware version 3.16.9.

## Features

Currently only read operations are available:

* general status info
* WLAN clients
* DHCP leases

## Usage

```python
>>> from tplink_wr import RouterSession, fetchers
>>>
>>> rt = RouterSession("192.168.0.1", "admin", "admin")
>>>
>>> general = fetchers.status.GeneralStatus.fetch(rt)
>>> print(general.lan)
LANStatus(mac='12-34-56-78-90-AB', ip='192.168.0.1', mask='255.255.255.0')
>>> stats = fetchers.wlan.WLANStats.fetch(rt)
>>> leases = fetchers.dhcp.DHCPLeases.fetch(rt)
>>>
>>> import pprint
>>> pp = pprint.PrettyPrinter(indent=2)
>>> pp.pprint(general.dict())
{ 'device_type': <RouterType.WAN: 1>,
  'firmware': '3.16.9 Build 150929 Rel.37860n ',
  'hardware': 'WR840N v2 00000000',
  'lan': { 'ip': '192.168.0.1',
           'mac': '12-34-56-78-90-AB',
           'mask': '255.255.255.0'},
  'mode_3g': False,
  'rx_bytes': 3330853277,
  'rx_packets': 8909427,
  'tx_bytes': 550131568,
  'tx_packets': 2593047,
  'uptime': 99788,
  'wan': [ { 'dns': '1.2.3.0 , 1.2.3.1',
             'gateway': '1.2.10.1',
             'ip': '1.2.10.15',
             'link_status': <WANLinkStatus.LINK_UP: 4>,
             'mac': '12-34-56-78-90-AC',
             'mask': '255.255.224.0',
             'type': <WANType.DYNAMIC: 1>}],
  'wireless': True,
  'wlan': { 'channel_auto': 6,
            'channel_manual': None,
            'channel_width': <WLANChannelWidth.AUTO: 2>,
            'enabled': True,
            'ip': '192.168.0.1',
            'mac': '12-34-56-78-90-AB',
            'name': 'TP-LINK_90AB',
            'type': <WLANType.BGN_MIXED: 6>,
            'wds_status': <WDSStatus.DISABLE: 6>}}
>>> pp.pprint(stats.dict())
{ 'clients': [ {'mac': '81-69-01-93-77-49', 'rx': 341, 'tx': 217},
               {'mac': 'C4-49-F0-84-00-52', 'rx': 179, 'tx': 90}],
  'mac_filter_enabled': False,
  'mac_filter_whitelist': False,
  'ssid': ['TP-LINK_90AB']}
>>> pp.pprint(leases.dict())
{ 'leases': [ { 'expire': 6701,
                'ip': '192.168.0.110',
                'mac': '65-CD-44-29-F2-0A',
                'name': 'DESKTOP-ABCDEFG'},
              { 'expire': 6973,
                'ip': '192.168.0.100',
                'mac': '81-69-01-93-77-49',
                'name': 'OnePlus-9R'},
              { 'expire': 7186,
                'ip': '192.168.0.102',
                'mac': 'C4-49-F0-84-00-52',
                'name': 'arch'}]}
```
