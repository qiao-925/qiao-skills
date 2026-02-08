# 🔍 数据来源验证Prompt

## 🎯 核心目标
**数据质量 > 数据数量** - 通过自动化脚本验证数据来源的有效性，确保引用链接的可用性和相关性

## 📋 Prompt模板

### 🔍 链接验证模式

```
你是一位数据来源验证专家，擅长通过自动化脚本验证链接的有效性和内容相关性。

**验证要求**：
1. 分析文章内容，识别需要验证的数据来源
2. 创建Python验证脚本，检查链接可用性
3. 通过语义分析评估内容相关性
4. 生成详细的验证报告和统计数据

**脚本功能要求**：
- HTTP状态码检查（200、301、302、404等）
- 超时和连接错误处理
- 并发处理提高效率
- 内容抓取和语义相关性分析
- 详细的验证日志和统计报告

**输出格式**：
📊 **验证统计**：[总数、成功数、失败数、成功率]
✅ **有效链接**：[状态码、响应时间、相关性评分]
❌ **无效链接**：[错误类型、失败原因]
🔍 **相关性分析**：[内容匹配度、主题相关性]
💡 **优化建议**：[基于验证结果的改进建议]

请对以下内容进行数据来源验证：[粘贴文章内容或链接列表]
```

### 📊 批量验证模式

```
作为批量验证专家，请帮我：

**验证目标**：
- 批量验证大量数据来源的有效性
- 自动识别和分类不同类型的链接
- 生成可读的验证报告和统计数据
- 提供数据质量评估和改进建议

**验证脚本要求**：
```python
# 核心功能模块
1. 链接分类器：识别官方文档、技术博客、学术论文等
2. 状态检查器：HTTP状态码、响应时间、重定向处理
3. 内容分析器：标题提取、关键词匹配、相关性评分
4. 报告生成器：统计图表、详细日志、优化建议
```

**输出结构**：
📈 **质量指标**：[可用性、相关性、权威性评分]
📋 **分类统计**：[按来源类型的成功/失败统计]
🎯 **相关性矩阵**：[链接与文章主题的匹配度]
⚠️ **问题识别**：[常见错误类型和解决方案]
🔄 **优化建议**：[基于验证结果的改进方案]

请执行批量验证：[提供链接列表或文章内容]
```

### 🎯 智能分析模式

```
你是一位智能数据分析专家，请帮我：

**分析维度**：
1. **可用性分析**：链接的可访问性和稳定性
2. **相关性分析**：内容与文章主题的匹配度
3. **权威性分析**：来源的可信度和影响力
4. **时效性分析**：内容的更新频率和时效性
5. **完整性分析**：数据覆盖的全面性

**智能评估算法**：
- **可用性权重**：40%（可访问性、响应速度）
- **相关性权重**：30%（内容匹配、主题相关）
- **权威性权重**：20%（来源可信度、影响力）
- **时效性权重**：10%（更新频率、内容新鲜度）

**输出报告**：
📊 **综合评分**：[加权平均的总体质量评分]
🎯 **质量分布**：[各评分区间的链接分布]
📈 **趋势分析**：[验证结果的时间趋势]
💡 **改进建议**：[针对低质量链接的优化方案]

请进行智能分析：[提供验证数据]
```

### 🔧 自定义验证模式

```
我们正在进行自定义数据来源验证。

**验证配置**：
- **超时设置**：[自定义超时时间]
- **并发数**：[并发请求数量]
- **重试策略**：[失败重试次数和间隔]
- **评分标准**：[自定义相关性评分算法]
- **输出格式**：[自定义报告格式]

**验证流程**：
1. 你创建自定义验证脚本
2. 我确认配置参数
3. 你执行验证并生成报告
4. 我评估结果质量
5. 迭代优化直到满足要求

**特殊要求**：
- [具体的技术要求或限制]
- [特定的验证标准]
- [自定义的输出格式]

请开始自定义验证：[描述具体需求]
```

---

## 🎯 使用场景

### 📝 技术文章验证
- 验证技术博客中的引用链接
- 检查官方文档链接的有效性
- 评估第三方资源的质量
- 确保参考文献的可访问性

### 📊 研究报告验证
- 验证学术论文的引用来源
- 检查数据集的可用性
- 评估研究方法的可靠性
- 确保结论的可重现性

### 💼 商业文档验证
- 验证产品文档的外部链接
- 检查竞争对手信息的准确性
- 评估市场数据的可靠性
- 确保商业决策的数据支撑

### 🎓 学术研究验证
- 验证研究假设的数据支撑
- 检查理论框架的引用准确性
- 评估实验数据的来源可靠性
- 确保研究结论的可信度

---

## 🔧 验证脚本模板

### 📋 基础验证脚本

```python
import requests
import concurrent.futures
import time
from urllib.parse import urlparse
import json

class LinkValidator:
    def __init__(self, timeout=10, max_workers=5):
        self.timeout = timeout
        self.max_workers = max_workers
        self.results = []
    
    def validate_single_link(self, url):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=self.timeout)
            response_time = time.time() - start_time
            
            return {
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'content_length': len(response.content),
                'is_valid': 200 <= response.status_code < 400,
                'error': None
            }
        except Exception as e:
            return {
                'url': url,
                'status_code': None,
                'response_time': None,
                'content_length': 0,
                'is_valid': False,
                'error': str(e)
            }
    
    def validate_batch(self, urls):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(self.validate_single_link, urls))
        
        return self.generate_report(results)
    
    def generate_report(self, results):
        total = len(results)
        valid = sum(1 for r in results if r['is_valid'])
        failed = total - valid
        
        return {
            'summary': {
                'total': total,
                'valid': valid,
                'failed': failed,
                'success_rate': valid / total * 100 if total > 0 else 0
            },
            'valid_links': [r for r in results if r['is_valid']],
            'failed_links': [r for r in results if not r['is_valid']],
            'detailed_results': results
        }
```

### 🎯 高级分析脚本

```python
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import time

class ContentAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def analyze_content(self, url, keywords):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取文本内容
            text = soup.get_text()
            title = soup.find('title').get_text() if soup.find('title') else ''
            
            # 计算相关性评分
            relevance_score = self.calculate_relevance(text, title, keywords)
            
            return {
                'url': url,
                'title': title,
                'content_length': len(text),
                'relevance_score': relevance_score,
                'keyword_matches': self.find_keywords(text, keywords),
                'domain_authority': self.assess_domain_authority(url)
            }
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'relevance_score': 0
            }
    
    def calculate_relevance(self, text, title, keywords):
        score = 0
        text_lower = text.lower()
        title_lower = title.lower()
        
        for keyword in keywords:
            # 标题中的关键词权重更高
            if keyword.lower() in title_lower:
                score += 3
            # 正文中的关键词
            if keyword.lower() in text_lower:
                score += 1
        
        return min(score, 10)  # 最高10分
    
    def assess_domain_authority(self, url):
        domain = urlparse(url).netloc
        
        # 简单的权威性评估
        authority_indicators = [
            'github.com', 'stackoverflow.com', 'docs.microsoft.com',
            'developer.mozilla.org', 'w3.org', 'ietf.org'
        ]
        
        for indicator in authority_indicators:
            if indicator in domain:
                return 'high'
        
        return 'medium'
```

---

## 📊 验证报告模板

### 📈 统计报告

```
# 数据来源验证报告

## 📊 验证统计
- **总链接数**: 25
- **有效链接**: 18 (72%)
- **无效链接**: 7 (28%)
- **平均响应时间**: 1.2秒
- **平均相关性评分**: 7.8/10

## ✅ 有效链接 (18个)
1. https://docs.python.org/3/ - 状态码: 200, 响应时间: 0.8s, 相关性: 9/10
2. https://github.com/python/cpython - 状态码: 200, 响应时间: 1.1s, 相关性: 8/10
...

## ❌ 无效链接 (7个)
1. https://example.com/old-doc - 状态码: 404, 错误: 页面不存在
2. https://broken-link.com - 状态码: None, 错误: 连接超时
...

## 💡 优化建议
1. 替换404错误的链接为最新文档
2. 优化超时链接的网络连接
3. 增加更多官方文档引用
4. 定期验证链接有效性
```

---

## 💡 最佳实践

### 🎯 验证策略
1. **分层验证**：先验证可用性，再分析相关性
2. **批量处理**：使用并发提高验证效率
3. **定期检查**：建立链接验证的定期机制
4. **质量评估**：建立多维度的质量评分体系

### 🔧 技术优化
1. **超时设置**：根据网络环境调整超时时间
2. **重试机制**：对临时性错误进行重试
3. **缓存机制**：避免重复验证相同链接
4. **错误处理**：优雅处理各种网络异常

### 📊 数据分析
1. **趋势分析**：跟踪链接质量的变化趋势
2. **分类统计**：按来源类型分析质量分布
3. **相关性评估**：评估内容与主题的匹配度
4. **权威性分析**：评估来源的可信度和影响力

---

## ⚠️ 注意事项

### 🚨 验证限制
- 某些网站可能限制爬虫访问
- 动态内容可能需要JavaScript渲染
- 某些链接可能需要认证才能访问
- 网络环境可能影响验证结果

### 🔒 隐私保护
- 遵守网站的robots.txt规则
- 合理控制请求频率，避免对服务器造成压力
- 保护敏感信息，避免在验证过程中泄露
- 遵守相关法律法规和网站使用条款

---

*记住：数据来源验证是确保内容质量的重要环节。通过自动化脚本进行系统性的验证，可以大大提高数据来源的可靠性和文章的可信度。*
