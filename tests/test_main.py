"""
测试主应用功能 - 集成测试
"""
import pytest
import requests
import time

# 应用基础 URL
BASE_URL = "http://localhost:8080"

def test_application_is_running():
    """测试应用是否正在运行"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        print(f"✅ 应用健康检查通过: {data}")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"应用未运行或无法连接: {e}")

def test_root_endpoint():
    """测试根端点"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Dingo Marketing" in data["message"]
        print(f"✅ 根端点测试通过: {data}")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"无法连接到应用: {e}")

def test_health_endpoint():
    """测试健康检查端点"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "components" in data
        print(f"✅ 健康检查端点测试通过: {data}")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"无法连接到应用: {e}")

def test_api_status_endpoint():
    """测试 API 状态端点"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/status", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        print(f"✅ API 状态端点测试通过: {data}")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"无法连接到应用: {e}")

def test_api_docs_endpoint():
    """测试 API 文档端点"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        assert response.status_code == 200
        print("✅ API 文档端点可访问")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"无法连接到应用: {e}")

def test_invalid_endpoint():
    """测试无效端点"""
    try:
        response = requests.get(f"{BASE_URL}/invalid-endpoint", timeout=5)
        assert response.status_code == 404
        print("✅ 无效端点正确返回 404")
    except requests.exceptions.RequestException as e:
        pytest.skip(f"无法连接到应用: {e}")

if __name__ == "__main__":
    # 可以直接运行此文件进行快速测试
    print("🧪 开始测试 Dingo Marketing 应用...")
    
    try:
        test_application_is_running()
        test_root_endpoint()
        test_health_endpoint()
        test_api_status_endpoint()
        test_api_docs_endpoint()
        test_invalid_endpoint()
        print("🎉 所有测试通过!")
    except Exception as e:
        print(f"❌ 测试失败: {e}") 