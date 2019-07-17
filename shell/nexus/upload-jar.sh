#!/bin/bash

# 批量上传jar，pom
# 在已有GAV文件的基础下，GAV文件格式G,A,V
# 本地settings.xml文件配置好私服信息

gav_file=$1
storage="/nexus3/storage"
log_file="upload-$(date +"%F-%H-%M").log"
url="127.0.0.1:8081/nexus/repository/thirdparty/"
repo="thirdparty"


for line in $(cat ${gav_file});do
    jar_group_id=$(echo $line|awk -F',' '{print $1}')
    jar_name=$(echo $line|awk -F',' '{print $2}')
    jar_version=$(echo $line|awk -F',' '{print $3}')
    jar_pkg=${jar_name}-${jar_version}.jar
    jar_pom=${jar_name}-${jar_version}.pom

    if [ -f ${storage}/${jar_pkg} ];then
        if [ -f ${storage}/${jar_pom} ];then
            # 上传jar时指定pom
            mvn  deploy:deploy-file -Dfile=${storage}/${jar_pkg} -Durl=${url} -DgroupId=${jar_group_id} -DartifactId=${jar_name} -Dversion=${jar_version} -DgeneratePom=false -Dpackaging=jar -DpomFile=${storage}/${jar_pom} -DrepositoryId=${repo} | tee -a ${log_file}
        else
            # 只上传jar包
            mvn  deploy:deploy-file -Dfile=${storage}/${jar_pkg} -Durl=${url} -DgroupId=${jar_group_id} -DartifactId=${jar_name} -Dversion=${jar_version} -DgeneratePom=false -Dpackaging=jar -DrepositoryId=${repo} | tee -a ${log_file}
        fi
    elif [ -f ${storage}/${jar_pom} ];then
        # 只上传pom
        mvn  deploy:deploy-file -Dfile=${storage}/${jar_pom} -Durl=${url} -DgroupId=${jar_group_id} -DartifactId=${jar_name} -Dversion=${jar_version} -Dpackaging=pom -DrepositoryId=${repo} | tee -a ${log_file}
    else
        echo "${jar_pkg} ${jar_pom} 都不存在！" | tee -a ${log_file}
    fi
done





