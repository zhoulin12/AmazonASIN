**项目简介**
- 一个用于抓取亚马逊商品页面信息的脚本，支持变体监听、详情解析，以及将图片嵌入到 Excel 单元格中
- 主脚本： [asin.py](file:///d:/Seleniumxuexi/asin.py)；打包脚本： [package.py](file:///d:/Seleniumxuexi/package.py)

**主要功能**
- 使用 Playwright 监听 AJAX，获取变体 ASIN 和价格文本
- 使用 requests 或 Playwright 获取商品标题、详情、图片等信息
- 导出 Excel，并将图片以“每个链接一个单元格”的方式嵌入到工作表中
- 自动兼容两种写入方式：
  - 优先使用 xlsxwriter 直接插入图片
  - openpyxl 兜底插入图片，保证无 xlsxwriter 时也能看到图片
- 可将脚本打包为单文件可执行程序

**环境要求**
- Python 3.9+（Windows）
- 已安装 Playwright 浏览器（Chromium）

**依赖安装**
- 建议在虚拟环境中安装

```bash
pip install requests playwright pandas beautifulsoup4 openpyxl xlsxwriter pillow pyinstaller
python -m playwright install chromium
```

**输入与运行**
- 将待处理的 ASIN 写入同目录的“亚马逊Asin.txt”，可换行或空格分隔
- 运行

```bash
python d:\Seleniumxuexi\asin.py
```

- 脚本会为每个基准 ASIN 创建一个同名文件夹，并在其中生成 asin_results.xlsx

**解析与写入规则**
- 页面解析：[extract_details_from_html](file:///d:/Seleniumxuexi/asin.py#L35) 会提取：
  - 商品标题：页面标题文本
  - 商品图片：altImages 区域的所有 img src，作为列表存储
  - 商品详情、商品详情2、商品详情3：页面若干区域文本
  - 详情图片描述：A+ 模块中的段落文本
  - 详情图片：A+ 模块中的所有 img src，作为列表存储
- Excel 写入：
  - 将图片列表拆分成多列：商品图片1、商品图片2…；详情图片1、详情图片2…
  - 每列对应一个链接，并尝试嵌入该图片到对应单元格
  - 使用 xlsxwriter 时设置行高约 120、列宽约 30，图片缩放 0.6
  - 若 xlsxwriter 不可用，自动使用 openpyxl 兜底插入图片
- 相关实现位置：
  - DataFrame 列拆分与写入：[run_batch 写入区](file:///d:/Seleniumxuexi/asin.py#L245-L347)

**打包为可执行文件**
- 打包脚本会确保 Playwright 浏览器被包含，并收集 Excel 相关依赖

```bash
python d:\Seleniumxuexi\package.py
```

- 关键参数：
  - 收集库：playwright、openpyxl、xlsxwriter、pandas、bs4、PIL
  - 隐藏导入：PIL.Image、PIL.PngImagePlugin、PIL.JpegImagePlugin
  - 浏览器资源：PLAYWRIGHT_BROWSERS_PATH=0 并打包 chromium
- 生成的单文件可执行程序名称：AmazonSpider.exe（通常位于 dist 目录）

**常见问题**
- Excel 中仍显示文本而非图片
  - 请确认安装了 xlsxwriter 或 openpyxl 和 pillow
  - 某些图片链接可能返回 403，已在请求中添加常见请求头以提高成功率
- 浏览器未安装或版本不匹配
  - 运行前执行 python -m playwright install chromium
- 被页面风控拦截
  - requests 路径遇到验证会自动回退到 Playwright
  - 可减少频率、增加等待或使用更稳定的网络环境

**配置与行为说明**
- Playwright
  - 浏览器窗口：headless=False，slow_mo=300
  - locale 与 Accept-Language：en-US 优先，便于解析
- 路径行为
  - 程序运行根目录：打包后为可执行文件所在目录，源码运行为脚本目录
  - 输入文件名：亚马逊Asin.txt（与脚本同目录）
  - 输出文件：每个 ASIN 文件夹下的 asin_results.xlsx

**目录结构示例**
- 根目录
  - asin.py（主逻辑）
  - package.py（打包逻辑）
  - 亚马逊Asin.txt（输入）
  - <ASIN1>/asin_results.xlsx
  - <ASIN2>/asin_results.xlsx

**合规与免责声明**
- 本项目仅用于技术研究与学习示例，使用前请遵守目标网站的服务条款与法律法规
- 请勿用于批量化抓取或商业用途；对使用造成的风险与后果自负

**许可**
- 你可在遵循上述合规前提下自由使用与修改此脚本

