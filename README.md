# 说明
通过selenium打开地图，模拟鼠标拖动整屏，然后拼接到一起
# 准备
## 下载Chromedriver.exe
下载地址 [ChromeDriver.exe](http://npm.taobao.org/mirrors/chromedriver)

找到合适的版本，下载以后置于python.exe相同目录

# 使用方法
## 流程
启动脚本，调整浏览器中地图的起始位置，返回终端按提示继续任务
## 用法示例
```python
python getmap.py 3 3 abc.png
#截取三行，三列，拼接保存为abc.png
```
