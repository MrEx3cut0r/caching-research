import pytest
import requests

class TestSimple:
    def test_health(self):
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        print(f"Health: {response.json()}")
    
    def test_create_cache_aside(self):
        response = requests.post(
            "http://localhost:8000/articles",
            params={
                "title": "Simple Test",
                "content": "Simple content",
                "strategy": "cache_aside"
            }
        )
        print(f"Create response: {response.status_code} - {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        return data["id"]
    
    def test_get_cache_aside(self):
        article_id = self.test_create_cache_aside()
        response = requests.get(
            f"http://localhost:8000/articles/{article_id}",
            params={"strategy": "cache_aside"}
        )
        print(f"Get response: {response.status_code} - {response.text}")
        assert response.status_code == 200
    
    def test_all_strategies_simple(self):
        strategies = ["cache_aside", "write_through", "read_through"]
        
        for strategy in strategies:
            print(f"\nTesting {strategy}:")
            
            # Create
            response = requests.post(
                "http://localhost:8000/articles",
                params={
                    "title": f"{strategy} Article",
                    "content": f"Content for {strategy}",
                    "strategy": strategy
                }
            )
            print(f"  Create: {response.status_code}")
            
            if response.status_code == 200:
                article_id = response.json()["id"]
                
                # Get
                response = requests.get(
                    f"http://localhost:8000/articles/{article_id}",
                    params={"strategy": strategy}
                )
                print(f"  Get: {response.status_code}")