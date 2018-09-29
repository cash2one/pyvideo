
from selenium import webdriver
 
from selenium.webdriver.chrome.options import Options
 
mobile_emulation = {
 
   "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
 
   "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"

}

path = './Source/win/chromedriver.exe'
 
chrome_options = Options()
 
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation) # 这里看清楚了，不是add_argument
 
driver = webdriver.Chrome(chrome_options = chrome_options, executable_path=path)

driver.get('https://share.html5.qq.com/fx/u?r=A1r8QyC')