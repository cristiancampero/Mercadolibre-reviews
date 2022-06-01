from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

class Scraper():

    def setUp(self):
        # setting to open chrome in background
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1024,768')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # open chrome browser
        self.driver = webdriver.Chrome(executable_path='C:/Users/usuario/Downloads/chromedriver.exe', options=options)
        # go to the page
        self.driver.get("https://www.mercadolibre.com.ar/noindex/catalog/reviews/MLA16060758?noIndex=true&access=view_all&modal=true&controlled=true")


    def close_cookie_banner(self):
        # accept cookies
        cookie = self.driver.find_element(By.CLASS_NAME, value="cookie-consent-banner-opt-out__action--key-accept")
        cookie.click()


    def total_reviews(self):
        # number of reviews and rating
        rating = self.driver.find_element(By.CLASS_NAME, value="ui-review-view__rating__summary__average").text
        average_reviews = self.driver.find_element(By.CLASS_NAME, value="ui-review-view__rating__summary__label").text

        print(f"\n{average_reviews}: {rating}")

        for i in range(5):
            levels_rating = self.driver.find_element(By.XPATH, value=f"/html/body/main/div/section/header/article/div/div[2]/ul/li[{i + 1}]/div[1]").text
            n_of_starts = self.driver.find_element(By.XPATH, value=f"/html/body/main/div/section/header/article/div/div[2]/ul/li[{i + 1}]/div[3]").text

            print(f"{levels_rating}: {n_of_starts}")
        

    def scroll_down(self):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


    def get_reviews(self):

        # create a dic to save the data
        self.all_reviews = []

        amount_of_reviews = self.driver.find_elements(By.CLASS_NAME, value=f"ui-review-view__comments__review-comment__title")
        print(f"\nExtracting {len(amount_of_reviews)} reviews:")
        
        for i in range(len(amount_of_reviews)):
            # get data from each review
            title = self.driver.find_element(By.XPATH, value=f"/html/body/main/div/section/div[2]/div[3]/div/div/div/article[{i + 1}]/h3").text
            
            review = self.driver.find_element(By.XPATH, value=f"/html/body/main/div/section/div[2]/div[3]/div/div/div/article[{i + 1}]/p").text
            
            starts = self.driver.find_element(By.XPATH, value=f"/html/body/main/div/section/div[2]/div[3]/div/div/div/article[{i + 1}]/div[1]/label").text
            
            likes = self.driver.find_element(By.XPATH, value=f"/html/body/main/div/section/div[2]/div[3]/div/div/div/article[{i + 1}]/div[2]/button[1]/span/p").text
            
            dislikes = self.driver.find_element(By.XPATH, value=f"/html/body/main/div/section/div[2]/div[3]/div/div/div/article[{i + 1}]/div[2]/button[2]/span/p").text

            # save data
            data = {
                "Title": title,
                "Review": review,
                "Stars": starts,
                "Likes": likes,
                "Dislikes": dislikes
            }

            # save each dictionary in a list
            self.all_reviews.append(data)


    def export_to_csv(self):
        # export to a csv file
        df = pd.DataFrame(self.all_reviews)
        df.to_csv("all_reviews.csv", sep=";")


    def tearDown(self):
        print('closing the browser...')
        sleep(1)
        self.driver.close()
        

if __name__ == "__main__":
    s = Scraper()
    s.setUp()
    s.close_cookie_banner()
    s.total_reviews()
    s.scroll_down()
    s.get_reviews()
    s.export_to_csv()
    s.tearDown()
