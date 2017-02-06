#!/bin/sh -x
if id | grep -qv uid=0; then
    echo "Must run setup as root"
    exit 1
fi

create_socket_dir() {
    local dirname="$1"
    local ownergroup="$2"
    local perms="$3"

    mkdir -p $dirname
    chown $ownergroup $dirname
    chmod $perms $dirname
}

set_perms() {
    local ownergroup="$1"
    local perms="$2"
    local pn="$3"

    chown $ownergroup $pn
    chmod $perms $pn
}

rm -rf /jail
mkdir -p /jail
cp -p index.html /jail

./chroot-copy.sh zookd /jail
./chroot-copy.sh zookfs /jail

#./chroot-copy.sh /bin/bash /jail

./chroot-copy.sh /usr/bin/env /jail
./chroot-copy.sh /usr/bin/python /jail

# to bring in the crypto libraries
./chroot-copy.sh /usr/bin/openssl /jail

mkdir -p /jail/usr/lib /jail/usr/lib/i386-linux-gnu /jail/lib /jail/lib/i386-linux-gnu
cp -r /usr/lib/python2.7 /jail/usr/lib
cp /usr/lib/i386-linux-gnu/libsqlite3.so.0 /jail/usr/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libnss_dns.so.2 /jail/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libresolv.so.2 /jail/lib/i386-linux-gnu
cp -r /lib/resolvconf /jail/lib

mkdir -p /jail/usr/local/lib
cp -r /usr/local/lib/python2.7 /jail/usr/local/lib

mkdir -p /jail/etc
cp /etc/localtime /jail/etc/
cp /etc/timezone /jail/etc/
cp /etc/resolv.conf /jail/etc/

mkdir -p /jail/usr/share/zoneinfo
cp -r /usr/share/zoneinfo/America /jail/usr/share/zoneinfo/

create_socket_dir /jail/echosvc 203:200 755
create_socket_dir /jail/authsvc 204:200 755

mkdir -p /jail/tmp
chmod a+rwxt /jail/tmp

mkdir -p /jail/dev
mknod /jail/dev/urandom c 1 9

cp -r zoobar /jail/
rm -rf /jail/zoobar/db

python /jail/zoobar/zoodb.py init-person
python /jail/zoobar/zoodb.py init-transfer
python /jail/zoobar/zoodb.py init-cred

# python executables
for f in /jail/zoobar/*.py; do
    set_perms 200:200 550 $f
done
set_perms 202:200 550 /jail/zoobar/index.cgi

# database
set_perms 200:200 770 /jail/zoobar/db
set_perms 200:200 770 /jail/zoobar/db/person
set_perms 200:200 660 /jail/zoobar/db/person/person.db
set_perms 204:200 700 /jail/zoobar/db/cred
set_perms 204:200 600 /jail/zoobar/db/cred/cred.db
set_perms 201:200 700 /jail/zoobar/db/transfer
set_perms 201:200 600 /jail/zoobar/db/transfer/transfer.db

# static files
chmod -w /jail/zoobar/templates
chmod -w /jail/zoobar/templates/*
chmod -w /jail/zoobar/media
chmod -w /jail/zoobar/media/*

rm -f /jail/zoobar/*.pyc
