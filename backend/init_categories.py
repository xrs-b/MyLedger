#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分类初始化脚本
创建默认分类和支付方式数据
"""

import sys
import os

# 添加后端路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, init_db
from app.models import Category, CategoryItem, PaymentMethod


# 支出分类
EXPENSE_CATEGORIES = [
    ("餐饮", "food", 1, [
        ("外卖/餐厅", 1),
        ("食材杂货", 2),
        ("饮料零食", 3),
        ("下午茶/咖啡", 4),
    ]),
    ("交通", "transport", 2, [
        ("飞机", 1),
        ("高铁", 2),
        ("地铁/公交", 3),
        ("打车/自驾", 4),
        ("共享单车", 5),
    ]),
    ("购物", "shopping", 3, [
        ("服装/鞋子", 1),
        ("电子产品", 2),
        ("日用品", 3),
        ("化妆品", 4),
        ("家居用品", 5),
    ]),
    ("娱乐", "entertainment", 4, [
        ("电影/演出", 1),
        ("游戏/充值", 2),
        ("旅游/门票", 3),
        ("运动健身", 4),
    ]),
    ("住房", "housing", 5, [
        ("房租/房贷", 1),
        ("水电费", 2),
        ("物业费", 3),
        ("装修材料", 4),
    ]),
    ("通讯", "communication", 6, [
        ("电话费", 1),
        ("网络费", 2),
    ]),
    ("人情", "social", 7, [
        ("送礼", 1),
        ("红包/份子钱", 2),
        ("聚会请客", 3),
    ]),
    ("医疗", "medical", 8, [
        ("药品", 1),
        ("医院/诊所", 2),
        ("保健品", 3),
    ]),
    ("教育", "education", 9, [
        ("学费/培训费", 1),
        ("书籍/资料", 2),
        ("学习用品", 3),
    ]),
    ("其他", "other", 10, [
        ("宠物", 1),
        ("理财亏损", 2),
        ("捐款", 3),
        ("罚款", 4),
        ("未知消费", 5),
    ]),
]

# 收入分类
INCOME_CATEGORIES = [
    ("工资", "salary", 1, [
        ("固定工资", 1),
        ("奖金/提成", 2),
        ("加班费", 3),
    ]),
    ("副业", "side_hustle", 2, [
        ("兼职", 1),
        ("自由职业", 2),
        ("卖二手", 3),
    ]),
    ("投资", "investment", 3, [
        ("股票收益", 1),
        ("基金收益", 2),
        ("利息收入", 3),
    ]),
    ("其他", "other", 4, [
        ("红包收入", 1),
        ("退款", 2),
        ("报销", 3),
        ("意外之财", 4),
    ]),
]

# 支付方式
PAYMENT_METHODS = [
    ("现金", "cash", 1),
    ("银行卡", "card", 2),
    ("支付宝", "alipay", 3),
    ("微信", "wechat", 4),
    ("信用卡", "credit_card", 5),
    ("电子钱包", "e_wallet", 6),
]


def seed_categories(db: Session):
    """插入分类数据"""
    total_items = 0
    
    # 支出分类
    for name, icon, sort_order, items in EXPENSE_CATEGORIES:
        category = db.query(Category).filter(
            Category.name == name,
            Category.type == 'expense'
        ).first()
        
        if not category:
            category = Category(
                name=name,
                type='expense',
                icon=icon,
                sort_order=sort_order
            )
            db.add(category)
            db.flush()
        
        # 二级分类
        for item_name, item_order in items:
            existing = db.query(CategoryItem).filter(
                CategoryItem.category_id == category.id,
                CategoryItem.name == item_name
            ).first()
            
            if not existing:
                db_item = CategoryItem(
                    category_id=category.id,
                    name=item_name,
                    sort_order=item_order
                )
                db.add(db_item)
                total_items += 1
    
    # 收入分类
    for name, icon, sort_order, items in INCOME_CATEGORIES:
        category = db.query(Category).filter(
            Category.name == name,
            Category.type == 'income'
        ).first()
        
        if not category:
            category = Category(
                name=name,
                type='income',
                icon=icon,
                sort_order=sort_order
            )
            db.add(category)
            db.flush()
        
        # 二级分类
        for item_name, item_order in items:
            existing = db.query(CategoryItem).filter(
                CategoryItem.category_id == category.id,
                CategoryItem.name == item_name
            ).first()
            
            if not existing:
                db_item = CategoryItem(
                    category_id=category.id,
                    name=item_name,
                    sort_order=item_order
                )
                db.add(db_item)
                total_items += 1
    
    return total_items


def seed_payment_methods(db: Session):
    """插入支付方式数据"""
    count = 0
    
    for name, icon, sort_order in PAYMENT_METHODS:
        existing = db.query(PaymentMethod).filter(PaymentMethod.name == name).first()
        
        if not existing:
            pm = PaymentMethod(
                name=name,
                icon=icon,
                sort_order=sort_order
            )
            db.add(pm)
            count += 1
    
    return count


def main():
    """主函数"""
    print("=" * 50)
    print("  MyLedger - 分类数据初始化")
    print("=" * 50)
    print()
    
    # 初始化数据库表
    print("📊 正在创建数据库表...")
    init_db()
    print("  ✅ 数据库表创建完成")
    
    # 获取数据库会话
    db = SessionLocal()
    
    try:
        # 插入分类
        print()
        print("📂 正在插入分类数据...")
        items_count = seed_categories(db)
        print(f"  ✅ 插入 {items_count} 个二级分类")
        
        # 插入支付方式
        print()
        print("💳 正在插入支付方式...")
        pm_count = seed_payment_methods(db)
        print(f"  ✅ 插入 {pm_count} 个支付方式")
        
        # 提交事务
        db.commit()
        
        # 统计
        cat_count = db.query(Category).count()
        item_count = db.query(CategoryItem).count()
        pm_count = db.query(PaymentMethod).count()
        
        print()
        print("=" * 50)
        print("  ✅ 初始化完成!")
        print()
        print(f"  📂 一级分类: {cat_count} 个")
        print(f"  📝 二级分类: {item_count} 个")
        print(f"  💳 支付方式: {pm_count} 个")
        print("=" * 50)
        
    except Exception as e:
        db.rollback()
        print(f"  ❌ 错误: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
