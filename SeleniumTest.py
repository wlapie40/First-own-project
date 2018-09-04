from selenium import webdriver
import time
import bs4
import xlsxwriter


pn = 'DQ.B85EG.002'

driver = webdriver.Ie()
driver.get("http://plwro-pcof58:5000/searchFG")

fgsn = driver.find_element_by_id("FGPN_Search")
fgsn.send_keys('DQ.B85EG.002')

Login = driver.find_element_by_id("submit")
Login.click()

time.sleep(3)
elem = driver.find_element_by_id("nsearchsuchbg")
elem.clear()
elem.send_keys(pn)
Search = driver.find_element_by_id("suchbutton")
time.sleep(3)
Search.click()

soup = bs4.BeautifulSoup

x = {line.findAll('b', {'ng-bind': 'Sub.PartNumber'})[0].getText()}
print(x)

# select = browser.findElement(By.xpath("//tr/td[contains(text(), 'ALL_incidents')]"))

# stockPL = driver.find_elements_by_class_name('span')
# print(stockPL)
#
# stockDE = driver.find_element_by_xpath('//*[@id="fromarticleidG792272"]/td[6]/span[2]')

# print(stockPL)
# stockDE = driver.find_element_by_xpath()
# print(stockDE)
# try:



# soup = bs4.BeautifulSoup(driver.page_source,'html.parser')


#     print(x)
# except:
#     print("no results")
#
# workbook = xlsxwriter.Workbook(r'S:\Public\Lenovo_noGluten\Stock_for_PN_' + pn + '.xlsx')
# worksheet = workbook.add_worksheet('PartNumbers')
# worksheet.set_column('A:C', 20)
# bold = workbook.add_format({'bold': True})
#
# worksheet.write('A1', 'Part#', bold)
# worksheet.write('B1', 'Sub Type', bold)
# r = 2
# for keys, values in x.items():
#     worksheet.write('A'+str(r), keys)
#     worksheet.write('B'+str(r), values)
#     r += 1
# workbook.close()

print('Done')




