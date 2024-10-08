import json
from urllib import parse

from fastapi import Header, HTTPException

from sduojApi import contestIdToGroupIdList, examIdToGroupIdList
from type.functions import get_ps_group, get_current_groups
from utils.utilsTime import afterTime


def is_superadmin(SDUOJUserInfo):
    return "superadmin" in SDUOJUserInfo["roles"]


def is_admin(SDUOJUserInfo):
    return is_superadmin(SDUOJUserInfo) or "admin" in SDUOJUserInfo["roles"]


def is_role_member(role_group_id, groups):
    return role_group_id in groups


async def judge_in_groups(ct_id, e_id, psid, groups, SDUOJUserInfo, TAgroup, mode=0):
    current_groups = get_current_groups(ct_id, e_id, psid)
    groups = [int(num) for num in groups]
    c_group = list(set(current_groups) & set(groups))  # 获取与用户组重叠的部分，判断用户是否在组里
    if mode == 1:  # 组里成员可以但是admin与TA不可以
        if not c_group or is_admin(SDUOJUserInfo) or TAgroup in groups:
            raise HTTPException(status_code=403, detail="Permission Denial")
    elif mode == 0:  # 组里成员和admin和TA都可以
        if not c_group and not is_admin(SDUOJUserInfo) and not TAgroup in groups:
            raise HTTPException(status_code=403, detail="Permission Denial")
        return is_admin(SDUOJUserInfo), TAgroup in groups
    elif mode == 2:  # 组里成员和TA可以, admin不可以
        if (not c_group and TAgroup in groups) or is_admin(SDUOJUserInfo):
            raise HTTPException(status_code=403, detail="Permission Denial")


def is_manager(obj, SDUOJUserInfo):
    # 超级管理员
    if is_superadmin(SDUOJUserInfo):
        return

    # 创建者 或 管理组成员
    if obj.username == SDUOJUserInfo["username"] or \
            obj.manageGroupId in SDUOJUserInfo["groups"]:
        return

    raise HTTPException(detail="Permission Denial", status_code=403)


def in_group(groupId, SDUOJUserInfo):
    if is_superadmin(SDUOJUserInfo):
        return
    if groupId not in SDUOJUserInfo["groups"]:
        raise HTTPException(detail="Permission Denial", status_code=403)


# 用户是否可以查看题单信息
# 开启报告模式，则题单始终可查
# 关闭报告模式，题单在任意题组的作答时间内可查

# 判断题组的提交权限
# 题组只有在【作答时间内】&&【未交卷】才可以提交，
def manager(SDUOJUserInfo):
    if not is_admin(SDUOJUserInfo):
        raise HTTPException(detail="Permission Denial", status_code=403)


def cover_header(SDUOJUserInfo=Header(None)):
    try:
        return json.loads(json.loads(parse.unquote(SDUOJUserInfo)))
    except:
        raise HTTPException(detail="Permission Denial", status_code=403)


def parse_header(SDUOJUserInfo):
    try:
        return parse.quote(json.dumps(SDUOJUserInfo))
    except:
        raise HTTPException(detail="Gateway Message Error", status_code=500)

# original_string = '''{"userId":8853,"username":"testTA","nickname":"1","email":"12@qq.com","studentId":"sducs1","roles":["admin,user"],"groups":[63,64],"ipv4":"127.0.0.1","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"}'''
# encode = parse_header(original_string)
# print(encode)
# print(cover_header(encode)['userId'])
