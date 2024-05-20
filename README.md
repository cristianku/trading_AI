# trading_AI

Using Neural Networks AI make crypto and trading predictions


-- The idea is to have a costant feed of data from data source like Kraken into an InfluxDB

My configuration is the following:

 - Fedora server 39 with a Nvidia Quadro P6000, AMD RYZEN 9 5900X, 128GB RAM
 - Second Fedora 39 server that act as Disk Server with a Mellanox-4 SAS board connected to an external disk enclosures
via two SAS SFF-8088( 6Gbit) to two ICY Box IB-564SAS-12G 
( in the middle Dual Ports Mini SAS SFF-8088 to internal SAS 36Pin SFF-8087 and Sas expanders 46M0997 
flashed with the last firmware)


API

Alpha Vantage : https://www.alphavantage.co


needed python libraries:

pip3 install request
pip3 install pytz
pip3 install pandas
pip3 install pykrakenapi  --> https://github.com/dominiktraxl/pykrakenapi


INFLUXDB installation on Fedora 39
https://www.influxdata.com/downloads/?_gl=1*1fk4nix*_ga*MjAzOTIwNTE3MS4xNzE2MTM3NTM5*_ga_CNWQ54SDD8*MTcxNjE1NDU1OC4yLjEuMTcxNjE1NzA5NS42MC4wLjEyNjQ3MjcwMjA.

<h3> Step 1 – Create InfluxDB Repo


```bash
cat <<EOF | sudo tee /etc/yum.repos.d/influxdata.repo
[influxdata]
name = InfluxData Repository - Stable
baseurl = https://repos.influxdata.com/stable/\$basearch/main
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdata-archive_compat.key
EOF
```
<h3>Step 2 – Install InfluxDB


```bash
sudo yum install influxdb2
```

```bash
sudo yum install influxdb2-cli
```



```bash
influx version
```

You can also see the detailed information on InfluxDB with the following command.
```bash
rpm -qi influxdb2
```


```bash
Name        : influxdb2
Version     : 2.7.1
Release     : 1
Architecture: x86_64
Install Date: Thu 13 Jul 2023 10:32:32 AM EDT
Group       : default
Size        : 103759839
License     : MIT
Signature   : RSA/SHA512, Fri 28 Apr 2023 01:47:08 PM EDT, Key ID d8ff8e1f7df8b07e
Source RPM  : influxdb2-2.7.1-1.src.rpm
Build Date  : Fri 28 Apr 2023 09:28:30 AM EDT
Build Host  : ip-10-0-35-48.ec2.internal
Relocations : / 
Packager    : support@influxdb.com
Vendor      : InfluxData
URL         : https://influxdata.com
Summary     : Distributed time-series database.
Description :
Distributed time-series database.
```


<h3>Step 3 – Start InfluxDB Service

After installing InfluxDB, start the InfluxDB service and enable it to start at system reboot.


```bash
systemctl start influxdb
systemctl enable influxdb
```

```bash
systemctl status influxdb
```

You will see the following output.

```
● influxdb.service - InfluxDB is an open-source, distributed, time series database
     Loaded: loaded (/usr/lib/systemd/system/influxdb.service; enabled; vendor preset: disabled)
     Active: active (running) since Thu 2023-07-13 10:33:15 EDT; 4s ago
       Docs: https://docs.influxdata.com/influxdb/
    Process: 15431 ExecStart=/usr/lib/influxdb/scripts/influxd-systemd-start.sh (code=exited, status=0/SUCCESS)
   Main PID: 15432 (influxd)
      Tasks: 8 (limit: 4666)
     Memory: 46.1M
        CPU: 599ms
     CGroup: /system.slice/influxdb.service
             └─15432 /usr/bin/influxd
```

--- View your server configuration with the CLI

```bash
influx server-config
```


-- Change the default port
```bash
sudo vi /etc/influxdb/config.toml
```

-- Add the followingline
```bash
http-bind-address = ":8086"
```

```
cristianku@fedora-server:~$ cat /etc/influxdb/config.toml
bolt-path = "/var/lib/influxdb/influxd.bolt"
engine-path = "/var/lib/influxdb/engine"
http-bind-address = ":9086"
```

-- restart the service
```bash
sudo systemctl restart influxdb
```


-- The service listens on port 8086
```bash
sudo ss -tunelp| grep 8086
```

-- Firewall settings 
```bash
sudo firewall-cmd --zone=FedoraServer --add-port=8086/tcp --permanent
sudo firewall-cmd --reload
```

<h4> Now, open your web browser and access the InfluxDB web interface using the URL http://your-server-ip:9086. You will see InfluxDB user welcome screen.

<h3>InfluxDB configuration options

https://docs.influxdata.com/influxdb/v2/reference/config-options/?t=TOML#view-your-server-configuration-with-the-cli

```bash
influx server-config
```
<h3>InfluxDB Chronograf
https://docs.influxdata.com/chronograf/v1/introduction/installation/?t=RedHat+%26amp%3B+CentOS

```bash
sudo dnf install chronograf
```

sudo systemctl start chronograf

sudo systemctl enable chronograf

```bash
sudo firewall-cmd --zone=FedoraServer --add-port=8888/tcp --permanent
sudo firewall-cmd --reload
```


http://fedora-server:8888



