#!/usr/bin/env python3
from tplink_wr import fetchers, RouterSession

rt = RouterSession("192.168.0.1", "admin", "admin")

general = fetchers.status.GeneralStatus.fetch(rt)
print(general.lan)

stats = fetchers.wlan.WLANStats.fetch(rt)
leases = fetchers.dhcp.DHCPLeases.fetch(rt)

import pprint
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(general.dict())
pp.pprint(stats.dict())
pp.pprint(leases.dict())
