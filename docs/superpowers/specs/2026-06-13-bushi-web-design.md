# 卜术占卜Web应用 · 设计文档

**日期：** 2026-06-13
**状态：** 待用户审批

---

## 一、项目概述

一个部署在 Render 上的 Flask Web 应用，用户通过浏览器访问链接即可使用五种中华传统占卜工具。每个工具独立路由、独立页面、独立计算。

### 五种工具

| 工具 | 路由 | 用途 | 输入 |
|------|------|------|------|
| 小六壬 | `/xiaoliuren` | 快速判断吉凶 | 农历月日时 |
| 梅花易数 | `/meihua` | 万物起卦看大方向 | 数字/时间/文字 |
| 六爻 | `/liuyao` | 正经问一件事的成败 | 摇6次卦 + 问事类型 |
| 奇门遁甲 | `/qimen` | 择时择地、大事布局 | 问事时间 + 问事类型 |
| 大六壬 | `/liuren` | 复杂人事纠纷 | 问事时辰 + 问事类型 |

---

## 二、技术架构

```
用户浏览器
    │ 访问 https://xxx.onrender.com
    ▼
┌────────────────────────────┐
│     Flask app.py            │
│                              │
│  GET  /          → index页  │
│  GET  /xiaoliuren → 小六壬  │
│  GET  /meihua     → 梅花   │
│  GET  /liuyao     → 六爻   │
│  GET  /qimen      → 奇门   │
│  GET  /liuren     → 六壬   │
│                              │
│  POST /api/xiaoliuren       │
│  POST /api/meihua           │
│  POST /api/liuyao           │
│  POST /api/qimen            │
│  POST /api/liuren           │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│      计算引擎 (scripts/)     │
│                              │
│  xiaoliuren.py → JSON       │
│  meihua.py     → JSON       │
│  liuyao.py     → JSON       │
│  qimen.py      → JSON       │
│  liuren.py     → JSON       │
└────────────────────────────┘
```

**前端：** 单 HTML 页面，JS fetch 调用 API，动态渲染结果卡片。不刷新页面切换工具。

**后端：** Flask 处理路由 + API。每个占卜工具一个 POST 路由，接收参数，调计算脚本，返回 JSON。

**部署：** Render Web Service，Python 3，gunicorn 启动。

---

## 三、文件结构

```
web占卜/
├── app.py                    # Flask 主程序
├── requirements.txt          # Flask, gunicorn
├── .gitignore
├── README.md
├── static/
│   ├── style.css            # 深色主题样式
│   └── app.js               # 前端交互逻辑
├── templates/
│   └── index.html           # SPA 页面
├── scripts/
│   ├── xiaoliuren.py        # 小六壬计算
│   ├── meihua.py            # 梅花易数计算
│   ├── liuyao.py            # 六爻计算
│   ├── qimen.py             # 奇门遁甲计算
│   └── liuren.py            # 大六壬计算
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-06-13-bushi-web-design.md
```

---

## 四、API 设计

### 通用格式

**请求：** `POST /api/<tool>`
```json
{
  "params": { ... 每个工具不同 ... }
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "result": "大安",
    "interpretation": "...",
    "detail": { ... }
  }
}
```

错误时：
```json
{
  "success": false,
  "error": "参数不正确"
}
```

### 各工具 API

| API | 请求参数 | 响应核心字段 |
|-----|---------|------------|
| POST /api/xiaoliuren | month, day, hour_name | result (六掌诀), steps (推算步骤), advice |
| POST /api/meihua | method (number/time/text), values | upper_gua, lower_gua, moving_yao, body_use, interpretation |
| POST /api/liuyao | lines[6] (每爻正反面), question_type | hexagram, changed, shi_yao, yong_shen, analysis |
| POST /api/qimen | year,month,day,hour, q_type | grid[9] (九宫), yong_shen_gong, auspicious, advice |
| POST /api/liuren | year,month,day,hour, q_type | four_lessons, three_transmissions, twelve_generals, analysis |

---

## 五、前端交互

### 导航

首页默认显示小六壬。顶部横向标签栏切换五个工具。切换时 JS 替换输入表单，不刷新页面。

### 输入区

每个工具有独立的表单：
- 小六壬：三个下拉框（月/日/时）+ 「用当前时间」按钮
- 梅花：三个 tab（数字/时间/文字），默认数字
- 六爻：虚拟摇卦按钮 ×6 + 问事类型下拉 + 开始按钮
- 奇门：日期时间选择器 + 问事类型下拉 + 开始按钮
- 六壬：日期时间选择器 + 问事类型下拉 + 开始按钮

### 结果区

用户点"开始"后，JS 显示 loading → fetch API → 收到 JSON → 渲染结果卡片。卡片内容随工具不同而变化，但结构统一为：标题（吉凶结论）→ 推算过程（可折叠）→ 白话解读 → 具体建议。

### 样式

深色主题（--bg: #0f0f14），金色点缀（--gold: #c9a96e），与命运双鉴风格统一。响应式布局（手机/平板/桌面）。

---

## 六、开发依赖

```
Flask==3.1.0
gunicorn==23.0.0
```

- 所有计算脚本零依赖（纯 Python 标准库）
- Python >= 3.7

---

## 七、部署

**平台：** Render
**类型：** Web Service
**启动命令：** `gunicorn app:app`
**Python 版本：** 3.11+
**免费额度：** 每月 750 小时

部署后获得 `https://<app-name>.onrender.com` 链接。

---

## 八、不做的

- 不保存用户历史记录
- 不做用户登录/注册
- 不做太乙神数（算国运的，不算个人）
- 第一次访问不弹使用指南（以后可以加）
