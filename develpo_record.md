# **develop log**
## 2017-06-09
1. 对数码提供多个provider_id的支持，可在配置文件里面添加provider_bak的字典元素
2. 修改的文件为:
     * get_media_from_request.py
     * loop_check_inject.py
     * parameters.json
3. **目前未对修改进行测试**，只上传到git服务器上
4. 注意：需要将上面的三个文件上传到服务器上进行测试
        
## 2017-06-21
1. 将m3u8的请求地址内的ip更换成内网的地址10.255.46.99
2. 将m3u8被的真正的播放地址的ip替换成10.255.46.99
3. 更正几个隐形bug

## 2017-06-21
1. 在注入状态页／inject_status页显示添加media_id相关的title，title获取，从对应的接口请求数据
2. 修复description，NoneType错误
3. httpresponse body 为bytes
4. 修复inject_status接口内纪录无法删除的bug
5. 调整删除的流程，只有删除了数码的cdn后才删除本地的数据库，否者不删除

## 2017-06-26
1. 添加搜索页面, 调整异步请求
2. 由于mysql的media表跟url表接口调整，需要相应的调整

## 2017-07-17
1. parameters.json添加我方cdn地址配置项
2. 修改m3u8文件内的播放地址的ip，替换成epg_cdn-ip

## 2017-07-18
1. 修改inject_status页面现实错误的问题

## 2017-07-20
1. 在本地的sqlite数据库中查询，检测已经注入的内容，同mysql数据库mop7内的url表进行对比，将却少的表记录，写入到mysql的url表内
2. 在搜索页面显示，当前注入的媒资所有的信息, 搜索到的每条记录带有删除健，在本页删除，并且带有alert提示

## 2017-08-01
1. 修改搜索页删除提示
2. 调整清理cidtable
3. 调整trans_transfer_status_to_percent函数
4. loop_check_inject_insert_mysql 发生错误时，记录删除的数据库记录相关信息
5. 注入主函数，注入错误，将错误的具体信息记录下来

## 2017-08-08
1. 填写409的xml记录，调用数码接口进行删除
2. 添加提取日志409错误的脚本

## 2017-08-16
1. 根据在run_record.log中生成的409错误，提取其中的assetid，根据数码提供注入码率相关信息，生成删除消息，运行删除脚本进行数码注入删除
2. 记录，在网页中删除，已经注入或者正在注入的记录