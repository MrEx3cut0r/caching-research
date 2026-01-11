import pytest
import requests
import time
import statistics
import json
import os

class TestAllStrategies:
    
    def setup_method(self):
        self.base_url = "http://localhost:8000"
        self.strategies = ["cache_aside", "write_through", "read_through", "write_behind"]
        os.makedirs("test-results", exist_ok=True)
    
    def test_all_strategies_health(self):
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
    
    def test_create_with_all_strategies(self):
        for strategy in self.strategies:
            data = {
                "title": f"Test {strategy}",
                "content": f"Content for {strategy} strategy",
                "strategy": strategy
            }
            response = requests.post(f"{self.base_url}/articles", params=data)
            print(f"{strategy}: {response.status_code} - {response.text[:100]}")
            assert response.status_code == 200
            result = response.json()
            assert result["title"] == data["title"]
            article_id = result["id"]
            
            response = requests.get(f"{self.base_url}/articles/{article_id}", params={"strategy": strategy})
            assert response.status_code == 200
    
    def test_performance_comparison(self):
        results = {}
        
        for strategy in self.strategies:
            times = []
            
            for i in range(100):
                start = time.perf_counter()
                response = requests.get(
                    f"{self.base_url}/articles/test_hot",
                    params={"strategy": strategy}
                )
                elapsed = time.perf_counter() - start
                
                if response.status_code == 200:
                    times.append(elapsed)
                else:
                    print(f"Error {strategy}: {response.status_code}")
            
            if times:
                results[strategy] = {
                    "avg_ms": statistics.mean(times) * 1000,
                    "min_ms": min(times) * 1000,
                    "max_ms": max(times) * 1000,
                    "samples": len(times)
                }
        
        print("\n" + "="*60)
        print("PERFORMANCE COMPARISON")
        print("="*60)
        
        for strategy, metrics in results.items():
            print(f"\n{strategy.upper():20}")
            print(f"  Avg: {metrics['avg_ms']:.2f} ms")
            print(f"  Min: {metrics['min_ms']:.2f} ms")
            print(f"  Max: {metrics['max_ms']:.2f} ms")
            print(f"  Samples: {metrics['samples']}")
        
        with open("test-results/strategies_comparison.json", "w") as f:
            json.dump(results, f, indent=2)
        
        return results
