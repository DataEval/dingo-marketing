.PHONY: help install install-dev run test lint format clean

# 默认目标
help:
	@echo "Dingo Marketing - AI Agent 驱动的自动化运营系统"
	@echo ""
	@echo "可用命令:"
	@echo "  install      安装生产依赖"
	@echo "  install-dev  安装开发依赖"
	@echo "  run          启动应用"
	@echo "  test         运行测试"
	@echo "  lint         代码检查"
	@echo "  format       代码格式化"
	@echo "  clean        清理临时文件"

# 安装依赖
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# 运行应用
run:
	python run.py

# 测试
test:
	pytest

test-cov:
	pytest --cov=src --cov-report=html

# 代码质量
lint:
	flake8 src/ tests/
	mypy src/
	bandit -r src/

format:
	black src/ tests/
	isort src/ tests/

# 清理
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

# 开发环境设置
setup-dev: install-dev
	pre-commit install

# 安全检查
security:
	safety check
	bandit -r src/

# 生成需求文件
freeze:
	pip freeze > requirements-freeze.txt

# 数据库操作（如果需要）
db-init:
	python -c "from src.database import init_database; import asyncio; asyncio.run(init_database())"

# 启动开发服务器
dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# 生产环境启动
prod:
	uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4 