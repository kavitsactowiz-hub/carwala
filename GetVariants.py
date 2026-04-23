import json
from lxml import html
from request_getpagedata import getPageData
from PageDetails import extractdata, carmodelist
from concurrent.futures import ThreadPoolExecutor
from db import fetch_all_cars,insert_variants_data
from urllib.parse import urljoin

BaseUrl = "https://www.carwale.com"


fullVariantsObjectList = {}
def process(link):
    data = getPageData(link.get("carlink"))
    if data.status_code == 200:
        root = html.fromstring(data.text)
        alist = root.xpath('//div[contains(@class,"Kl1AE_")]//a')
        if alist:
             fullVariantslist = {}
             for each_a in alist:
                 fullVariantslist[each_a.text_content()] = urljoin(BaseUrl,each_a.get("href"))
    
             fullVariantsObjectList[link.get("carname")] = fullVariantslist
# process("https://www.carwale.com/maruti-suzuki-cars/fronx/")
result = fetch_all_cars()
with ThreadPoolExecutor(max_workers=7) as e:
    e.map(process,result)
    
insert_variants_data(fullVariantsObjectList)
# with open("fullVariantsLinks.json","w",encoding="utf-8") as f:
#     json.dump(fullVariantsObjectList,f)