from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

from tplink_wr.parse.utils import extract_vars
from tplink_wr.router import RouterInterface

from .fetcher import Fetcher


class RouterType(IntEnum):
    WAN = 1
    WITH_3G = 2
    APC = 4
    PURE_3G = 16


class WLANType(IntEnum):
    UNKNOWN = 0
    B = 1
    G = 2
    N = 3
    BG_MIXED = 4
    GN_MIXED = 5
    BGN_MIXED = 6
    A = 7
    N_DUPL = 8
    AN_MIXED = 9


class WLANChannelWidth(IntEnum):
    UNKNOWN = 0
    MHZ_20 = 1
    AUTO = 2
    MHZ_40 = 3


class WDSStatus(IntEnum):
    INIT = 0
    SCAN = 1
    JOIN = 2
    AUTH = 3
    ASSOC = 4
    RUN = 5
    DISABLE = 6


class WANLinkStatus(IntEnum):
    UNKNOWN = 0
    DISABLED = 1
    TIMEOUT = 2
    LINK_DOWN = 3
    LINK_UP = 4


class WANType(IntEnum):
    UNKNOWN = 0
    DYNAMIC = 1
    STATIC = 2
    PPPOE = 3
    DYNAMIC_1X = 4
    STATIC_1X = 5
    BIGPOND = 6
    L2TP = 7
    PPTP = 8


@dataclass
class LANStatus:
    mac: str
    ip: str
    mask: str


@dataclass
class WLANStatus:
    enabled: bool
    name: str
    type: WLANType
    channel_manual: Optional[int]
    channel_auto: Optional[int]
    channel_width: WLANChannelWidth
    mac: str
    ip: str
    wds_status: WDSStatus


@dataclass
class WANStatus:
    link_status: WANLinkStatus
    mac: str
    ip: str
    type: WANType
    mask: str
    gateway: str
    dns: str


@dataclass
class GeneralStatus(Fetcher):
    wireless: bool
    uptime: int
    firmware: str
    hardware: str
    device_type: RouterType
    mode_3g: bool

    rx_bytes: int
    tx_bytes: int
    rx_packets: int
    tx_packets: int

    lan: LANStatus
    wlan: Optional[WLANStatus]
    wan: list[WANStatus]

    @classmethod
    def fetch(cls, router: RouterInterface):
        doc = router.page("StatusRpm")
        general, lan, wlan, statist, wan = extract_vars(doc, [
            "statusPara", "lanPara", "wlanPara", "statistList", "wanPara"
        ]).values()

        status = {
            **cls._parse_status(general),
            **cls._parse_statist(statist),
            "lan": cls._parse_lan(lan),
            "wlan": cls._parse_wlan(wlan, general),
            "wan": cls._parse_wan(wan, general),
        }

        status_obj = cls(**status)
        return status_obj

    @staticmethod
    def _parse_status(status) -> dict:
        return {
            "wireless": bool(status[0]),
            "uptime": status[4],
            "firmware": status[5],
            "hardware": status[6],
            "device_type": RouterType(status[7]),
            "mode_3g": bool(status[8]),
        }

    @staticmethod
    def _parse_statist(statist) -> dict:
        statist_parse = lambda value: int(value.replace(",", ""))
        return {
            "rx_bytes": statist_parse(statist[0]),
            "tx_bytes": statist_parse(statist[1]),
            "rx_packets": statist_parse(statist[2]),
            "tx_packets": statist_parse(statist[3]),
        }

    @staticmethod
    def _parse_lan(lan) -> LANStatus:
        return LANStatus(
            mac=lan[0],
            ip=lan[1],
            mask=lan[2],
        )

    @staticmethod
    def _parse_wlan(wlan, general) -> Optional[WLANStatus]:
        if not general[0]:
            return None

        return WLANStatus(
            enabled=bool(wlan[0]),
            name=wlan[1],
            type=WLANType(wlan[3]),
            channel_manual=None if wlan[2] == 15 else wlan[2],
            channel_width=WLANChannelWidth(wlan[6]),
            channel_auto=wlan[9],
            mac=wlan[4],
            ip=wlan[5],
            wds_status=WDSStatus(wlan[10]),
        )

    @staticmethod
    def _parse_wan(wan, general) -> list[WANStatus]:
        wan_count = general[1]
        wan_params_per_item = general[2]
        assert len(wan) == wan_count * wan_params_per_item
        assert wan_params_per_item >= 12

        result = []
        for i in range(wan_count):
            base = i * wan_params_per_item
            wan_status = WANStatus(
                link_status=WANLinkStatus(wan[base]),
                mac=wan[base+1],
                ip=wan[base+2],
                type=WANType(wan[base+3]),
                mask=wan[base+4],
                gateway=wan[base+7],
                dns=wan[base+11],
            )
            result.append(wan_status)

        return result
