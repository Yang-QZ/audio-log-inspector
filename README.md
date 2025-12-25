# Audio Log Inspector

MTK8676成组化平台audio日志分析工具 / Audio Log Analysis Tool for MTK8676 Platform

## 简介 (Introduction)

这是一个专为联发科 MTK8676 芯片平台设计的音频 HAL (Hardware Abstraction Layer) 日志分析工具。该工具可以解析 Android logcat 日志，提取音频相关信息，并生成详细的分析报告。

This is an audio HAL (Hardware Abstraction Layer) log analysis tool specifically designed for MediaTek MTK8676 chipset platform. It can parse Android logcat logs, extract audio-related information, and generate detailed analysis reports.

## 功能特性 (Features)

- 📊 自动解析音频 HAL 日志
- 🔍 识别音频错误和警告
- 🎵 跟踪音频流操作（打开/关闭）
- 🔊 监控音频设备切换
- 📈 生成统计分析报告
- ⚡ 支持 MTK8676 平台特定日志格式

- 📊 Automatic audio HAL log parsing
- 🔍 Error and warning detection
- 🎵 Audio stream operation tracking (open/close)
- 🔊 Audio device change monitoring
- 📈 Statistical analysis report generation
- ⚡ MTK8676 platform-specific log format support

## 安装 (Installation)

```bash
# 克隆仓库 (Clone repository)
git clone https://github.com/<your-username>/audio-log-inspector.git
cd audio-log-inspector

# 确保安装 Python 3.6+ (Ensure Python 3.6+ is installed)
python3 --version
```

## 使用方法 (Usage)

### 基本用法 (Basic Usage)

```bash
# 分析日志文件 (Analyze log file)
python3 audio_log_inspector.py <log_file>

# 示例 (Example)
python3 audio_log_inspector.py sample_log.txt
```

### 保存报告 (Save Report)

```bash
# 分析并保存报告到文件 (Analyze and save report to file)
python3 audio_log_inspector.py <log_file> <output_report>

# 示例 (Example)
python3 audio_log_inspector.py sample_log.txt report.txt
```

### 获取设备日志 (Getting Device Logs)

```bash
# 从 Android 设备获取音频相关日志 (Get audio-related logs from Android device)
adb logcat -d > logcat.txt

# 或者实时监控 (Or monitor in real-time)
adb logcat | grep -i audio > audio_log.txt
```

## 示例输出 (Example Output)

```
================================================================================
Audio Log Inspector Report - MTK8676 Platform
================================================================================

## Summary Statistics
Total audio-related log entries: 23
Errors (E): 2
Warnings (W): 2
Audio stream operations: 4
Device changes: 3

## Errors Detected
--------------------------------------------------------------------------------
1. [10:15:42.100] AudioFlinger
   Failed to create track, error: -12 (ENOMEM)
2. [10:15:42.105] AudioPolicyManager
   getOutput() failed to allocate output stream

## Warnings Detected
--------------------------------------------------------------------------------
1. [10:15:33.200] AudioFlinger
   buffer underrun detected on track 1234
2. [10:15:43.200] audio_hw_primary
   device busy, waiting...

## Audio Stream Operations
--------------------------------------------------------------------------------
Streams opened: 2
Streams closed: 2

## Audio Device Changes
--------------------------------------------------------------------------------
1. [10:15:35.100] setDeviceConnectionState() device: AUDIO_DEVICE_OUT_WIRED_HEADSET state: connected
```

## 配置文件 (Configuration)

`config_mtk8676.json` 包含 MTK8676 平台的配置信息：
- 支持的音频标签 (Supported audio tags)
- 错误和警告关键字 (Error and warning keywords)
- 设备类型 (Device types)
- 音频流类型 (Stream types)
- 常见问题模式 (Common issue patterns)

## 支持的日志标签 (Supported Log Tags)

- AudioFlinger
- AudioPolicyManager
- AudioHAL
- audio_hw_primary
- MTKAudioHardware
- AudioALSA
- AudioStreamOut
- AudioStreamIn

## 系统要求 (Requirements)

- Python 3.6 或更高版本 (Python 3.6 or higher)
- 对于 Android 设备日志：ADB 工具 (For Android device logs: ADB tools)

## 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！
Issues and Pull Requests are welcome!

## 许可证 (License)

MIT License

## 作者 (Author)

Yang-QZ

## 更新日志 (Changelog)

### v1.0.0 (2025-12-25)
- 初始版本发布 (Initial release)
- 支持 MTK8676 音频 HAL 日志分析 (MTK8676 audio HAL log analysis support)
- 错误和警告检测 (Error and warning detection)
- 音频流和设备跟踪 (Audio stream and device tracking)
