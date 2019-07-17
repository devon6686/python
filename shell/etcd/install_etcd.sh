#!/usr/bin/env bash

ETCD_VERSION=v3.3.12
DOWNLOAD_URL=https://github.com/coreos/etcd/releases/download
ETCD_DIR=/opt/app

if [ ! -e etcd-${ETCD_VERSION}-linux-amd64.tar.gz ];then
    wget ${DOWNLOAD_URL}/${ETCD_VERSION}/etcd-${ETCD_VERSION}-linux-amd64.tar.gz
fi

mkdir -p ${ETCD_DIR} && tar xzvf tcd-${ETCD_VERSION}-linux-amd64.tar.gz -C ${ETCD_DIR} --strip-components=1

${ETCD_DIR}/etcd --version
ETCD_API=3 ${ETCD_DIR}/etcdctl version

