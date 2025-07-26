# 🚀 REST API Generator

**FastAPI 기반 자동 REST API 생성기** - ML 과정 학습용

이 프로젝트는 ML 과정 학생들이 **API 개발 실무**를 학습하기 위한 교육용 도구입니다. 자연어 요구사항부터 완전한 프로덕션 레벨 API까지 자동 생성해주는 강력한 도구를 제공합니다.

## 📚 프로젝트 구조

```
📁 L2_RestAPI_Generator/
├── 📁 api_generator/
│   ├── 📄 main1_exercise.py    # 🎯 실습용 (TODO 구현 연습)
│   ├── 📄 main1.py            # 📖 기본 완성 버전
│   ├── 📄 main2.py            # 🌟 향상된 UI/UX 버전
│   ├── 📄 main3.py            # 🤖 AI 통합 버전
│   ├── 📄 ai_code_gen.py      # 🧠 AI 코드 생성 엔진
│   └── 📄 README.md           # 이 파일
├── 📁 user_management_system/ # 📝 생성된 예제 프로젝트
├── 📄 requirements.txt        # 🔧 프로젝트 의존성
└── 📄 LICENSE                 # ⚖️ 라이센스
```

## 🎓 학습 단계별 가이드

### 1단계: 기초 실습 (main1_exercise.py)
```bash
python main1_exercise.py
```

**목적**: GPT를 활용한 실습 학습
- TODO 주석으로 표시된 빈 함수들
- GPT 프롬프트를 사용해 직접 구현 연습
- REST API 설계 원칙 이해

**실습 내용**:
- `_generate_main_code()` - FastAPI 메인 앱 코드 생성
- `_generate_endpoint_code()` - FastAPI 개별 엔드포인트 코드 생성
- `_generate_models()` - Pydantic 데이터 모델 생성  
- `_generate_database_code()` - 데이터베이스 설정 코드 생성
- `_generate_documentation()` - API 문서 생성

**실습 과제 예시**:
```python
# GPT 프롬프트 예시 (main1_exercise.py 사용)
"""
TODO 부분을 구현해주세요.
요구사항:
- REST API 엔드포인트 자동 생성
- CRUD 기능 지원
- 데이터베이스 연동
- 인증 시스템 포함
"""
```

### 2단계: 기본 완성 버전 (main1.py)
```bash
python main1.py
```

**기능**:
- ✅ 웹 기반 인터페이스
- ✅ 3가지 실무 예제 (사용자 관리, 블로그, 전자상거래)
- ✅ 5개 파일 자동 생성 (main.py, models.py, database.py, requirements.txt, README.md)
- ✅ 다양한 데이터베이스 지원 (PostgreSQL, MySQL, MongoDB, SQLite)
- ✅ 인증 시스템 (JWT, OAuth2, API Key)

### 2-1단계: 생성된 프로젝트의 API 코드 채우기기 (user_management_system/main.py)
```bash
python user_management_system/main.py
```

**TODO**:
함수 내부 기능 채우기

### 3단계: 향상된 버전 (main2.py)
```bash
python main2.py
```

**추가 기능**:
- 🎨 개선된 사용자 인터페이스
- 🔗 실시간 엔드포인트 관리 (추가/편집/삭제)
- 📑 탭 기반 네비게이션
- 📋 빠른 템플릿 추가 기능
- 🎯 미리보기 및 검증 기능

### 4단계: AI 통합 버전 (main3.py + ai_code_gen.py)
```bash
# .env 파일에 OpenAI API 키 설정 후
python main3.py
```

**AI 기능**:
- 🧠 자연어 → API 스펙 자동 변환
- 🔍 지능형 비즈니스 로직 생성
- 📝 자동 코드 리뷰 및 최적화
- 💡 AI 기반 개선 제안

## 🛠️ 설치 및 실행

### 기본 설치
```bash
# 저장소 클론
git clone <repository-url>
cd L2_RestAPI_Generator

# 의존성 설치
pip install -r requirements.txt

# 기본 버전 실행
cd api_generator
python main1.py
```

### AI 기능 사용 (선택사항)
```bash
# OpenAI API 키 설정
echo "OPENAI_API_KEY=your-api-key-here" > .env

# AI 통합 버전 실행
python main3.py
```

## 🎯 주요 기능

### 🌐 웹 인터페이스
- 직관적인 브라우저 기반 UI
- 실시간 코드 생성 및 미리보기
- 원클릭 파일 다운로드

### 📦 완전한 프로젝트 생성
생성되는 파일들:
```
📁 생성된_프로젝트/
├── 📄 main.py         # FastAPI 메인 애플리케이션
├── 📄 models.py       # Pydantic 데이터 모델
├── 📄 database.py     # 데이터베이스 설정 및 ORM
├── 📄 requirements.txt # 필요한 패키지 목록
└── 📄 README.md       # 완전한 API 문서
```

### 🎨 다양한 설정 지원
- **프레임워크**: FastAPI, Flask, Express.js
- **데이터베이스**: PostgreSQL, MySQL, MongoDB, SQLite
- **인증**: JWT, OAuth2, API Key, 없음

### 🤖 AI 향상 기능 (main3.py)
```python
# 자연어로 API 요구사항 입력
request = {
    "description": "온라인 서점을 위한 API가 필요해요. 책 검색, 주문, 리뷰 기능이 있어야 합니다.",
    "domain": "전자상거래",
    "complexity": "medium"
}
# → 완전한 API 스펙과 코드 자동 생성
```

## 📖 실무 예제

### 1. 사용자 관리 시스템
- 회원가입, 로그인, 프로필 관리
- JWT 인증 시스템
- PostgreSQL 데이터베이스

### 2. 블로그 시스템  
- 포스트 작성, 수정, 삭제
- 카테고리 및 태그 관리
- MySQL 데이터베이스

### 3. 전자상거래 시스템
- 상품 관리, 장바구니, 주문 처리
- 결제 시스템 통합 준비
- PostgreSQL 데이터베이스

## 🚀 사용법

### 1. 웹 인터페이스 접속
```
http://localhost:8000
```

### 2. API 설정
- API 이름과 설명 입력
- 프레임워크 및 데이터베이스 선택
- 인증 방식 설정

### 3. 엔드포인트 정의
- 예제 템플릿 선택 또는
- 커스텀 엔드포인트 직접 추가

### 4. 코드 생성 및 다운로드
- "API 생성하기" 버튼 클릭
- 생성된 코드 확인
- 전체 프로젝트 파일 다운로드

### 5. 생성된 API 실행
```bash
cd 다운로드한_프로젝트
pip install -r requirements.txt
python main.py
# → http://localhost:8000/docs 에서 API 문서 확인
```

## 🔧 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **Pydantic**: 데이터 검증 및 직렬화
- **SQLAlchemy**: Python SQL ORM
- **Uvicorn**: ASGI 서버

### AI Integration
- **OpenAI GPT-4**: 자연어 처리 및 코드 생성
- **LangChain**: AI 워크플로우 관리

### Frontend
- **Alpine.js**: 가벼운 JavaScript 프레임워크
- **Tailwind CSS**: 유틸리티 우선 CSS 프레임워크

## 📚 API 엔드포인트

### 기본 기능
- `GET /` - 웹 인터페이스
- `GET /api/examples` - 예제 목록
- `POST /api/generate` - 코드 생성
- `POST /api/download` - 파일 다운로드

### AI 기능 (main3.py)
- `POST /api/ai/generate-from-description` - 자연어 → API 스펙
- `POST /api/ai/enhance-code` - AI 코드 최적화
- `GET /api/ai/status` - AI 기능 상태 확인

## 🎓 학습 가이드

### 1. 초보자 (main1_exercise.py)
1. TODO 주석 확인
2. GPT 프롬프트 작성
3. 함수별 구현 연습
4. 코드 리뷰 및 개선

### 2. 중급자 (main1.py → main2.py)
1. 완성된 코드 분석
2. 웹 인터페이스 구조 이해
3. 코드 생성 로직 파악
4. UI/UX 개선 방법 학습

### 3. 고급자 (main3.py + ai_code_gen.py)
1. AI 통합 방법론 학습
2. 프롬프트 엔지니어링 실습
3. 코드 품질 자동화
4. 실무 적용 방안 모색

## 📄 라이센스

이 프로젝트는 AGPL-3.0 라이센스 하에 배포됩니다. 사용하실 수 있지만 상업적 목적으로 사용하지 마세요. 자세한 내용은 [LICENSE](../LICENSE) 파일을 참조하세요.

**Made for AI Course Students**

*이 도구를 통해 학생들이 현대적인 API 개발 기술을 효과적으로 학습하고, AI 도구를 활용한 개발 워크플로우를 경험할 수 있기를 바랍니다.*