# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

L2_RestAPI_Generator is an educational FastAPI-based REST API code generator designed for ML course students to learn API development practices. The project generates complete, production-ready APIs from templates or natural language descriptions using AI integration.

## Development Commands

### Running the Application
```bash
# Navigate to api_generator directory
cd api_generator

# Run basic version (complete implementation)
python main1.py

# Run enhanced UI version
python main2.py

# Run AI-integrated version (requires OpenAI API key)
python main3.py
```

### Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Core dependencies: fastapi, uvicorn, pydantic, jinja2, python-multipart, sqlalchemy
```

### Testing Generated APIs
```bash
# Navigate to generated project (e.g., user_management_system)
cd user_management_system
pip install -r requirements.txt
python main.py

# Access API documentation at http://localhost:8001/docs
```

### AI Features Setup (main3.py)
```bash
# Create .env file with OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Optional environment variables
echo "OPENAI_URL=https://api.openai.com/v1" >> .env
echo "OPENAI_API_MODEL=gpt-4o" >> .env
```

## Architecture

### Core Components

**api_generator/**: Main application directory
- `main1_exercise.py`: Learning version with TODO functions for student practice
- `main1.py`: Complete basic implementation with web interface
- `main2.py`: Enhanced UI version with real-time endpoint management
- `main3.py`: AI-integrated version using OpenAI API
- `ai_code_gen.py`: AI code generation engine with OpenAI integration

**Generated Project Structure**: Each generated API follows this pattern:
```
=� generated_project/
   main.py         # FastAPI application with all endpoints
   models.py       # Pydantic data models
   database.py     # Database configuration and ORM setup
   requirements.txt # Python dependencies
   README.md       # Complete API documentation
```

### Code Generation Flow

1. **Template-based Generation** (main1.py, main2.py):
   - Uses predefined templates for common API patterns
   - Supports 3 example domains: User Management, Blog System, E-commerce
   - Generates 5 files per project with complete CRUD operations

2. **AI-Enhanced Generation** (main3.py + ai_code_gen.py):
   - Natural language � API specification conversion
   - Intelligent business logic generation  
   - Automatic code review and optimization
   - AI-powered improvement suggestions

### Supported Configurations

**Frameworks**: FastAPI (primary), Flask, Express.js
**Databases**: PostgreSQL, MySQL, MongoDB, SQLite
**Authentication**: JWT, OAuth2, API Key, None
**Features**: CRUD operations, pagination, validation, documentation

## Key Classes and Models

### Core Models (main1.py, main2.py, main3.py)
- `EndpointModel`: API endpoint specification
- `APISpecModel`: Complete API specification
- `HTTPMethod`, `Framework`, `Database`, `AuthMethod`: Configuration enums

### AI Integration Models (ai_code_gen.py)
- `NaturalLanguageRequest`: Natural language API requirements
- `AIGeneratedSpec`: AI-generated API specification with reasoning
- `AICodeGenerator`: Template-based code generation with AI assistance
- `AIEnhancedCodeGenerator`: Advanced AI-powered code generation

### Generated API Models (models.py in generated projects)
- Pydantic models for request/response validation
- Database models with proper relationships
- Authentication and authorization models

## Educational Usage

### Learning Progression
1. **Stage 1**: Use `main1_exercise.py` with TODO functions for hands-on learning
2. **Stage 2**: Analyze `main1.py` complete implementation
3. **Stage 3**: Explore enhanced UI in `main2.py`
4. **Stage 4**: Study AI integration in `main3.py` + `ai_code_gen.py`

### Example Projects
The `user_management_system/` directory contains a complete generated API example with user registration, authentication, and profile management using JWT and PostgreSQL.

## Development Notes

- All generated APIs include comprehensive error handling and validation
- FastAPI automatic documentation generation is enabled for all projects
- The web interface runs on http://localhost:8000 for generators
- Generated APIs typically run on http://localhost:8001
- AI features require valid OpenAI API key configuration
- Project uses Korean language extensively in documentation and comments for educational context