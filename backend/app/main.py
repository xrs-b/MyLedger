"""
MyLedger 后端 API
移动账本后端服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入路由
from .routers import auth, categories, records, projects, statistics, admin

app = FastAPI(
    title="MyLedger API",
    description="移动账本后端 API",
    version="1.0.0"
)

# CORS 配置 - 允许所有来源（开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(records.router)
app.include_router(projects.router)
app.include_router(statistics.router)
app.include_router(admin.router)


@app.get("/health")
async def health():
    """健康检查接口"""
    return {
        "status": "ok",
        "message": "MyLedger API is running"
    }


@app.get("/")
async def root():
    """根路径返回版本信息"""
    return {
        "name": "MyLedger",
        "version": "1.0.0",
        "description": "移动端记账应用"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=888)
