import logging

logging.basicConfig(
    # 書き出されるlogレベルを変更出来る
    level=logging.WARNING, filename='sample.log',
    # 書出しモード、フォーマット：実行時間、プロセス、ログのレベル、出力するメッセージ
    filemode='w', format='%(asctime)s-%(process)s-%(levelname)s-%(message)s'
)

logging.debug('debug.log')
logging.info('info.log')
logging.warning('warning.log')
logging.error('error.log')
logging.critical('critical.log')

user = 'Taro'
# 変数埋め込みも可能
logging.error(f'user = {user} raised error')

a = 10
b = 0
try:
    c = a / b
except Exception as e:
    # exe_info=Trueとすると、トレースまでログに取得される
    logging.error(e, exc_info=True)
