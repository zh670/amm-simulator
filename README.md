# AMM 时间管理工具

这是一个轻量级的时间管理工具，支持文本或语音记录时间，并自动生成日报、周报、月报、年报与建议，还可以导出多种格式以及做简单的思维发散。

## 功能概览

- **记录**：用文字或语音记录正在做的事情与时间。
- **统计**：自动汇总每天的记录，并提供分析与建议。
- **报告**：自动生成周报、月报、年报。
- **导出**：支持 JSON / CSV / Markdown。
- **思维发散**：记录想法并提供下一步问题提示。

## 使用方式

```bash
python -m time_manager.cli log "写周报 for 45m note: 完成总结"
python -m time_manager.cli summary
python -m time_manager.cli report weekly
python -m time_manager.cli export csv ./time-export.csv
python -m time_manager.cli brainstorm "提升专注力" "最近容易分心"
```

### 语音输入

如果本机已安装 `speech_recognition` 以及麦克风环境可用，可以启用语音输入：

```bash
python -m time_manager.cli log --voice
```

## 数据存储

默认数据文件：`~/.amm_time_manager/data.json`。可通过环境变量自定义路径：

```bash
export TIME_MANAGER_DATA=/path/to/data.json
```

## 报告说明

- 日报：当天记录
- 周报：本周（周一至周日）
- 月报：当前月
- 年报：当前年

## 发散提示

`brainstorm` 会记录你的主题与想法，并给出5条可执行的发散提示，帮助你快速切入下一步思考。


## 预览 BloomMind 原型

这个仓库包含一个可直接运行的静态预览页：`preview_bloommind.html`。

```bash
python -m http.server 8000
```

然后在浏览器打开：`http://localhost:8000/preview_bloommind.html`。


### Mac 用户一键预览（无需命令行）

如果你是 Mac 用户，不想运行任何命令：

1. 在 Finder 打开仓库目录。
2. 双击 `open_bloommind_preview.command`。
3. 浏览器会自动打开 `preview_bloommind.html`。

你也可以直接双击 `preview_bloommind.html` 进行预览。
