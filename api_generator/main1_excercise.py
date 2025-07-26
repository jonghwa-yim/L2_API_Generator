# REST API 자동 생성기 - 실행 가능한 FastAPI 구현
# pip install fastapi uvicorn pydantic

from datetime import datetime
from enum import Enum
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="REST API Generator", description="AI 기반 REST API 자동 생성기")

# ============================================================================
# 1. 데이터 모델 정의
# ============================================================================


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class Framework(str, Enum):
    FASTAPI = "fastapi"
    FLASK = "flask"
    EXPRESS = "express"


class Database(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    SQLITE = "sqlite"


class AuthMethod(str, Enum):
    NONE = "none"
    JWT = "jwt"
    OAUTH2 = "oauth2"
    API_KEY = "api-key"


class EndpointModel(BaseModel):
    path: str = Field(..., description="API 경로")
    method: HTTPMethod = Field(..., description="HTTP 메서드")
    description: str = Field(..., description="엔드포인트 설명")
    parameters: Optional[str] = Field(None, description="파라미터")
    request_body: Optional[str] = Field(None, description="요청 본문")
    responses: Optional[str] = Field(None, description="응답")
    tags: List[str] = Field(default_factory=list, description="태그")


class APISpecModel(BaseModel):
    name: str = Field(..., description="API 이름")
    description: str = Field(..., description="API 설명")
    version: str = Field(default="1.0.0", description="버전")
    framework: Framework = Field(default=Framework.FASTAPI, description="프레임워크")
    database: Database = Field(default=Database.POSTGRESQL, description="데이터베이스")
    authentication: AuthMethod = Field(default=AuthMethod.JWT, description="인증 방식")
    endpoints: List[EndpointModel] = Field(..., description="엔드포인트 목록")


class GeneratedCodeResponse(BaseModel):
    main_code: str
    models: str
    database: str
    requirements: str
    documentation: str


# ============================================================================
# 2. 코드 생성 엔진
# ============================================================================


class FastAPICodeGenerator:
    def generate_api(self, spec: APISpecModel) -> GeneratedCodeResponse:
        """API 스펙을 바탕으로 완전한 FastAPI & RestAPI 코드 생성"""
        # 필요 함수: _generate_main_code, _generate_models, _generate_database_code, _generate_requirements, _generate_documentation
        # Returns: GeneratedCodeResponse

        main_code = self._generate_main_code(spec)
        models = self._generate_models(spec)
        database = self._generate_database_code(spec)
        requirements = self._generate_requirements(spec)
        documentation = self._generate_documentation(spec)

        return GeneratedCodeResponse(
            main_code=main_code,
            models=models,
            database=database,
            requirements=requirements,
            documentation=documentation,
        )

    def _generate_main_code(self, spec: APISpecModel) -> str:
        """RestAPI 기반, 메인 FastAPI 앱 코드 생성
        Args:
            spec (APISpecModel): API 스펙 모델
        Returns:
            str: FastAPI 앱 코드
        """
        # TODO: 실제 FastAPI 앱 코드 생성 로직 구현
        return

    def _generate_endpoint_code(
        self, endpoint: EndpointModel, spec: APISpecModel
    ) -> str:
        """개별 엔드포인트 코드 생성.
        비즈니스 로직을 포함한 FastAPI 엔드포인트 코드 생성.
        Args:
            endpoint (EndpointModel): 엔드포인트 모델
            spec (APISpecModel): API 스펙 모델
        Returns:
            str: 엔드포인트 코드
        """
        # TODO: 실제 엔드포인트 코드 생성 로직 구현
        return

    def _generate_models(self, spec: APISpecModel) -> str:
        """데이터 모델 코드 생성
        Args:
            spec (APISpecModel): API 스펙 모델
        Returns:
            str: Pydantic 모델 코드
        """
        # TODO: 실제 Pydantic 모델 생성 로직 구현
        return

    def _generate_database_code(self, spec: APISpecModel) -> str:
        """MongoDB 또는 SQLAlchemy 기반 데이터베이스 설정 코드 생성
        Args:
            spec (APISpecModel): API 스펙 모델
        Returns:
            str: 데이터베이스 설정 코드
        """

        db_configs = {
            "postgresql": "postgresql://user:password@localhost/dbname",
            "mysql": "mysql://user:password@localhost/dbname",
            "sqlite": "sqlite:///./app.db",
            "mongodb": "mongodb://localhost:27017/dbname",
        }

        db_url = db_configs.get(spec.database.value, db_configs["sqlite"])

        #TODO: 실제 데이터베이스 설정 코드 생성 로직 구현

        return

    def _generate_requirements(self, spec: APISpecModel) -> str:
        """requirements.txt 생성"""
        base_requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "pydantic==2.5.0",
        ]

        if spec.database == Database.MONGODB:
            base_requirements.append("motor==3.3.2")
        else:
            base_requirements.extend(["sqlalchemy==2.0.23", "alembic==1.13.0"])

        if spec.database == Database.POSTGRESQL:
            base_requirements.append("psycopg2-binary==2.9.9")
        elif spec.database == Database.MYSQL:
            base_requirements.append("pymysql==1.1.0")

        if spec.authentication != AuthMethod.NONE:
            base_requirements.extend(
                ["python-jose[cryptography]==3.3.0", "passlib[bcrypt]==1.7.4"]
            )

        return "\\n".join(base_requirements)

    def _generate_documentation(self, spec: APISpecModel) -> str:
        """Markdown 형식의 API 문서 생성. 
        API Endpoints 에 대한 설명, 파라미터, 요청 본문, 응답 등을 포함.
        API 문서는 개요, 빠른 시작, 엔드포인트 목록, 사용 예시, 개발 정보 등을 포함합니다.
        Args:
            spec (APISpecModel): API 스펙 모델
        Returns:
            str: API 문서 Markdown
        """
        # TODO: 실제 API 문서 생성 로직 구현
        return

    def _path_to_function_name(self, path: str, method: str) -> str:
        """경로를 함수명으로 변환"""
        import re

        # /api/users/{id} -> get_users_by_id
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



# ============================================================================
# 3. 예제 데이터
# ============================================================================

# 예제 1: 사용자 관리 시스템
USER_MANAGEMENT_EXAMPLE = {
    "name": "User Management API",
    "description": "사용자 등록, 인증, 프로필 관리를 위한 REST API",
    "version": "1.0.0",
    "framework": "fastapi",
    "database": "postgresql",
    "authentication": "jwt",
    "endpoints": [
        {
            "path": "/api/auth/register",
            "method": "POST",
            "description": "새 사용자 등록",
            "parameters": "없음",
            "request_body": '{"username": "testuser", "email": "test@example.com", "password": "password123"}',
            "responses": '{"success": true, "message": "User created", "data": {"id": 1, "username": "testuser"}}',
            "tags": ["authentication"],
        },
        {
            "path": "/api/auth/login",
            "method": "POST",
            "description": "사용자 로그인",
            "parameters": "없음",
            "request_body": '{"username": "testuser", "password": "password123"}',
            "responses": '{"access_token": "jwt_token_here", "token_type": "bearer"}',
            "tags": ["authentication"],
        },
        {
            "path": "/api/users",
            "method": "GET",
            "description": "사용자 목록 조회",
            "parameters": "page, limit (선택사항)",
            "request_body": "없음",
            "responses": '{"success": true, "data": {"items": [], "total": 10}}',
            "tags": ["users"],
        },
        {
            "path": "/api/users/{user_id}",
            "method": "GET",
            "description": "특정 사용자 정보 조회",
            "parameters": "user_id: 사용자 ID",
            "request_body": "없음",
            "responses": '{"success": true, "data": {"id": 1, "username": "testuser", "email": "test@example.com"}}',
            "tags": ["users"],
        },
    ],
}

# 예제 2: 블로그 시스템
BLOG_SYSTEM_EXAMPLE = {
    "name": "Blog System API",
    "description": "블로그 포스트 작성, 댓글, 카테고리 관리 API",
    "version": "1.2.0",
    "framework": "fastapi",
    "database": "mysql",
    "authentication": "jwt",
    "endpoints": [
        {
            "path": "/api/posts",
            "method": "GET",
            "description": "블로그 포스트 목록 조회",
            "parameters": "page, category, search (선택사항)",
            "request_body": "없음",
            "responses": '{"success": true, "data": {"items": [], "total": 50, "page": 1}}',
            "tags": ["posts"],
        },
        {
            "path": "/api/posts",
            "method": "POST",
            "description": "새 블로그 포스트 작성",
            "parameters": "인증 필요",
            "request_body": '{"title": "My Blog Post", "content": "Post content here", "category_id": 1}',
            "responses": '{"success": true, "data": {"id": 1, "title": "My Blog Post", "slug": "my-blog-post"}}',
            "tags": ["posts"],
        },
        {
            "path": "/api/posts/{post_id}",
            "method": "GET",
            "description": "특정 블로그 포스트 조회",
            "parameters": "post_id: 포스트 ID",
            "request_body": "없음",
            "responses": '{"success": true, "data": {"id": 1, "title": "Post Title", "content": "Full content", "comments": []}}',
            "tags": ["posts"],
        },
        {
            "path": "/api/categories",
            "method": "GET",
            "description": "카테고리 목록 조회",
            "parameters": "없음",
            "request_body": "없음",
            "responses": '{"success": true, "data": [{"id": 1, "name": "Technology", "post_count": 15}]}',
            "tags": ["categories"],
        },
    ],
}

# 예제 3: 전자상거래 API
ECOMMERCE_EXAMPLE = {
    "name": "E-commerce API",
    "description": "온라인 쇼핑몰을 위한 완전한 전자상거래 API",
    "version": "2.0.0",
    "framework": "fastapi",
    "database": "postgresql",
    "authentication": "jwt",
    "endpoints": [
        {
            "path": "/api/products",
            "method": "GET",
            "description": "상품 목록 조회",
            "parameters": "category, min_price, max_price, search",
            "request_body": "없음",
            "responses": '{"success": true, "data": {"items": [], "total": 200, "filters": {}}}',
            "tags": ["products"],
        },
        {
            "path": "/api/products/{product_id}",
            "method": "GET",
            "description": "상품 상세 정보 조회",
            "parameters": "product_id: 상품 ID",
            "request_body": "없음",
            "responses": '{"success": true, "data": {"id": 1, "name": "Product Name", "price": 99.99, "images": []}}',
            "tags": ["products"],
        },
        {
            "path": "/api/cart",
            "method": "GET",
            "description": "장바구니 조회",
            "parameters": "인증 필요",
            "request_body": "없음",
            "responses": '{"success": true, "data": {"items": [], "total_amount": 199.99, "item_count": 3}}',
            "tags": ["cart"],
        },
        {
            "path": "/api/cart/items",
            "method": "POST",
            "description": "장바구니에 상품 추가",
            "parameters": "인증 필요",
            "request_body": '{"product_id": 1, "quantity": 2}',
            "responses": '{"success": true, "message": "Item added to cart", "data": {"cart_total": 149.99}}',
            "tags": ["cart"],
        },
        {
            "path": "/api/orders",
            "method": "POST",
            "description": "주문 생성",
            "parameters": "인증 필요",
            "request_body": '{"items": [{"product_id": 1, "quantity": 2}], "shipping_address": {}}',
            "responses": '{"success": true, "data": {"order_id": "ORD-001", "total_amount": 199.99, "status": "pending"}}',
            "tags": ["orders"],
        },
    ],
}

# ============================================================================
# 4. API 엔드포인트
# ============================================================================

# 전역 코드 생성기 인스턴스
code_generator = FastAPICodeGenerator()


@app.post("/api/generate", response_model=GeneratedCodeResponse)
async def generate_api_code(spec: APISpecModel):
    """API 스펙을 바탕으로 완전한 코드 생성"""
    try:
        result = code_generator.generate_api(spec)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"코드 생성 중 오류 발생: {str(e)}")


@app.get("/api/examples")
async def get_examples():
    """사용 가능한 예제 목록 반환"""
    return {
        "examples": [
            {
                "id": "user_management",
                "name": "사용자 관리 시스템",
                "description": "사용자 등록, 인증, 프로필 관리",
                "endpoints_count": len(USER_MANAGEMENT_EXAMPLE["endpoints"]),
                "framework": "FastAPI",
                "database": "PostgreSQL",
            },
            {
                "id": "blog_system",
                "name": "블로그 시스템",
                "description": "포스트, 댓글, 카테고리 관리",
                "endpoints_count": len(BLOG_SYSTEM_EXAMPLE["endpoints"]),
                "framework": "FastAPI",
                "database": "MySQL",
            },
            {
                "id": "ecommerce",
                "name": "전자상거래 시스템",
                "description": "상품, 장바구니, 주문 관리",
                "endpoints_count": len(ECOMMERCE_EXAMPLE["endpoints"]),
                "framework": "FastAPI",
                "database": "PostgreSQL",
            },
        ]
    }


@app.get("/api/examples/{example_id}")
async def get_example(example_id: str):
    """특정 예제의 상세 스펙 반환"""
    examples = {
        "user_management": USER_MANAGEMENT_EXAMPLE,
        "blog_system": BLOG_SYSTEM_EXAMPLE,
        "ecommerce": ECOMMERCE_EXAMPLE,
    }

    if example_id not in examples:
        raise HTTPException(status_code=404, detail="예제를 찾을 수 없습니다")

    return examples[example_id]


@app.post("/api/download")
async def download_generated_code(spec: APISpecModel):
    """생성된 코드 파일들을 JSON으로 반환 (다운로드용)"""
    try:
        result = code_generator.generate_api(spec)

        files = {
            "main.py": result.main_code,
            "models.py": result.models,
            "database.py": result.database,
            "requirements.txt": result.requirements,
            "README.md": result.documentation,
        }

        return {
            "success": True,
            "message": "코드가 성공적으로 생성되었습니다",
            "files": files,
            "project_name": spec.name.replace(" ", "_").lower(),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 생성 중 오류 발생: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def get_web_interface():
    """웹 인터페이스 HTML 반환"""
    return """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>REST API Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <div x-data="apiGenerator()" class="max-w-7xl mx-auto p-6" x-init="init()">
        <!-- 헤더 -->
        <div class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-800 mb-2">🚀 REST API Generator</h1>
            <p class="text-lg text-gray-600">Python FastAPI 기반 자동 REST API 생성기</p>
            <p class="text-sm text-gray-500 mt-2">3가지 실무 예제 포함</p>
        </div>
        
        <!-- 예제 선택 -->
        <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
            <h2 class="text-2xl font-semibold mb-4 text-center">🎯 빠른 시작 - 예제 선택</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <template x-for="example in examples" :key="example.id">
                    <div class="border-2 border-gray-200 rounded-lg p-6 hover:border-blue-400 hover:shadow-md transition-all cursor-pointer"
                         @click="loadExample(example.id)"
                         :class="selectedExample === example.id ? 'border-blue-500 bg-blue-50' : ''">
                        <h3 class="font-bold text-lg mb-2" x-text="example.name"></h3>
                        <p class="text-gray-600 text-sm mb-3" x-text="example.description"></p>
                        <div class="flex justify-between items-center text-xs">
                            <span class="bg-green-100 text-green-800 px-2 py-1 rounded" 
                                  x-text="example.endpoints_count + '개 API'"></span>
                            <span class="text-gray-500" x-text="example.database"></span>
                        </div>
                    </div>
                </template>
            </div>
        </div>

        <!-- 메인 컨텐츠 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- 설정 패널 -->
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h2 class="text-xl font-semibold mb-6">⚙️ API 설정</h2>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium mb-2">API 이름</label>
                        <input x-model="spec.name" 
                               type="text" 
                               placeholder="예: My Awesome API"
                               class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-2">설명</label>
                        <textarea x-model="spec.description" 
                                  placeholder="API의 목적과 기능을 설명해주세요"
                                  class="w-full p-3 border border-gray-300 rounded-lg h-24 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"></textarea>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium mb-2">프레임워크</label>
                            <select x-model="spec.framework" 
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                                <option value="fastapi">🐍 FastAPI</option>
                                <option value="flask">🌶️ Flask</option>
                                <option value="express">📗 Express.js</option>
                            </select>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium mb-2">데이터베이스</label>
                            <select x-model="spec.database" 
                                    class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                                <option value="postgresql">🐘 PostgreSQL</option>
                                <option value="mysql">🐬 MySQL</option>
                                <option value="sqlite">📱 SQLite</option>
                                <option value="mongodb">🍃 MongoDB</option>
                            </select>
                        </div>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium mb-2">인증 방식</label>
                        <select x-model="spec.authentication" 
                                class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                            <option value="none">🚫 인증 없음</option>
                            <option value="jwt">🔑 JWT</option>
                            <option value="oauth2">🔐 OAuth 2.0</option>
                            <option value="api-key">🗝️ API Key</option>
                        </select>
                    </div>
                </div>
                
                <button @click="generateAPI()" 
                        :disabled="isGenerating || !spec.name || !spec.description"
                        class="w-full mt-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all font-semibold text-lg shadow-lg">
                    <span x-show="!isGenerating">🚀 API 생성하기</span>
                    <span x-show="isGenerating" class="flex items-center justify-center">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        생성 중...
                    </span>
                </button>
            </div>

            <!-- 결과 패널 -->
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h2 class="text-xl font-semibold mb-6">📄 생성된 코드</h2>
                
                <div x-show="generatedCode && generatedCode.main_code">
                    <!-- 탭 -->
                    <div class="flex space-x-1 mb-4 bg-gray-100 p-1 rounded-lg">
                        <button @click="activeTab = 'main'" 
                                :class="activeTab === 'main' ? 'bg-white shadow' : 'hover:bg-gray-200'"
                                class="flex-1 px-3 py-2 rounded-md text-sm font-medium transition-all">
                            main.py
                        </button>
                        <button @click="activeTab = 'models'" 
                                :class="activeTab === 'models' ? 'bg-white shadow' : 'hover:bg-gray-200'"
                                class="flex-1 px-3 py-2 rounded-md text-sm font-medium transition-all">
                            models.py
                        </button>
                        <button @click="activeTab = 'database'" 
                                :class="activeTab === 'database' ? 'bg-white shadow' : 'hover:bg-gray-200'"
                                class="flex-1 px-3 py-2 rounded-md text-sm font-medium transition-all">
                            database.py
                        </button>
                    </div>
                    
                    <!-- 코드 표시 -->
                    <div class="bg-gray-900 rounded-lg p-4 mb-4">
                        <pre class="text-green-400 text-xs overflow-auto h-80 whitespace-pre-wrap"><code x-text="getActiveTabContent()"></code></pre>
                    </div>
                    
                    <!-- 다운로드 및 실행 정보 -->
                    <div class="space-y-3">
                        <button @click="downloadAll()" 
                                class="w-full bg-green-600 text-white p-3 rounded-lg hover:bg-green-700 transition-colors font-medium">
                            📥 모든 파일 다운로드
                        </button>
                        
                        <div class="bg-blue-50 p-4 rounded-lg">
                            <h4 class="font-medium text-blue-800 mb-2">🏃‍♂️ 실행 방법:</h4>
                            <ol class="text-sm text-blue-700 space-y-1">
                                <li>1. 파일들을 다운로드하여 프로젝트 폴더에 저장</li>
                                <li>2. <code class="bg-blue-200 px-1 rounded">pip install -r requirements.txt</code></li>
                                <li>3. <code class="bg-blue-200 px-1 rounded">python main.py</code></li>
                                <li>4. http://localhost:8000/docs 에서 API 문서 확인</li>
                            </ol>
                        </div>
                    </div>
                </div>
                
                <div x-show="!generatedCode || !generatedCode.main_code" class="text-center py-16">
                    <div class="text-6xl mb-4">🛠️</div>
                    <p class="text-gray-500 text-lg">예제를 선택하거나 설정을 입력하고<br>생성 버튼을 클릭하세요</p>
                </div>
            </div>
        </div>

        <!-- 성공 메시지 -->
        <div x-show="showSuccess" 
             x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0 transform translate-y-2"
             x-transition:enter-end="opacity-100 transform translate-y-0"
             class="fixed bottom-4 right-4 bg-green-500 text-white p-4 rounded-lg shadow-lg">
            ✅ API 코드가 성공적으로 생성되었습니다!
        </div>
    </div>

    <script>
        function apiGenerator() {
            return {
                spec: {
                    name: '',
                    description: '',
                    version: '1.0.0',
                    framework: 'fastapi',
                    database: 'postgresql',
                    authentication: 'jwt',
                    endpoints: []
                },
                examples: [],
                generatedCode: null,
                isGenerating: false,
                activeTab: 'main',
                selectedExample: null,
                showSuccess: false,
                
                async init() {
                    await this.loadExamples();
                },
                
                async loadExamples() {
                    try {
                        const response = await fetch('/api/examples');
                        const data = await response.json();
                        this.examples = data.examples;
                    } catch (error) {
                        console.error('예제 로드 실패:', error);
                    }
                },
                
                async loadExample(exampleId) {
                    try {
                        this.selectedExample = exampleId;
                        const response = await fetch(`/api/examples/${exampleId}`);
                        const data = await response.json();
                        this.spec = { ...data };
                    } catch (error) {
                        console.error('예제 로드 실패:', error);
                        alert('예제를 불러오는데 실패했습니다.');
                    }
                },
                
                async generateAPI() {
                    if (!this.spec.name || !this.spec.description) {
                        alert('API 이름과 설명을 입력해주세요.');
                        return;
                    }
                    
                    this.isGenerating = true;
                    try {
                        const response = await fetch('/api/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(this.spec)
                        });
                        
                        if (!response.ok) {
                            const errorData = await response.json();
                            throw new Error(errorData.detail || 'API 생성 실패');
                        }
                        
                        this.generatedCode = await response.json();
                        this.showSuccessMessage();
                        
                    } catch (error) {
                        console.error('API 생성 오류:', error);
                        alert('API 생성 중 오류가 발생했습니다: ' + error.message);
                    } finally {
                        this.isGenerating = false;
                    }
                },
                
                getActiveTabContent() {
                    if (!this.generatedCode) return '';
                    
                    switch(this.activeTab) {
                        case 'main': return this.generatedCode.main_code || '';
                        case 'models': return this.generatedCode.models || '';
                        case 'database': return this.generatedCode.database || '';
                        default: return '';
                    }
                },
                
                async downloadAll() {
                    try {
                        const response = await fetch('/api/download', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(this.spec)
                        });
                        
                        if (!response.ok) {
                            throw new Error('다운로드 요청 실패');
                        }
                        
                        const data = await response.json();
                        
                        // 각 파일을 개별적으로 다운로드
                        Object.entries(data.files).forEach(([filename, content]) => {
                            this.downloadFile(filename, content);
                        });
                        
                    } catch (error) {
                        console.error('다운로드 오류:', error);
                        alert('파일 다운로드 중 오류가 발생했습니다: ' + error.message);
                    }
                },
                
                downloadFile(filename, content) {
                    const element = document.createElement('a');
                    const file = new Blob([content], { type: 'text/plain' });
                    element.href = URL.createObjectURL(file);
                    element.download = filename;
                    document.body.appendChild(element);
                    element.click();
                    document.body.removeChild(element);
                },
                
                showSuccessMessage() {
                    this.showSuccess = true;
                    setTimeout(() => {
                        this.showSuccess = false;
                    }, 3000);
                }
            }
        }
    </script>
</body>
</html>
"""


# ============================================================================
# 5. 애플리케이션 실행부
# ============================================================================

if __name__ == "__main__":
    print("🚀 REST API Generator 시작!")
    print("=" * 50)
    print("📖 API 문서: http://localhost:8000/docs")
    print("🌐 웹 인터페이스: http://localhost:8000")
    print("📋 예제 API: http://localhost:8000/api/examples")
    print("=" * 50)
    print("💡 사용법:")
    print("1. 웹 브라우저로 http://localhost:8000 접속")
    print("2. 예제 중 하나 선택 또는 직접 설정")
    print("3. 'API 생성하기' 버튼 클릭")
    print("4. 생성된 코드 다운로드 및 실행")
    print("=" * 50)

    uvicorn.run("main1_excercise:app", host="localhost", port=8000, reload=True)
