# Version history

V0–V4是回溯整理的階段名稱。只有v0.4.0是本次準備的發布快照；沒有建立虛構的歷史commit或tags。

## v0.5.0 — Planned

- QLoRA參數敏感度：learning rate、rank/alpha、target modules。
- 前置：文章群組切分、未微調同後端對照、mask/截斷/解析檢查。
- 固定資料後比較品質與成本，候選組多seed驗證。尚未實作。

## v0.4.0 — Publication snapshot, 2026-10-14

- 整理五份notebook及歷史指標，完成公開目錄、執行說明與限制文件。
- 移除outputs、執行次數、憑證賦值、私人資料路徑與個人kernel metadata。
- 修正發布副本的adapter路徑不一致、Phase2示範解碼整段prompt問題。
- 基準notebook可關閉學生；教師API預設關閉；禁止下載失敗靜默改toy；預設不沿用舊CSV快取。
- 產資料缺少服務／教師時停止，拒絕覆寫已有JSONL。
- 原始研究檔未修改；發布副本修改後未重跑模型，故歷史結果不是這份程式的新實驗結果。

## V4 / v0.4.x — Historical milestone

adapter合併、F16 GGUF、Q4_K_M量化、Ollama部署與後端行為觀察。

## V3 / v0.3.x — Historical milestone

內部驗證、FaithBench 750筆比較、recall與specificity取捨分析。

## V2 / v0.2.x — Historical milestone

Qwen3-4B QLoRA訓練；從整段文字loss修正成assistant-only supervision；存adapter與loss紀錄。

## V1 / v0.1.x — Historical milestone

本機模型摘要生成、GPT-4o中性prompt標註、JSONL資料；修正prompt大括號格式化問題。

## V0 / v0.0.x — Historical milestone

FaithBench載入與標籤政策、規則和LLM基準、指標輸出；從概念驗證形成評估流程。
