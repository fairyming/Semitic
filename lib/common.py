from functools import reduce

# 字典列表去重
def list_dict_duplicate_removal(data_list):
    def run_function(x, y): return x if y in x else x + [y]
    return reduce(run_function, [[], ] + data_list)

# msg转换为字典
def deal_msg(msg):
    msg_dict = dict()
    tmp = msg.split('|')
    for i in tmp:
        msg_dict[i.split(":")[0]] = i.split(":")[1]
    return msg_dict