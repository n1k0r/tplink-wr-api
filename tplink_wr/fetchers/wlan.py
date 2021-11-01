from dataclasses import dataclass

from tplink_wr.parse.utils import extract_vars
from tplink_wr.router import RouterInterface

from .fetcher import Fetcher


@dataclass
class WLANStats(Fetcher):
    ssid: list[str]
    mac_filter_enabled: bool
    mac_filter_whitelist: bool
    clients: list

    @classmethod
    def fetch(cls, router: RouterInterface):
        last = stats_raw = cls._load_page(router, 1)

        while not last["last_page"]:
            last = cls._load_page(router, last["page_num"]+1)
            stats_raw["clients"] += last["clients"]

        stats = cls(
            ssid=[
                str(ssid)
                for ssid in stats_raw["ssid"]
            ],
            mac_filter_enabled=bool(
                stats_raw["mac_filter_enabled"]
            ),
            mac_filter_whitelist=bool(
                stats_raw["mac_filter_whitelist"]
            ),
            clients=stats_raw["clients"],
        )
        return stats

    @staticmethod
    def _load_page(router: RouterInterface, page: int) -> dict:
        doc = router.page("WlanStationRpm", params={"Page": page})
        wlan_para, host_list, ssid_list = extract_vars(doc, [
            "wlanHostPara", "hostList", "ssidList"
        ]).values()

        clients_count = wlan_para[0]
        limit_per_page = wlan_para[2]
        params_per_client = wlan_para[4]

        stats = {
            "page_num": page,
            "last_page": False,

            "ssid": ssid_list,
            "mac_filter_enabled": wlan_para[5],
            "mac_filter_whitelist": wlan_para[6],
            "clients_count": clients_count,
            "clients": [],
        }

        clients_left = clients_count - (page - 1) * limit_per_page
        this_page_count = min(clients_left, limit_per_page)
        for i in range(this_page_count):
            base = i * params_per_client
            stats["clients"].append({
                "mac": host_list[base],
                "rx": host_list[base + 2],
                "tx": host_list[base + 3],
            })

        if clients_left <= limit_per_page:
            stats["last_page"] = True

        return stats
