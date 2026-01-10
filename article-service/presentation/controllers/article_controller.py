from fastapi import APIRouter, Query, HTTPException
from application.use_cases.get_article import GetArticleUseCase
from application.use_cases.create_article import CreateArticleUseCase
from infrastructure.repositories.cache_strategies.cache_aside import CacheAsideStrategy
from infrastructure.repositories.cache_strategies.write_through import WriteThroughStrategy
from infrastructure.repositories.cache_strategies.write_behind import WriteBehindStrategy
from infrastructure.repositories.cache_strategies.read_through import ReadThroughStrategy

router = APIRouter(prefix="/articles", tags=["articles"])

def get_cache_strategy(strategy_name: str):
    try:
        if strategy_name == "write_through":
            return WriteThroughStrategy()
        elif strategy_name == "write_behind":
            return WriteBehindStrategy()
        elif strategy_name == "read_through":
            return ReadThroughStrategy()
        return CacheAsideStrategy()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Strategy initialization failed: {str(e)}")

@router.get("/{article_id}")
async def get_article(
    article_id: str,
    strategy: str = Query("cache_aside", enum=["cache_aside", "write_through", "write_behind", "read_through"])
):
    try:
        strategy_impl = get_cache_strategy(strategy)
        use_case = GetArticleUseCase(strategy_impl)
        article = use_case.execute(article_id)
        
        if article:
            return {
                "id": article.id,
                "title": article.title,
                "content": article.content,
                "views": article.views,
                "created_at": article.created_at.isoformat()
            }
        return {"error": "Article not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
async def create_article(
    title: str,
    content: str,
    strategy: str = Query("cache_aside", enum=["cache_aside", "write_through", "write_behind", "read_through"])
):
    try:
        strategy_impl = get_cache_strategy(strategy)
        use_case = CreateArticleUseCase(strategy_impl)
        article = use_case.execute(title, content)
        
        return {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "views": article.views,
            "created_at": article.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))