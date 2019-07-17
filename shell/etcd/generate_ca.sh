#!/usr/bin/env bash

#下载并安装cfssl和cfssljson

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

# 生成自签名证书-根CA
CERT_DIR="/data/certs"

if [ -d ${CERT_DIR} ];then
    rm -rf ${CERT_DIR}
fi

mkdir -p ${CERT_DIR}

cat > ${CERT_DIR}/etcd-root-ca-csr.json << EOF
{
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "O": "etcd",
            "OU": "system",
            "L": "Shanghai",
            "ST": "Shanghai",
            "C": "CN"
        }
    ],
    "CN": "etcd-root-ca"
}
EOF

cfssl gencert --initca=true ${CERT_DIR}/etcd-root-ca-csr.json | cfssljson --bare ${CERT_DIR}/etcd-root-ca
## 此时会在${CERT_DIR}目录下生成：
## CSR： etcd-root-ca.csr
## 自签名根CA公钥和私钥：etcd-root-ca.pem, etcd-root-ca-key.pem
##

# verify
if rpm -qa | grep -i openssl &> /dev/null;then
    echo "##Info: openssl already installed!"
else
    yum -y install openssl openssl-devel
fi

echo "##Info: openssl x509 -in ${CERT_DIR}/etcd-root-ca.pem -text -noout"
openssl x509 -in ${CERT_DIR}/etcd-root-ca.pem -text -noout

## cert-generation configuration for other TLS assets

cat > ${CERT_DIR}/etcd-gencert.json << EOF
{
    "signing": {
        "defaults": {
            "usages": [
                "signing",
                "key encipherment",
                "server auth",
                "client auth"
            ],
            "expiry": "87600h"
        }
    }
}
EOF

## 为etcd集群各节点创建证书签名请求并生成相应的公私钥
NODE_NAME="etcd-node"
NODE1_IP="10.0.0.11"
NODE2_IP="10.0.0.12"
NODE3_IP="10.0.0.13"

cat > ${CERT_DIR}/${NODE_NAME}-ca-csr.json << EOF
{
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "O": "etcd-cluster",
            "OU": "system",
            "L": "Shanghai",
            "ST": "Shanghai",
            "C": "CN"
        }
    ],
    "CN": "etcd-nodes",
    "hosts": [
        "127.0.0.1",
        "localhost",
        "10.0.0.10",
        "10.0.0.11",
        "10.0.0.12",
        "10.0.0.13",
        "10.0.0.14"
    ]
}
EOF
## 预留2个节点地址，以防之后扩大etcd集群规模

cfssl gencert \
    --ca ${CERT_DIR}/etcd-root-ca.pem \
    --ca-key ${CERT_DIR}/etcd-root-ca-key.pem \
    --config ${CERT_DIR}/etcd-gencert.json \
    ${CERT_DIR}/${NODE_NAME}-ca-csr.json | cfssljson --bare ${CERT_DIR}/${NODE_NAME}

# 此时会生成etcd-node的证书(etcd-node.pem公钥)，私钥(etcd-node-root.pem)，以及CSR：etcd-node.csr
# 将根CA，etcd node的证书以及私钥传到对应nodes节点上








