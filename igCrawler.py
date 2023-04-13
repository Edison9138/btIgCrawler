#pip install selenium
#pip install webdriver_manager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Specify the path of "chromedriver.exe"
# Remember to download the chromedriver 
PATH = "C:/Users/ediso/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Go to the IG login page
driver.get("https://www.instagram.com/")

# Get the places to enter username and password
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)

username.clear()
password.clear()

# Enter username and passward
username.send_keys("BeyondTaiwan")
password.send_keys("BeyondTW2020")

# Login in 
login = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
login.click()

# Wait for a bit
time.sleep(3)

# Go to BT homepage
driver.get("https://www.instagram.com/beyondtaiwan/")
time.sleep(5)

# Scroll down once. In this case, can get the data of the latest 33 posts
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(3)

# Select all posts
posts_elements = driver.find_elements(By.CLASS_NAME, "_aagu")
print("Number of posts get: ", len(posts_elements))

# List storing all posts and their data
posts = []

regular_posts = 0
non_regular_posts = 0

for post_element in posts_elements:
    driver.execute_script("arguments[0].click();", post_element)
    # post.click()
    time.sleep(2)

    try:
        # Select and click on the insight button
        view_insight_button = driver.find_element(By.XPATH, "//*[text()='View insights']")
        view_insight_button.click()
        regular_posts += 1

        time.sleep(2)

        insight_blocks = driver.find_elements(By.CLASS_NAME, "wbloks_1")
        num_insight_blocks = len(insight_blocks)
        print("number of insight blocks", len(insight_blocks))
        # If has "external link taps" will have 1 more "wbloks_1"

        # The parse structures of likes, comments, replies, and saves are the same
        # Likes
        likes_block = insight_blocks[14]
        likes_span = likes_block.find_element(By.XPATH, ".//span")
        likes = likes_span.text

        # Comments
        comments_block = insight_blocks[18]
        comments_span = comments_block.find_element(By.XPATH, ".//span")
        comments = comments_span.text

        # Replies
        replies_block = insight_blocks[22]
        replies_span = replies_block.find_element(By.XPATH, ".//span")
        replies = replies_span.text

        # Saves
        saves_block = insight_blocks[26]
        saves_span = saves_block.find_element(By.XPATH, ".//span")
        saves = saves_span.text
        print(likes, comments, replies, saves)

        # Interactions
        interactions_block = insight_blocks[36]
        interactions_spans = interactions_block.find_elements(By.XPATH, ".//span")
        interations = interactions_spans[0].text
        print(interations)

        # The parse structure of profile visits and external link taps are the same
        # Profile visits
        profile_visits_block = insight_blocks[37]
        profile_visits_spans = profile_visits_block.find_elements(By.XPATH, ".//span")
        profile_visits = profile_visits_spans[1].text
        print(profile_visits)

        # Omit External link taps since not every post has it
        # External link taps
        # external_link_taps_block = insight_blocks[38]
        # external_link_taps_spans = external_link_taps_block.find_elements(By.XPATH, ".//span")
        # external_link_taps = external_link_taps_spans[1].text
        # print(external_link_taps)

        # Account reach
        account_reach_block = insight_blocks[48] if num_insight_blocks == 55 else insight_blocks[47]
        account_reach_spans = account_reach_block.find_elements(By.XPATH, ".//span")
        account_reach = account_reach_spans[0].text
        account_reach_not_follow = account_reach_spans[2].text
        account_reach_not_follow = account_reach_not_follow[:account_reach_not_follow.index("%")]
        print(account_reach)
        print(account_reach_not_follow)

        # The parse structure of impressions, from home, from hashtags, from profile, from other, follows back are the same
        # Impressions 
        impressions_block = insight_blocks[49] if num_insight_blocks == 55 else insight_blocks[48]
        impressions_spans = impressions_block.find_elements(By.XPATH, ".//span")
        impressions = impressions_spans[1].text
        print(impressions)

        # Impressions from home
        impressions_from_home_block = insight_blocks[50] if num_insight_blocks == 55 else insight_blocks[49]
        impressions_from_home_spans = impressions_from_home_block.find_elements(By.XPATH, ".//span")
        impressions_from_home = impressions_from_home_spans[1].text
        print(impressions_from_home)

        # Impressions from hashtag
        impressions_from_hashtag_block = insight_blocks[51] if num_insight_blocks == 55 else insight_blocks[50]
        impressions_from_hashtag_spans = impressions_from_hashtag_block.find_elements(By.XPATH, ".//span")
        impressions_from_hashtag = impressions_from_hashtag_spans[1].text
    
        print(impressions_from_hashtag)

        # Impressions from profile
        impressions_from_profile_block = insight_blocks[51] if num_insight_blocks == 55 else insight_blocks[50]
        impressions_from_profile_spans = impressions_from_profile_block.find_elements(By.XPATH, ".//span")
        impressions_from_profile = impressions_from_profile_spans[1].text
        print(impressions_from_profile)

        # Impressions from other
        impressions_from_other_block = insight_blocks[52] if num_insight_blocks == 55 else insight_blocks[51]
        impressions_from_other_spans = impressions_from_other_block.find_elements(By.XPATH, ".//span")
        impressions_from_other = impressions_from_other_spans[1].text
        print(impressions_from_other)

        # Follows back
        follows_block = insight_blocks[53] if num_insight_blocks == 55 else insight_blocks[52]
        follows_block_spans = follows_block.find_elements(By.XPATH, ".//span")
        follows = follows_block_spans[1].text
        print(follows)

        # Impressions from profile
        impressions_from_profile_block = insight_blocks[52] if num_insight_blocks == 55 else insight_blocks[51]
        impressions_from_profile_spans = impressions_from_profile_block.find_elements(By.XPATH, ".//span")
        impressions_from_profile = impressions_from_profile_spans[1].text
        print(impressions_from_profile)

        # Impressions from other
        impressions_from_other_block = insight_blocks[53] if num_insight_blocks == 55 else insight_blocks[52]
        impressions_from_other_spans = impressions_from_other_block.find_elements(By.XPATH, ".//span")
        impressions_from_other = impressions_from_other_spans[1].text
        print(impressions_from_other)

        # Follows back
        follows_block = insight_blocks[54] if num_insight_blocks == 55 else insight_blocks[53]
        follows_block_spans = follows_block.find_elements(By.XPATH, ".//span")
        follows = follows_block_spans[1].text
        print(follows)

        post_data = [likes, comments, replies, saves, interations, profile_visits, account_reach, account_reach_not_follow,\
                impressions, impressions_from_home, impressions_from_profile, impressions_from_hashtag, impressions_from_other, follows]
        

        post_data = [data.replace(",", "") for data in post_data]
        posts.append(post_data)

        # Click the Chrome's go back button to close the post
        time.sleep(3)
        driver.execute_script("window.history.go(-1)") 
        time.sleep(3)

    except NoSuchElementException:
        non_regular_posts += 1
        # Click the Chrome's go back button to close the post
        time.sleep(2)
        driver.execute_script("window.history.go(-1)") 

print("Number of posts get: ", len(posts_elements))
print("Number of non-regular posts: ", non_regular_posts)
print("Number of regular posts: ", regular_posts)
df = pd.DataFrame(posts, columns=["likes", "comments", "replies", "saves", "interactions", "profile_visits", "account_reach", "account_reach_not_follow"\
                                , "impressions", "impressions_from_home", "impressions_from_hashtag", "impressions_from_profile", "impressions_from_other", "follows"])

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.width', None)  # Auto-expand the display
pd.set_option('display.expand_frame_repr', False)  # Prevent the dataframe from wrapping

df = df[~df["impressions"].str.contains(r'[^0-9]')]
for col in df.columns:
    df[col] = df[col].astype(int)
print(df)

today = date.today()
date_format = today.strftime("%b_%d")
df.to_excel("ig_post_data" + date_format + ".xlsx", index=False)
