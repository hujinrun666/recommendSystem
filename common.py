import time
# 公共函数

# 定义装饰器，监控运行时间
def timmer(func):
    # *args表示任意多个无名参数
    # **kwargs表示任意多个关键字参数
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        stop_time = time.time()
        print('Func %s, run time: %s' % (func.__name__, stop_time - start_time))
        return res
    return wrapper