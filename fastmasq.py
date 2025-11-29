from config_manager import ConfigManager
from service_manager import DnsServiceManager

from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import click

import json
import asyncio
from typing import List, Annotated

app = FastAPI(title="Dnsmasq management API")
# config_manager = ConfigManager("/etc/hosts.dnsmasq", "/etc/fastmasq.json")
config_manager = ConfigManager("/tmp/hosts.dnsmasq", "/tmp/fastmasq.json")
service_manager = DnsServiceManager()


class DnsRecord(BaseModel):
    domain: str
    record: str


class DomainName(BaseModel):
    domain: str


class AddRecordRequest(DnsRecord):
    pass


class GetRecordRequest(DomainName):
    pass


class RemoveRecordRequest(DomainName):
    pass


class ActionStatusResponse(BaseModel):
    success: bool


@app.post("/get", response_model=DnsRecord)
async def get_record(req: DomainName):
    """
    Get record with specified domain
    """
    try:
        record = config_manager.get_record(req.domain)
        return DnsRecord(domain=req.domain, record=record)
    except:
        return DnsRecord(domain=req.domain, record="")


@app.post("/list", response_model=List[DnsRecord])
async def list_records():
    """
    List all records
    """
    records = []
    for domain, record in config_manager.read_records().items():
        records += [DnsRecord(domain=domain, record=record)]
    return records


@app.post("/set", response_model=DnsRecord)
async def set_record(record: DnsRecord):
    """
    Set record
    """
    config_manager.set_record(record.domain, record.record)
    service_manager.refresh()
    return await get_record(DomainName(domain=record.domain))


@app.post("/del")
async def del_record(req: DomainName):
    """
    Delete record by domain
    """
    config_manager.delete_record(req.domain)
    service_manager.refresh()


@app.post("/config")
async def get_config_file():
    """
    Get native config (can be used in pair with `upload_config`)
    """
    return FileResponse(path=config_manager.jsdb)


@app.post("/upload", response_model=ActionStatusResponse)
async def upload_config(config: Annotated[bytes, File()]):
    """
    Upload native config
    """
    success = False
    try:
        records = json.loads(str(config, encoding="utf-8"))
        config_manager.write_records(records)
        service_manager.refresh()
        success = True
    except Exception as e:
        print(f"Failed to upload config: {e}")

    return ActionStatusResponse(success=success)


async def main(host, port):
    startup = config_manager.read_records()
    config_manager.write_records(startup)  # Not so elegant, but ok...
    await service_manager.start()

    config = uvicorn.Config(app, host=host, port=port)
    api_server = uvicorn.Server(config)
    await api_server.serve()
    await service_manager.stop()


@click.command(context_settings=dict(show_default=True))
@click.option(
    "-H", "--host", type=str, default="0.0.0.0", metavar="HOST", help="Host to listen"
)
@click.option(
    "-p", "--port", type=int, default=9898, metavar="PORT", help="Port to listen"
)
def cmdline_start(**kwargs):
    asyncio.run(main(**kwargs))


if __name__ == "__main__":
    cmdline_start()
