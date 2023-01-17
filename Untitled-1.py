self.driver.find_element_by_xpath("//div[@class='gv-footer']//button").click()
                self.driver.find_element_by_xpath("//button[@class='sc-1ebmiy2-0 dCqZTO']").click()
                self.driver.find_element_by_xpath("//button[@class='sc-1ebmiy2-0 dCqZTO']").click()       
                self.driver.find_element_by_xpath("//div[@class='gv-footer']//button ").click()#Next button
                time.sleep(5)
                self.driver.find_element_by_xpath("//div[@class='gv-footer']//button ").click()#Next button 2
                time.sleep(10)
                self.driver.find_element_by_xpath("(//div[@class='buttons']//button)[2]").click() #signup
                time.sleep(5)
                self.driver.find_element_by_xpath("//div[@class='cmc-cookie-policy-banner__close']").click()#cookies
                time.sleep(5)
                self.driver.find_element_by_xpath("//div[@class='sc-b1f0826a-0 cKSWpr']//span[text()='Maybe later']").click()#we would love

        def get_table(self):
                self.table = self.driver.find_element_by_xpath("//div[@class='sc-853bfcae-1 eibzVK']")
                self.three_dots = self.table.find_elements_by_xpath("//button[@class='sc-a4a6801b-0 kIPIkU sc-9bc013b0-0 jpztv']")
                self.get_crypto_names = self.driver.find_elements_by_xpath("//tbody/tr/td[3]/div/a/div/div/p")
                
                for crypto_name in self.get_crypto_names:
                        self.names = crypto_name.text

                for three_dot in self.three_dots:
                        three_dot.click()
                        historic = self.driver.find_element_by_xpath("(//button[@class = 'sc-1ebmiy2-0 juUwCn'])[3]").click()
                        print(historic.text)

        def table_data(self):
                self.driver.find_element_by_xpath("//button[@class='sc-1ebmiy2-0 kDjqxm']").click()
                self.driver.find_element_by_xpath("//div[@class='yzncs8-4 jaVFYH']//li[4]").click()
                self.driver.find_element_by_xpath("//div[@class='yzncs8-2 keWhlt']//button[text()='Continue']").click()
                time.sleep(3)
                
 
#https://stackoverflow.com/questions/49192522/web-scraping-coinmarketcap-com-with-python-requests-beautifulsoup
#https://www.youtube.com/watch?v=thHCp3TL6QE
#https://stackoverflow.com/questions/65189994/web-scraping-using-selenium-using-python-not-retrieving-all-elements
#https://github.com/pkia/CoinMarketCap_Scraper/blob/main/scraper.py
#https://github.com/mohhamad-esmaili/coinmarketcap-python-scraper/blob/main/coinmarketcap.py
#https://github.com/sharad-s/coinmarketcap-scraper/blob/master/scraper.py
#https://stackoverflow.com/questions/67714663/scrape-data-from-all-columns-into-python-using-selenium-to-load-more

a=scraper()
a.get_page()
a.get_table()
















        
        # def search_tip(self):
        #         div_tag = self.driver.find_element(by=By.XPATH, value='//div[@class="sc-8ukhc-2 iCMWiP"]')
        #         element = WebDriverWait(div_tag, 20).until(EC.element_to_be_clickable((By.XPATH, ".//button[@class='sc-1ebmiy2-0 HBft']")))
        #         self.driver.execute_script("arguments[0].click();", element)

        #         '''
        #         Find the Got it button on the pop up screen with search_tip and clicks 

        #         '''

        # def pop_up(self):
        #         self.driver.switch_to.frame('enlptp-0 hYAjiB popped')
        #         newsletter_pop_up = self.driver.find_element(by=By.XPATH, value='//*[@id="sc-1ebmiy2-0 dCqZTO"]')
        #         time.sleep(5)
        #         newsletter_pop_up.click()

        #         '''

        #         Finds the newsletter_pop_up and then clicks maybe later button 

        #         '''

    

#a.url_built()


""" 


# Find all the rows in the table
rows = table.find_elements(By.TAG_NAME, "tr")

# Iterate over the rows
for row in rows[1:]:  # Skip the first row, which is the table header
    # Find the name, symbol, and market cap of the cryptocurrency
    name = row.find_element(By.XPATH, './/*[@class="currency-name-container"]').text
    symbol = row.find_element(By.XPATH, './/*[@class="col-symbol"]').text
    market_cap = row.find_element(By.XPATH, './/*[@class="market-cap"]').text
    
    # Print the name, symbol, and market cap
    print(f"{name} ({symbol}): {market_cap}")

# Close the webdriver
driver.close() 
""" 