#从app模块中导入app应用
from app import manager

#防止被引用后执行，只有在当前模块中才可以使用
# python myblog.py runserver
if __name__=='__main__':
    manager.run()