# API

* `devBaseUrl`: `10.40.20.179:8000`
* ``

## 1. 上传文件

上传规范文件夹，包含 `data.json` 文件和若干图片文件

* url: `/upload`
* method: `post`
* body: 
  * `files`: 文件对象列表
  * `name`: 规范名称
  * 示例：
  
  ```json
  formData({
      "files": ["fileObject", "fileObject"],
      "name": "20kV及以下变电所设计规范"
  })
  ```

* response:

  * `code`: 状态码，1 为上传成功，0 为上传失败
  * `msg`: 相应消息
  * 实例：

  ```json
  {
      "code": 0,
      "msg": "文件名已存在"
  }
  ```

## 2. 请求类别列表

请求类别文件列表

* url: `/require`

* method: `post`

* body:
  
  * `type`: 请求类型，为 1
  * `page`: 页码，从 0 开始
  * `pageNum`: 每页的规范数
  * 示例：

  ```json5
  // 每页 10 条规范，请求第 1 页
  {
      "type": 1,
      "page": 1,
      "classNum": 10
  }
  ```

* response

  * `code`、`msg`
  * `totalClass`: 总的类别条数，用于前端计算页数
  * `pageList`：类别列表，每个类别包括 `id` 和 `name` 属性

  ```json
  
  {
      "code": 1,
      "msg": "xxxx",
      "totalClass": 100,
      "pageList": [
          {"id": "xxxxxx", "name": "xxx"},
          {"id": "******", "name": "***"}
      ]
  }
  ```
  
  ``

## 3. 请求规范列表

请求规范列表

* url: `/require`

* method: `post`

* body: 

  * `type`: 2
  * `classId`: 所选类别的id
  ```json5
  {
      "type": 2,
      "classId": "xxx",
  }
  ```
  
*  response

  * `code`,  `msg`

  * `formList`: 规范列表

  ```json
  {
      "code": 1,
      "msg": "xxxx",
       "formList": [
           {"id":"xxx", "content": "前五十个字符"}
        ]
  }
  ```

## 4. 请求 item 列表

获取 formualtion_id 所对应的 item

* url: `/require`

* method: `post`

* body:

  * `type`: 3
  * `formulationId`

  ```json
  {
      "type": 3,
      "formulationId": "xxxx",
  }
  ```
  
* response:

  * `code`, `message`
  * `itemList`

  ```json
  {
      "code": 1,
      "msg": "xxxx",
      "itemList": [
          {"id": "***", "type": "text", "context": "xxxxx", "pic": ""}
      ]
  }
  ```

  
