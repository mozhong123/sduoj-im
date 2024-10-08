from typing import Union, Optional

from pydantic import BaseModel, ConfigDict


class base_interface(BaseModel):
    e_id: Optional[int] = None
    ct_id: Optional[int] = None
    psid: Optional[int] = None


class notice_information_interface(BaseModel):
    nt_title: str
    nt_content: str


class notice_delete_interface(BaseModel):
    nt_id: int


class notice_add_interface(notice_information_interface, base_interface):
    username: str
    up_username: str


class notice_user_add_interface(notice_delete_interface):
    username: str


class notice_update_interface(notice_information_interface, notice_delete_interface):
    up_username: str
