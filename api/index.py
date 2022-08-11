from flask import Flask, render_template,redirect,url_for
import asyncio
from pyppeteer import launch

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

async def run(url_code,url_id):
    browser = await launch({'headless': False},
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False
    )
    # browser = await launch({'headless': False})
    page = await browser.newPage()
    await page.goto('https://lordsmobile.igg.com/gifts/')
    await page.focus('#iggid')
    await page.keyboard.type(url_id)
    await page.focus('#cdkey_1')
    await page.keyboard.type(url_code)
    await page.click('[id="btn_claim_1"]');
    await page.click('[id="btn_msg_close"]');
    print("Code Redeemed...!!!")
    await browser.close()

@app.route('/', methods=['POST', 'GET'])
def Home():
    return render_template("home.html")

@app.route('/redeem/<url_code>/<url_id>', methods=['POST', 'GET'])
def redeem(url_code,url_id):
    global s_code
    # print("The Redeem Code :-", url_code)
    # print("The Redeem ID :-", url_id)
    if str(url_code) in list(s_code):
        return redirect(url_for('Home'))
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(run(url_code,url_id))
    s_code.add(str(url_code))
    return redirect(url_for('Home'))


if __name__ == '__main__':
    app.run(debug=True)

# import asyncio
# from pyppeteer import launch

# async def main():
#     browser = await launch({'headless': True})
#     page = await browser.newPage()
#     await page.goto('https://lordsmobile.igg.com/gifts/')
#     await page.focus('#iggid')
#     await page.keyboard.type('1234')
#     await page.focus('#cdkey_1')
#     await page.keyboard.type('atharv')
#     await page.click('[id="btn_claim_1"]');
#     await page.click('[id="btn_msg_close"]');
#     print("Code Redeemed...!!!")
#     await browser.close()

# asyncio.get_event_loop().run_until_complete(main())
