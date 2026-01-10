import asyncio
import aiohttp
import pytest
import time
import statistics

class TestPerformance:
    @pytest.mark.asyncio
    async def test_simple_load(self):
        async with aiohttp.ClientSession() as session:
            times = []
            for i in range(40):
                start = time.time()
                async with session.get("http://localhost:8000/health") as response:
                    assert response.status == 200
                times.append(time.time() - start)
            avg = statistics.mean(times) * 1000
            print(f"Avg response: {avg:.2f}ms")

    @pytest.mark.asyncio
    async def test_cache_hit_miss(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:8000/articles",
                params={"title": "Test", "content": "Content", "strategy": "cache_aside"}
            ) as resp:
                article_id = (await resp.json())["id"]

            miss_times = []
            for _ in range(5):
                start = time.time()
                async with session.get(
                    f"http://localhost:8000/articles/{article_id}",
                    params={"strategy": "cache_aside"}
                ) as resp:
                    miss_times.append(time.time() - start)
                await asyncio.sleep(0.01)

            hit_times = []
            for _ in range(5):
                start = time.time()
                async with session.get(
                    f"http://localhost:8000/articles/{article_id}",
                    params={"strategy": "cache_aside"}
                ) as resp:
                    hit_times.append(time.time() - start)

            avg_miss = statistics.mean(miss_times) * 1000
            avg_hit = statistics.mean(hit_times) * 1000
            
            print(f"Avg miss: {avg_miss:.2f}ms, Avg hit: {avg_hit:.2f}ms")
            
            improvement = avg_miss - avg_hit
            if improvement > 0:
                print(f"Improvement: {improvement:.2f}ms ({avg_miss/avg_hit:.1f}x faster)")
            else:
                print("No improvement detected")
            
            assert avg_hit <= avg_miss * 1.1

    @pytest.mark.asyncio
    async def test_strategy_comparison(self):
        async with aiohttp.ClientSession() as session:
            strategies = ["cache_aside", "write_through", "write_behind", "read_through"]
            results = {}
            
            for strategy in strategies:
                times = []
                for _ in range(5):
                    start = time.time()
                    async with session.get(
                        f"http://localhost:8000/articles/test_hot",
                        params={"strategy": strategy}
                    ) as resp:
                        assert resp.status == 200
                    times.append(time.time() - start)
                
                results[strategy] = statistics.mean(times) * 1000
                print(f"{strategy}: {results[strategy]:.2f}ms")
            
            return results