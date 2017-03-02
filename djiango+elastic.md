#djiango + elastic 部署日志收集、查找系统

###安装
参考：https://www.elastic.co/start

1. 安装Elasticsearch
2. 安装Kibana
3. 安装X-Pack
    * 切换到elasticsearch 安装目录 运行bin/elasticsearch-plugin install x-pack
    * 切换到kibana 安装目录运行bin/kibana-plugin install x-pack
    
4. 安装Logstash

### 启动
1. 启动（elasticsearch） 切换到elasticsearch安装目录 运行bin/elasticsearch
2. 启动（kibana）切换到kibana安装目录运行bin/kibana
3. 启动（Logstash）

    * 切换到安装目录 在 config 新建 mylogstash.conf
    * 内容如下
           ```
           input { stdin {}}
           output {
              elasticsearch {
                 hosts => ["localhost:9200"]
                 user => elastic
                 password => changeme
              }
           } 
           ```
           
    * 在安装目录下运行 bin/logstash -f config/mylogstash.conf 

4. 访问http://localhost:5601 用户名：elastic，密码：changeme
