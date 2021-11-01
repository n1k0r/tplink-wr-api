from dataclasses import dataclass

from tplink_wr.parse.utils import extract_vars
from tplink_wr.router import RouterInterface

from .fetcher import Fetcher


@dataclass
class DHCPLeases(Fetcher):
    leases: list

    @classmethod
    def fetch(cls, router: RouterInterface):
        doc = router.page("AssignedIpAddrListRpm")
        dyn_para, dyn_list = extract_vars(doc, ["DHCPDynPara", "DHCPDynList"]).values()

        leases_count = dyn_para[0]
        params_per_lease = dyn_para[1]
        assert len(dyn_list) == leases_count * params_per_lease
        assert params_per_lease >= 4

        leases_raw = []
        for i in range(leases_count):
            base = i * params_per_lease

            expire = None
            expire_raw = dyn_list[base+3]
            if ":" in expire_raw:
                hours, minutes, seconds = [
                    int(part)
                    for part in expire_raw.split(":")
                ]
                expire = seconds + minutes * 60 + hours * 60 * 60

            leases_raw.append({
                "name": dyn_list[base],
                "mac": dyn_list[base+1],
                "ip": dyn_list[base+2],
                "expire": expire,
            })

        leases = cls(leases=leases_raw)
        return leases
