import json
from lxml import html
from request_getpagedata import getPageData
from PageDetails import extractdata, carmodelist
from concurrent.futures import ThreadPoolExecutor
from db import insert_car_data

BaseUrl = "https://www.carwale.com/"


data = getPageData(BaseUrl)
if data.status_code == 200:
    root = html.fromstring(data.text)
    scriptdatastr = root.xpath('string(//script[contains(text(),"window.__INITIAL_STATE__")])')
    scriptdata = []
    scriptdata = scriptdatastr.split("window.__CLIENT_RENDER__")[0].split("window.__INITIAL_STATE__")[1].strip().lstrip("=")
    
finaljsondata = json.loads(scriptdata.strip().rstrip(";"))
maskingName = []

for eachModel in finaljsondata.get("homePage").get("makeList"):
    maskingName.append(eachModel.get("maskingName"))

print(maskingName)
if maskingName:
    with ThreadPoolExecutor(max_workers=5) as e:
        e.map(extractdata,maskingName)

    for link in carmodelist:
        insert_car_data(link)
