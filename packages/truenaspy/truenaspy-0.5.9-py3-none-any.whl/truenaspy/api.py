"""TrueNAS API."""
from __future__ import annotations

from datetime import datetime, timedelta
from logging import getLogger
from typing import Any, Self

from aiohttp import ClientSession

from .auth import Auth
from .collects import (
    Alerts,
    Boot,
    Charts,
    CloudSync,
    Datasets,
    Disk,
    Interfaces,
    Jail,
    Job,
    Pool,
    Replication,
    Rsync,
    Service,
    Smart,
    Snapshottask,
    System,
    Update,
    VirtualMachine,
)
from .exceptions import TruenasError, TruenasNotFoundError
from .helper import (
    ExtendedDict,
    as_local,
    b2gib,
    search_attrs,
    systemstats_process,
    utc_from_timestamp,
)
from .subscription import Events, Subscriptions

_LOGGER = getLogger(__name__)


class TruenasClient(object):
    """Handle all communication with TrueNAS."""

    def __init__(
        self,
        host: str,
        token: str,
        session: ClientSession | None = None,
        use_ssl: bool = False,
        verify_ssl: bool = True,
        scan_intervall: int = 60,
        timeout: int = 300,
    ) -> None:
        """Initialize the TrueNAS API."""
        self._access = Auth(host, token, use_ssl, verify_ssl, timeout, session)
        self._is_scale: bool = False
        self._is_virtual: bool = False
        self._sub = Subscriptions(
            (self.async_update, self.async_is_alive), scan_intervall
        )
        self.is_connected: bool = False
        self._systemstats_errored: list[str] = []
        self.query = self._access.async_request
        self.alerts: list[dict[str, Any]] = []
        self.charts: list[dict[str, Any]] = []
        self.cloudsync: list[dict[str, Any]] = []
        self.datasets: list[dict[str, Any]] = []
        self.disks: list[dict[str, Any]] = []
        self.interfaces: list[dict[str, Any]] = []
        self.jails: list[dict[str, Any]] = []
        self.pools: list[dict[str, Any]] = []
        self.replications: list[dict[str, Any]] = []
        self.rsynctasks: list[dict[str, Any]] = []
        self.services: list[dict[str, Any]] = []
        self.smartdisks: list[dict[str, Any]] = []
        self.snapshots: list[dict[str, Any]] = []
        self.stats: dict[str, Any] = {}
        self.system_infos: dict[str, Any] = {}
        self.update_infos: dict[str, Any] = {}
        self.virtualmachines: list[dict[str, Any]] = []

    async def async_get_system(self) -> dict[str, Any]:
        """Get system info from TrueNAS."""
        response = await self.query(path="system/info")
        self.system_infos = search_attrs(System, response)

        response = await self.query(path="system/version_short")
        self.system_infos.update({"short_version": response})

        response = await self.query(path="system/is_freenas")
        self._is_scale = response is False
        self._is_virtual = self.system_infos["system_manufacturer"] in [
            "QEMU",
            "VMware, Inc.",
        ] or self.system_infos["system_product"] in ["VirtualBox"]

        if (uptime := self.system_infos["uptime_seconds"]) > 0:
            now = datetime.now().replace(microsecond=0)
            uptime_tm = datetime.timestamp(now - timedelta(seconds=int(uptime)))
            self.system_infos.update(
                {
                    "uptimeEpoch": str(
                        as_local(utc_from_timestamp(uptime_tm)).isoformat()
                    )
                }
            )

        # Get stats.
        query = [
            {"name": "load"},
            {"name": "cpu"},
            {"name": "arcsize"},
            {"name": "arcrate"},
            {"name": "memory"},
        ]

        if not self._is_virtual:
            query.append({"name": "cputemp"})

        stats: list[dict[str, Any]] = await self.async_get_stats(query)
        for item in stats:
            # CPU temperature
            if item.get("name") == "cputemp" and "aggregations" in item:
                self.system_infos["cpu_temperature"] = round(
                    max(item["aggregations"]["mean"].values()), 1
                )

            # CPU load
            if item.get("name") == "load":
                tmp_arr = ["load_shortterm", "load_midterm", "load_longterm"]
                systemstats_process(self.system_infos, tmp_arr, item, "")

            # CPU usage
            if item.get("name") == "cpu":
                tmp_arr = ["interrupt", "system", "user", "nice", "idle"]
                systemstats_process(self.system_infos, tmp_arr, item, "cpu")
                self.system_infos["cpu_usage"] = round(
                    self.system_infos["cpu_system"] + self.system_infos["cpu_user"], 2
                )

            # arcratio
            if item.get("name") == "memory":
                tmp_arr = ["used", "free", "cached", "buffers"]
                systemstats_process(self.system_infos, tmp_arr, item, "memory")
                self.system_infos["memory_total_value"] = round(
                    self.system_infos["memory_used"]
                    + self.system_infos["memory_free"]
                    + self.system_infos["memory_arc_size"],
                    2,
                )
                if (total_value := self.system_infos["memory_total_value"]) > 0:
                    self.system_infos["memory_usage_percent"] = round(
                        100
                        * (float(total_value) - float(self.system_infos["memory_free"]))
                        / float(total_value),
                        0,
                    )

            # arcsize
            if item.get("name") == "arcsize":
                tmp_arr = ["arc_size"]
                systemstats_process(self.system_infos, tmp_arr, item, "memory")

            # arcratio
            if item.get("name") == "arcrate":
                tmp_arr = ["hits", "misses"]
                systemstats_process(self.system_infos, tmp_arr, item, "")

        self._sub.notify(Events.SYSTEM.value)
        return self.system_infos

    async def async_get_interfaces(self) -> list[dict[str, Any]]:
        """Get interface info from TrueNAS."""
        response = await self.query(path="interface")
        self.interfaces = search_attrs(Interfaces, response)

        # Get stats
        query = [
            {"name": "interface", "identifier": interface["id"]}
            for interface in self.interfaces
        ]
        stats = await self.async_get_stats(query)
        for interface in self.interfaces:
            for item in stats:
                # Interface
                if (
                    item.get("name") == "interface"
                    and item["identifier"] == interface["id"]
                ):
                    # 12->13 API change
                    item["legend"] = [
                        legend.replace("if_octets_", "") for legend in item["legend"]
                    ]
                    systemstats_process(interface, ["received", "sent"], item, "rx-tx")

        self._sub.notify(Events.INTERFACES.value)
        return self.interfaces

    async def async_get_stats(self, items: list[dict[str, Any]]) -> Any:
        """Get statistics."""
        now = datetime.now()
        start = int((now - timedelta(seconds=90)).timestamp())
        end = int((now - timedelta(seconds=30)).timestamp())
        query: dict[str, Any] = {
            "graphs": items,
            "reporting_query": {"start": start, "end": end, "aggregate": True},
        }

        for param in query["graphs"]:
            if param["name"] in self._systemstats_errored:
                query["graphs"].remove(param)

        stats = []
        try:
            stats = await self._access.async_request(
                "reporting/get_data", method="post", json=query
            )

            if "error" in stats:
                for param in query["graphs"]:
                    await self._access.async_request(
                        "reporting/get_data",
                        method="post",
                        json={
                            "graphs": [param],
                            "reporting_query": {
                                "start": start,
                                "end": end,
                                "aggregate": True,
                            },
                        },
                    )
                    if "error" in stats:
                        self._systemstats_errored.append(param["name"])

                _LOGGER.warning(
                    "Fetching following graphs failed, check your NAS: %s",
                    self._systemstats_errored,
                )
                await self.async_get_stats(items)
        except TruenasError as error:
            # ERROR FIX: Cobia NAS-123862
            if self.system_infos.get("short_version") not in [
                "23.10.0",
                "23.10.0.0",
                "23.10.0.1",
            ]:
                _LOGGER.error(error)

        return stats

    async def async_get_services(self) -> list[dict[str, Any]]:
        """Get service info from TrueNAS."""
        response = await self.query(path="service")
        self.services = search_attrs(Service, response)
        self._sub.notify(Events.SERVICES.value)
        return self.services

    async def async_get_pools(self) -> list[dict[str, Any]]:
        """Get pools from TrueNAS."""
        response = await self.query(path="pool")
        self.pools = search_attrs(Pool, response)

        try:
            response = await self.query(path="boot/get_state")
        except TruenasError as error:
            _LOGGER.debug(error)
            response = ExtendedDict()

        boot = search_attrs(Boot, response)
        self.pools.append(boot)

        # Process pools
        dataset_available = {}
        dataset_total = {}
        for dataset in self.datasets:
            if mountpoint := dataset.get("mountpoint"):
                available = dataset.get("available", 0)
                dataset_available[mountpoint] = b2gib(available)
                dataset_total[mountpoint] = b2gib(available + dataset.get("used", 0))

        for pool in self.pools:
            if value := dataset_available.get(pool["path"]):
                pool.update({"available_gib": value})

            if value := dataset_total.get(pool["path"]):
                pool.update({"total_gib": value})

            if pool["name"] in ["boot-pool", "freenas-boot"]:
                pool.update({"available_gib": b2gib(pool["root_dataset_available"])})
                pool.update(
                    {
                        "total_gib": b2gib(
                            pool["root_dataset_available"] + pool["root_dataset_used"]
                        )
                    }
                )
                # self.pools[uid].pop("root_dataset")

        self._sub.notify(Events.POOLS.value)
        return self.pools

    async def async_get_datasets(self) -> list[dict[str, Any]]:
        """Get datasets from TrueNAS."""
        # response = await self.query(path="pool/dataset/details")
        response = await self.query(path="pool/dataset")
        self.datasets = search_attrs(Datasets, response)
        self._sub.notify(Events.DATASETS.value)
        return self.datasets

    async def async_get_disks(self) -> list[dict[str, Any]]:
        """Get disks from TrueNAS."""
        response = await self.query(path="disk")
        self.disks = search_attrs(Disk, response)
        # Get disk temperatures
        temperatures = await self._access.async_request(
            "disk/temperatures", method="post", json={"names": []}
        )
        for disk in self.disks:
            disk.update({"temperature": temperatures.get(disk["name"], 0)})
        self._sub.notify(Events.DISKS.value)
        return self.disks

    async def async_get_jails(self) -> list[dict[str, Any]] | None:
        """Get jails from TrueNAS."""
        if self._is_scale is False:
            try:
                response = await self.query(path="jail")
                self.jails = search_attrs(Jail, response)
            except TruenasNotFoundError as error:
                _LOGGER.warning(error)
                self.jails = []
        self._sub.notify(Events.JAILS.value)
        return self.jails

    async def async_get_virtualmachines(self) -> list[dict[str, Any]]:
        """Get VMs from TrueNAS."""
        response = await self.query(path="vm")
        self.virtualmachines = search_attrs(VirtualMachine, response)
        self._sub.notify(Events.VMS.value)
        return self.virtualmachines

    async def async_get_cloudsync(self) -> list[dict[str, Any]]:
        """Get cloudsync from TrueNAS."""
        response = await self.query(path="cloudsync")
        self.cloudsync = search_attrs(CloudSync, response)
        self._sub.notify(Events.CLOUD.value)
        return self.cloudsync

    async def async_get_replications(self) -> list[dict[str, Any]]:
        """Get replication from TrueNAS."""
        response = await self.query(path="replication")
        self.replications = search_attrs(Replication, response)
        self._sub.notify(Events.REPLS.value)
        return self.replications

    async def async_get_snapshottasks(self) -> list[dict[str, Any]]:
        """Get replication from TrueNAS."""
        response = await self.query(path="pool/snapshottask")
        self.snapshots = search_attrs(Snapshottask, response)
        self._sub.notify(Events.SNAPS.value)
        return self.snapshots

    async def async_get_charts(self) -> list[dict[str, Any]]:
        """Get Charts from TrueNAS."""
        response = await self.query(path="chart/release")
        self.charts = search_attrs(Charts, response)
        self._sub.notify(Events.CHARTS.value)
        return self.charts

    async def async_get_smartdisks(self) -> list[dict[str, Any]]:
        """Get smartdisk from TrueNAS."""
        response = await self.query(path="smart/test/results", params={"offset": 1})
        self.smartdisks = search_attrs(Smart, response)
        self._sub.notify(Events.SMARTS.value)
        return self.smartdisks

    async def async_get_alerts(self) -> list[dict[str, Any]]:
        """Get smartdisk from TrueNAS."""
        response = await self.query(path="alert/list")
        self.alerts = search_attrs(Alerts, response)
        self._sub.notify(Events.ALERTS.value)
        return self.alerts

    async def async_get_rsynctasks(self) -> list[dict[str, Any]]:
        """Get smartdisk from TrueNAS."""
        response = await self.query(path="rsynctask")
        self.rsynctasks = search_attrs(Rsync, response)
        self._sub.notify(Events.RSYNC.value)
        return self.rsynctasks

    async def async_get_update(self) -> dict[str, Any]:
        """Get update info from TrueNAS."""
        try:
            response = await self.query(path="update/check_available", method="post")
        except TruenasError as error:
            _LOGGER.debug(error)
            response = ExtendedDict()
        self.update_infos = search_attrs(Update, response)

        try:
            response = await self.query(path="update/get_trains")
        except TruenasError as error:
            _LOGGER.debug(error)
            response = ExtendedDict()
        self.update_infos.update({"current_train": response.get("current")})

        if jobid := self.system_infos.get("job_id", 0):
            response = await self.query(path="core/get_jobs", params={"id": jobid})
            jobs = search_attrs(Job, response)
            for job in jobs:
                if (
                    job.get("state") != "RUNNING"
                    or not self.update_infos["update_available"]
                ):
                    self.update_infos.update(
                        {"progress": 0, "status": None, "job_id": 0}
                    )
        return self.update_infos

    async def async_is_alive(self) -> bool:
        """Check connection."""
        result = await self._access.async_request("core/ping")
        return "pong" in result

    def subscribe(self, _callback: str, *args: Any) -> None:
        """Subscribe event."""
        self._sub.subscribe(_callback, *args)

    def unsubscribe(self, _callback: str, *args: Any) -> None:
        """Unsubscribe event."""
        self._sub.subscribe(_callback, *args)

    async def async_update(self) -> None:
        """Update all datas."""
        try:
            await self.async_is_alive()
            nb_events = len(Events)
            nb_errors = 0
            for event in Events:
                try:
                    fnc = getattr(self, f"async_get_{event.value}")
                    await fnc()
                except TruenasError as error:
                    _LOGGER.error(error)
                    nb_errors += 1
            self.is_connected = (
                False if nb_errors > 0 and nb_events == nb_errors else True
            )
        except TruenasError as error:
            _LOGGER.error(error)
            self.is_connected = False

    async def async_close(self) -> None:
        """Close open client session."""
        await self._access.async_close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The LaMetricCloud object.
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.async_close()
