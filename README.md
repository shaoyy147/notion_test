# Notion2Moments



## 使用说明

## Notion 的准备

1. 将所需使用的 Notion 模版 拷贝至自己的 Notion 下
    - 点击打开此 [Notion2Moments模版](https://sticky-cotton-ad9.notion.site/856c69b89f9b46c5aaba8f1e16915ed0?v=05d976ec4040453e90f7a13796b3b8ed&pvs=74) 链接 *（建议右键在新新标签页打开）* 
    - 点击右上角重叠方块 `duplicate` 按钮
2. 创建一个Notion Integration
    - 进入 Notion官方 [My integrations](https://www.notion.so/my-integrations) 页面 *（建议右键在新新标签页打开）* 
    - 点击正中间 `Create new integration`，输入一个便于记忆区分的名称 (e.g Notion2Moments)
    - 进入该 Integration，点击 Capabilities，**只勾选** `Read content` 以及圈选 `No user Infomation`。此项目只需读取 database 的内容，因此这里给予最小权限来保障自己 Notion 的安全
    - （完成后可以顺带将 Notion Secret 复制下来保存起来，后续步骤会用到。具体方法为：点击左边的 `Secrets` 菜单项，右侧点击 `Show` -> `Copy` 即可）
3. 将模版与该Integration绑定
    - 在 Notion 里进入刚才拷贝的 Notion2Moments模版
    - 点击又上角三个点`...`，弹出菜单
    - 进入菜单最下方 `Connect to`，点击刚才创建的Integration名称，弹出提醒款，选择`Confirm`即可



## Github 的准备

Github 侧的配置

1. fork这个repo: 在页面上方点击 `Fork` 即可
2. 设置环境变量
    - 进入 fork 后的 repo，点击上方 `Setting`
    - 左侧 `Security` 小标题下方 `Securities and variables` 点击展开后选中 `Action`
    - 添加 Notion Secret: 点击右侧绿色的 `New repository secret` 按钮，`Name` 输入框下填写 `NOTION_SECRET`，`Secret` 下方输入框填写之前创建的 Notion Integration 里的 Secret 
    - 添加 Notion Database: 再次点击右侧绿色的 `New repository secret` 按钮，`Name` 输入框下填写 `NOTION_DATABASE_ID`，`Secret` 下方输入框填写之前拷贝模版所对应的 Notion ID。获取方式如下
        - 在你的 Notion 中，进入该模版 database 所在的页面，复制该页面链接
        - 粘贴该链接，链接为这样的格式 `https://www.notion.so/8l6c69b89f9b46c5ceb38f1e96915ed0?v=05d976ec4640453e90f7a13796e3b8e2`，其中 `notion.so`斜杠后至问号`?`部分为所需的 Notion ID，即这个例子中的 `8l6c69b89f9b46c5ceb38f1e96915ed0` 







 3. 修改 Github Action 配置，开始进行自动更新：在 Github 页面上即刻操作，进入`work.yml` 文件，点击修改，将``前面的警号#删除，并保持缩进对齐，例如 xxxx
，保存commit。

（服务的手动更新）
后面要多加一些样例