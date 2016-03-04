#!/usr/bin/python3
import urllib.request
import xml.etree.ElementTree as ET

urllib.request.urlretrieve("https://www.beeline.ru/Scripts/regions.xml", "regions.xml")
regions = ET.parse('regions.xml').getroot()
market = {}
for region in regions:
    marketCode = ""
    marketName = ""
    for attrib in region.attrib:
        if attrib == "MarketCode":
            marketCode = region.attrib[attrib]
        if attrib == "name":
            marketName = region.attrib[attrib]
    if marketCode != "" and marketName != "":
        market[marketCode] = marketName
print("ALTER TABLE MARKET_CODE MODIFY DESCRIPTION VARCHAR(50);")
for item in market:
    print(
            "MERGE INTO MARKET_CODE USING dual ON (MARKET_CODE = '" + item +
            "')WHEN MATCHED THEN UPDATE SET DESCRIPTION='" + market[item] + "';"
    )
print("COMMIT;")
