


from typing import Dict, List


class SignIn():

    def _sign_in(self,user_info:Dict[str,str]) ->bool:
        raise NotImplementedError("签到方法:'_sign_in(url)'没有实现")

    
    def signin_all(self) -> List[str]:
        raise NotImplementedError("多用户签到方法：'sign_in_all(user_infos)'没有实现")