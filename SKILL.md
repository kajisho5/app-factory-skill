---
name: app-factory-skill
description: 'Generate build prompts for mass-produced App Store apps (iPhone/iPad/Mac/Watch) from an app-factory dashboard pipeline (a candidate list of low-rated competitor apps and their top complaints): pick a candidate that wedges into those complaints (ads, sneaky subscriptions, abandoned updates, data loss), then write a complete, paste-ready development prompt for the AI/agent that will build the app — with house defaults baked in (Apple HIG compliance, portrait-iPhone/rotating-iPad orientation policy, dark mode, Dynamic Type, VoiceOver, String Catalogs, privacy manifest, App Review guideline 4.3 awareness, upfront disclosure of free-tier limits, acceptance-test report, Liquid Glass layered icons, demo mocks for iPhone/iPad/Mac/iPhone Duo, raster (PNG) previews alongside vector sources, public-first GitHub repos with a no-secrets rule). Originally built for the kajisho5/app-factory-dashboard pipeline; adapt the data source and paths to your own setup (see README). Use this skill whenever the user mentions an app pipeline or 量産ダッシュボード, picking the next app to build, writing a プロンプト for an app, or adding a new default rule to the prompts — even when they do not say "skill". Japanese-first workflow; prompts are written in Japanese.'
---

# app-factory-skill

このスキルは「アプリ量産」のためのプロンプト生成ワークフローです。アプリ本体の実装は、プロンプトを受け取った別のClaudeが行います。このスキルを使うエージェントの仕事は、**候補の選定と、開発プロンプトの作成まで**です。勝手にアプリ本体を実装し始めないでください。

## 情報源

- 候補リスト: 自分のアプリ量産ダッシュボードのリポジトリにある候補CSV（例： kajisho5/app-factory-dashboard の `data/source/app_pipeline_60.csv`、61件）。各候補には対象競合（App Storeの低評価アプリ）、評価・レビュー数、低評価レビューの不満内訳、差別化の切り口（angle）、推定開発日数、シーズン、市場、対応プラットフォームが入っている
- 事業計画: 同リポジトリの事業計画ドキュメント（例： `data/source/business_plan.md`）、概要は README
- 量産ペースは運用者ごとに異なる（元の環境では月5本・年60本ペース）。状態管理（候補・仕様・開発中・審査中・公開・保守・撤退）はダッシュボード側で行う

## ワークフロー

1. **候補を選ぶ** — ユーザーが指定しない場合は、CSVから根拠つきで提案する。提案前に、保存済みのプロンプト（手順4の保存先フォルダと、このリポジトリの `examples/`）を確認し、すでにプロンプト作成済みの候補を重複して提案しない。判断材料： 需要の証明（競合のレビュー数・売上ランキング）、不満の集中度（1〜2種類の不満に偏っているほど切り口が刺さる）、推定開発日数（短いほど量産の1周が速い）、シーズン（年賀状・確定申告など時期ものは締切から逆算し、間に合わないものは提案しない）。写真・保管系などデータ消失リスクの高いものや開発日数の長いものは、量産の流れが回ってからの後回しが無難
2. **プロンプトを作る** — `templates/prompt-template.md` の共通デフォルトをすべて含め、アプリ固有部分（コンセプト／技術条件／機能仕様／課金設計／権限とプライバシー）を候補の内容で埋める。完成例が `examples/` に2本ある（誠実QRリーダー、宛名印刷）ので、粒度と書き方の基準にすること
3. **デザインの抜けを監査する** — 仕上がったプロンプトを design-check-skill（例： kajisho5/design-check-skill）のプラットフォーム別チェックリスト（iPhone / iPad / iPhone Duo / Mac / 共通）で監査し、抜けがあれば直して再チェックする。監査は design-check-skill の終了条件（「新規の抜けゼロ」のパスが3回連続するまで回す）に従う
4. **保存して渡す** — プロンプトは自分の作業フォルダ配下の `<アプリのslug>/prompt.md` に保存し（元の環境では `~/workspace/apps/<slug>/prompt.md`）、ファイルとしてユーザーに渡す（チャットに全文を貼らない）
5. **公開までの橋渡し** — プロンプトを渡したら、ダッシュボード上で候補の状態を進める（候補→仕様、着手したら開発中）ようユーザーに案内する。このスキルからダッシュボードやCSVを書き換えることはしない
6. **デフォルトが変わったら差分も出す** — 共通デフォルトに追加・変更があったら、テンプレートと作成済みプロンプトを更新するだけでなく、ユーザーが手元のプロンプトに貼れるよう、**追加文言だけの差分をコードブロックで別途提示する**（ユーザーはプロンプトを自分の環境で管理しているため）

## 公開後の扱い

- 公開後の状態管理（保守・集中投下・撤退の判定）はダッシュボード／事業計画側の役割であり、このスキルの対象は新規アプリのプロンプト作成まで
- OSアップデート対応や不具合修正など、保守用のプロンプトが必要になった場合も、同じテンプレートと共通デフォルトで作る（差別化の原則と課金の誠実さは保守でも維持する）
- 問い合わせ対応やレビュー返信の文面作成はこのスキルの対象外

## 共通デフォルト（全プロンプト必須）

### デザイン
- **Appleの Human Interface Guidelines (HIG) に必ず沿う** [3]。HIGと実装側の判断が衝突したらHIGを優先し、その旨を報告させる
- iOS標準の見た目と操作感を基本とし、独自UIは必要最小限にする
- **画面の向き**: iPhoneは縦向き固定（回転対応しない）。iPadは回転と画面分割（Split View / Stage Manager）に対応し、サイズ変更でレイアウトが崩れないこと。例外（写真・動画系など横が自然なもの）は候補ごとに指定
- iPhoneは片手操作を想定し、主要アクションは画面の下部〜中部に配置。シートの開閉操作は全画面で一貫させる
- iPadは画面幅を活かしたレイアウト（サイドバー＋詳細など）にし、ポインタのホバーとハードウェアキーボードの主要ショートカットに対応する
- Mac対応アプリでは標準のメニューバー・主要ショートカット・ウィンドウのリサイズ追従を用意する。「Designed for iPad」で動作させる場合はその方針を明記し、Mac専用UIは作らない
- ソフトウェアキーボード表示時に、入力中の項目や確定ボタンが隠れないようにする
- 起動画面（Launch Screen）はシンプルにし、広告・ロゴアニメ・待機演出を入れない

### 品質・標準対応
- ダークモード（色はアセットカタログ定義、両モードで確認）
- Dynamic Type（最大文字サイズでも崩れない）
- VoiceOverラベルとコントラスト比の確保
- UI文字列は String Catalogs (.xcstrings) で管理し、ハードコードしない（初期言語は日本語、Global展開に備える）
- 権限拒否時の代替導線（設定アプリへの誘導）と、データ空状態の画面を必ず用意する
- 無料版の制限（件数・機能）は、ユーザーがぶつかる前に画面上で明示させる。制限到達時の挙動も明示し、無言でデータを削除させない
- プライバシーマニフェスト (PrivacyInfo.xcprivacy) と必須理由APIの申告 [2]
- ユーザーデータはiCloudバックアップ対象にし、アップデートや機種変更で消えない設計（パイプラインの不満で「データ消失」が頻出するため、差別化としても効く）

### 課金の誠実さ
- 候補の切り口が課金不満の場合、そのまま設計原則にする： 広告なし・サブスクなし・買い切り（非消耗型IAP 1点）を基本形とする
- 課金画面に「買い切りであること、定期支払いが発生しないこと」を明記させる
- 無料お試し・期間限定価格など誤認させる表現、作業の佳境（印刷直前など）で課金画面を挟む導線を明示的に禁止する
- StoreKit商品IDはプロンプト内で明示する（例： `<アプリのslug>.pro`）

### 審査・法務
- App Store審査ガイドライン4.3（スパム）を意識させる [1]： テンプレートや部品を使い回しても各アプリの固有価値を実装と掲載文で明確にし、違いの分からない類似アプリを連続して提出させない
- アプリ名・掲載文・キーワードに競合の商標・製品名を使わせない。根拠のない最上級・誇大表現も使わせない
- プライバシーラベル等の申告と実装の一致を必須にする（申告と異なる収集が必要になったら勝手に実装せず報告させる）

### アイコンとモック
- アプリアイコンは **fresnel**（Liquid Glassアイコン作成ツール。例： kajisho5/fresnel [6]。無い場合は任意のレイヤードアイコン作成手段でよい）で作成し、iOSの Liquid Glass スタイルのレイヤードアイコン (.icon) にする [4][5]。必要な全サイズを書き出し、ライト／ダーク／クリア／ティントの外観バリアントも用意。デザインはHIGのアイコン指針に従う（文字を入れない、シンプルなグリフ）
- デモモックは **iPhone / iPad / Mac / iPhone Duo（iPhone 2台並び）**。ただしアプリの対応プラットフォーム分のみ（Mac版のないアプリにMacモックは不要）。主要画面を実機フレームで表示し、App Store掲載素材に転用できる品質にする。iPhone Duoは2画面の状態を一致させ、役割分担が分かる並びにする
- **視覚成果物はベクター原版に加えてラスター画像（PNG）のプレビューを必ず添える**。確認する人の環境で表示できない形式だけに頼らない（例： スマートフォンで確認する運用では、SVG単体は表示できないことがある）

### リポジトリと進め方
- 成果物はGitHubの新規**パブリック**リポジトリで管理し、工程ごとにコミット・プッシュ（後日プライベートに変更する運用）。**秘密情報（APIキー・証明書・個人情報）は公開期間があるため絶対にコミットしない**
- 提出用ビルドは、その時点で最新のXcodeと現行のiOS SDKで作成させる（提出要件は変わるため、提出前に最新の要件を確認させる）
- 進め方の歯止め： 最初はプロジェクト構成と画面遷移の設計だけを提示して確認待ち → 機能ブロックごとに実装し、各ステップでビルド確認 → 仕様にない判断は勝手に広げず、選択肢と推奨案を提示して確認

### 納品物（プロンプトに明記）
- ビルド可能なXcodeプロジェクト一式 / アプリアイコン一式 / デモモック（対応プラットフォーム分、PNG添付、成果物はリポジトリの `deliverables/` にまとめる） / README（ビルド手順・定数一覧・App Store Connect側作業のチェックリスト） / 動作確認レポート（主要フロー・権限拒否時・データ空時・両モード・最大文字サイズ・iPad分割表示の確認結果） / App Store掲載文の下書き（タイトル・サブタイトル各30字以内、説明文）

## やらないこと

- アプリ本体の実装（それはプロンプトを受け取るClaudeの仕事）
- ダッシュボードやパイプラインCSVの書き換え（状態管理はユーザーのダッシュボード側）
- 仕様の根拠のないプラットフォーム追加や、候補データにない競合情報の創作

## 出典・参考

共通デフォルトのうち外部の権威ある情報に基づく主張の出典です。本文中の [n] はこの一覧への参照です。

1. App Store Review Guidelines（§4.3 Spam）: https://developer.apple.com/app-store/review/guidelines/
2. Apple Developer Documentation — Privacy manifest files（プライバシーマニフェストと必須理由API）: https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
3. Apple Human Interface Guidelines（トップ）: https://developer.apple.com/design/human-interface-guidelines
4. Apple Human Interface Guidelines — Materials（Liquid Glass）: https://developer.apple.com/design/human-interface-guidelines/materials
5. Apple Human Interface Guidelines — App Icons: https://developer.apple.com/design/human-interface-guidelines/app-icons
6. fresnel（レイヤードアイコン作成ツール）: https://github.com/kajisho5/fresnel
