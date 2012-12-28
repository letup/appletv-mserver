#!/bin/bash
/bin/cp cgi/* /usr/lib/cgi-bin
chown www-data.www-data /usr/lib/cgi-bin/*
chmod +x /usr/lib/cgi-bin/*
mkdir -p /DataVolume/.avs/pl/
chmod -R 755 /DataVolume/.avs/
mkdir -p /opt/avs
/bin/cp -af mbl/bin /opt/avs
/bin/cp -af mbl/lib /opt/avs
/bin/cp -f mbl/avs /etc/apache2/sites-available
/bin/cp -f server/* /opt/avs
chmod 755 /opt/avs/bin/*
chmod 755 /opt/avs/*.sh
chmod 755 /opt/avs/*.py
/bin/cp -f avs.sh /opt/avs/
chmod +x /opt/avs/avs.sh
ln -s /opt/avs/avs.sh /opt/etc/init.d/Savs.sh
ln -s /opt/avs/avs.sh /opt/etc/init.d/Kavs.sh
cd /etc/apache2/sites-enabled
ln -sf ../sites-available/avs .
apache2ctl restart
/opt/avs/avs.sh restart
