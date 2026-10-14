# Publication scope

## 納入

- 5份去除輸出的notebook，對應評估、資料生成、訓練、驗收與部署。
- 歷史彙總指標CSV，不含原文、逐例摘要與完整教師回應。
- README、CHANGELOG、已知限制、來源對照表、直接依賴與靜態檢查腳本。

## 排除

- distill_data.jsonl/csv、exp1_results_long.csv：原文／摘要／逐例回應；資料授權與公開範圍未逐一確認。
- student_halluc_detector/、student_merged_fp16/、所有GGUF/checkpoint/optimizer檔：大型產物，不是原始程式。
- llama.cpp/：第三方程式，不整份複製；部署notebook按需取得。
- 概念notebook與中文Phase1副本：內容重複或較早版本，發布保留目前主流程。
- prompt修補腳本：修補內容已整合到主notebook，不再要求讀者手動套patch。
- 舊目標、交接記憶、求職資料、面試論證備忘錄：私人脈絡或過時結論，不適合當公開專案說明。
- 舊loss曲線與notebook輸出：避免與整理後程式混淆；歷史數字以明確標記的彙總呈現。

`source_manifest.json`列出原檔到公開檔的對照。公開副本有移除憑證、路徑修正與執行保護等修改，不能當成原檔的逐位元備份。

版本策略：每個完成且可檢視的更新做commit；里程碑發布才打tag。首次公開為v0.4.0，參數比較完成後才發布v0.5.0。不要只因README寫了計畫就先宣稱完成該版本。
