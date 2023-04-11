# 简单文本传输
将文本持久化保存，并返回一个用于访问文本的url。对于已经保存的文本，可以在web页面对其进行修改和删除。
程序本身由Python + Sqlite数据库 + 几个简单的Html页面构成。
 
# docker 快速运行
```bash
docker run -d -p 5000:5000 -v ./data/:/app/data/ --restart=always --name simpletexttransfer nyar233/simpletexttransfer
```
