#!/bin/bash

# 批量上传aar，pom
# 在已有GAV文件的基础下，GAV文件格式G,A,V

gav_file=$1
storage="/nexus3/storage"
log_file="upload-$(date +"%F-%H-%M").log"
repo="thirdparty"
upload_url="127.0.0.1:8081/nexus/service/rest/v1/components?repository=${repo}"
user="admin"
password="admin123"

for line in $(cat ${gav_file});do
    aar_group_id=$(echo $line|awk -F',' '{print $1}')
    aar_name=$(echo $line|awk -F',' '{print $2}')
    aar_version=$(echo $line|awk -F',' '{print $3}')
    aar_pkg=${aar_name}-${aar_version}.jar
    aar_pom=${aar_name}-${aar_version}.pom

    if [ -f ${storage}/${aar_pkg} ];then
        if [ -f ${storage}/${aar_pom} ];then
            # 上传aar时指定pom
            curl -u ${user}:${password} -X POST ${upload_url} -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "maven2.groupId=${aar_group_id}" -F "maven2.artifactId=${aar_name}" -F "maven2.version=${aar_version}" -F "maven2.packaging=aar" -F "maven2.generate-pom=false" -F "maven2.asset1=@${storage}/${aar_pkg}" -F "maven2.asset1.extension=aar" -F "maven2.asset2=@${storage}/${aar_pom}" -F "maven2.asset2.extension=pom"
        else
            # 只上传aar包
            curl -u ${user}:${password} -X POST ${upload_url} -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "maven2.groupId=${aar_group_id}" -F "maven2.artifactId=${aar_name}" -F "maven2.version=${aar_version}" -F "maven2.packaging=aar" -F "maven2.generate-pom=false" -F "maven2.asset1=@${storage}/${aar_pkg}" -F "maven2.asset1.extension=aar"
        fi
    else
        echo "${aar_pkg} ${aar_pom} 都不存在！" | tee -a ${log_file}
    fi
done





