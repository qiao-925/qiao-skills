# 文档搜索策略与提问指引

## 提问/抓取指引

- 在 Cursor 提问时添加：`use context7`，并指明要查的包与页面（如 "Streamlit file_uploader"）
- 若 Context7 报错或无结果：调用 `firecrawl_scrape <URL>` 抓取表中推荐的官方文档 URL
- 需要的主要文档 URL 与首选抓取方式参见项目中的 `references/tech-stack-docs.md`

## 搜索关键词构造

```
# 基础搜索
{库名} {方法名} example

# 错误搜索
{库名} {错误消息}

# 版本搜索
{库名} {版本号} migration guide
```

## 搜索示例

```
llama_index VectorStoreIndex example
llama_index AttributeError has no attribute 'query'
llama_index 0.10 migration guide
```

## 文档查找优先级

1. 官方文档网站
2. API 参考文档
3. GitHub README
4. 官方示例代码

## 类似问题搜索资源

- GitHub Issues
- Stack Overflow
- 官方论坛/Discord
