#!/usr/bin/env bash

if [ ! -e /usr/local/bin/cfssl ];then
    wget -O /tmo/cfssl https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
    chmod +x /tmp/cfssl
    mv /tmp/cfssl /usr/local/bin/cfssl
fi

if [ ! -e /usr/local/bin/cfssljson ];then
    wget -O /tmo/cfssljson https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
    chmod +x /tmp/cfssljson
    mv /tmp/cfssljson /usr/local/bin/cfssljson
fi

echo -e "### cfssl version: "
/usr/local/bin/cfssl version

echo -e "\n### cfssljson usage: "
/usr/local/bin/cfssljson -h
