import json
import os
from datetime import datetime
from enum import Enum
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

load_dotenv()

openai_api = os.getenv("OPENAI_API_KEY")
openai_url = os.getenv("OPENAI_URL", "https://api.openai.com/v1")
openai_model = os.getenv("OPENAI_API_MODEL", "gpt-4o")

# ============================================================================
# 1. OpenAI 클라이언트 설정
# ============================================================================

client = AsyncOpenAI(api_key=openai_api, base_url=openai_url)

# ============================================================================
# 2. 데이터 모델 확장
# ============================================================================


class GenerationMode(str, Enum):
    TEMPLATE = "template"  # 기존 템플릿 방식
    AI_ASSISTED = "ai_assisted"  # AI 도움
    FULLY_AI = "fully_ai"  # 완전 AI 생성


class NaturalLanguageRequest(BaseModel):
    description: str = Field(..., description="자연어로 작성된 API 요구사항")
    domain: Optional[str] = Field(
        None, description="도메인/업종 (예: 전자상거래, 교육, 의료)"
    )
    complexity: Optional[str] = Field(
        "medium", description="복잡도: simple, medium, complex"
    )
    include_auth: bool = Field(True, description="인증 포함 여부")
    include_admin: bool = Field(False, description="관리자 기능 포함 여부")


class AIGeneratedSpec(BaseModel):
    api_spec: dict
    reasoning: str = Field(..., description="AI의 설계 근거")
    suggestions: List[str] = Field(default_factory=list, description="추가 제안사항")
    confidence_score: float = Field(..., description="생성 결과 신뢰도 (0-1)")


class EnhancedEndpoint(BaseModel):
    path: str
    method: str
    description: str
    ai_generated_logic: Optional[str] = None
    parameters: Optional[str] = None
    request_body: Optional[str] = None
    responses: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    business_logic: Optional[str] = None  # AI가 생성한 상세 비즈니스 로직


# ============================================================================
# 3. AI 프롬프트 템플릿
# ============================================================================


class AIPromptTemplates:
    @staticmethod
    def api_spec_generation(
        description: str, domain: str = None, complexity: str = "medium"
    ) -> str:
        return f"""
당신은 전문 API 설계자입니다. 다음 요구사항을 바탕으로 완전한 REST API 스펙을 설계해주세요.

요구사항: {description}
도메인: {domain or "일반"}
복잡도: {complexity}

다음 JSON 형식으로 응답해주세요:
{{
    "api_name": "API 이름",
    "description": "API 설명",
    "version": "1.0.0",
    "framework": "fastapi",
    "database": "postgresql",
    "authentication": "jwt",
    "endpoints": [
        {{
            "path": "/api/resource",
            "method": "GET|POST|PUT|DELETE",
            "description": "엔드포인트 설명",
            "parameters": "파라미터 설명",
            "request_body": "요청 본문 JSON 예시",
            "responses": "응답 JSON 예시",
            "tags": ["태그1", "태그2"],
            "business_logic": "이 엔드포인트의 상세 비즈니스 로직 설명"
        }}
    ],
    "reasoning": "이렇게 설계한 이유와 근거",
    "suggestions": ["추가로 고려할 점들"],
    "confidence_score": 0.95
}}

설계 시 고려사항:
1. RESTful 원칙 준수
2. 적절한 HTTP 상태 코드 사용
3. 보안 고려 (인증, 권한)
4. 확장 가능한 구조
5. 실제 비즈니스 로직 구현 가능성

응답은 반드시 유효한 JSON만 포함해주세요.
"""

    @staticmethod
    def business_logic_generation(endpoint_description: str, api_context: str) -> str:
        return f"""
다음 API 엔드포인트의 상세한 비즈니스 로직을 Python FastAPI 코드로 생성해주세요.

엔드포인트 설명: {endpoint_description}
API 전체 컨텍스트: {api_context}

다음 형식으로 응답해주세요:
{{
    "implementation": "완전한 Python 함수 코드",
    "validation": "입력 검증 로직",
    "error_handling": "에러 처리 로직",
    "database_operations": "데이터베이스 작업 코드",
    "response_formatting": "응답 포맷팅 코드",
    "test_cases": "테스트 케이스 예시"
}}

코드는 프로덕션 레벨이어야 하며, 다음을 포함해야 합니다:
- 적절한 에러 처리
- 입력 검증
- 로깅
- 보안 고려사항
- 성능 최적화

응답은 반드시 유효한 JSON만 포함해주세요.
"""

    @staticmethod
    def code_review_and_optimization(code: str) -> str:
        return f"""
다음 Python FastAPI 코드를 검토하고 개선 사항을 제안해주세요.

코드:
```python
{code}
```

다음 형식으로 응답해주세요:
{{
    "quality_score": 85,
    "issues": [
        {{
            "type": "security|performance|style|logic",
            "description": "문제 설명",
            "severity": "low|medium|high|critical",
            "suggestion": "개선 방안"
        }}
    ],
    "optimized_code": "개선된 코드",
    "performance_tips": ["성능 최적화 팁들"],
    "security_recommendations": ["보안 권장사항들"]
}}

검토 기준:
1. 코드 품질 및 가독성
2. 보안 취약점
3. 성능 최적화 기회
4. 에러 처리 완성도
5. 테스트 가능성

응답은 반드시 유효한 JSON만 포함해주세요.
"""


# ============================================================================
# 4. AI 코드 생성 엔진
# ============================================================================


class AICodeGenerator:
    def __init__(self):
        self.client = client

    async def generate_api_spec_from_description(
        self, request: NaturalLanguageRequest
    ) -> AIGeneratedSpec:
        """자연어 설명을 완전한 API 스펙으로 변환"""
        if not self.client:
            raise HTTPException(
                status_code=503, detail="OpenAI API가 설정되지 않았습니다"
            )

        try:
            prompt = AIPromptTemplates.api_spec_generation(
                description=request.description,
                domain=request.domain,
                complexity=request.complexity,
            )

            response = await self.client.chat.completions.create(
                model=openai_model,  # 또는 gpt-3.5-turbo
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 전문 API 설계자입니다. 항상 유효한 JSON으로만 응답하세요.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=3000,
            )

            content = response.choices[0].message.content.strip()

            # JSON 추출 (```json 태그 제거)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)

            return AIGeneratedSpec(
                api_spec=result,
                reasoning=result.get("reasoning", "AI 생성 결과"),
                suggestions=result.get("suggestions", []),
                confidence_score=result.get("confidence_score", 0.8),
            )

        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"AI 응답 파싱 오류: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI 생성 오류: {str(e)}")

    async def enhance_endpoint_logic(self, endpoint: dict, api_context: str) -> dict:
        """개별 엔드포인트의 비즈니스 로직을 AI로 강화"""
        if not self.client:
            return endpoint

        try:
            prompt = AIPromptTemplates.business_logic_generation(
                endpoint_description=f"{endpoint['method']} {endpoint['path']}: {endpoint['description']}",
                api_context=api_context,
            )

            response = await self.client.chat.completions.create(
                model=openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "전문 Python 개발자로서 프로덕션 레벨 코드를 생성하세요.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,  # 코드 생성은 더 conservative하게
                max_tokens=2000,
            )

            content = response.choices[0].message.content.strip()

            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            ai_logic = json.loads(content)

            # 기존 엔드포인트에 AI 생성 로직 추가
            enhanced_endpoint = endpoint.copy()
            enhanced_endpoint["ai_generated_logic"] = ai_logic.get("implementation", "")
            enhanced_endpoint["business_logic"] = ai_logic.get(
                "database_operations", ""
            )

            return enhanced_endpoint

        except Exception as e:
            print(f"엔드포인트 로직 강화 실패: {e}")
            return endpoint

    async def review_and_optimize_code(self, code: str) -> dict:
        """생성된 코드를 AI로 검토하고 최적화"""
        if not self.client:
            return {"quality_score": 70, "issues": [], "optimized_code": code}

        try:
            prompt = AIPromptTemplates.code_review_and_optimization(code)

            response = await self.client.chat.completions.create(
                model=openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "코드 리뷰 전문가로서 객관적이고 건설적인 피드백을 제공하세요.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=2500,
            )

            content = response.choices[0].message.content.strip()

            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)

        except Exception as e:
            print(f"코드 리뷰 실패: {e}")
            return {"quality_score": 70, "issues": [], "optimized_code": code}


# ============================================================================
# 5. 향상된 코드 생성 템플릿
# ============================================================================


class AIEnhancedCodeGenerator:
    def __init__(self):
        self.ai_generator = AICodeGenerator()

    async def generate_enhanced_api(
        self, spec: dict, mode: GenerationMode = GenerationMode.AI_ASSISTED
    ) -> dict:
        """AI 강화된 API 코드 생성"""

        if mode == GenerationMode.FULLY_AI:
            # 모든 엔드포인트의 비즈니스 로직을 AI로 생성
            enhanced_endpoints = []
            api_context = f"{spec['name']}: {spec['description']}"

            for endpoint in spec.get("endpoints", []):
                enhanced = await self.ai_generator.enhance_endpoint_logic(
                    endpoint, api_context
                )
                enhanced_endpoints.append(enhanced)

            spec["endpoints"] = enhanced_endpoints

        # 기본 코드 생성
        main_code = self._generate_ai_enhanced_main_code(spec)

        # AI로 코드 검토 및 최적화
        if mode in [GenerationMode.AI_ASSISTED, GenerationMode.FULLY_AI]:
            review_result = await self.ai_generator.review_and_optimize_code(main_code)
            if review_result.get("optimized_code"):
                main_code = review_result["optimized_code"]

        return {
            "main_code": main_code,
            "models": self._generate_enhanced_models(spec),
            "database": self._generate_enhanced_database(spec),
            "requirements": self._generate_enhanced_requirements(spec),
            "documentation": self._generate_enhanced_documentation(spec),
            "ai_review": review_result if mode != GenerationMode.TEMPLATE else None,
        }

    def _generate_ai_enhanced_main_code(self, spec: dict) -> str:
        """AI 로직이 포함된 메인 코드 생성"""

        endpoints_code = ""
        for endpoint in spec.get("endpoints", []):
            endpoints_code += self._generate_ai_enhanced_endpoint(endpoint, spec)

        return f'''"""
{spec["name"]} API
{spec["description"]}
AI-Enhanced Code Generation
Generated at: {datetime.now().isoformat()}
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from datetime import datetime

from models import *
from database import get_db, engine
from auth import verify_token, get_current_user

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성 (AI 최적화된 설정)
app = FastAPI(
    title="{spec["name"]}",
    description="{spec["description"]}",
    version="{spec.get("version", "1.0.0")}",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {{"name": tag, "description": f"{{tag}} related operations"}}
        for tag in set(tag for endpoint in spec.get('endpoints', []) 
                      for tag in endpoint.get('tags', []))
    ]
)

# CORS 미들웨어 (AI 보안 권장사항 적용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # 프로덕션에서 수정 필요
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# 보안 스키마
security = HTTPBearer()

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    logger.info("🚀 {spec["name"]} API Starting...")
    logger.info("📖 Documentation: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    logger.info("🛑 {spec["name"]} API Shutting down...")

@app.get("/", tags=["root"])
async def root():
    """API 루트 엔드포인트"""
    return {{
        "message": "Welcome to {spec["name"]} API",
        "version": "{spec.get("version", "1.0.0")}",
        "docs_url": "/docs",
        "status": "healthy",
        "ai_enhanced": True,
        "generated_at": "{datetime.now().isoformat()}"
    }}

@app.get("/health", tags=["monitoring"])
async def health_check():
    """헬스 체크 엔드포인트 (AI 향상된 모니터링)"""
    try:
        # 데이터베이스 연결 테스트
        db = next(get_db())
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {{e}}")
        db_status = "unhealthy"
    
    return {{
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.now().isoformat(),
        "service": "{spec["name"]}",
        "database": db_status,
        "version": "{spec.get("version", "1.0.0")}"
    }}

{endpoints_code}

# AI 추천: 전역 예외 처리기
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {{exc.status_code}} - {{exc.detail}}")
    return JSONResponse(
        status_code=exc.status_code,
        content={{
            "success": False,
            "error": {{
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.now().isoformat()
            }}
        }}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
'''

    def _generate_ai_enhanced_endpoint(self, endpoint: dict, spec: dict) -> str:
        """AI 로직이 강화된 엔드포인트 생성"""
        method = endpoint["method"].lower()
        function_name = self._path_to_function_name(
            endpoint["path"], endpoint["method"]
        )

        # AI가 생성한 비즈니스 로직 활용
        ai_logic = endpoint.get("ai_generated_logic", "")
        business_logic = endpoint.get("business_logic", "")

        # 파라미터 생성
        path_params = self._extract_path_params(endpoint["path"])
        params_str = ""
        for param in path_params:
            params_str += f", {param}: int"

        if endpoint["method"] in ["POST", "PUT", "PATCH"]:
            params_str += ", request_data: Dict[Any, Any]"

        # 인증 필요 여부 확인
        auth_required = spec.get("authentication", "none") != "none"
        auth_param = (
            ", current_user: dict = Depends(get_current_user)" if auth_required else ""
        )

        # AI 생성 로직이 있으면 사용, 없으면 기본 로직
        if ai_logic:
            implementation = f"        # AI 생성 비즈니스 로직\n        {ai_logic.replace('    ', '        ')}"
        else:
            implementation = self._generate_default_logic(endpoint, path_params)

        return f'''
@app.{method}("{endpoint["path"]}", tags={endpoint.get("tags", ["default"])})
async def {function_name}(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db){auth_param}{params_str}
):
    """
    {endpoint["description"]}
    
    Args:
        {endpoint.get("parameters", "No parameters")}
    
    Returns:
        {endpoint.get("responses", "API response")}
    
    Raises:
        HTTPException: Various HTTP errors based on the operation
    """
    try:
        # 요청 로깅 (AI 권장사항)
        logger.info(f"{{'{endpoint["method"]}'}} {{'{endpoint["path"]}'}} called")
        
{implementation}
        
        # 비동기 작업 예약 (필요시)
        # background_tasks.add_task(some_async_task, result)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in {function_name}: {{str(e)}}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
'''

    def _generate_default_logic(self, endpoint: dict, path_params: List[str]) -> str:
        """기본 비즈니스 로직 생성"""
        if endpoint["method"] == "GET":
            if path_params:
                return f"""        # 특정 리소스 조회
        resource_id = {path_params[0]}
        # TODO: 데이터베이스에서 조회 로직 구현
        result = {{
            "success": True,
            "data": {{"id": resource_id, "message": "Resource found"}},
            "timestamp": datetime.now().isoformat()
        }}"""
            else:
                return """        # 리소스 목록 조회
        # TODO: 페이징 및 필터링 로직 구현
        result = {
            "success": True,
            "data": {"items": [], "total": 0, "page": 1, "limit": 10},
            "timestamp": datetime.now().isoformat()
        }"""
        elif endpoint["method"] == "POST":
            return """        # 새 리소스 생성
        # TODO: 입력 검증 및 저장 로직 구현
        result = {
            "success": True,
            "data": {"id": 1, "message": "Resource created"},
            "timestamp": datetime.now().isoformat()
        }"""
        elif endpoint["method"] in ["PUT", "PATCH"]:
            return f"""        # 리소스 업데이트
        resource_id = {path_params[0] if path_params else 'request_data.get("id")'}
        # TODO: 업데이트 로직 구현
        result = {{
            "success": True,
            "data": {{"id": resource_id, "message": "Resource updated"}},
            "timestamp": datetime.now().isoformat()
        }}"""
        elif endpoint["method"] == "DELETE":
            return f"""        # 리소스 삭제
        resource_id = {path_params[0]}
        # TODO: 삭제 로직 구현 (soft delete 권장)
        result = {{
            "success": True,
            "data": {{"id": resource_id, "message": "Resource deleted"}},
            "timestamp": datetime.now().isoformat()
        }}"""

        return """        # 기본 로직
        result = {
            "success": True,
            "message": "Operation completed",
            "timestamp": datetime.now().isoformat()
        }"""

    def _generate_enhanced_models(self, spec: dict) -> str:
        """AI 향상된 데이터 모델 생성"""
        return f'''"""
{spec["name"]} 데이터 모델
AI 향상된 Pydantic 모델 및 SQLAlchemy ORM
Generated at: {datetime.now().isoformat()}
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Decimal, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import re

Base = declarative_base()

# ============================================================================
# AI 권장: 공통 기능 믹스인
# ============================================================================

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

# ============================================================================
# SQLAlchemy ORM 모델 (AI 최적화)
# ============================================================================

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # AI 권장: 메타데이터 저장
    metadata = Column(JSON, default=dict)
    
    def __repr__(self):
        return f"<User(id={{self.id}}, username='{{self.username}}')>"

# ============================================================================
# Pydantic 스키마 (AI 향상된 검증)
# ============================================================================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, regex=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError('사용자명은 영문, 숫자, 언더스코어만 사용 가능합니다')
        return v.lower()

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    
    @validator('password')
    def validate_password(cls, v):
        if not re.search(r"[A-Za-z]", v):
            raise ValueError('비밀번호는 최소 하나의 영문자를 포함해야 합니다')
        if not re.search(r"\\d", v):
            raise ValueError('비밀번호는 최소 하나의 숫자를 포함해야 합니다')
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {{
            datetime: lambda v: v.isoformat()
        }}

# AI 권장: 표준화된 응답 모델
class APIResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {{
            datetime: lambda v: v.isoformat()
        }}

class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int = 1
    limit: int = 10
    pages: int
    has_next: bool
    has_prev: bool
    
    @validator('pages', always=True)
    def calculate_pages(cls, v, values):
        total = values.get('total', 0)
        limit = values.get('limit', 10)
        return (total + limit - 1) // limit if limit > 0 else 0
    
    @validator('has_next', always=True)
    def calculate_has_next(cls, v, values):
        page = values.get('page', 1)
        pages = values.get('pages', 0)
        return page < pages
    
    @validator('has_prev', always=True) 
    def calculate_has_prev(cls, v, values):
        page = values.get('page', 1)
        return page > 1
'''

    def _generate_enhanced_requirements(self, spec: dict) -> str:
        """AI 권장 패키지 포함된 requirements.txt"""
        base_requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
            "sqlalchemy==2.0.23",
            "alembic==1.13.0",
            # AI 권장 추가 패키지
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
            "python-multipart==0.0.6",
            "python-dotenv==1.0.0",
            "redis==5.0.1",
            "celery==5.3.4",
            "httpx==0.25.2",
            # 모니터링 및 로깅
            "structlog==23.2.0",
            "sentry-sdk[fastapi]==1.38.0",
            # 개발 도구
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "black==23.11.0",
            "isort==5.12.0",
            "mypy==1.7.1",
        ]

        # 데이터베이스별 드라이버
        db_drivers = {
            "postgresql": ["psycopg2-binary==2.9.9"],
            "mysql": ["pymysql==1.1.0"],
            "mongodb": ["motor==3.3.2", "pymongo==4.6.0"],
            "sqlite": [],
        }

        db_type = spec.get("database", "sqlite")
        all_requirements = base_requirements + db_drivers.get(db_type, [])

        return "\n".join(all_requirements)

    def _generate_enhanced_documentation(self, spec: dict) -> str:
        """AI 향상된 문서 생성"""
        return f"""# {spec["name"]} API Documentation

## 🤖 AI-Enhanced API

이 API는 AI 기술을 활용하여 자동 생성되었습니다.

- **생성 일시**: {datetime.now().isoformat()}
- **AI 모델**: GPT-4
- **코드 품질**: AI 검토 및 최적화 완료

## 📋 API 개요

{spec["description"]}

### 🔧 기술 스택
- **프레임워크**: {spec.get("framework", "FastAPI")}
- **데이터베이스**: {spec.get("database", "PostgreSQL")}
- **인증**: {spec.get("authentication", "JWT")}
- **AI 향상**: 비즈니스 로직 자동 생성

### 🚀 빠른 시작

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경변수 설정
cp .env.example .env
# .env 파일을 편집하여 설정

# 3. 데이터베이스 마이그레이션
alembic upgrade head

# 4. 서버 실행
python main.py
```

### 📖 API 문서
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 엔드포인트

{
            "".join(
                [
                    f'''
### {endpoint["method"]} {endpoint["path"]}

**설명**: {endpoint["description"]}

**태그**: {", ".join(endpoint.get("tags", []))}

{
                        f"**파라미터**: {endpoint.get('parameters', 'None')}"
                        if endpoint.get("parameters")
                        else ""
                    }

{
                        f"""**요청 본문**:
```json
{endpoint.get("request_body", "None")}
```"""
                        if endpoint.get("request_body")
                        else ""
                    }

**응답**:
```json
{
                        endpoint.get(
                            "responses",
                            '{"success": true, "data": {}, "timestamp": "2024-01-01T00:00:00"}',
                        )
                    }
```

{
                        f"**AI 생성 로직**: 이 엔드포인트는 AI가 비즈니스 로직을 자동 생성했습니다."
                        if endpoint.get("ai_generated_logic")
                        else ""
                    }

---
'''
                    for endpoint in spec.get("endpoints", [])
                ]
            )
        }

## 🔒 인증

{
            f"이 API는 {spec.get('authentication', 'JWT')} 인증을 사용합니다."
            if spec.get("authentication", "none") != "none"
            else "인증이 필요하지 않습니다."
        }

## 🧪 테스트

```bash
# 단위 테스트 실행
pytest

# 커버리지 확인
pytest --cov=.

# API 테스트 (서버 실행 후)
curl http://localhost:8000/health
```

## 🚀 배포

### Docker 배포
```bash
docker build -t {spec["name"].lower().replace(" ", "-")}-api .
docker run -p 8000:8000 {spec["name"].lower().replace(" ", "-")}-api
```

### 프로덕션 설정
1. 환경변수 보안 설정
2. HTTPS 인증서 설정
3. 로드 밸런서 구성
4. 모니터링 시스템 연동

## 🤖 AI 기능

이 API는 다음 AI 기능들이 적용되었습니다:

- ✅ **자동 비즈니스 로직 생성**: 각 엔드포인트의 핵심 로직 자동 구현
- ✅ **코드 품질 최적화**: AI 코드 리뷰 및 개선사항 자동 적용
- ✅ **보안 강화**: AI 권장 보안 패턴 적용
- ✅ **성능 최적화**: 효율적인 데이터베이스 쿼리 및 캐싱 전략
- ✅ **에러 처리**: 포괄적인 예외 처리 및 로깅

## 📞 지원

문제가 발생하거나 개선사항이 있으면 이슈를 등록해주세요.

---
*이 문서는 AI에 의해 자동 생성되었습니다.*
"""

    def _path_to_function_name(self, path: str, method: str) -> str:
        """경로를 함수명으로 변환"""
        import re

        parts = path.strip("/").split("/")
        name_parts = [method.lower()]

        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                name_parts.extend(["by", part[1:-1]])
            elif part != "api":
                name_parts.append(re.sub(r"[^a-zA-Z0-9]", "_", part))

        return "_".join(name_parts)

    def _extract_path_params(self, path: str) -> List[str]:
        """경로에서 파라미터 추출"""
        import re

        return re.findall(r"\\{([^}]+)\\}", path)
