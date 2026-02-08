"""
认证路由
用户注册、登录、JWT Token 管理
"""

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

from ..database import get_db
from ..models import User
from ..schemas.user import (
    UserCreate, UserLogin, UserResponse, Token, 
    RegisterResponse, LoginResponse, MessageResponse
)
import os

# 配置
SECRET_KEY = os.getenv("SECRET_KEY", "myleger-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7天
INVITE_CODE = "vip1123"

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 密码流
oauth2_scheme = OAuth2PasswordRequestForm(tokenUrl="/api/v1/auth/login")

# 路由
router = APIRouter(prefix="/api/v1/auth", tags=["认证"])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT Token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    """解码 JWT Token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": payload.get("sub"),
            "user_id": payload.get("user_id")
        }
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token 无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证用户身份",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = decode_token(token)
        username = token_data.get("username")
        if username is None:
            raise credentials_exception
    except HTTPException:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="账户已禁用")
    
    return user


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


# ============ API 端点 ============

@router.post("/register", response_model=RegisterResponse, summary="用户注册")
async def register(
    username: str = Form(..., min_length=3, max_length=50, description="账号名"),
    password: str = Form(..., min_length=6, max_length=50, description="密码"),
    invite_code: str = Form(..., min_length=1, max_length=20, description="邀请码"),
    db: Session = Depends(get_db)
):
    """
    用户注册
    
    - username: 账号名 (3-50字符)
    - password: 密码 (6-50字符)
    - invite_code: 邀请码 (固定: vip1123)
    
    第一个注册的用户自动成为管理员
    """
    # 验证邀请码
    if invite_code != INVITE_CODE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邀请码错误"
        )
    
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查是否是第一个用户（管理员）
    user_count = db.query(User).count()
    is_first_user = user_count == 0
    
    # 创建用户
    hashed_password = pwd_context.hash(password)
    new_user = User(
        username=username,
        password_hash=hashed_password,
        is_admin=is_first_user
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return RegisterResponse(
        message="注册成功",
        is_admin=is_first_user,
        user=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录 (OAuth2 密码流)
    
    - username: 账号名
    - password: 密码
    
    返回 JWT Token
    """
    # 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # 验证密码
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查账户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账户已禁用"
        )
    
    # 创建 Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse, summary="获取当前用户")
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return UserResponse.model_validate(current_user)


@router.post("/logout", response_model=MessageResponse, summary="退出登录")
async def logout():
    """
    退出登录
    
    前端删除 Token 即可，服务端无需处理
    """
    return MessageResponse(message="退出成功")


@router.post("/refresh", response_model=Token, summary="刷新 Token")
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    刷新 Token
    
    使用当前用户信息生成新的 Token
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username, "user_id": current_user.id},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
