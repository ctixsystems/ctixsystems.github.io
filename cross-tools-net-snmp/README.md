# SNMPD compiled for Netgear Orbi RBR50 / RSR50
Files contained in this repository are [net-snmp source](http://www.net-snmp.org/download.html), cross compiled using [crosstool-ng](https://crosstool-ng.github.io/) to run on the Netgear Orbi ARMv7l CPU.

## Compiling the binaries

From the net-snmpd source tree

```bash
./configure --host=arm-unknown-linux-uclibcgnueabihf \
            --target=arm-unknown-linux-uclibcgnueabihf --build=i686 \
            --disable-manuals --disable-ipv6 \
            --with-cc=arm-unknown-linux-uclibcgnueabihf-gcc \
            --with-ar=arm-unknown-linux-uclibcgnueabihf-ar \
            --without-rpm --disable-applications \
            --disable-embedded-perl \
            --disable-deprecated \
            --with-ldflags=-Bstatic \
            --without-perl-modules

make
```

This will place required files in agent/.lib directory

## Structure
- ```/tmp/snmpd/snmpd``` - the SNMPD executable
- ```/tmp/snmpd/snmpd.conf``` - the configuration file - update rocommunity to include relevant entwrok address range of snmp client
- ```/lib/``` - required libraries


## Use
To get the files on the Orbi device, you need to:
 - Start netcat with the source tgz by running the command ```nc -l -p LISTEN_PORT < snmpd.tgz```
 - [enable telnet](https://orbilogin.com/debug.htm) and connect to the device with ```admin:ORBIPASSWORD```
 - On the orbi device execute the folowing commands 

```bash
cd /tmp
nc HOST LISTEN_PORT > snmpd.tgz
cd /
tar xvfz /tmp/snmpd.tgz
vi /tmp/snmpd/snmpd.conf
/tmp/snmpd/snmpd -c /tmp/snmpd/snmpd.conf

```

## Limitations
- No persistence / autostart capability (should be able to use [this approach](https://hackingthenetgearorbi.wordpress.com/2019/07/03/new-functionality-but-cooler-this-time/))
