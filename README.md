# Local Summary Consistency Checker with QLoRA

將 GPT-4o 的摘要事實一致性判斷，以教師標籤蒸餾至 Qwen3-4B，並完成 FaithBench 評估、GGUF 量化與 Ollama 本地部署。

**目的：測試本地小模型是否能透過蒸餾取得大型模型的特定任務能力，並觀察品質與部署資源的取捨。** 目前是偵測器原型；沒有證明生成模型的幻覺降低，也沒有證明學生整體優於未微調模型。

目前發布版本：**v0.4.0**（歷史流程整理版）。V0–V4是依現有成果回溯整理的里程碑，並非過去已有的Git版本。此repo只有目前可取得的整理後程式，不提供不存在的舊程式快照。

## 動機與任務

摘要可能包含原文不支持的事實。大型模型可協助判斷，但本專案希望探索可本地執行的小模型替代方案。輸入為原文與摘要，輸出 `CONSISTENT` 或 `HALLUCINATED`。這是相對於來源文本的一致性判斷，不是一般世界知識查核，也不是金融／法律／醫療決策工具。

## 資料與流程

```text
CNNDM文章 → 本機LLM生成摘要 → GPT-4o教師標註
         → QLoRA SFT → 內部驗證 / FaithBench人工金標評估
         → adapter合併 → F16 GGUF → Q4_K_M → Ollama
```

- 摘要生成器：Ollama `qwen3:4b`、`llama3.2:3b`。
- 標註教師：GPT-4o，中性／Benign-aware prompt。
- 訓練資料：2,000筆教師標籤資料；按完全相同source字串計為959篇不同來源。
- 學生：`Qwen/Qwen3-4B-Instruct-2507`。
- 外部評估：[FaithBench](https://github.com/vectara/FaithBench)，歷史執行750筆。此repo以含Unwanted標註為正例，其餘為負例，gray另計；這是本實驗的二元政策，不代表所有可能政策。
- 本repo不包含CNNDM原文、教師產生的完整資料、FaithBench副本或模型權重。使用者須從原始來源取得資料並遵守各自授權與使用條件。

## 每個step做了什麼

| 階段 | 工作與產物 | 版本定位 |
|---|---|---|
| Step 0：建置評估 | 載入FaithBench、二元化標籤，建立文字重疊、數字規則、Ollama與GPT教師對照；整理中性prompt | V0／v0.0.x：先建立能力驗收基準 |
| Step 1：建立蒸餾資料 | 本機模型生成自然摘要，GPT-4o產生教師標籤與錯誤報告，寫JSONL；修正prompt格式化大括號問題 | V1／v0.1.x：取得可訓練資料 |
| Step 2：QLoRA微調 | NF4量化基底掛LoRA，修正成assistant-only loss，訓練並存adapter | V2／v0.2.x：完成任務微調 |
| Step 3：學生評估 | 重建歷史內部驗證切分，查看混淆矩陣、延遲與錯例；學生接回FaithBench比較 | V3／v0.3.x：量化效果與限制 |
| Step 4：量化部署 | 合併adapter、轉F16 GGUF、量化Q4_K_M，在Ollama比較品質、延遲與檔案大小 | V4／v0.4.0：完成本地部署流程 |
| Next | 建立乾淨對照後，比較QLoRA學習率、rank與作用層，候選設定再做多seed確認 | 規畫v0.5.0，尚未執行 |

## 程式入口

| Notebook | 用法 |
|---|---|
| `00_faithbench_baselines.ipynb` | 先建立規則／prompt基準；訓練後再開USE_STUDENT重跑學生 |
| `01_generate_teacher_data.ipynb` | 讀自己的文章CSV，生成摘要並付費呼叫教師標註 |
| `02_train_qlora.ipynb` | 從distill_data.jsonl訓練，存student_halluc_detector/ |
| `03_evaluate_student.ipynb` | 載入adapter，驗收歷史內部驗證集合 |
| `04_deploy_gguf_ollama.ipynb` | 在新kernel合併、轉GGUF、建立Ollama模型與比較 |

所有notebook置於repo根目錄，**kernel工作目錄也設成repo根目錄**。目前路徑依此設計。不要直接一鍵Run All：先檢查各設定格，尤其付費API、模型下載與部署操作。

## 執行準備

歷史使用Windows、Python 3.11與CUDA GPU。套件與GPU相容性須依實際設備驗證；目前沒有完整環境lockfile，`requirements.txt`僅列直接依賴，不保證重建歷史精確環境。

1. 建立獨立Python環境；依GPU與驅動安裝相容的CUDA PyTorch。不要直接套用CPU版環境做訓練。
2. `python -m pip install -r requirements.txt`，啟動Jupyter並選正確kernel。
3. 安裝並啟動Ollama，取得上述兩個摘要模型。Ollama是外部服務，非pip套件即可提供。
4. 準備 `data/articles.csv`，至少包含 `article` 欄；或設定 `ARTICLES_CSV` 環境變數。真實資料不隨repo發布。
5. 要執行Step 1，先在kernel啟動前以環境變數設定 `OPENAI_API_KEY`；repo不讀取`.env`，也不在notebook保存金鑰。資料生成缺教師或Ollama時會停止，且拒絕覆寫已有的JSONL。
6. Step 0預設不呼叫付費教師API、不載入學生；需要時分別設定 `USE_YOURS=True` / `USE_STUDENT=True`。預設Ollama開啟；先測規則可設 `USE_OLLAMA=False`。FaithBench下載失敗會停止；只有明確關閉USE_FAITHBENCH才使用toy資料，toy結果不是benchmark。
7. Step 2須檢查assistant loss mask、超長輸入與有效答案token。Step 3載入Step 2根目錄adapter。Step 4會另外clone llama.cpp，並安裝其轉檔依賴；首次執行需網路與足夠磁碟空間。

## 歷史結果

以下來自原有實驗CSV，**不是本次發布副本重新執行的結果**。

| FaithBench偵測器（n=750） | Balanced accuracy | 幻覺recall | Specificity |
|---|---:|---:|---:|
| GPT-4o教師 | 0.600 | 0.499 | 0.701 |
| Ollama qwen3:4b prompt-only | 0.584 | 0.264 | 0.904 |
| QLoRA學生 | 0.568 | 0.503 | 0.633 |

學生提高了相對於此prompt對照的召回率，也增加誤報；整體BA沒有更好。模型版本、模板與後端未完全對齊，不能把差異當成微調的乾淨因果效果。學生與教師recall接近，不等於能力追平。

歷史部署：F16約8.1GB，Q4_K_M約2.5GB，檔案約縮小3.2倍。舊300筆內部集合上BA為0.719與0.730，延遲約0.52與0.49秒／筆。該集合曾用於訓練期eval且按列切分，這不是獨立測試的無損證明，也不代表VRAM或速度改善3.2倍。

彙總CSV見 `results/faithbench_historical_metrics.csv`。部署數字來自舊成果摘要，未附完整可稽核的逐例紀錄；與FaithBench結果不能混成同一張排名。

## 限制與下一版

目前按列切85/15，同文章的不同摘要可能跨集合；教師標籤未充分人工稽核，輸出解析有無效答案默認負例問題，長輸入截斷仍須檢查。詳見 [limitations](docs/limitations.md)。

**Next：測試QLoRA微調參數對蒸餾模型的影響。** 執行前先完成文章群組切分、同HF模型同後端的未微調對照、mask與輸出解析檢查。之後固定資料、prompt與評估方式，比較LR（5e-5／1e-4／2e-4）、rank（8／16／32，維持alpha/r=2）與作用層（q/v、attention、attention+MLP）。報BA、recall、specificity、訓練時間、峰值VRAM與adapter大小；候選設定做多seed，不預設一定改善。

## 版本與發布範圍

版本歷程見 [CHANGELOG](CHANGELOG.md)，發布檔案取捨見 [publication scope](docs/publication_scope.md)。未附LICENSE：程式再利用授權待作者決定；模型、資料及第三方工具遵循各自授權。

技術參考：[QLoRA論文](https://arxiv.org/abs/2305.14314)、[PEFT](https://github.com/huggingface/peft)、[TRL](https://github.com/huggingface/trl)、[llama.cpp](https://github.com/ggml-org/llama.cpp)。
