from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
import time


class TokenAli:
    @staticmethod
    def take_token(token_json_file_path):
        file = open(token_json_file_path, mode='r', encoding='UTF-8')
        file_content = file.read()
        file.close()
        if file_content.strip() != "":
            response_json = json.loads(file_content)
            now = int(time.time())
            exp_time = response_json["Token"]["ExpireTime"]
            if exp_time - now < 60:  # 如果token60秒后过期
                accesskey_id = "LTAIYZfnAG47b1hw"
                accesskey_seceret = "b54UIjMRok0bqKd7mrHgtaNBjl6vk0"
                # 创建AcsClient实例
                client = AcsClient(
                    accesskey_id,
                    accesskey_seceret,
                    "cn-shanghai"
                )
                # 创建request，并设置参数。
                request = CommonRequest()
                request.set_method('POST')
                request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
                request.set_version('2019-02-28')
                request.set_action_name('CreateToken')
                response = client.do_action_with_exception(request)
                response_str = str(response, "utf-8")
                file_w = open(token_json_file_path, mode='w', encoding='UTF-8')
                file_w.write(response_str)
                file_w.close()
                return json.loads(response_str)["Token"]["Id"]
            else:
                return response_json["Token"]["Id"]

        else:
            accesskey_id = "LTAIYZfnAG47b1hw"
            accesskey_seceret = "b54UIjMRok0bqKd7mrHgtaNBjl6vk0"
            # 创建AcsClient实例
            client = AcsClient(
                accesskey_id,
                accesskey_seceret,
                "cn-shanghai"
            )
            # 创建request，并设置参数。
            request = CommonRequest()
            request.set_method('POST')
            request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
            request.set_version('2019-02-28')
            request.set_action_name('CreateToken')
            response = client.do_action_with_exception(request)
            response_str = str(response, "utf-8")
            file_w = open(token_json_file_path, mode='w', encoding='UTF-8')
            file_w.write(response_str)
            file_w.close()
            return json.loads(response_str)["Token"]["Id"]
