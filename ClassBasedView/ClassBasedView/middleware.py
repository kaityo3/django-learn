import logging
from django.utils.deprecation import MiddlewareMixin
import time

application_logger = logging.getLogger("application-logger")
error_logger = logging.getLogger("error-logger")
performance_logger = logging.getLogger("performance-logger")

class MyMiddleware(MiddlewareMixin):
    # viewを呼び出す前に実行される
    def process_view(self, request, view_func, view_args, view_kwargs):
        # どのパスのviewが呼び出されたか確認することが出来る。
        # 応用すればどのUserがどの時間にアクセスしたかログを取ることも可能
        application_logger.info(request.get_full_path())
        # print(dir(request))

    # エラーが出力された際の処理
    def process_exception(self, request, exception):
        # エラーとトレースを出力
        error_logger.error(exception, exc_info=True)

class PerformanceMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        start_time = time.time()
        request.start_time = start_time

    # responceを返すときの処理の前に呼ばれる
    def process_template_response(self, request, response):
        print("処理")
        responce_time = time.time() - request.start_time
        performance_logger.info(f"{request.get_full_path()}: {responce_time}ms")
        return response
