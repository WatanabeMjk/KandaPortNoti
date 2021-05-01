import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
import requests


def lambda_handler(event, context):
    # line notify APIのトークン
    line_notify_token = os.getenv("LINE_NOTIFY_TOKEN")
    # line notify APIのエンドポイントの設定
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headless_chromium = os.getenv('HEADLESS_CHROMIUM', '')
    driver = os.getenv('CHROMEDRIVER', '')
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
