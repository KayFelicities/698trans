from shared_functions import *  # NOQA


def ReportResponseList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    OAD_num = get_num_of_SEQUENCE(data[offset:], '上报的对象')
    offset += 1
    for OAD_count in range(OAD_num):
        offset += take_OAD(data[offset:])
    return offset


def ReportResponseRecordList(data):
    return ReportResponseList(data)


def ReportNotificationList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultNormal_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultNormal')
    offset += 1
    for A_ResultNormal_count in range(A_ResultNormal_num):
        offset += take_A_ResultNormal(data[offset:])
    return offset


def ReportNotificationRecordList(data):
    offset = 0
    offset += take_PIID_ACD(data[offset:])
    A_ResultRecord_num = get_num_of_SEQUENCE(data[offset:], 'A_ResultNormal')
    offset += 1
    for A_ResultRecord_count in range(A_ResultRecord_num):
        offset += take_A_ResultRecord(data[offset:])
    return offset
