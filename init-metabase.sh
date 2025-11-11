#!/bin/zsh

mkdir -p metabase/plugins

curl -O https://maxcompute-repo.oss-cn-hangzhou.aliyuncs.com/jdbc/latest/odps-jdbc-jar-with-dependencies.jar
mv odps-jdbc-jar-with-dependencies.jar ./metabase/plugins/

curl -O https://maxcompute-repo.oss-cn-hangzhou.aliyuncs.com/metabase/maxcompute.metabase-driver.jar
mv maxcompute.metabase-driver.jar ./metabase/plugins/

docker run -d -p 3000:3000 --name metabase --mount type=bind,source=./metabase/plugins,destination=/plugins metabase/metabase:v0.50.x