# US Stock Auto Trading Simulator

Pythonで実装した米国株の自動売買シミュレーター。20日移動平均線×50日移動平均線のゴールデンクロス戦略を使用してバックテストを実行します。

## 機能

- ✅ 複数銘柄の同時シミュレーション（AAPL, MSFT等）
- ✅ テクニカル指標計算（移動平均線、RSI等）
- ✅ 移動平均線クロスオーバー戦略
- ✅ バックテストエンジン（手数料・スリッページ計上）
- ✅ ポートフォリオ管理と損益計算
- ✅ パフォーマンス分析（シャープレシオ、ドローダウン等）
- ✅ 結果の可視化（チャート、トレード履歴等）
- ✅ **Webアプリ版（FastAPI）** - ブラウザで利用可能、iPhone対応

## プロジェクト構成

```
stock-simulator/
├── src/
│   ├── api.py                # FastAPI バックエンド
│   ├── data_fetcher.py       # 株価データ取得
│   ├── indicator.py          # テクニカル指標計算
│   ├── strategy.py           # 売買戦略定義
│   ├── simulator.py          # バックテストエンジン
│   ├── portfolio.py          # ポートフォリオ管理
│   ├── main.py               # CLIエントリーポイント
│   └── __init__.py
├── frontend/
│   ├── index.html            # Webアプリページ
│   ├── style.css             # スタイル（レスポンシブ対応）
│   └── app.js                # JavaScriptロジック
├── data/                      # 株価データベース
├── output/                    # 結果出力
├── run_server.sh             # サーバー起動スクリプト
├── requirements.txt
└── README.md
```

## インストール

```bash
# 依存ライブラリをインストール
pip install -r requirements.txt
```

## 使用方法

### Webアプリ版（推奨 - iPhone対応）

```bash
# サーバー起動
./run_server.sh

# または
cd src
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

ブラウザで `http://localhost:8000` を開く（iPhone、iPad、PCから利用可能）

### CLIバージョン

```bash
cd src
python main.py
```

### シミュレーション設定の変更

`src/main.py` の `main()` 関数内で以下を変更できます：

```python
symbols = ['AAPL', 'MSFT']          # 対象銘柄
start_date = '2023-01-01'           # 開始日
end_date = '2024-09-30'             # 終了日
initial_capital = 100000            # 初期資金
```

## 戦略説明

### 移動平均線クロスオーバー戦略

- **ゴールデンクロス（買いシグナル）** ：20日MAが50日MAを上回る
- **デッドクロス（売りシグナル）** ：20日MAが50日MAを下回る

```
       ↑ 短期MA (20日)
      /
     /
    / ← ゴールデンクロス = BUY
   /
  /-------- 長期MA (50日)
```

## 出力結果

### コンソール出力
- 初期資金と最終資産
- 総利益率（%）
- トレード数
- 勝率
- シャープレシオ
- 最大ドローダウン

### ファイル出力

#### `output/equity_curve.csv`
日ごとの資産推移

| date | equity |
|------|--------|
| 2023-01-03 | 100000.00 |
| 2023-01-04 | 100500.50 |
| ... | ... |

#### `output/trades.csv`
すべての売買履歴

| date | symbol | action | shares | price | profit |
|------|--------|--------|--------|-------|--------|
| 2023-09-15 | AAPL | BUY | 302 | 165.44 | |
| 2023-09-22 | AAPL | SELL | 302 | 157.34 | -2444.34 |

#### `output/backtest_chart.png`
資産推移と日次リターンのグラフ

## 結果例

```
============================================================
SIMULATION RESULTS
============================================================
Initial Capital:     $     100,000
Final Value:         $      96,872
Total Return:               -3.13%
Total Trades:                  13
Winning Trades:                 1
Win Rate:                     7.7%
Sharpe Ratio:               -0.22
Max Drawdown:               -7.85%
============================================================
```

## パフォーマンス指標

- **Total Return** ：(最終資産 - 初期資金) / 初期資金 × 100
- **Sharpe Ratio** ：（平均日次リターン / リターンの標準偏差） × √252
- **Max Drawdown** ：ピークから谷までの最大下落率
- **Win Rate** ：利益が出たトレードの割合

## 拡張可能性

このシミュレーターは以下のように拡張できます：

- [ ] 複数戦略の実装（RSI、MACD等）
- [ ] パラメータ最適化
- [ ] リスク管理（損切り、ポジションサイジング）
- [ ] ウォークフォワード分析
- [ ] 機械学習による予測モデル
- [ ] リアルタイム取引機能

## 注意事項

- これはシミュレーターです。過去のテスト結果が将来の利益を保証するものではありません
- 実際の取引には多くの要因（流動性、スリッページ、経済ニュース等）が関与します
- 投資は自己責任で行ってください

## ライセンス

MIT License

## 作成者

Claude Haiku 4.5
