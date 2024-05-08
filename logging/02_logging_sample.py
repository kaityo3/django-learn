import logging

logger = logging.getLogger(__name__)
# loggerの閾値
logger.setLevel(logging.DEBUG)

# handler-ログを出力するためのハンドラーを定義する(loggerへの設定は最後)
# ターミナルへの出力を担う
s_handler = logging.StreamHandler()
# ファイルへのログ出力を担う
f_handler = logging.FileHandler('logging2.log', encoding='utf-8')

# 各ハンドラーのログレベルを設定する
s_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Formatter - 各ハンドラーのフォーマットを定義する(ハンドラーへの登録はあと)
s_formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
f_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')

# handlerにformatterを設定する
s_handler.setFormatter(s_formatter)
f_handler.setFormatter(f_formatter)

# loggerにhandlerを設定する
logger.addHandler(s_handler)
logger.addHandler(f_handler)


logger.debug('デバッグログ')
logger.info('インフォログ')
logger.warning('ワーニングログ')
logger.error('エラーログ')
logger.critical('クリティカルログ')

a = 10
b = 0
try:
    c = a / b
except Exception as e:
    # exe_info=Trueとすると、トレースまでログに取得される
    logger.error(e, exc_info=True)
