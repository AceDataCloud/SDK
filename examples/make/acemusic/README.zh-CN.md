# Make 中的 ACE Music

在 Make Apps SDK 扩展打开 `makecomapp.json`，为本地清单绑定自己的 Make 测试应用，再在应用编辑器同步模块。源码不含正式环境地址、应用 ID 或密钥。

登录[应用列表](https://platform.acedata.cloud/console/applications)，打开**通用应用**。首次使用时先点击**初始化通用应用**，再点击 **API KEY** 旁的复制按钮（图中标注 **1**）。

![通用应用中 API KEY 旁标注 1 的复制按钮](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

在 Make 连接的 **AceDataCloud API token** 字段中粘贴原始 Key。确认它有 ACE Music 权限。连接检查只读取一页任务历史。

原生模块支持创意写歌、自定义歌词写歌、导入 MP3、翻唱、双轨融合、写歌词、按原 ID 查询、批量查询和分页历史。提交歌曲后保存 `task_id`，将其映射到 **Retrieve task (ACE Music)**。成功导入会交付一条参考音轨；完整的歌曲组可交付两条；部分失败仍返回已完成音轨。歌词可直接返回文本，也可能返回待处理任务号。

生成、写词和导入参考音频各自计费。遇到网络中断先核对原任务号和历史，避免重复提交。[接口文档](https://github.com/AceDataCloud/ACEMusicAPI)
