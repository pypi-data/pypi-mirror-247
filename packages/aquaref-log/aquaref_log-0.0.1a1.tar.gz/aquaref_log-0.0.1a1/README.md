# Aquaref-Log

> 原主项目名`Flater`

---

## 简介

为主模块`Aquaref`及其它扩展模块提供日志输出的功能

## 使用

### 导入
```Python
from aquareflog import ...
```

### 输出记录
```Python
from aquareflog import Debug, Error, Info, Success  # 颜色不同，其它效果一样

Debug("Debug")
Error("Error")
Info("Info")
Success("Success")
```

### 获取记录
```Python
from aquareflog import GetLog, Debug

for index in range(5):
    Debug(f"Debug{index}")

print(GetLog())
```

### 禁用输出
```Python
from os import environ
environ["FLATER.LOG.ENABLE"] = "false"
```

### 启用输出
```Python
from os import environ
environ["FLATER.LOG.ENABLE"] = "true"
```