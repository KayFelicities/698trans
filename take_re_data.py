from link_layer import *  # NOQA
import data_translate


def get_setnormal_res(data):
    offset = 0
    ret_dict = get_addr(data)
    offset += 5 + int(ret_dict['SA_len']) + 10
    if data[offset] == '00':
        return 'ok'
    else:
        return data_translate.dar_explain[data[offset]]
