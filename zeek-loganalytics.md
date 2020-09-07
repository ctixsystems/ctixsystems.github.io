---
layout: default
title: "Configuring Azure log analytics to consume zeek telemetry"
permalink: /zeek-loganalytics/
---
Work in progress -- coming soon

## Configuring Linux OMS Agent to ship zeek logs to Azure
The Linux OMS agent uses [fluentd](https://docs.fluentd.org/quickstart) and is able to directly parse and ship the json log format used by zeek. To configure this, two modifications 
need to be made to the OMS agent configuration:
- need to add a file (`zeek.conf`) in the `/etc/opt/microsoft/omsagent/<workspace id>/conf/omsagent.d` directory
- need to update the `omsagent.conf` file in `/etc/opt/microsoft/omsagent/<workspace id>/conf` directory

### zeek.conf
This configuration file instructs the OMS agent to ship json logs from the identified zeek log files to the OMS agent. You need to include
both a *source* and *match* stanza for each of the logs.

```
# zeek.conf
# Allows transport of Zeek json logs to Azure Monitor (log analytics workspace) via OMS Agent
# Stored in /etc/opt/microsoft/omsagent/<workspace id>/conf/omsagent.d/
# Also needs edit to omsagent.conf file as well

<source>
  type sudo_tail
  path /usr/local/zeek/logs/current/x509.log
  pos_file /var/opt/microsoft/omsagent/state/CUSTOM_LOG_BLOB.zeekx509-1c80-4fdb-adb0-9fb973a294b1.pos
  read_from_head false
  run_interval 60
  #tag oms.blob.CustomLog.CUSTOM_LOG_BLOB.zeekconn_CL_3e6fdd2e-1c80-4fdb-adb0-9fb973a294b1.*
  tag oms.api.zeekx509
  format json
</source>

<source>
  type sudo_tail
  path /usr/local/zeek/logs/current/ssl.log
  pos_file /var/opt/microsoft/omsagent/state/CUSTOM_LOG_BLOB.zeekssl-1c80-4fdb-adb0-9fb973a294b1.pos
  read_from_head false
  run_interval 60
  #tag oms.blob.CustomLog.CUSTOM_LOG_BLOB.zeekconn_CL_3e6fdd2e-1c80-4fdb-adb0-9fb973a294b1.*
  tag oms.api.zeekssl
  format json
</source>

<match oms.api.zeekssl>
  type out_oms_api
  log_level info
  buffer_chunk_limit 5m
  buffer_type file
  buffer_path /var/opt/microsoft/omsagent/3e6fdd2e-1c80-4fdb-adb0-9fb973a294b1/state/out_oms_api_zeekssl*.buffer
  buffer_queue_limit 10
  flush_interval 20s
  retry_limit 10
  retry_wait 30s
</match>

<match oms.api.zeekx509>
  type out_oms_api
  log_level info
  buffer_chunk_limit 5m
  buffer_type file
  buffer_path /var/opt/microsoft/omsagent/3e6fdd2e-1c80-4fdb-adb0-9fb973a294b1/state/out_oms_api_zeekx509*.buffer
  buffer_queue_limit 10
  flush_interval 20s
  retry_limit 10
  retry_wait 30s
</match>
```

Updates to the omsagent.conf as follows are also required *need to confirm this - seems redundant - suspect it replaces the match requirement in zeek.conf:

```
# Addition to omsagent.conf to allow transport of zeek json logs to Azure MOnitor (log analytics workspace)
# See also zeek.conf

<match oms.api.**>
  type out_oms_api
  log_level info

  buffer_chunk_limit 5m
  buffer_type file
  buffer_path /var/opt/microsoft/omsagent/3e6fdd2e-1c80-4fdb-adb0-9fb973a294b1/state/out_oms_api*.buffer
  buffer_queue_limit 10
  flush_interval 20s
  retry_limit 10
  retry_wait 30s
</match>
```
## Processing zeek logs in Azure log analytics

## Profit!

## References
- [Zeek introduction](https://docs.zeek.org/en/stable/intro/index.html)
- [Microsoft Log Analytics Agent](https://docs.microsoft.com/en-us/azure/azure-monitor/platform/log-analytics-agent)
- [Collecting custom JSON data sources with the Log Analytics agent for Linux in Azure Monitor](https://docs.microsoft.com/en-gb/azure/azure-monitor/platform/data-sources-json)
