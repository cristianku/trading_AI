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
https://computingforgeeks.com/how-to-install-influxdb-on-fedora/?utm_content=cmp-true

-- adding repository
```bash
sudo tee /etc/yum.repos.d/influxdb.repo<<EOF
[influxdb]
name = InfluxDB Repository - RHEL 
baseurl = https://repos.influxdata.com/rhel/8/x86_64/stable/
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdata-archive_compat.key
EOF
```
-- InfluxDB installation 
```bash
sudo dnf install influxdb2 influxdb2-cli
```
