import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import requests
import shutil

# line notify APIのトークン
line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
# line notify APIのエンドポイントの設定
line_notify_api = 'https://notify-api.line.me/api/notify'


def move_bin(
    fname: str, src_dir: str = "/var/task/bin", dest_dir: str = "/tmp/bin"
) -> None:
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest_file = os.path.join(dest_dir, fname)
    shutil.copy2(os.path.join(src_dir, fname), dest_file)
    os.chmod(dest_file, 0o775)


def create_driver(
    options: webdriver.chrome.options.Options,
) -> webdriver.chrome.webdriver:
    driver = webdriver.Chrome(
        executable_path="/tmp/bin/chromedriver", chrome_options=options
    )
    return driver


def lambda_handler(event, context):

    move_bin("headless-chromium")
    move_bin("chromedriver")
    options = Options()
    options.binary_location = "/tmp/bin/headless-chromium"
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--disable-application-cache")
    options.add_argument("--disable-infobars")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--enable-logging")
    options.add_argument("--log-level=0")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--homedir=/tmp")

    driver = create_driver(options)
    driver.get('https://select-type.com/rsv/?id=NU9l1ADZjFk')
    select_box = Select(driver.find_element_by_name('c_id'))
    select_box.select_by_value('141223')
    logging.basicConfig(level=logging.INFO)
    logging.info('calendar_log_info')
    for calendar_cell in driver.find_elements_by_class_name('symbol-gray'):
        if calendar_cell.text != '×':
            # ヘッダーの指定
            headers = {'Authorization': f'Bearer {line_notify_token}'}
            # 送信するデータの指定
            data = {'message': f'{"https://select-type.com/rsv/?id=NU9l1ADZjFk"}'}
            # line notify apiにpostリクエストを送る
            requests.post(line_notify_api, headers=headers, data=data)
            logging.info(calendar_cell.text)

    driver.close()
    driver.quit()

    return {
        'status_code': 200
    }


if __name__ == "__main__":
    print(lambda_handler(event=None, context=None))
