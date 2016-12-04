from shared_functions import *  # NOQA


def ReportResponseList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    OAD_num = get_num_of_SEQUENCE(data[offset:], '上报的对象')
    offset += 1
    config.line_level += 1
    for OAD_count in range(OAD_num):
        end_flag = 1 if OAD_count == OAD_num - 1 else 0
        offset += take_OAD(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def ReportResponseRecordList(data):
    return ReportResponseList(data)


def ReportNotificationList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultNormal_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultNormal')
    offset += 1
    config.line_level += 1
    for A_ResultNormal_count in range(A_ResultNormal_num):
        end_flag = 1 if A_ResultNormal_count == A_ResultNormal_num - 1 else 0
        offset += take_A_ResultNormal(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset


def ReportNotificationRecordList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultRecord_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultNormal')
    offset += 1
    config.line_level += 1
    for A_ResultRecord_count in range(A_ResultRecord_num):
        end_flag = 1 if A_ResultRecord_count == A_ResultRecord_num - 1 else 0
        offset += take_A_ResultRecord(data[offset:], end_flag=end_flag)
    config.line_level -= 1
    return offset
