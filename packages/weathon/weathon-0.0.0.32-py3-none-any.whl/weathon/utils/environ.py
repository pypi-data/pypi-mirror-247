# -*- coding: utf-8 -*-
# @Time    : 2022/10/9 21:27
# @Author  : LiZhen
# @FileName: environment_utils.py
# @github  : https://github.com/Lizhen0628
# @Description:

import os
import random
import numpy as np



def set_seed(seed: int = 7) -> None:
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    # torch.manual_seed(seed)
    # torch.cuda.manual_seed(seed)
    # torch.backends.cudnn.deterministic = True

def set_tokenizer() -> None:
    set_environ("TOKENIZERS_PARALLELISM", "false")


def init_environ() -> None:
    set_tokenizer()
    set_seed()



def set_environ(key,val) -> str:
    return os.environ.setdefault(key, val)


def get_environ(key,default_value="") -> str:
    """
    根据key 获取环境变量中的值
    """
    return os.environ.get(key,default_value)