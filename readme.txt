
http://www.cnblogs.com/syios/p/4762546.html
oauth ��֤��һ����̣�
��һ��:��ȡδ��Ȩ��Request Token (������)  ��ת�������̵ĵ�¼ҳ��
�ڶ���:��ȡ�û���ȨRequest Token(������) �û������˺�������е�¼��Ȩ
������:����Ȩ����Request Token(������)  ��ȡAccess Token (���ʱ��)
һ���һ�����ϲ��� client_id �� rediret_uri ������������ע��ʱ���У�������֤���ṩ����֤ҳ�棬Ȼ���û����½��֤��
�ڶ����û��ڸ�ҳ������Ȩ�󣬻���ת�� redirect_uri������ code ������
��������redirect_uri �ڻ�ȡ�� code �󣬴��� code ������֤���ṩ�Ļ�ȡ access_token ��url����ʱ��Ҫ���ݵĲ���������
client_id
client_secret
scope	������������ʾ��Ȩ����/��Χ���ֶΣ�
code
redirect_uri
��ʱ��������᷵��һ�� access_token��һ����й���ʱ��� uid�����Ǻ������� uid �� access_token �Ϳ��Է��ʸ��û�����Ȩ�Ľӿ�


���ȣ���Ҫ�� api ���������½���Ŀ��Ȼ�������Ŀ�� api ����
https://console.developers.google.com/apis/dashboard?project=qmovie-b7747&duration=PT1H
������Ҫ�� api ����������������û���г��� api �������� mirror����

Ȼ���½�ƾ�ݣ�oauth web application �����ȡһ�����֣����Ի��һ��
client_id  �Լ���Ӧ�� client_secret ���� api ��������ƾ��һ�������ظղŴ����� client ƾ�ݣ�����һ�� client_secrets.json �ļ�����
����ʹ�� oauth ��Ȩʱ��Ҫָ�� scope�� https://developers.google.com/identity/protocols/googlescopes
�г������е� scope��mirror ������
https://www.googleapis.com/auth/glass.timeline
�û������Ϣ�����������ȣ�����͹��ˣ���
https://www.googleapis.com/auth/userinfo.profile

������Ҫʹ����������ͨ�� oauth ��֤���м����Ҫ����ҳ�ϻ�ȡ��һ�� code���� code ������Ȩ�룬���������Ȩ�룬����Ϳ��Ի��һ�� access_token����ͨ�� http ��ʽ���� google api ʱ�����ϸ� access_token �Ϳ���ͨ����֤�����ʵ�����Ȩ�����˵� scope�����ǹ��ܼ�����Ȼ��Ϳ��԰��� google �ĵ����ᵽ��  http ʾ����������

https://developers.google.com/api-client-library/python/auth/web-app

���У���Ҫ��װ�Ŀ���Ҫ��  google-api-python-client   googleapiclient

�������������Բ������� timeline ������https://developers.google.com/apis-explorer/?hl=zh_CN#p/mirror/v1/


����ʵ��
�����ĵ�
https://developers.google.com/api-client-library/python/auth/web-app
�Ĳ��裬����һ������ȡ�� access_token��

ʵ���Ͽ��Բ���� redirect_uri�����õ�ʱ��ҲҪ����Ϊ�գ�������Ҫ�û�����֤����������code������������Ҫѡ��Ӧ������Ϊ ����������� web������������� redirect_uri

https://developers.google.com/resources/api-libraries/documentation/mirror/v1/python/latest/mirror_v1.timeline.html
�����нӿڵ�˵��

ͨ��
https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=ya29.Glt5BDo_u0mphps7VVGYYOqiPeBjrm3ObslyUWn-2y2ac_b1SYhgKc8LCxw6nLk6E6tH_Z1TQ51k392JcB8whByh1M9BuyLlrSFJG_AiFy0hcw_mYZINmoHmN-gK
���Ի�ȡ��������Ϣ��
{
  �� id: "xxxx",
  �� name: "xxxx",
  �� given_name: "xxxx",
  �� family_name: "xxxx",
  �� link: "https://plus.google.com/1111111111111111111",
  �� picture: "https://lh4.googleusercontent.comxxxxxxxx/xx.jpg",
  �� locale: "en-US"
}

