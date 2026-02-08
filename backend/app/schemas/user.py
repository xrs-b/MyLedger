"""
用户 Schema
Pydantic 数据验证模型
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============ 请求 Schema ============

class UserCreate(BaseModel):
    """用户注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description="账号名")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    invite_code: str = Field(..., min_length=1, max_length=20, description="邀请码")


class UserLogin(BaseModel):
    """用户登录请求"""
    username: str = Field(..., description="账号名")
    password: str = Field(..., description="密码")


class UserUpdate(BaseModel):
    """用户更新请求"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    is_active: Optional[bool] = None


class ChangePassword(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=50, description="新密码")


# ============ 响应 Schema ============

class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    """用户详情响应（包含统计）"""
    record_count: int = 0
    project_count: int = 0


class InviteCodeCheck(BaseModel):
    """邀请码验证响应"""
    valid: bool
    message: str = ""


# ============ Token Schema ============

class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token 数据"""
    username: Optional[str] = None
    user_id: Optional[int] = None


# ============ 消息响应 ============

class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str


class RegisterResponse(BaseModel):
    """注册响应"""
    message: str
    is_admin: bool
    user: UserResponse


class LoginResponse(Token):
    """登录响应"""
    user: UserResponse
