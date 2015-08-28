# crack_wordpress
>wordpress暴力破解工具
>1.参数化操作
>2.内置两种暴力破解方式，通过wp-login模拟发包登录或者采用xmlrpc.php post数据包均可。
>3.内置自动获取用户名功能。/?author=1 还有rss >两种方式获取。由于wp主题众多，匹配正则太少，所以会不准。配合百度爬虫试了一下效果，准确率70%。

>使用方法：
>新建pass.txt并且添加测试密码。
>-u 后面接wp的url 记得带上http://
>-a 后面跟用户名 默认是admin
>-g 自动判断管理员用户名，准确率较低。获取用户名后自动退出。
>-w 用 /wp-login.php 模拟后台网页登录
>-x 用 /xmlrpc.php接口 POST登录
