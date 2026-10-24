---
name: app-factory-skill
description: 'Generate build prompts for mass-produced App Store apps (iPhone/iPad/Mac/Watch) from the app-factory-dashboard pipeline: pick a candidate app that wedges into low-rated competitors complaints (ads, sneaky subscriptions, abandoned updates, data loss), then write a complete, paste-ready development prompt for the Claude that will build the app — with all house defaults baked in (Apple HIG compliance, portrait-iPhone/rotating-iPad orientation policy, dark mode, Dynamic Type, VoiceOver, String Catalogs, privacy manifest, Liquid Glass icons made with kajisho5/fresnel, demo mocks for iPhone/iPad/Mac/iPhone Duo, PNG previews because the user checks on iPhone, public-first GitHub repos with a no-secrets rule). Use this skill whenever the user mentions the app pipeline, the 量産ダッシュボード, picking the next app to build, writing a プロンプト for an app, or adding a new default rule to the prompts — even when they do not say "skill". Japanese-first workflow; prompts are written in Japanese.'
---

# app-factory-skill

このスキルは「アプリ量産」のためのプロンプト生成ワークフローです。アプリ本体の実装は、プロンプトを受け取った別のClaudeが行います。このスキルを使うエージェントの仕事は、**候補の選定と、開発プロンプトの作成まで**です。勝手にアプリ本体を実装し始めないでください。

## 情報源

- 候補リスト: GitHub リポジトリ `kajisho5/app-factory-dashboard` の `data/source/app_pipeline_60.csv`（61件）。各候補には対象競合（App Storeの低評価アプリ）、評価・レビュー数、低評価レビューの不満内訳、差別化の切り口（angle）、推定開発日数、シーズン、市場、対応プラットフォームが入っている
- 事業計画: 同リポジトリ `data/source/business_plan.md`、概要は README
- 月5本・年60本ペースの量産計画。状態管理（候補・仕様・開発中・審査中・公開・保守・撤退）はダッシュボード側で行う

## ワークフロー

1. **候補を選ぶ** — ユーザーが指定しない場合は、CSVから根拠つきで提案する。判断材料： 需要の証明（競合のレビュー数・売上ランキング）、不満の集中度（1〜2種類の不満に偏っているほど切り口が刺さる）、推定開発日数（短いほど量産の1周が速い）、シーズン（年賀状・確定申告など時期ものは締切から逆算し、間に合わないものは提案しない）。写真・保管系などデータ消失リスクの高いものや開発日数の長いものは、量産の流れが回ってからの後回しが無難
2. **プロンプトを作る** — `templates/prompt-template.md` の共通デフォルトをすべて含め、アプリ固有部分（コンセプト／技術条件／機能仕様／課金設計／権限とプライバシー）を候補の内容で埋める。完成例が `examples/` に2本ある（誠実QRリーダー、宛名印刷）ので、粒度と書き方の基準にすること
3. **保存して渡す** — プロンプトは `~/workspace/apps/<アプリのslug>/prompt.md` に保存し、ファイルとしてユーザーに渡す（チャットに全文を貼らない）
4. **デフォルトが変わったら差分も出す** — 共通デフォルトに追加・変更があったら、テンプレートと作成済みプロンプトを更新するだけでなく、ユーザーが手元のプロンプトに貼れるよう、**追加文言だけの差分をコードブロックで別途提示する**（ユーザーはプロンプトを自分の環境で管理しているため）

## 共通デフォルト（全プロンプト必須）

### デザイン
- **Appleの Human Interface Guidelines (HIG) に必ず沿う**。HIGと実装側の判断が衝突したらHIGを優先し、その旨を報告させる
- **画面の向き**: iPhoneは縦向き固定（回転対応しない）。iPadは回転と画面分割（Split View / Stage Manager）に対応し、サイズ変更でレイアウトが崩れないこと。例外（写真・動画系など横が自然なもの）は候補ごとに指定

### 品質・標準対応
- ダークモード（色はアセットカタログ定義、両モードで確認）
- Dynamic Type（最大文字サイズでも崩れない）
- VoiceOverラベルとコントラスト比の確保
- UI文字列は String Catalogs (.xcstrings) で管理し、ハードコードしない（初期言語は日本語、Global展開に備える）
- 権限拒否時の代替導線（設定アプリへの誘導）と、データ空状態の画面を必ず用意する
- プライバシーマニフェスト (PrivacyInfo.xcprivacy) と必須理由APIの申告
- ユーザーデータはiCloudバックアップ対象にし、アップデートや機種変更で消えない設計（パイプラインの不満で「データ消失」が頻出するため、差別化としても効く）

### 課金の誠実さ
- 候補の切り口が課金不満の場合、そのまま設計原則にする： 広告なし・サブスクなし・買い切り（非消耗型IAP 1点）を基本形とする
- 課金画面に「買い切りであること、定期支払いが発生しないこと」を明記させる
- 無料お試し・期間限定価格など誤認させる表現、作業の佳境（印刷直前など）で課金画面を挟む導線を明示的に禁止する

### アイコンとモック
- アプリアイコンは **kajisho5/fresnel**（Liquid Glassアイコン作成ツール）で作成し、iOSの Liquid Glass スタイルのレイヤードアイコン (.icon) にする。ライト／ダーク／ティントの外観バリアントも用意
- デモモックは **iPhone / iPad / Mac / iPhone Duo（iPhone 2台並び）**。ただしアプリの対応プラットフォーム分のみ（Mac版のないアプリにMacモックは不要）
- **視覚成果物はSVG原版に加えてPNGプレビューを必ず添える**。ユーザーは基本iPhoneで確認しており、SVGは表示できない

### リポジトリと進め方
- 成果物はGitHubの新規**パブリック**リポジトリで管理し、工程ごとにコミット・プッシュ（後日プライベートに変更する運用）。**秘密情報（APIキー・証明書・個人情報）は公開期間があるため絶対にコミットしない**
- 進め方の歯止め： 最初はプロジェクト構成と画面遷移の設計だけを提示して確認待ち → 機能ブロックごとに実装し、各ステップでビルド確認 → 仕様にない判断は勝手に広げず、選択肢と推奨案を提示して確認

### 納品物（プロンプトに明記）
- ビルド可能なXcodeプロジェクト一式 / fresnel製アプリアイコン一式 / デモモック（対応プラットフォーム分、PNG添付） / README（ビルド手順・定数一覧） / App Store掲載文の下書き（タイトル・サブタイトル各30字以内、説明文）

## やらないこと

- アプリ本体の実装（それはプロンプトを受け取るClaudeの仕事）
- ダッシュボードやパイプラインCSVの書き換え（状態管理はユーザーのダッシュボード側）
- 仕様の根拠のないプラットフォーム追加や、候補データにない競合情報の創作
