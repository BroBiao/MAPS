from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time



class Metamask(object):

    def __init__(self, driver):
        self.driver = driver

    # unlock metamask
    def unlock_wallet(self, password):
        pw = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
        pw.send_keys(password)
        unlock_btn = self.driver.find_element(By.XPATH, '//button[normalize-space()="登录"]')
        unlock_btn.click()
        self.close_all_popup()

    # check native token balance
    def get_native_balance(self):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="代币"]'))).click()
        except ElementClickInterceptedException:
            self.close_all_popup()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="代币"]'))).click()
        balance = self.driver.find_element(By.XPATH, '//p[@data-testid="multichain-token-list-item-value"]')
        balance = balance.text.split(' ')[0]
        return float(balance)

    # add new account and copy address
    def add_new_account(self):
        try:
            account_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'button.mm-box:nth-child(2)')))
            account_btn.click()
        except ElementClickInterceptedException:
            self.close_all_popup()
            account_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'button.mm-box:nth-child(2)')))
            account_btn.click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
            '//button[normalize-space()="Add account or hardware wallet"]'))).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
            '//button[normalize-space()="Add a new account"]'))).click()

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
            '//button[normalize-space()="创建"]'))).click()

        copy_addr_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
            'button.mm-text:nth-child(1)')))
        copy_addr_btn.click()

    # switch to previous account
    def switch_account(self, index):
        try:
            account_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'button.mm-box:nth-child(2)')))
        except ElementClickInterceptedException:
            self.close_all_popup()
            account_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'button.mm-box:nth-child(2)')))
        account_btn.click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.multichain-account-menu-popover__list')))
        all_accounts = self.driver.find_elements(By.CSS_SELECTOR, 'div.multichain-account-menu-popover__list--menu-item')
        target_account = all_accounts[index]
        target_account.click()

    # conncect in metamask
    def connect_account(self, index=-1):
        self.close_all_popup()
        WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'choose-account-list__list')))
        all_accounts = self.driver.find_elements(By.CLASS_NAME, 'choose-account-list__account')
        if len(all_accounts) > 1:
            # select all accounts
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
                '//input[@data-testid="choose-account-list-operate-all-check-box"]'))).click()
            time.sleep(0.5)
            # unselect all account
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
                '//input[@data-testid="choose-account-list-operate-all-check-box"]'))).click()
            target_account = self.driver.find_elements(By.CSS_SELECTOR, '.check-box.choose-account-list__list-check-box.far.fa-square')[index]
            target_account.click()
        else:
            pass
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="下一步"]'))).click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="连接"]'))).click()

    def import_token(self, token_address, token_name):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="代币"]'))).click()
        except ElementClickInterceptedException:
            self.close_all_popup()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="代币"]'))).click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="添加代币"]'))).click()
        token_addr = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.mm-box")))
        token_addr.send_keys(token_address)
        token_ticker = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 
            "div.box--padding-top-4:nth-child(1) > div:nth-child(2) > input:nth-child(1)")))
        time.sleep(2)
        if token_ticker.get_attribute('value') == token_name:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="下一步"]'))).click()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="导入"]'))).click()

    def send_token(self, token_name, recv_addr='clipboard', amount='max'):
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="代币"]'))).click()
        except ElementClickInterceptedException:
            self.close_all_popup()
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="代币"]'))).click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'//p[normalize-space()="{token_name}"]'))).click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, f'//p[normalize-space()="发送"]'))).click()
        recv_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ens-input__wrapper__input")))
        time.sleep(0.5)
        if recv_addr == 'clipboard':
            recv_input.send_keys(Keys.CONTROL + 'v')
        else:
            recv_input.send_keys(recv_addr)
        WebDriverWait(self.driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "mm-box.loading-overlay")))
        if amount == 'max':
            max_btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".send-v2__amount-max")))
            time.sleep(1)
            max_btn.click()
            time.sleep(2)
        else:
            amount_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, 
                '//input[@data-testid="currency-input"]')))
            amount_input.send_keys(str(amount))
        WebDriverWait(self.driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "mm-box.loading-overlay")))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//button[normalize-space()="下一步"]'))).click()
        WebDriverWait(self.driver, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "mm-box.loading-overlay")))
        # time.sleep(1)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//button[normalize-space()="确认"]'))).click()
        while True:
            try:
                res = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 
                    "div.activity-list-item:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2)")))
                tx_res = res.text
                if tx_res == '已确认':
                    return 'success'
                elif tx_res == '失败':
                    return 'fail'
                else:
                    time.sleep(1)
                    continue
            except:
                continue

    def disconnect_account(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="账户选项"]'))).click()
        except ElementClickInterceptedException:
            self.close_all_popup()
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="账户选项"]'))).click()
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, 
            '//button[@data-testid="global-menu-connected-sites"]'))).click()
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, f'//a[normalize-space()="断开连接"]'))).click()
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="断开连接"]'))).click()

    def close_all_popup(self):
        try:
            while True:
                WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'popover-wrap')))
                WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//button[normalize-space()="明白了"]'))).click()
                time.sleep(1)
        except:
            pass