
http://www.cnblogs.com/syios/p/4762546.html
oauth 认证的一般过程：
第一步:获取未授权的Request Token (请求标记)  跳转到服务商的登录页面
第二步:获取用户授权Request Token(请求标记) 用户输入账号密码进行登录授权
第三步:用授权过的Request Token(请求标记)  换取Access Token (访问标记)
一般第一步带上参数 client_id 和 rediret_uri （这两个参数注册时会有）访问认证商提供的认证页面，然后用户会登陆认证；
第二步用户在该页面上授权后，会跳转到 redirect_uri，带上 code 参数；
第三步，redirect_uri 在获取到 code 后，带上 code 访问认证商提供的获取 access_token 的url，这时候要传递的参数包括：
client_id
client_secret
scope	（或者其他表示授权类型/范围的字段）
code
redirect_uri
这时候服务器会返回一个 access_token，一般会有过期时间和 uid，我们后续根据 uid 和 access_token 就可以访问该用户已授权的接口


首先，需要在 api 管理中心新建项目，然后进入项目的 api 管理
https://console.developers.google.com/apis/dashboard?project=qmovie-b7747&duration=PT1H
启用需要的 api 集，可以搜索查找没有列出的 api 集（比如 mirror）；

然后新建凭据，oauth web application ，随便取一个名字，可以获得一个
client_id  以及对应的 client_secret （在 api 管理器的凭据一栏，下载刚才创建的 client 凭据，会是一个 client_secrets.json 文件），
其中使用 oauth 授权时需要指定 scope， https://developers.google.com/identity/protocols/googlescopes
列出了所有的 scope，mirror 包括：
https://www.googleapis.com/auth/glass.timeline
用户身份信息包括（姓名等，这个就够了）：
https://www.googleapis.com/auth/userinfo.profile

接下来要使用这两项来通过 oauth 认证（中间会需要从网页上获取到一个 code，该 code 就是授权码，有了这个授权码，程序就可以获得一个 access_token，在通过 http 方式请求 google api 时，加上该 access_token 就可以通过认证，访问到被授权访问了的 scope（就是功能集），然后就可以按照 google 文档中提到的  http 示例发出请求；

https://developers.google.com/api-client-library/python/auth/web-app

其中，需要安装的库主要是  google-api-python-client   googleapiclient

在这个链接里可以测试所有 timeline 的请求：https://developers.google.com/apis-explorer/?hl=zh_CN#p/mirror/v1/


具体实现
根据文档
https://developers.google.com/api-client-library/python/auth/web-app
的步骤，可以一步步获取到 access_token；

实际上可以不添加 redirect_uri（配置的时候也要保持为空，这样需要用户在认证过后主动把code发过来），需要选择应用类型为 其他，如果是 web，则必须配置有 redirect_uri

https://developers.google.com/resources/api-libraries/documentation/mirror/v1/python/latest/mirror_v1.timeline.html
有所有接口的说明

通过
https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=ya29.Glt5BDo_u0mphps7VVGYYOqiPeBjrm3ObslyUWn-2y2ac_b1SYhgKc8LCxw6nLk6E6tH_Z1TQ51k392JcB8whByh1M9BuyLlrSFJG_AiFy0hcw_mYZINmoHmN-gK
可以获取到如下信息：
{
  ● id: "xxxx",
  ● name: "xxxx",
  ● given_name: "xxxx",
  ● family_name: "xxxx",
  ● link: "https://plus.google.com/1111111111111111111",
  ● picture: "https://lh4.googleusercontent.comxxxxxxxx/xx.jpg",
  ● locale: "en-US"
}

