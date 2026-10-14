# Historical limitations

本發布保留歷史方法供閱讀，未假裝已完成下列修正。

1. 按列切分85/15，2,000列有959個source字串群組；可能跨集合共享文章。Phase3沿用的是Phase2訓練期驗證集，不是獨立test。
2. 單一教師與兩種摘要生成來源，尚無充分人工標籤稽核；風格分布只是低specificity的可能解釋，未證實主因。
3. FaithBench已被反覆檢視，後續用它調參應承認探索性；不能聲稱是全新未看過測試。
4. HF學生與Ollama prompt-only對照的模型版本、數值路徑、模板不同。教師成績不是學生理論上限。
5. Phase3/4及部分baseline解析會把無法辨識答案視為CONSISTENT。歷史指標受此政策限制，應改明列無效輸出率。
6. 2048-token截斷可能移除摘要、證據或監督答案；assistant_only_loss設為True不等於實際mask已驗證。
7. 部分markdown是當時操作註記，可能有舊模型名稱、分類為一個字的簡化表述，或對同kernel狀態的假設；以設定格與README為準。Phase4建議使用全新kernel釋放GPU。
8. 核心Python相依與llama.cpp revision未鎖定，模型及教師revision亦未完全固定。未執行乾淨環境端到端重現。
9. API與模型生成仍可能失敗；產資料需檢查失敗標籤(-1)、空摘要與錯誤文字，並保留生成設定。不要把toy/mock當真實訓練資料。
10. 舊部署摘要不足以證明無損、延遲顯著改善或可用於生產。沒有multi-seed與信賴區間，沒有直接量測降低實際交付幻覺的效果。
