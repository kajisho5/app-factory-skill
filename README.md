# app-factory-skill

アプリ量産ダッシュボード（kajisho5/app-factory-dashboard）のパイプライン候補から次に作るアプリを選び、開発担当のClaudeに渡す「開発プロンプト」を作成するためのスキルです。

## 使い方

Claude（やスキル対応エージェント）にこのリポジトリをスキルとして読み込ませ、「パイプラインから次のアプリを選んで」「○○のプロンプトを作って」と頼むだけです。進め方の詳細は `SKILL.md` にあります。

## 構成

- `SKILL.md` — ワークフローと共通デフォルトの本体
- `templates/prompt-template.md` — プロンプトの雛形（共通デフォルト＋アプリ固有部分の差し替え枠）
- `examples/` — 作成済みプロンプトの実例2本（誠実QRリーダー / 宛名印刷 はがき・封筒）

## 前提

- 候補データは kajisho5/app-factory-dashboard の `data/source/app_pipeline_60.csv`
- アプリ本体の実装はこのスキルでは行わず、生成したプロンプトを別のClaudeに渡して作らせる運用です
- アプリアイコンは kajisho5/fresnel で作成します
