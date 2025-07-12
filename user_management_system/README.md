# User Management API API 문서

## 개요
사용자 등록, 인증, 프로필 관리를 위한 REST API

- **버전:** 1.0.0
- **프레임워크:** fastapi
- **데이터베이스:** postgresql
- **인증:** jwt

## 빠른 시작

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. 실행
```bash
python main.py
```

### 3. API 문서 확인
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## API 엔드포인트


### HTTPMethod.POST /api/auth/register

**설명:** 새 사용자 등록

**파라미터:** 없음

**요청 본문:**
```json
{"username": "testuser", "email": "test@example.com", "password": "password123"}
```

**응답:**
```json
{"success": true, "message": "User created", "data": {"id": 1, "username": "testuser"}}
```

---

### HTTPMethod.POST /api/auth/login

**설명:** 사용자 로그인

**파라미터:** 없음

**요청 본문:**
```json
{"username": "testuser", "password": "password123"}
```

**응답:**
```json
{"access_token": "jwt_token_here", "token_type": "bearer"}
```

---

### HTTPMethod.GET /api/users

**설명:** 사용자 목록 조회

**파라미터:** page, limit (선택사항)

**요청 본문:**
```json
없음
```

**응답:**
```json
{"success": true, "data": {"items": [], "total": 10}}
```

---

### HTTPMethod.GET /api/users/{user_id}

**설명:** 특정 사용자 정보 조회

**파라미터:** user_id: 사용자 ID

**요청 본문:**
```json
없음
```

**응답:**
```json
{"success": true, "data": {"id": 1, "username": "testuser", "email": "test@example.com"}}
```

---


## 사용 예시

### 기본 요청
```bash
curl -X GET "http://localhost:8001/" -H "accept: application/json"
```

```PowerShell
Invoke-WebRequest -Uri "http://localhost:8001/" -Method GET -Headers @{accept="application/json"}
```

### 헬스 체크
```bash
curl -X GET "http://localhost:8001/health" -H "accept: application/json"
```

### 유저 등록
```PowerShell
Invoke-RestMethod -Uri "http://localhost:8001/api/auth/register" -Method POST -Headers @{accept="application/json"} -Body '{"username": "testuser", "email": "test@example.com", "password": "password123"}' -ContentType "application/json"
```

## 개발 정보

이 API는 REST API Generator에 의해 자동 생성되었습니다.

- 생성 시간: 2025-07-12T10:56:28.689327
- 프레임워크: FastAPI
- 문서화: 자동 생성 (OpenAPI/Swagger)

## 다음 단계

1. 데이터베이스 연결 설정
2. 인증 시스템 구현
3. 비즈니스 로직 추가
4. 테스트 작성
5. 배포 설정
