from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
from twitter_api import twitter as tt
import random
import os


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=~/.config/chromium/Default')
    options.add_argument('--start-maximized');
    return webdriver.Chrome(executable_path='selenium_api/selenium_stuff/chromedriver', options=options)


def get_timestamp_str():
    return datetime.now().strftime('%H-%M')


def get_query():
    with open('selenium_api/tweet_search_params.txt') as f:
        return ' OR '.join([x.replace('\n', '') for x in f.readlines()])


def default_sleep():
    sleep(3.2)


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def run(n_follows):
    driver = get_driver()

    default_sleep()
    driver.get('https://www.twitter.com/')
    default_sleep()

    search_field = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/label/div[2]/div/input')
    search_field.send_keys(get_query())
    search_field.send_keys(Keys.ENTER)

    default_sleep()

    latest = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[2]')
    latest.click()

    default_sleep()

    bs = BeautifulSoup(driver.page_source, 'lxml')
    
    posts = bs.find('div', {'aria-label': 'Timeline: Search timeline'}).findChild('div').findChildren(recursive=False)
    profile_urls = []
    for p in posts:
        try:
            profile_urls.append(p.find('a', {'role': 'link'})['href'].replace('/', ''))
        except:
            pass

    if len(profile_urls) > n_follows:
        to_follow = profile_urls[:n_follows]
    else:
        to_follow = profile_urls

    for url in to_follow:
        print(f'url: {url}')
        
        driver.execute_script("window.open('');")

        default_sleep()

        driver.switch_to.window(driver.window_handles[1])
        driver.get(f'https://www.twitter.com/{url}')

        default_sleep()
        default_sleep()

        bs = BeautifulSoup(driver.page_source, 'lxml')
        follow_btn = bs.find('span', text='Follow')
        driver.find_element(By.XPATH, xpath_soup(follow_btn)).click()
        
        default_sleep()

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        default_sleep()
    
    return to_follow


def unfollow_and_save_new(timestamp, new_profiles):
    file_path = f'selenium_api/follow_lists/{timestamp}.txt'

    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            old_profiles = [int(x.replace('\n', '')) for x in f.readlines()]

        api = tt.get_api()
        for profile in old_profiles:
            try:
                api.destroy_friendship(screen_name=profile)
            except:
                pass
    
    if new_profiles is not None:
        with open(file_path, 'w+') as f:
            f.write('\n'.join(new_profiles))


if __name__ == '__main__':
    timestamp = get_timestamp_str()

    new_profiles = None
    if (random.randint(0, 3) == 0):
        sleep(random.randint(0, 180))
        new_profiles = run(random.randint(1, 3))
    
    unfollow_and_save_new(timestamp, new_profiles)
    

