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
      "files": [fileObject, fileObject],
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

## 2. 请求规范列表

请求规范文件列表

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
      "pageNum": 10
  }
  ```

* response

  * `code`、`msg`
  * `totalPage`: 总的规范条数，用于前端计算页数
  * `pageList`：规范列表，每条规范包括 `id` 和 `name` 属性

  ```json
  {
      "totalPage": 100,
      "pageList": [
          {"id": "xxxxxx", "name": "xxx"},
          {"id": "******", "name": "***"}
      ]
  }
  ```

  
