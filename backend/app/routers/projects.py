"""
项目路由
项目 CRUD API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from decimal import Decimal

from ..database import get_db
from ..models import Project, Record, User
from ..schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    ProjectDetailResponse, ProjectListResponse, MessageResponse
)
from .auth import get_current_user

router = APIRouter(prefix="/api/v1/projects", tags=["项目"])


@router.get("", response_model=ProjectListResponse, summary="获取项目列表")
async def get_projects(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的项目列表
    - status: 筛选状态 (ongoing/completed)
    """
    query = db.query(Project).filter(Project.user_id == current_user.id)
    
    if status:
        query = query.filter(Project.status == status)
    
    projects = query.order_by(Project.created_at.desc()).all()
    
    return {
        "projects": projects,
        "total": len(projects)
    }


@router.get("/{project_id}", response_model=ProjectDetailResponse, summary="获取项目详情")
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目详情（包含关联记录）"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 计算人均费用
    avg_expense = Decimal('0')
    if project.member_count > 0:
        avg_expense = project.total_expense / project.member_count
    
    # 计算消费率
    expense_rate = 0.0
    if project.budget > 0:
        expense_rate = float(project.total_expense / project.budget * 100)
    
    # 获取关联记录
    records = db.query(Record).filter(
        Record.project_id == project_id
    ).order_by(Record.date.desc()).all()
    
    return ProjectDetailResponse(
        id=project.id,
        user_id=project.user_id,
        title=project.title,
        start_date=project.start_date,
        end_date=project.end_date,
        budget=project.budget,
        member_count=project.member_count,
        total_expense=project.total_expense,
        status=project.status,
        description=project.description,
        created_at=project.created_at,
        updated_at=project.updated_at,
        avg_expense=avg_expense,
        expense_rate=expense_rate,
        records=records
    )


@router.post("", response_model=ProjectResponse, summary="创建项目")
async def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新项目"""
    # 验证日期
    if project.end_date < project.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="结束日期不能早于开始日期"
        )
    
    db_project = Project(
        user_id=current_user.id,
        title=project.title,
        start_date=project.start_date,
        end_date=project.end_date,
        budget=project.budget,
        member_count=project.member_count,
        description=project.description,
        status="ongoing"
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse, summary="更新项目")
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新项目"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    # 更新字段
    update_data = project_update.model_dump(exclude_unset=True)
    
    # 验证日期
    if 'end_date' in update_data and 'start_date' not in update_data:
        if update_data['end_date'] < project.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束日期不能早于开始日期"
            )
    
    if 'start_date' in update_data and 'end_date' not in update_data:
        if project.end_date < update_data['start_date']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束日期不能早于开始日期"
            )
    
    if 'start_date' in update_data and 'end_date' in update_data:
        if update_data['end_date'] < update_data['start_date']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束日期不能早于开始日期"
            )
    
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    
    return project


@router.delete("/{project_id}", response_model=MessageResponse, summary="删除项目")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除项目（级联删除关联记录）"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    db.delete(project)
    db.commit()
    
    return MessageResponse(message="删除成功")


@router.post("/{project_id}/complete", response_model=ProjectResponse, summary="完成项目")
async def complete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """标记项目为已完成"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    project.status = "completed"
    db.commit()
    db.refresh(project)
    
    return project


@router.post("/{project_id}/reopen", response_model=ProjectResponse, summary="重新打开项目")
async def reopen_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """重新打开已完成的项目"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="项目不存在"
        )
    
    project.status = "ongoing"
    db.commit()
    db.refresh(project)
    
    return project
