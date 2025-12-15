"""
API服务器
提供RESTful API接口，集成所有功能模块
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import uvicorn
import asyncio
import jwt
from datetime import datetime, timedelta
import logging

# 导入模块
from ..core_modules.topic_analyzer import TopicAnalyzer
from ..core_modules.content_generator import ContentGenerator
from ..core_modules.seo_optimizer import SEOOptimizer
from ..core_modules.auto_publisher import AutoPublisher
from ..workflow.automation_engine import AutomationEngine

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('APIServer')

# 初始化FastAPI
app = FastAPI(
    title="微信公众号AI写作系统",
    description="基于AI的微信公众号自动化写作系统API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT配置
JWT_SECRET_KEY = "your-secret-key"
JWT_ALGORITHM = "HS256"
security = HTTPBearer()

# 全局变量
automation_engine = None
modules = {}

# 请求模型
class TopicAnalysisRequest(BaseModel):
    topic: str = Field(..., description="分析的主题")
    account_id: Optional[str] = Field(None, description="公众号ID")

class ContentGenerationRequest(BaseModel):
    topic: str = Field(..., description="文章主题")
    outline: Optional[Dict] = Field(None, description="文章大纲")
    style: Optional[str] = Field("professional", description="写作风格")
    word_count: Optional[int] = Field(2000, description="字数目标")
    keywords: Optional[List[str]] = Field(None, description="关键词列表")

class SEOOptimizationRequest(BaseModel):
    article_id: str = Field(..., description="文章ID")
    keywords: List[str] = Field(..., description="目标关键词")
    target_audience: Optional[str] = Field(None, description="目标受众")

class PublishRequest(BaseModel):
    article_id: str = Field(..., description="文章ID")
    account_id: str = Field(..., description="发布账号ID")
    publish_time: Optional[datetime] = Field(None, description="定时发布时间")

class TaskRequest(BaseModel):
    task_type: str = Field(..., description="任务类型")
    parameters: Dict = Field(..., description="任务参数")

# 响应模型
class APIResponse(BaseModel):
    success: bool = Field(True, description="是否成功")
    message: str = Field("操作成功", description="响应消息")
    data: Optional[Dict] = Field(None, description="响应数据")
    error: Optional[str] = Field(None, description="错误信息")

# JWT认证
def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """获取当前用户"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的认证信息")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="无效的认证信息")

# 初始化函数
@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    global automation_engine, modules

    logger.info("正在初始化API服务器...")

    # 初始化配置
    config = {
        'worker_count': 3,
        'database': {
            'host': 'localhost',
            'port': 3306,
            'database': 'wechat_writer',
            'username': 'root',
            'password': 'password'
        },
        'api_keys': {
            'openai': 'your-openai-key',
            'claude': 'your-claude-key',
            'wechat': 'your-wechat-key'
        }
    }

    # 初始化模块
    modules['topic_analyzer'] = TopicAnalyzer(config)
    modules['content_generator'] = ContentGenerator(config)
    modules['seo_optimizer'] = SEOOptimizer(config)
    modules['auto_publisher'] = AutoPublisher(config)

    # 初始化自动化引擎
    automation_engine = AutomationEngine(config)
    await automation_engine.initialize()

    logger.info("API服务器初始化完成")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理"""
    global automation_engine

    if automation_engine:
        await automation_engine.stop()
        logger.info("自动化引擎已停止")

# API路由

@app.get("/", response_model=APIResponse)
async def root():
    """根路径"""
    return APIResponse(
        message="微信公众号AI写作系统API",
        data={
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "analyze_topic": "/api/v1/topics/analyze",
                "generate_content": "/api/v1/content/generate",
                "optimize_seo": "/api/v1/content/optimize-seo",
                "publish": "/api/v1/content/publish",
                "tasks": "/api/v1/tasks",
                "automation": "/api/v1/automation"
            }
        }
    )

@app.post("/api/v1/auth/login", response_model=APIResponse)
async def login(username: str, password: str):
    """用户登录"""
    # 这里应该验证用户凭据
    if username and password:  # 简化验证
        access_token = create_access_token(data={"sub": username})
        return APIResponse(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 86400
            }
        )
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

@app.post("/api/v1/topics/analyze", response_model=APIResponse)
async def analyze_topic(
    request: TopicAnalysisRequest,
    username: str = Depends(get_current_user)
):
    """分析选题"""
    try:
        # 获取账号信息
        account_info = await get_account_info(request.account_id or "default")

        # 执行分析
        analysis = await modules['topic_analyzer'].analyze_topic(
            request.topic,
            account_info
        )

        return APIResponse(
            message="选题分析完成",
            data=analysis
        )
    except Exception as e:
        logger.error(f"选题分析失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/content/generate", response_model=APIResponse)
async def generate_content(
    request: ContentGenerationRequest,
    username: str = Depends(get_current_user)
):
    """生成内容"""
    try:
        # 生成文章
        article = await modules['content_generator'].generate_article(
            topic=request.topic,
            outline=request.outline,
            style=request.style,
            word_count=request.word_count,
            keywords=request.keywords
        )

        # 保存草稿
        draft_id = await save_article_draft(article, username)

        return APIResponse(
            message="内容生成成功",
            data={
                "draft_id": draft_id,
                "article": article
            }
        )
    except Exception as e:
        logger.error(f"内容生成失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/content/optimize-seo", response_model=APIResponse)
async def optimize_seo(
    request: SEOOptimizationRequest,
    username: str = Depends(get_current_user)
):
    """SEO优化"""
    try:
        # 获取文章
        article = await get_article_by_id(request.article_id)

        # 执行SEO优化
        optimized = await modules['seo_optimizer'].optimize_article(
            article,
            request.keywords
        )

        # 更新文章
        await update_article(request.article_id, optimized)

        return APIResponse(
            message="SEO优化完成",
            data=optimized
        )
    except Exception as e:
        logger.error(f"SEO优化失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/content/publish", response_model=APIResponse)
async def publish_content(
    request: PublishRequest,
    background_tasks: BackgroundTasks,
    username: str = Depends(get_current_user)
):
    """发布内容"""
    try:
        if request.publish_time:
            # 定时发布
            task_id = automation_engine.add_task(
                f"定时发布_{request.article_id}",
                modules['auto_publisher'].publish_at,
                request.article_id,
                request.account_id,
                request.publish_time
            )
            return APIResponse(
                message="已设置定时发布",
                data={"task_id": task_id, "publish_time": request.publish_time}
            )
        else:
            # 立即发布
            background_tasks.add_task(
                modules['auto_publisher'].publish,
                request.article_id,
                request.account_id
            )
            return APIResponse(
                message="文章正在发布中"
            )
    except Exception as e:
        logger.error(f"发布失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/tasks", response_model=APIResponse)
async def get_tasks(username: str = Depends(get_current_user)):
    """获取任务列表"""
    try:
        tasks = []

        # 获取运行中的任务
        for task_id, task in automation_engine.running_tasks.items():
            tasks.append({
                "id": task.id,
                "name": task.name,
                "status": task.status.value,
                "created_at": task.created_at,
                "started_at": task.started_at
            })

        # 获取已完成的任务
        for task_id, task in automation_engine.completed_tasks.items():
            tasks.append({
                "id": task.id,
                "name": task.name,
                "status": task.status.value,
                "created_at": task.created_at,
                "completed_at": task.completed_at
            })

        return APIResponse(
            data={"tasks": tasks}
        )
    except Exception as e:
        logger.error(f"获取任务列表失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/tasks/{task_id}/cancel", response_model=APIResponse)
async def cancel_task(
    task_id: str,
    username: str = Depends(get_current_user)
):
    """取消任务"""
    try:
        # 查找并取消任务
        if task_id in automation_engine.running_tasks:
            task = automation_engine.running_tasks[task_id]
            task.status = TaskStatus.CANCELLED
            del automation_engine.running_tasks[task_id]
            return APIResponse(message="任务已取消")
        else:
            raise HTTPException(status_code=404, detail="任务不存在")
    except Exception as e:
        logger.error(f"取消任务失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/automation/status", response_model=APIResponse)
async def get_automation_status(username: str = Depends(get_current_user)):
    """获取自动化状态"""
    try:
        status = {
            "is_running": automation_engine.is_running,
            "worker_count": automation_engine.worker_count,
            "queue_size": automation_engine.task_queue.qsize(),
            "running_tasks": len(automation_engine.running_tasks),
            "completed_today": len([
                t for t in automation_engine.completed_tasks.values()
                if t.completed_at and t.completed_at.date() == datetime.now().date()
            ]),
            "failed_today": len([
                t for t in automation_engine.failed_tasks.values()
                if t.completed_at and t.completed_at.date() == datetime.now().date()
            ])
        }

        return APIResponse(
            data=status
        )
    except Exception as e:
        logger.error(f"获取自动化状态失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/automation/start", response_model=APIResponse)
async def start_automation(username: str = Depends(get_current_user)):
    """启动自动化"""
    try:
        if not automation_engine.is_running:
            automation_engine.start()
            return APIResponse(message="自动化引擎已启动")
        else:
            return APIResponse(message="自动化引擎已在运行")
    except Exception as e:
        logger.error(f"启动自动化失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/automation/stop", response_model=APIResponse)
async def stop_automation(username: str = Depends(get_current_user)):
    """停止自动化"""
    try:
        if automation_engine.is_running:
            await automation_engine.stop()
            return APIResponse(message="自动化引擎已停止")
        else:
            return APIResponse(message="自动化引擎未在运行")
    except Exception as e:
        logger.error(f"停止自动化失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/batch/analyze-topics", response_model=APIResponse)
async def batch_analyze_topics(
    topics: List[str],
    account_id: Optional[str] = None,
    username: str = Depends(get_current_user)
):
    """批量分析选题"""
    try:
        account_info = await get_account_info(account_id or "default")
        results = []

        for topic in topics:
            analysis = await modules['topic_analyzer'].analyze_topic(
                topic,
                account_info
            )
            results.append(analysis)

        # 按评分排序
        results.sort(key=lambda x: x['final_score'], reverse=True)

        return APIResponse(
            message=f"成功分析 {len(results)} 个选题",
            data={"results": results}
        )
    except Exception as e:
        logger.error(f"批量分析失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/dashboard", response_model=APIResponse)
async def get_dashboard_data(
    days: int = 7,
    username: str = Depends(get_current_user)
):
    """获取仪表板数据"""
    try:
        # 获取最近N天的数据
        dashboard_data = await get_analytics_data(days)

        return APIResponse(
            data=dashboard_data
        )
    except Exception as e:
        logger.error(f"获取仪表板数据失败：{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 辅助函数
async def get_account_info(account_id: str) -> Dict:
    """获取账号信息"""
    # 从数据库获取账号信息
    return {
        "name": "示例公众号",
        "audience_profile": {
            "interests": ["科技", "AI", "写作"],
            "age_distribution": {"18-25": 0.2, "26-35": 0.5, "36-45": 0.3},
            "gender_distribution": {"male": 0.6, "female": 0.4}
        },
        "followers": 50000
    }

async def save_article_draft(article: Dict, username: str) -> str:
    """保存文章草稿"""
    # 保存到数据库并返回ID
    import uuid
    draft_id = str(uuid.uuid4())
    # TODO: 实际保存逻辑
    return draft_id

async def get_article_by_id(article_id: str) -> Dict:
    """根据ID获取文章"""
    # TODO: 从数据库获取文章
    return {
        "id": article_id,
        "title": "示例标题",
        "content": "示例内容...",
        "summary": "示例摘要"
    }

async def update_article(article_id: str, article_data: Dict):
    """更新文章"""
    # TODO: 更新数据库中的文章
    pass

async def get_analytics_data(days: int) -> Dict:
    """获取分析数据"""
    # TODO: 从数据库获取分析数据
    return {
        "articles_published": 21,
        "total_reads": 105000,
        "total_likes": 5250,
        "total_shares": 2100,
        "avg_read_time": 180,
        "growth_rate": 0.15,
        "top_articles": [
            {"title": "AI写作工具测评", "reads": 15000},
            {"title": "如何提高写作效率", "reads": 12000}
        ]
    }

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理"""
    return APIResponse(
        success=False,
        message=exc.detail,
        error=str(exc)
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理"""
    logger.error(f"未处理的异常：{str(exc)}")
    return APIResponse(
        success=False,
        message="服务器内部错误",
        error=str(exc)
    )

# 运行服务器
if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )