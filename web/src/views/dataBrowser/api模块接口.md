# IndexAPI 接口文档

## 概述

本项目提供指数API管理相关接口，包含两个主要模块：
- **API参数配置管理** (`/api/indexapi/param/`)：管理指数API参数配置信息
- **API请求记录管理** (`/api/indexapi/req/`)：管理指数API的请求记录和审批流程

---

## 通用说明

### 请求基础信息

| 项目 | 说明 |
|------|------|
| 基础路径 | `/api/indexapi/` |
| 请求格式 | JSON |
| Content-Type | `application/json` |

### 响应格式

所有接口统一返回 `ResultDTO<T>` 对象，结构如下：

```json
{
  "status": 200,
  "message": "成功",
  "data": {},
  "timestamp": 1748294400000,
  "dateTime": "2026-05-26 10:00:00:000",
  "dataVersion": "1.0.0",
  "poweredBy": "datadriver"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| status | int | 状态码，200表示成功，0表示失败，401/403/500表示异常 |
| message | string | 提示信息 |
| data | object | 返回数据，分页查询时为 PageInfo 对象 |
| timestamp | long | 时间戳（毫秒） |
| dateTime | string | 时间（格式：yyyy-MM-dd HH:mm:ss:SSS） |
| timeConsuming | long | 耗时（毫秒） |
| dataVersion | string | 数据版本（默认1.0.0） |
| poweredBy | string | 支持信息（默认datadriver） |
| resultCount | int | 结果数量 |
| error | string | 错误描述 |
| path | string | 访问路径 |

### 分页查询返回 (PageInfo)

```json
{
  "status": 200,
  "message": "成功",
  "data": {
    "pageNum": 1,
    "pageSize": 10,
    "total": 100,
    "pages": 10,
    "list": []
  }
}
```

---

## 一、API参数配置管理

**接口路径**: `/api/indexapi/param/`

### 1.1 分页查询参数配置

查询指数API参数配置的分页列表。

**请求地址**: `POST /api/indexapi/param/page`

**请求参数** (IndexApiDto):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcStrategyType | string | 否 | 所属策略 |
| vcInterfacceName | string | 否 | 接口名称（模糊查询） |
| vcIndexType | string | 否 | 指标类型 |
| pageNum | int | 否 | 页码（继承自GenericDto） |
| pageSize | int | 否 | 每页条数（继承自GenericDto） |

**响应数据** (IndexApiParamModel 列表):

| 参数名 | 类型 | 说明 |
|--------|------|------|
| vcStrategyId | string | 主键ID |
| vcStrategyType | string | 所属策略 |
| vcInterfacceName | string | 接口名称 |
| vcIndexType | string | 指标类型 |
| vcRemake | string | 接口说明 |
| VcConfig | string | 接口配置 |
| dUpdatetime | string | 更新时间（格式：yyyy-MM-dd HH:mm:ss） |

**请求示例**:
```json
{
  "vcStrategyType": "策略A",
  "vcInterfacceName": "getIndex",
  "vcIndexType": "type1",
  "pageNum": 1,
  "pageSize": 10
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "操作成功",
  "data": {
    "pageNum": 1,
    "pageSize": 10,
    "total": 50,
    "pages": 5,
    "list": [
      {
        "vcStrategyId": "001",
        "vcStrategyType": "策略A",
        "vcInterfacceName": "getIndexData",
        "vcIndexType": "type1",
        "vcRemake": "获取指数数据接口",
        "VcConfig": "{\"url\":\"http://example.com\"}",
        "dUpdatetime": "2026-05-26 10:30:00"
      }
    ]
  }
}
```

**数据库表**: `PAA_CR_INDEX_API_PARAM`

---

### 1.2 新增参数配置

新增一条指数API参数配置记录。

**请求地址**: `POST /api/indexapi/param/insert`

**请求参数** (IndexApiParamModel):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcStrategyId | string | 是 | 主键ID |
| vcStrategyType | string | 是 | 所属策略 |
| vcInterfacceName | string | 是 | 接口名称 |
| vcIndexType | string | 是 | 指标类型 |
| vcRemake | string | 否 | 接口说明 |
| VcConfig | string | 否 | 接口配置 |

**请求示例**:
```json
{
  "vcStrategyId": "002",
  "vcStrategyType": "策略B",
  "vcInterfacceName": "queryIndex",
  "vcIndexType": "type2",
  "vcRemake": "查询指数接口",
  "VcConfig": "{\"url\":\"http://api.example.com\"}"
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "新增成功",
  "data": {}
}
```

---

### 1.3 更新参数配置

更新已有的指数API参数配置记录。

**请求地址**: `POST /api/indexapi/param/update`

**请求参数** (IndexApiParamModel):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcStrategyId | string | 是 | 主键ID（条件） |
| vcStrategyType | string | 否 | 所属策略 |
| vcInterfacceName | string | 否 | 接口名称 |
| vcIndexType | string | 否 | 指标类型 |
| vcRemake | string | 否 | 接口说明 |
| VcConfig | string | 否 | 接口配置 |

**请求示例**:
```json
{
  "vcStrategyId": "002",
  "vcStrategyType": "策略B-更新",
  "vcInterfacceName": "queryIndexUpdated",
  "vcIndexType": "type2",
  "vcRemake": "查询指数接口-已更新",
  "VcConfig": "{\"url\":\"http://api.new.com\"}"
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "修改成功",
  "data": {}
}
```

---

### 1.4 删除参数配置

删除指定的指数API参数配置记录。

**请求地址**: `POST /api/indexapi/param/delete`

**请求参数** (IndexApiParamModel):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcStrategyId | string | 是 | 主键ID（条件） |

**请求示例**:
```json
{
  "vcStrategyId": "002"
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "删除成功",
  "data": {}
}
```

---

## 二、API请求记录管理

**接口路径**: `/api/indexapi/req/`

### 2.1 分页查询请求记录

查询指数API请求记录的分页列表。

**请求地址**: `POST /api/indexapi/req/page`

**请求参数** (IndexApiDto):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcReqUserid | string | 是 | 发起人用户ID |
| vcUseUsername | string | 否 | 使用人用户名（模糊查询） |
| vcPhone | string | 否 | 手机号（模糊查询） |
| vcIpAddr | string | 否 | IP地址（模糊查询） |
| vcAuditorStatus | string | 否 | 审批状态 |
| pageNum | int | 否 | 页码 |
| pageSize | int | 否 | 每页条数 |

**审批状态说明**:

| 状态码 | 说明 |
|--------|------|
| S | 审批通过 |
| F | 审批不通过 |
| W | 待审批 |
| P | IP变更待审批 |
| PF | IP变更不通过 |
| C | 取消申请 |

**响应数据** (IndexApiReqModel 列表):

| 参数名 | 类型 | 说明 |
|--------|------|------|
| vcRecordId | string | 主键ID |
| vcUseUserid | string | 使用人userid |
| vcUseUsername | string | 使用人用户名 |
| vcUseUsernameStr | string | 使用人用户名拼音 |
| vcUseCondition | string | 工作状况（0：在职，1：离职） |
| vcStatus | string | 状态（0：可用，1：禁用） |
| vcDelete | string | 是否删除（0：有效，1：已删除） |
| vcPhone | string | 手机号 |
| vcIpAddr | string | 请求API的IP地址 |
| fCompanyid | string | 使用人-机构ID |
| vcCompanyName | string | 使用人-机构名称 |
| vcCompanyNameStr | string | 使用人-机构名称拼音 |
| fDeptid | string | 使用人-部门ID |
| vcDeptname | string | 使用人部门名称 |
| fUseDeptid | string | 申请人部门ID |
| fUseDeptname | string | 申请人部门名称 |
| dReqDatetime | string | 申请时间 |
| dAuditorDatetime | string | 审批时间 |
| dUpdatetime | string | 更新时间 |
| vcAuditorStatus | string | 审批状态 |
| vcAuditorUserid | string | 审批人ID |
| vcAuditorUsername | string | 审批人用户名 |

**请求示例**:
```json
{
  "vcReqUserid": "user123",
  "vcUseUsername": "张三",
  "vcAuditorStatus": "W",
  "pageNum": 1,
  "pageSize": 10
}
```

**数据库表**: `PAA_CR_INDEX_API_REQ`

---

### 2.2 查询用户列表

查询系统用户列表信息。

**请求地址**: `POST /api/indexapi/req/listUser`

**请求参数** (IndexApiDto):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| 无特定字段 | - | - | 当前实现未使用查询条件 |

**响应数据** (IndexApiUserModel 列表):

| 参数名 | 类型 | 说明 |
|--------|------|------|
| userId | string | 用户ID |
| userName | string | 用户名 |
| companyId | string | 机构ID |
| companyName | string | 机构名称 |
| deptId | string | 部门ID |
| deptName | string | 部门名称 |
| phone | string | 手机号 |

**响应示例**:
```json
{
  "code": 1,
  "message": "操作成功",
  "data": [
    {
      "userId": "U001",
      "userName": "张三",
      "companyId": "C001",
      "companyName": "某某公司",
      "deptId": "D001",
      "deptName": "技术部",
      "phone": "13800138000"
    }
  ]
}
```

**数据来源**: `sys_user`, `SYS_DEPT`, `SYS_USER_DEPT`, `sys_dept` 表联查

---

### 2.3 新增请求记录

新增一条指数API使用请求记录。

**请求地址**: `POST /api/indexapi/req/insert`

**请求参数** (IndexApiReqModel):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcRecordId | string | 是 | 主键ID |
| vcUseUserid | string | 是 | 使用人userid |
| vcUseUsername | string | 是 | 使用人用户名 |
| vcUseUsernameStr | string | 否 | 使用人用户名拼音 |
| vcPhone | string | 否 | 手机号 |
| vcIpAddr | string | 是 | 要请求API的IP地址 |
| fUseDeptid | string | 是 | 申请人部门ID |
| fUseDeptname | string | 是 | 申请人部门名称 |
| vcReqUserid | string | 是 | 发起人userid |
| vcReqUsername | string | 是 | 发起人用户名 |
| fCompanyid | string | 是 | 使用人-机构ID |
| vcCompanyName | string | 是 | 使用人-机构名称 |
| fDeptid | string | 是 | 使用人-部门ID |
| vcDeptname | string | 是 | 使用人部门名称 |
| vcAuditorStatus | string | 否 | 审批状态（默认W待审批） |

**请求示例**:
```json
{
  "vcRecordId": "R001",
  "vcUseUserid": "U001",
  "vcUseUsername": "张三",
  "vcUseUsernameStr": "zhangsan",
  "vcPhone": "13800138000",
  "vcIpAddr": "192.168.1.100",
  "fUseDeptid": "D001",
  "fUseDeptname": "技术部",
  "vcReqUserid": "U002",
  "vcReqUsername": "李四",
  "fCompanyid": "C001",
  "vcCompanyName": "某某公司",
  "fDeptid": "D001",
  "vcDeptname": "技术部",
  "vcAuditorStatus": "W"
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "新增成功",
  "data": {}
}
```

---

### 2.4 更新请求记录

更新已有的指数API请求记录（主要用于IP变更等）。

**请求地址**: `POST /api/indexapi/req/update`

**请求参数** (IndexApiReqModel):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcRecordId | string | 是 | 主键ID（条件） |
| vcAuditorStatus | string | 否 | 审批状态 |
| vcIpAddr | string | 否 | IP地址 |

**请求示例**:
```json
{
  "vcRecordId": "R001",
  "vcAuditorStatus": "P",
  "vcIpAddr": "192.168.1.200"
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "修改成功",
  "data": {}
}
```

---

### 2.5 删除请求记录

删除指定的指数API请求记录。

**请求地址**: `POST /api/indexapi/req/delete`

**请求参数** (IndexApiReqModel):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcRecordId | string | 是 | 主键ID（条件） |

**请求示例**:
```json
{
  "vcRecordId": "R001"
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "删除成功",
  "data": {}
}
```

---

### 2.6 审批操作

对指数API请求记录进行审批操作（支持批量审批）。

**请求地址**: `POST /api/indexapi/req/updateAudit`

**请求参数** (IndexApiDto):

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| vcRecordIds | string[] | 是 | 主键ID数组（批量操作） |
| vcAuditorStatus | string | 是 | 审批状态（S/F/P/PF/C） |

**审批状态说明**:

| 状态码 | 说明 |
|--------|------|
| S | 审批通过 |
| F | 审批不通过 |
| P | IP变更待审批 |
| PF | IP变更不通过 |
| C | 取消申请 |

**请求示例**:
```json
{
  "vcRecordIds": ["R001", "R002", "R003"],
  "vcAuditorStatus": "S"
}
```

**响应示例**:
```json
{
  "code": 1,
  "message": "操作成功",
  "data": {}
}
```

---

## 三、数据模型

### IndexApiParamModel - API参数配置模型

```java
{
  "vcStrategyId": "string",    // 主键ID
  "vcStrategyType": "string",  // 所属策略
  "vcInterfacceName": "string", // 接口名称
  "vcIndexType": "string",      // 指标类型
  "vcRemake": "string",         // 接口说明
  "VcConfig": "string"          // 接口配置（JSON格式）
}
```

### IndexApiReqModel - API请求记录模型

```java
{
  "vcRecordId": "string",         // 主键ID
  "vcUseUserid": "string",         // 使用人userid
  "vcUseUsername": "string",       // 使用人用户名
  "vcUseUsernameStr": "string",    // 使用人用户名拼音
  "vcUseCondition": "string",       // 工作状况（0：在职，1：离职）
  "vcStatus": "string",            // 状态（0：可用，1：禁用）
  "vcDelete": "string",            // 是否删除（0：有效，1：已删除）
  "vcPhone": "string",             // 手机号
  "vcIpAddr": "string",            // 请求API的IP地址
  "vcIpAddrOld": "string",         // 变更前IP
  "fCompanyid": "string",          // 使用人-机构ID
  "vcCompanyName": "string",       // 使用人-机构名称
  "vcCompanyNameStr": "string",    // 使用人-机构名称拼音
  "fDeptid": "string",            // 使用人-部门ID
  "vcDeptname": "string",         // 使用人部门名称
  "fUseDeptid": "string",         // 申请人部门ID
  "fUseDeptname": "string",       // 申请人部门名称
  "dReqDatetime": "string",       // 申请时间
  "dAuditorDatetime": "string",   // 审批时间
  "dUpdatetime": "string",        // 更新时间
  "vcAuditorStatus": "string",    // 审批状态
  "vcAuditorUserid": "string",     // 审批人ID
  "vcAuditorUsername": "string",  // 审批人用户名
  "vcReqUserid": "string",        // 发起人userid
  "vcReqUsername": "string"       // 发起人用户名
}
```

### IndexApiUserModel - 用户信息模型

```java
{
  "userId": "string",       // 用户ID
  "userName": "string",     // 用户名
  "companyId": "string",     // 机构ID
  "companyName": "string",   // 机构名称
  "deptId": "string",       // 部门ID
  "deptName": "string",     // 部门名称
  "phone": "string"         // 手机号
}
```

---

## 四、数据库表结构

### PAA_CR_INDEX_API_PARAM - API参数配置表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| vcStrategyId | varchar2(50) | 主键ID |
| vcStrategyType | varchar2(50) | 所属策略 |
| vcInterfacceName | varchar2(300) | 接口名称 |
| vcIndexType | varchar2(50) | 指标类型 |
| vcRemake | varchar2(4000) | 接口说明 |
| VcConfig | clob | 接口配置 |
| dUpdatetime | date | 更新时间 |

### PAA_CR_INDEX_API_REQ - API请求记录表

| 字段名 | 类型 | 说明 |
|--------|------|------|
| vcRecordId | varchar2(50) | 主键ID |
| vcUseUserid | varchar2(50) | 使用人userid |
| vcUseUsername | varchar2(300) | 使用人用户名 |
| vcUseUsernameStr | varchar2(300) | 使用人用户名拼音 |
| vcUseCondition | varchar2(2) | 工作状况 |
| vcStatus | varchar2(2) | 状态 |
| vcDelete | varchar2(2) | 是否删除 |
| vcPhone | varchar2(50) | 手机号 |
| vcReqUserid | varchar2(50) | 发起人userid |
| vcReqUsername | varchar2(300) | 发起人用户名 |
| vcIpAddrOld | varchar2(300) | 变更前IP |
| vcIpAddr | varchar2(300) | 请求API的IP地址 |
| fCompanyid | varchar2(50) | 使用人-机构ID |
| vcCompanyName | varchar2(300) | 使用人-机构名称 |
| vcCompanyNameStr | varchar2(300) | 使用人-机构名称拼音 |
| fDeptid | varchar2(50) | 使用人-部门ID |
| vcDeptname | varchar2(300) | 使用人部门名称 |
| fUseDeptid | varchar2(50) | 申请人部门ID |
| fUseDeptname | varchar2(300) | 申请人部门名称 |
| dReqDatetime | date | 申请时间 |
| dAuditorDatetime | date | 审批时间 |
| vcAuditorStatus | varchar2(2) | 审批状态 |
| vcAuditorUserid | varchar2(50) | 审批人ID |
| vcAuditorUsername | varchar2(300) | 审批人用户名 |
| dUpdatetime | date | 更新时间 |

---

## 五、错误码说明

| code | 说明 |
|------|------|
| 1 | 成功 |
| 其他 | 失败，具体信息见message字段 |

**新增/修改/删除操作失败提示**:
- "新增成功" / "新增失败，条数为0"
- "修改成功" / "修改失败，条数为0"
- "删除成功" / "删除失败，条数为0"
- "操作成功" / "操作失败，条数为0"

---

*文档生成时间: 2026-05-26*
