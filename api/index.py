from flask import Flask, render_template,redirect,url_for

app = Flask(__name__)
s_code=set()

# def fun(code,ID):
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.chrome.service import Service
#     # from time import localtime, strftime
#     # print("Task Start Time :- ",strftime("%Y-%m-%d %H:%M:%S", localtime()))
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
#     options = webdriver.ChromeOptions()
#     options.headless = False
#     options.add_argument(f'user-agent={user_agent}')
#     options.add_argument("--window-size=1920,1080")
#     options.add_argument('--ignore-certificate-errors')
#     options.add_argument('--allow-running-insecure-content')
#     options.add_argument("--disable-extensions")
#     options.add_argument("--proxy-server='direct://'")
#     options.add_argument("--proxy-bypass-list=*")
#     options.add_argument("--start-maximized")
#     options.add_argument('--disable-gpu')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--no-sandbox')
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])
#     try:
#         s=Service('G:/Projects/LM BOT/Python/api/chromedriver.exe')
#         driver = webdriver.Chrome(service=s,options=options)
#         driver.get("https://lordsmobile.igg.com/gifts/")
#         element = driver.find_element(By.ID, "iggid")
#         element.send_keys(int(ID))
#         element = driver.find_element(By.ID, "cdkey_1")
#         element.send_keys(code)
#         element = driver.find_element(By.ID, "btn_claim_1").click()
#         element = driver.find_element(By.ID, "btn_msg_close").click()
#         # print("Redeemption Attempt Completed in ID :-", int(ID))
#         driver.close()
#     except Exception as e:
#         print(e)
#     # print("Task End Time :- ",strftime("%Y-%m-%d %H:%M:%S", localtime()))


from playwright.sync_api import sync_playwright

def run(playwright,url_code,url_id):
    chromium = playwright.chromium
    browser = chromium.launch()
    page = browser.new_page()
    # page.screenshot(path="ss/initial.png", full_page=True)
    page.goto("https://lordsmobile.igg.com/gifts/")
    # page.screenshot(path="ss/screenshot.png", full_page=True)
    page.locator('#iggid').fill(url_id)
    # page.screenshot(path="ss/screenshot1.png", full_page=True)
    page.locator('#cdkey_1').fill(url_code)
    # page.screenshot(path="ss/screenshot2.png", full_page=True)
    page.locator('#btn_claim_1').click()
    # page.screenshot(path="ss/screenshot3.png", full_page=True)
    page.locator('#btn_msg_close').click()
    # page.screenshot(path="ss/screenshot4.png", full_page=True)
    print("Code Redeemed...!!!")
    browser.close()

@app.route('/', methods=['POST', 'GET'])
def Home():
    import os
    os.system('pip install playwright')
    os.system('npx playwright install')
    return render_template("home.html")

@app.route('/redeem/<url_code>/<url_id>', methods=['POST', 'GET'])
def redeem(url_code,url_id):
    global s_code
    # print("The Redeem Code :-", url_code)
    # print("The Redeem ID :-", url_id)
    if str(url_code) in list(s_code):
        return render_template("home.html")
    with sync_playwright() as playwright:
        run(playwright,url_code,url_id)
    s_code.add(str(url_code))
    return redirect(url_for('Home'))


if __name__ == '__main__':
    app.run(debug=True)