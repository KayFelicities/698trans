import link_layer
import data_translate


def read_set_dar(re_text):
    data = link_layer.data_format(re_text)
    offset = 0
    ret_dict = link_layer.get_addr(data)
    offset += 5 + int(ret_dict['SA_len']) + 10
    if data[offset] == '00':
        return 'ok'
    else:
        return data_translate.dar_explain[data[offset]]


def get_ip(data):
    ip_text = ''
    for ip_section in data[0: 4]:
        ip_text += str(int(ip_section, 16)) + '.'
    return ip_text[: -1]


def format_ip(ip_text):
    ip_list = ip_text.replace(' ', '').split('.')
    text = ''
    for ip in ip_list:
        text += str('%02X' % int(ip))
    return text


def get_octet(data):
    offset = 1  # type
    octet_len = int(data[offset], 16)
    offset += 1
    octet_text = ''
    for i in range(octet_len):
        octet_text += data[offset + i]
    offset += octet_len
    return {'octet': octet_text, 'offset': offset}


def format_octet(octet_text):
    octet = octet_text.replace(' ', '')
    if len(octet) % 2 == 1:
        octet += 'F'
    octet_len_text = '%02X' % (len(octet) // 2)
    text = '09' + octet_len_text + octet
    return text
