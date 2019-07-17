#!/usr/bin/env bash

##----------------------------------------
## etcd nodes：
#       时间保持同步
#       添加名称解析
##----------------------------------------

CERT_NAME="etcd-node"
CERT_PATH="/opt/certs"
ETCD_PATH="/opt/app"
ETCD_DATA="/opt/data"
NODE1_NAME="etcd-1"
NODE2_NAME="etcd-2"
NODE3_NAME="etcd-3"
NODE1_IP="10.0.0.11"
NODE2_IP="10.0.0.12"
NODE3_IP="10.0.0.13"


ETCD_CLUSTER_TOKEN="etcd-cluster"
CA_NAME="etcd-root-ca"

if [ ! -d ${ETCD_DATA} ];then
    mkdir ${ETCD_DATA}
fi

# start service
${ETCD_PATH}/etcd --name ${NODE1_NAME} \
--data-dir ${ETCD_DATA} \
--listen-client-urls https://${NODE1_IP}:2379, http://127.0.0.1:2379 \
--advertise-client-urls https://${NODE1_IP}:2379 \
--listen-peer-urls https://${NODE1_IP}:2380 \
--initial-advertise-peer-urls https://${NODE1_IP}:2380 \
--initial-cluster ${NODE1_NAME}=https://${NODE1_IP}:2380,${NODE2_NAME}=https://${NODE2_IP}:2380,${NODE3_NAME}=https://${NODE3_IP}:2380 \
--initial-cluster-token ${ETCD_CLUSTER_TOKEN} \
--initial-cluster-state new \
--client-cert-auth \
--trusted-ca-file ${CERT_PATH}/${CA_NAME}.pem \
--cert-file ${CERT_PATH}/${CERT_NAME}.pem \
--key-file ${CERT_PATH}/${CERT_NAME}-key.pem \
--peer-client-cert-auth \
--peer-trusted-ca-file ${CERT_PATH}/${CA_NAME}.pem \
--peer-cert-file ${CERT_PATH}/${CERT_NAME}.pem \
--peer-key-file ${CERT_PATH}/${CERT_NAME}-key.pem
# --debug

##在其它节点，修改对应名称地址

# 检查集群健康状态
# export ETCD_API=3
# etcdctl --endpoints ${NODE1_IP}:2379,${NODE2_IP}:2379,${NODE3_IP}:2379 \
# --cacert ${CERT_PATH}/${CA_NAME}.pem \
# --cert ${CERT_PATH}/${CERT_NAME}.pem \
# --key ${CERT_PATH}/${CERT_NAME}-key.pem \
# endpoint health

