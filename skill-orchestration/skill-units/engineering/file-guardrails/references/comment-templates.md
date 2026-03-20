# 顶部说明模板

## Python

```python
"""一句话说明文件用途。

主要职责：
- 职责 1
- 职责 2

快速开始：
    from module import MainClass
    result = MainClass().run(...)
"""
```

## JavaScript / TypeScript

```ts
/**
 * 一句话说明文件用途。
 *
 * 主要职责：
 * - 职责 1
 * - 职责 2
 *
 * @example
 * import { run } from './module';
 * run();
 */
```

## Shell / Bash

```bash
#!/usr/bin/env bash
# 一句话说明脚本用途。
#
# 用法：
#   ./script.sh [options]
#
# 示例：
#   ./script.sh --help
```

## Go

```go
// Package name 提供一句话功能说明。
//
// 主要职责：
//   - 职责 1
//   - 职责 2
package name
```

## Java

```java
/**
 * 一句话说明类或文件用途。
 *
 * <p>主要职责：
 * <ul>
 *   <li>职责 1</li>
 *   <li>职责 2</li>
 * </ul>
 */
```

## 模板使用规则

- 保留最少必要字段，不要为了“完整”把每一段都写满。
- `主要职责` 只列高价值点，通常 2-4 条足够。
- `快速开始` 只在首次使用成本较高时保留。
- 如果文件足够简单，最小版一段注释通常就够了。
