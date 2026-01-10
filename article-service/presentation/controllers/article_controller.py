from fastapi import APIRouter, Query
from application.use_cases.get_article import GetArticleUseCase
from application.use_cases.create_article import CreateArticleUseCase
from infrastructure.repositories.cache_strategies.cache_aside import CacheAsideStrategy
from infrastructure.repositories.cache_strategies.write_through import WriteThroughStrategy

router = APIRouter()

def get_strategy(strategy_name: str):
    if strategy_name == "write_through":
        return WriteThroughStrategy()
    return CacheAsideStrategy() 

@router.get("/articles/{article_id}")
async def get_article(
    article_id: str,
    strategy: str = Query("cache_aside", enum=["cache_aside", "write_through"])
):
    strategy_impl = get_strategy(strategy)
    use_case = GetArticleUseCase(strategy_impl)
    article = use_case.execute(article_id)
    return article if article else {"error": "Not found"}

@router.post("/articles")
async def create_article(title: str, content: str, strategy: str = "cache_aside"):
    strategy_impl = get_strategy(strategy)
    use_case = CreateArticleUseCase(strategy_impl)
    article = use_case.execute(title, content)
    return article 