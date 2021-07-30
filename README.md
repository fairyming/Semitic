# Semitic

Semitic 网络检测响应

# 项目说明

### 客户端目录结构

```
├── Semitic_start.sh
├── Semitic_stop.sh
├── conf
│   ├── Semitic.conf
│   └── suricata.yaml
├── log
│   ├── Semitic.log
│   ├── fast.log
│   ├── stats.log
│   └── suricata.log
├── rules
│   └── local.rules
├── senteven.sh
└── upload_eve
    ├── error
    ├── sucess
    └── tmp
```

### 服务端-函数接口调用接口说明

1. 日志调用

   ```
   from lib.data import logger
   from lib.enums import CUSTOM_LOGGING
   
   logger.log(CUSTOM_LOGGING.SYSINFO, "sysinfo")
   logger.log(CUSTOM_LOGGING.SUCCESS, "success")
   logger.log(CUSTOM_LOGGING.ERROR, "error")
   logger.log(CUSTOM_LOGGING.WARNING, "warming")
   ```

2. 客户端上传eve.json

   ```
   curl -F "clientfile=@./upload_eve/tmp/eve_20200420141438.json" -H "Accept: application/json" http://172.16.71.1:5000/api/upload_eve
   ```

3. 