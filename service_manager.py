import asyncio
import signal

DNSMASQ_START = [
    "dnsmasq",
    "--keep-in-foreground",  # run in foreground
    "--log-facility=-",  # dump logs to stdout, not syslog
    "--log-queries",  # log DNS queries
]


class DnsServiceManager:
    def __init__(self, cmd=DNSMASQ_START):
        self.cmd = cmd
        self.process = None

    async def start(self):
        if self.process is not None:
            raise Exception("Can not start dnsmasq process: already running")
        self.process = await asyncio.create_subprocess_exec(*self.cmd)
        print(f"Successfully started dnsmasq (pid={self.process.pid})")

    async def stop(self):
        if self.process is None:
            print("Dnsmasq is not running, nothing to stop")
        self.process.send_signal(signal.SIGQUIT)
        await self.process.wait()
        self.process = None
        print("Successfully stopped dnsmasq")

    async def restart(self):
        await self.stop()
        await self.start()

    def refresh(self):
        if self.process is None:
            print("Dnsmasq is not running, nothing to refresh")
        self.process.send_signal(signal.SIGHUP)
        print("Successfully refreshed records table")
