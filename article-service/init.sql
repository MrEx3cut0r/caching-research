CREATE TABLE IF NOT EXISTS articles (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_articles_views ON articles(views DESC);
CREATE INDEX IF NOT EXISTS idx_articles_created_at ON articles(created_at DESC);

INSERT INTO articles (id, title, content, views) VALUES
('hot_article_1', 'Most Popular Article', 'This is a hot article...', 1000),
('hot_article_2', 'Second Popular', 'Another hot article...', 800),
('cold_article_1', 'Rarely Read', 'This is cold data...', 5),
('cold_article_2', 'Very Old Article', 'Old content...', 2)
ON CONFLICT (id) DO NOTHING;