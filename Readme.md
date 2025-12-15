# `Fastmasq` - exposing `dnsmasq` management of domain records via RESTful API

## Table of content

[Introduction](#introduction)

[Install dependencies](#install-dependencies-and-run-manual-and-with-docker)

[Managing scripts](#managing-scripts)

[Autocomplete](#autocomplete)

[Local DNS resolver setup](#local-dns-resolver-setup)

## Introduction

`fastmasq` is an attempt to manage DNS server via simple RESTful API. It supports setting/deleting/listing DNS records. Moreover, it also dumping and uploading complete JSON configs.

The tool is not production ready and not scalable. There is a little less than nothing done for security, therefore it is not recommended to expose it to internet. I wrote it in order to maintain my personal short list of addresses under the Private Network and share this list between my machines, because I really don't like entering IP addresses manually in work environment. And of course I had fun and new experience :)

Also, in this Readme I will provide a couple of tips how to integrate it into system in the convenient way.

## Install dependencies and run (manual and with docker)

TBD

## Managing scripts

The whole service can be managed with simple `curl` commands, and for convenience there are already implemented scripts (located in `scripts` directory). All of them rely on `FASTMASQ_SERVER` environment variable, which defines the address and port of `fastmasq` server splitted by colon (e.g. `127.0.0.1:1234`). Call examples:

- `./scripts/fastmasq_set.sh <domain> <address>` - Add new record

- `./scripts/fastmasq_del.sh <domain>` - Delete record

- `./scripts/fastmasq_list.sh` - List all records

- `./scripts/fastmasq_dump.sh <config_path>` - Dump `fastmasq` config from server to specified path

- `./scripts/fastmasq_upload.sh <config_path>` - Upload config to server

## Autocomplete

Autocompletion script (`scripts/hosts_caching.sh`) is kinda hackish, however it works in the most transparent way and does not break autocomplete for `ssh`, `ping`, etc., and in fact it can work in any shell implementation (`bash`, `zsh`, etc.). It just relies on `HOSTFILE` environment variable, and once per some period of time it updates domain names synchronized with specified `fastmasq` server via API call.

The idea is that this script is executed in shell initialization script in background (it manages to run in single instance by itself, even if multiple shell sessions will run). The following code snippet can be added to `.bashrc` or `.zshrc`:

```sh
# These variables are necessary
export FASTMASQ_SERVER=<FASTMASQ_SERVER_ADDRESS>:<PORT>
export HOSTFILE=<YOUR_HOSTFILE_PATH> # Be careful, it can be already set in your system

<PATH_TO_FASTMASQ_SCRIPTS>/hosts_caching.sh&
```

## Local DNS resolver setup

In linux you can add your DNS server running `fastmasq` in standard way by updating `/etc/resolv.conf`, adding something like:

```text
nameserver <FASTMASQ_DNS_SERVER_ADDRESS>
```

However, sometimes you do not want to pass all DNS requests through `fastmasq` server (because for external network it is useless, it only resolves records from config). Instead, you may wish to specify only subdomains to be served by your servers. For example, you may select your personal top-level domain (e.g. `mydomain`) and all DNS requests for this subdomain (e.g. `first.mydomain`, `second.mydomain`, etc.) will go to yout `fastmasq` server, meanwhile other will go to another depending on system configuration. The simplest way to do this in linux is to use `dnsmasq` as local DNS server, and in its config (usually `/etc/dnsmasq.conf`) add following something like this:

```
# format: server=/<subdomain>/<dns_server_address>
server=/mydomain/10.20.30.40
```

If you use Mac OS, you also can use `dnsmasq`, but there is easier standard solution. You can add corresponding file named by your subdomain into `/etc/resolver/` dir, specifying there your DNS server. For example, to add DNS server for `mydomain` top-level domain, you do:

```sh
# May require root privileges
mkdir -p /etc/resolver
echo "nameserver 10.20.30.40" >/etc/resolver/mydomain
```
