---
name: app-factory-skill
description: 'Write paste-ready Japanese development prompts for mass-produced App Store apps (iPhone, iPad, Mac, Apple Watch) from an app-factory pipeline CSV of low-rated competitor apps and their top complaints. Picks the next candidate with evidence (demand, complaint concentration, dev days, season deadline, template family), fills the shared prompt template with house defaults (HIG, size-class layout and resizing, orientation policy, Dark Mode, Dynamic Type, accessibility, String Catalogs, privacy manifest, honest one-time-purchase IAP with restore, guideline 4.3 awareness, layered Liquid Glass icons, demo mocks with fictional data and PNG previews, public-first repo with a no-secrets rule), audits the result with design-check-skill, and saves it as a file. Does not implement the app or edit the dashboard. Use when the user mentions the app pipeline or 量産ダッシュボード, picking the next app, writing an app プロンプト, or changing the prompt defaults.'
---

# app-factory-skill

「アプリ量産」のためのプロンプト生成ワークフローです。アプリ本体の実装は、プロンプトを受け取った別のAI（または人間）が行います。このスキルを使うエージェントの仕事は、**候補の選定と、開発プロンプトの作成・監査・保存まで**です。勝手にアプリ本体を実装し始めないでください。

## 情報源

- **候補CSV**： アプリ量産ダッシュボードのリポジトリにある候補リスト（元の環境では kajisho5/app-factory-dashboard の `data/source/app_pipeline_60.csv`。ファイル名は60だが、2026-10-21時点で61行）。元の環境の列は次のとおり。手元の形式が違う場合は読み替える

  | 列 | 中身 | 使い方 |
  |---|---|---|
  | `no` | 候補番号 | 報告・ファイル名で参照 |
  | `our_app` | 作るアプリの仮名 | アプリ名の叩き台 |
  | `template_family` | 共通部品の系統（T:単機能ツール、S:スキャナ 等） | 審査ガイドライン4.3対策で、同じ系統を連続させない判断に使う |
  | `target_app` / `target_url` | 対象競合と App Store のURL | 競合の現状確認 |
  | `target_rating` / `target_count` / `target_price` | 競合の評価・評価数・価格 | 需要の証明 |
  | `jp_rank(取得日)` | 取得日時点の順位 | 需要の証明（取得日を必ず併記） |
  | `reviews_sampled` | 調べたレビュー数 | 不満の母数 |
  | `top_complaints(低評価レビュー語数)` | 不満の内訳 | **キーワードの言及数であってレビュー件数ではない**。プロンプトでは「言及数」と書く |
  | `angle` | 差別化の切り口 | コンセプトの軸 |
  | `est_dev_days(推定)` | 推定開発日数 | 量産ペースと締切の判断 |
  | `season` | 時期もの（年賀状 等）か通年か | 締切の逆算 |
  | `market` | JP / Global 等 | 初期言語、EUで配信する場合の準備 |
  | `platforms` | 対応プラットフォーム（例： iPhone+iPad+Watch） | テンプレートのプラットフォーム別ブロックの取捨 |

- **事業計画・調査メモ**： 同リポジトリの `data/source/business_plan.md`（量産ペース、状態管理）と `data/source/platform_research.md`（Watch / Mac を付ける基準、Macネイティブか Designed for iPad かの基準、統合推奨の候補）
- 状態管理（候補・仕様・開発中・審査中・公開・保守・撤退）はダッシュボード側で行う

## ワークフロー

1. **候補を選ぶ** — ユーザーが指定しない場合は、CSVから根拠つきで2〜3件提案する
   - 提案前に、保存済みのプロンプト（手順5の保存先と、このリポジトリの `examples/`）を確認し、作成済みの候補を重複して提案しない。調査メモで「統合推奨」とされている候補は、統合先と一緒に扱う
   - 判断材料： 需要の証明（評価数・順位。順位は取得日を併記）、不満の集中度（1〜2種類の不満に偏っているほど切り口が刺さる）、推定開発日数（短いほど1周が速い）、シーズン、`template_family`
   - **シーズンものは締切から逆算する**： 公開したい時期 −（推定開発日数 ＋ 審査とTestFlight確認の余裕）が今日より前なら提案しない。今日の日付は必ず確認してから計算する
   - **審査ガイドライン4.3対策**： 直前に作った・審査中のアプリと同じ `template_family` を続けて提案するときは、その旨と、機能・UI・訴求をどう変えるかを添える
   - 写真・保管系などデータ消失リスクの高いものや開発日数の長いものは、量産が回ってからの後回しが無難
2. **プロンプトを作る** — `templates/prompt-template.md` を**構成ごと**使う。共通デフォルトは文言をそのまま残し、プラットフォーム別ブロック（【Mac対応時のみ】等）は `platforms` 列に合わせて残す／削る。アプリ固有部分（背景とコンセプト／技術条件／機能仕様／課金設計／権限とプライバシー）を候補の内容で埋める
   - `examples/` の2本は、アプリ固有部分の**具体性の基準**（数値・状態・例外まで書く粒度）として参照する
   - 不足していると実装側が迷う情報（使うフレームワーク、必要な権限と用途説明文、無料版の上限値、エラー時の挙動）は、推測で空欄にせず具体的に書く。決められないものは「確認待ち」として明示し、ユーザーに選択肢を出す
   - 競合の情報はCSVと App Store の掲載ページで確認できる範囲だけを書く（創作しない）
3. **デザインの抜けを監査する** — 仕上がったプロンプトを design-check-skill（kajisho5/design-check-skill）で監査し、その終了条件（観点を変えたパスで「新規の抜けゼロ」が3回連続）まで回す。design-check-skill が使えない環境では、この SKILL.md の共通デフォルトとプロンプトを1項目ずつ突き合わせる簡易チェックを行い、「design-check-skill による監査は未実施」と報告する
4. **自己点検する** — 渡す前に次を確認する
   - テンプレートの見出しがすべて残っている（削ったのは対象外プラットフォームのブロックだけ）
   - `＜…＞` の差し替え枠が残っていない
   - StoreKit商品ID、バンドルIDの案、リポジトリ名、価格、無料版の上限が書かれている
   - 機能仕様で使うAPIに必要な権限が「権限とプライバシー」にすべて書かれている（例： 写真の保存には追加専用の写真ライブラリ権限）
5. **保存して渡す** — プロンプトは作業フォルダ配下の `<アプリのslug>/prompt.md` に保存し（元の環境では `~/workspace/apps/<slug>/prompt.md`）、ファイルとしてユーザーに渡す（チャットに全文を貼らない）。監査の最終報告は短くまとめて添える
6. **公開までの橋渡し** — ダッシュボード上で候補の状態を進める（候補→仕様、着手したら開発中）ようユーザーに案内する。このスキルからダッシュボードやCSVを書き換えることはしない
7. **デフォルトが変わったら差分も出す** — 共通デフォルトに追加・変更があったら、この SKILL.md・テンプレート・`examples/` を更新し、さらにユーザーが手元のプロンプトに貼れるよう、**追加・変更した文言だけをコードブロックで別途提示する**（ユーザーはプロンプトを自分の環境で管理しているため）

## 公開後の扱い

- 公開後の状態管理（保守・集中投下・撤退の判定）はダッシュボード／事業計画側の役割。このスキルの対象は新規アプリのプロンプト作成まで
- OSアップデート対応や不具合修正など保守用のプロンプトが必要な場合も、同じテンプレートと共通デフォルトで作る（差別化の原則と課金の誠実さは保守でも維持する）
- 問い合わせ対応やレビュー返信の文面作成はこのスキルの対象外

## 共通デフォルト（全プロンプト必須）

文言の正本は `templates/prompt-template.md`。ここは要点の一覧です。変更するときは両方を揃えます。

### デザイン
- **Appleの Human Interface Guidelines (HIG) に必ず沿う** [3]。HIGと実装側の判断が衝突したらHIGを優先し、その旨を報告させる
- iOS標準の見た目と操作感を基本とし、独自UIは必要最小限にする
- **レイアウトはサイズクラスで組む**（端末の種類や向きで決め打ちしない）[7]
- **画面の向き**： iPhoneは縦向き固定（例外は候補ごとに指定）。ただし向きを固定してもウィンドウサイズの変化（Mac上のiPhoneミラーリング、iOS 27以降のシーンのリサイズ）で崩れないこと [7][8]。iPadは全方向に対応し、ウィンドウ表示で自由にリサイズされても崩れないこと。`UIRequiresFullScreen` は使わない（iPadOS 26で非推奨、iOS / iPadOS 27 SDKでは全画面固定にならない）[8]
- iPhoneは片手操作を想定し、主要アクションは画面の下部〜中部に配置。シートの開閉操作は全画面で一貫させる
- iPadは画面幅を活かしたレイアウト（サイドバー＋詳細など）にし、ポインタのホバーとハードウェアキーボードの主要ショートカットに対応する。主要コマンドはiPadのメニューバーにも出す
- Mac対応アプリは、Macネイティブか「Designed for iPad」かを候補ごとに明記する。ネイティブなら標準のメニューバー・主要ショートカット・ウィンドウのリサイズ追従を用意。Designed for iPadならMac専用UIは作らない
- Watch対応アプリは、一目で分かる1画面完結の操作、浅い階層とDigital Crown、コンプリケーションと通知で見せる内容、常時表示時の表示内容、iPhoneが近くにないときの動作を決める [9]
- ソフトウェアキーボード表示時に、入力中の項目や確定ボタンが隠れないようにする
- 起動画面（Launch Screen）をInfo.plistで構成する（iOS 27 SDK以降は提出の必須条件）。シンプルにし、広告・ロゴアニメ・待機演出を入れない [10]

### 品質・標準対応
- ダークモード（色はアセットカタログまたはシステムカラーで定義、両モードで確認）
- Dynamic Type（最大文字サイズでも崩れない）
- アクセシビリティ： VoiceOverラベル、コントラスト比（両モード）、コントロールの間隔と最小文字サイズ、色だけに頼らない区別、視差効果を減らす／透明度を下げる／コントラストを上げる 設定への対応 [11]
- UI文字列は String Catalogs (.xcstrings) で管理し、ハードコードしない（初期言語は `market` 列に従う。JPなら日本語）
- 権限拒否時の代替導線（設定アプリへの誘導）と、データ空状態の画面を必ず用意する
- 無料版の制限（件数・機能）は、ユーザーがぶつかる前に画面上で明示させる。制限到達時の挙動も明示し、無言でデータを削除させない
- プライバシーマニフェスト (PrivacyInfo.xcprivacy) と必須理由APIの申告 [2]
- ユーザーデータはiCloudバックアップ対象にし、アップデートや機種変更で消えない設計（パイプラインの不満で「データ消失」が頻出するため、差別化としても効く）

### 課金の誠実さ
- 候補の切り口が課金不満の場合、そのまま設計原則にする： 広告なし・サブスクなし・買い切り（非消耗型IAP 1点）を基本形とする
- 複数プラットフォームに出す場合はユニバーサル購入（1回の購入で全プラットフォームで使える）にする
- 課金画面に「買い切りであること、定期支払いが発生しないこと」を明記させ、購入ボタンには価格をそのまま表示させる
- 購入の復元（リストア）を課金画面と設定画面の両方に置く
- 無料お試し・期間限定価格など誤認させる表現と、作業の佳境（印刷直前など）で課金画面を挟む導線を明示的に禁止する
- StoreKit商品IDはプロンプト内で明示する（例： `<アプリのslug>.pro`）

### 審査・法務
- App Store審査ガイドライン4.3（スパム）を意識させる [1]： 部品を使い回しても各アプリの固有価値を実装と掲載文で明確にし、違いの分からない類似アプリを連続して提出させない
- アプリ名・掲載文・キーワードに競合の商標・製品名を使わせない。根拠のない最上級・誇大表現も使わせない
- プライバシーラベル等の申告と実装の一致を必須にする（申告と異なる収集が必要になったら勝手に実装せず報告させる）
- 提出用ビルドは、その時点で Apple が求める Xcode / SDK で作らせ、提出前に最新の要件を確認させる [12]

### アイコンとモック
- アプリアイコンはレイヤードアイコン (.icon) にする。作成は Icon Composer（Xcode同梱のApple公式ツール）または fresnel（kajisho5/fresnel [6]）[4][5]。キャンバスは iOS / iPadOS / macOS が1024×1024px、watchOSが1088×1088px（円形にマスク、背景を黒にしない）。レイヤーはマスク前の正方形で渡す。iOS / iPadOS / macOS はデフォルト／ダーク／クリア／ティントの外観をすべて用意する（自社ルール）。文字は入れない（自社ルール）
- デモモックは **iPhone / iPad / Mac / Apple Watch / iPhone Duo（iPhone 2台並び）** のうち、アプリの対応プラットフォーム分のみ。主要画面を実機フレームで表示し、App Store掲載素材に転用できる品質にする。iPhone Duoは2画面の状態を一致させ、役割分担が分かる並びにする
- **モックとサンプルデータは明らかに架空の人名・住所・電話番号・会社名を使う**（実在の人物・住所・企業を使わない）
- **視覚成果物はベクター原版に加えてPNGプレビューを必ず添える**（スマートフォンで確認する運用では、SVG単体は表示できないことがある）

### リポジトリと進め方
- 成果物はGitHubの新規**パブリック**リポジトリで管理し、工程ごとにコミット・プッシュ（後日プライベートに変更する運用）。**秘密情報（APIキー・証明書・個人情報）は公開期間があるため絶対にコミットしない**
- 進め方の歯止め： 最初はプロジェクト構成と画面遷移の設計だけを提示して確認待ち → 機能ブロックごとに実装し、各ステップでビルド確認 → 仕様にない判断は勝手に広げず、選択肢と推奨案を提示して確認

### 納品物（プロンプトに明記）
- ビルド可能なXcodeプロジェクト一式 / アプリアイコン一式 / デモモック（対応プラットフォーム分、PNG添付、`deliverables/` にまとめる） / README（ビルド手順・定数一覧・App Store Connect側作業のチェックリスト） / 動作確認レポート / App Store掲載文の下書き（タイトル・サブタイトル各30字以内、説明文）
- App Store Connect側作業のチェックリストには最低限： IAP商品登録、プライバシーポリシーURL、プライバシーラベル、年齢区分の質問への回答、スクリーンショット（必須サイズ）、アクセシビリティ・ニュートリションラベル（現時点は任意。対応した項目を申告）、EUで配信する場合はトレーダー情報 [12][13][14]

## やらないこと

- アプリ本体の実装（それはプロンプトを受け取るAIの仕事）
- ダッシュボードやパイプラインCSVの書き換え（状態管理はユーザーのダッシュボード側）
- 仕様の根拠のないプラットフォーム追加や、候補データ・掲載ページで確認できない競合情報の創作

## 出典・参考

共通デフォルトの根拠（2026年10月時点で確認）。本文中の [n] はこの一覧への参照です。

1. App Store Review Guidelines（§4.3 Spam）: https://developer.apple.com/app-store/review/guidelines/
2. Privacy manifest files: https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
3. Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines
4. HIG — Materials（Liquid Glass）: https://developer.apple.com/design/human-interface-guidelines/materials
5. HIG — App icons（仕様表・外観）: https://developer.apple.com/design/human-interface-guidelines/app-icons
6. fresnel（レイヤードアイコン作成ツール）: https://github.com/kajisho5/fresnel
7. HIG — Layout（サイズクラス、向きを固定してもリサイズに対応）: https://developer.apple.com/design/human-interface-guidelines/layout
8. TN3192: Migrating your app from the deprecated UIRequiresFullScreen key: https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key
9. HIG — Designing for watchOS: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos
10. TN3208: Preparing your app’s launch screen to meet App Store requirements: https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements
11. HIG — Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
12. Upcoming requirements（SDKの最低要件、年齢区分、EUトレーダー情報）: https://developer.apple.com/news/upcoming-requirements/
13. Screenshot specifications: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
14. Overview of Accessibility Nutrition Labels: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels
