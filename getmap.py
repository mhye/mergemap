#隐藏元素
from  selenium.webdriver.common.action_chains  import ActionChains
from selenium import webdriver
import time
from PIL import Image
from io import BytesIO
def hide_element(driver):
    #隐藏一些导航相关元素，截图时不需要这些
    script = """
    $("#left-panel").hide();//搜索框
    $("#tooltip-route").hide();//路线
    $("#app-right-top").hide();//右上角
    $("#map-operate").hide();//指南针，缩放
    $("#mapType-wrapper").hide();//地图类型切换
    $("#newuilogo").hide();//logo
    $("#MapHolder > div.BMap_scaleCtrl.anchorBL").hide();//比例尺
    $("#MapHolder > div.BMap_cpyCtrl.BMap_noprint.anchorBL").hide();//icp相关
    """
    driver.execute_script(script)


#截图
def catch(driver:webdriver.Chrome,size:tuple):
    #原尺寸
    origin = tuple(driver.get_window_size().values())
    #全屏
    driver.fullscreen_window()
    #因此无关元素
    hide_element(driver)
    time.sleep(3)

    #屏幕尺寸
    height = driver.get_window_size().get("height")
    width = driver.get_window_size().get("width")
    screensize = (width,height)

    #屏幕滚动距离
    move_x = width - 20
    move_y = height - 20

    rows,cols = size
    im_size = (
        width*cols-(cols-1)*20,
        height*rows - (rows-1)*20 )
    im = Image.new("RGBA",im_size)
    #要拖动的元素
    element = driver.find_element_by_css_selector('#MapHolder > canvas')

    for row in range(0,rows):
        for col in range(0,cols):
            print(f"截取第{row}行，第{col}列\n")
            if col ==0 and row == rows-1:
                #左下角放置百度的log和比例尺
                script_show ='$("#newuilogo").show();$("#MapHolder > div.BMap_scaleCtrl.anchorBL").show();'
                driver.execute_script(script_show)
                b = driver.get_screenshot_as_png()#拍照
                script_hide ='$("#newuilogo").hide();$("#MapHolder > div.BMap_scaleCtrl.anchorBL").hide();'
                driver.execute_script(script_hide)
            else:
                b = driver.get_screenshot_as_png()#拍照

            paste(im,b,screensize,(row,col))#粘贴
            #左移
            if col < cols-1:
                print(f"右移{move_x}像素")
                ActionChains(driver).drag_and_drop_by_offset(element,-move_x,0).perform()
            else:
            #返回并下移
                print(f"左移{move_x}*{col}像素,下移{move_y}像素")
                ActionChains(driver).drag_and_drop_by_offset(element,move_x*col,-move_y).perform()

            time.sleep(5)
    #返回起始位置
    print("返回起始位置")
    ActionChains(driver).drag_and_drop_by_offset(element,0,move_y*cols).perform()
    driver.set_window_size(*origin)
    return im

def paste(im:Image,b:bytes,screensize,index):
    w,h = screensize
    row,col = index
    x = col*(w-20)
    y = row*(h-20)
    box = (x,y)
    bio = BytesIO()
    bio.write(b)
    bio.seek(0)
    tmp = Image.open(bio)
    im.paste(tmp,box)

if __name__ == "__main__":
    import sys
    try:
        row = int(sys.argv[1])
        col = int(sys.argv[2])
        filename = sys.argv[3]
        if len(filename.split("."))<2:
            filename +=".png"
    except Exception as e:
        s = f"""用法:
python {sys.argv[0]} 行数 列数 文件名
范例:
python {sys.argv[0]} 3 3 h.png
        """
        print(s)
    
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=options)
    driver.get("https://ditu.baidu.com")

    while True:
        print("现在麻烦对截图起始位置，缩放比例进行调整....")
        key = input("请输入(yes或者y)，确认您已经调整好,或者输入(Q)退出本次操作:")
        if key.lower() in("y","yes"):
            print("开始截图,拼接操作...")
            break
        elif key.lower() == "q":
            driver.quit()
            sys.exit(0)
    
    im = catch(driver,(row,col))
    im.save(filename)
    driver.quit()
    sys.exit(0)


