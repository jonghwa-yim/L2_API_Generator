# OpenAI API 통합 REST API 생성기
# pip install fastapi uvicorn pydantic openai python-dotenv

import os
from datetime import datetime

from fastapi import FastAPI, HTTPException

from api_generator.ai_code_gen import (
    AICodeGenerator,
    AIEnhancedCodeGenerator,
    GenerationMode,
    NaturalLanguageRequest,
)

app = FastAPI(
    title="AI-Powered REST API Generator", description="OpenAI 통합 지능형 API 생성기"
)

# ============================================================================
# 기존 템플릿 기반 생성기 (단계별 학습용)
# ============================================================================

# Check main2.py and copy necessary codes


# ============================================================================
# AI 통합 생성기
# ============================================================================

ai_generator = AICodeGenerator()
enhanced_generator = AIEnhancedCodeGenerator()


# ============================================================================
# AI 기능 엔드포인트 (OpenAI API 키 필요)
# ============================================================================


@app.post("/api/ai/generate-from-description")
async def generate_api_from_description(request: NaturalLanguageRequest):
    """자연어 설명으로 API 스펙 생성 (OpenAI 필요)"""

    # OpenAI API 키 확인
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 설정해주세요.",
        )

    try:
        result = await ai_generator.generate_api_spec_from_description(request)
        return {
            "success": True,
            "data": result.api_spec,
            "reasoning": result.reasoning,
            "suggestions": result.suggestions,
            "confidence_score": result.confidence_score,
        }
    except Exception as e:
        import traceback

        error_detail = f"AI 생성 실패: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)


@app.post("/api/ai/enhance-code")
async def generate_enhanced_code(spec: dict, mode: str = "ai_assisted"):
    """AI로 향상된 코드 생성"""

    try:
        generation_mode = GenerationMode(mode)
        result = await enhanced_generator.generate_enhanced_api(spec, generation_mode)
        return {
            "success": True,
            "data": result,
            "mode": mode,
            "generated_at": datetime.now().isoformat(),
        }
    except Exception as e:
        # AI 실패 시 기본 생성기로 폴백
        result = None # TODO: Implement here like FastAPICodeGenerator.generate_api(spec)
        return {
            "success": True,
            "data": result,
            "mode": "basic_fallback",
            "note": f"AI 생성 실패로 기본 생성기 사용: {str(e)}",
        }


@app.get("/api/ai/status")
async def get_ai_status():
    """AI 기능 상태 확인"""
    return {
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY")),
        "features": {
            "natural_language_generation": bool(os.getenv("OPENAI_API_KEY")),
            "code_enhancement": bool(os.getenv("OPENAI_API_KEY")),
            "code_review": bool(os.getenv("OPENAI_API_KEY")),
        },
    }


if __name__ == "__main__":
    import uvicorn

    print("🤖 AI-Powered REST API Generator 시작!")
    print("=" * 60)
    print("🌐 웹 인터페이스: http://localhost:8000")
    print("📖 API 문서: http://localhost:8000/docs")
    print("🤖 AI 기능:")
    print("   - 자연어 → API 스펙 변환")
    print("   - 지능형 비즈니스 로직 생성")
    print("   - 자동 코드 리뷰 및 최적화")
    print("=" * 60)

    uvicorn.run("main3:app", host="localhost", port=8000, reload=True)
