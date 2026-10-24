# アプリ量産 共通プロンプトテンプレート

各アプリのプロンプトは、この区切り線より下を**構成ごと**コピーして作る。

- 「共通デフォルト」の文言はそのまま残す
- 【Mac対応時のみ】【Watch対応時のみ】のブロックは、候補の `platforms` 列に合わせて残す／見出しごと削る（【 】の注記自体は削る）
- `＜…＞` の差し替え枠はすべて埋める。埋められないものは「確認待ち」と書き、ユーザーに選択肢を出す
- アプリ固有部分の具体性は `examples/` の2本を基準にする

---

あなたはAppleプラットフォーム（iOS / iPadOS ＜/ macOS＞＜/ watchOS＞）のアプリ開発のエキスパートです。以下の仕様で、新規アプリ「＜アプリ名＞」をゼロから開発してください。

## 背景とコンセプト

＜対象競合の評価・評価数・低評価レビューの不満の内訳（言及数）と、差別化の切り口。このアプリの判断原則（「迷ったらこの原則に反しない方を選ぶ」）＞

## 技術条件

＜例： SwiftUI + Swift（最新の安定版）、iOS 26.0以上、対応プラットフォーム、サードパーティライブラリ禁止、データ保存（SwiftData 等）、使うApple純正フレームワーク、StoreKit 2。Xcodeでそのまま開いてビルドできる形で納品（XcodeGen の project.yml 方式でも可。その場合は生成手順をREADMEに明記）。UIは＜言語＞、コード内の識別子とコメントは英語＞

## 機能仕様

＜画面・振る舞いレベルで具体的に。数値（上限・回数・サイズ）、状態ごとの挙動、エラー時の挙動、工数が逼迫したときに後回しにしてよい順番と、削ってはいけないコア機能まで書く＞

## 課金設計

- 無料版でできること：＜具体的に＞
- 「Pro（買い切り）」＜価格＞ の非消耗型IAP 1点（StoreKit商品ID: `＜アプリのslug＞.pro`）で解放するもの：＜具体的に＞
- 無料版の制限は、ユーザーがぶつかる前に画面上で明示する（残り件数の表示、Pro限定項目を選ぶ前に分かる表示など）。上限到達時の挙動を明示し、データを無言で削除しない
- 課金画面に「これは買い切りです。毎月・毎週の支払いは発生しません」「広告は今後も入れません」と明記し、購入ボタンには価格をそのまま表示する
- 複数プラットフォームで配信する場合はユニバーサル購入とし、1回の購入で全プラットフォームで使えるようにする
- 購入の復元（リストア）ボタンを課金画面と設定画面の両方に置く
- 無料お試し・期間限定価格など誤認させる表現、隠れたサブスク、作業の佳境（保存・印刷・書き出しの直前など）で課金画面を挟む導線は使わない

## 権限とプライバシー

＜機能仕様で使う権限をすべて列挙し、それぞれの用途説明文（Info.plist の文言）を書く。例： カメラ、写真ライブラリ（追加のみ）、連絡先。トラッキングの有無（ATTダイアログを出すか）、解析SDKの有無、プライバシーラベルの想定（「データを収集しない」等）＞

- プライバシーラベル等の申告内容と実装を一致させる。申告と異なるデータ収集が必要になった場合は、勝手に実装せず報告する

## 共通デフォルト（全アプリ共通）

### デザイン原則
- **Appleの Human Interface Guidelines (HIG) に必ず沿うこと。** ナビゲーション構造、タップ領域（iPhone / iPad は44×44pt以上）、Safe Area、Dynamic Type、ダークモード、SF Symbolsの使い方など、HIGの規定から外れるUIを勝手に作らない。HIGと自分の判断が衝突したらHIGを優先し、その旨を報告する [1]
- iOS標準の見た目と操作感を基本とし、独自UIは必要最小限にする
- **レイアウト**: サイズクラス（実際に使える幅と高さ）でレイアウトを決め、端末の種類や向きで決め打ちしない [2]
- **画面の向き**: iPhoneは縦向き（ポートレート）固定を基本とする（例外は「機能仕様」で指定）。向きを固定していても、ウィンドウサイズの変化（Mac上のiPhoneミラーリング、iOS 27以降のシーンのリサイズ）でレイアウトが崩れないようにする。iPadは全方向に対応し、ウィンドウ表示で自由にリサイズされても崩れず、最小ウィンドウでも主要機能が使えるようにする。`UIRequiresFullScreen` は使わない [2][3]
- **iPhoneの操作性**: 片手操作を想定し、主要アクションは画面の下部〜中部に配置する。シート（ハーフモーダル）の開閉操作は全画面で一貫させる
- **iPadのレイアウト**: 画面幅を活かしたレイアウトにする（サイドバー＋詳細など。iPhone画面の引き伸ばしにしない）。ポインタのホバー効果と、ハードウェアキーボードの主要ショートカットに対応し、主要コマンドはiPadのメニューバーにも出す（メニューバーにしかない機能は作らない）
- **キーボード表示時**: ソフトウェアキーボードで入力中の項目や確定ボタンが隠れないよう、スクロールやレイアウト回避を行う
- **起動画面**: Launch ScreenをInfo.plistで構成する（iOS 27 SDK以降は提出の必須条件）。シンプルにし、広告・ロゴアニメ・待機演出を入れない。起動したらすぐ操作できる状態にする [4]

### 【Mac対応時のみ】Mac
- Macでの提供形態： ＜Macネイティブ（SwiftUIのマルチプラットフォーム） ／ Designed for iPad＞
- Macネイティブの場合： 標準のメニューバー項目（アプリメニューの情報・設定・終了、編集、表示、ウィンドウ、ヘルプ。書類を扱うならファイルも）、主要操作のキーボードショートカット（標準ショートカットと衝突させない）、ウィンドウのリサイズ追従を用意する。コントロールはMacの標準サイズ（28×28pt目安）にし、iPadの画面を拡大しただけにしない
- Designed for iPad の場合： Mac専用UIは作らない。iPad版のレイアウトがMacのウィンドウサイズで崩れないことを確認する

### 【Watch対応時のみ】Apple Watch
- 一目で分かる1画面完結の操作を中心にし、1回の操作が短時間で終わるようにする。画面階層は浅くし、縦方向の移動はDigital Crownで行えるようにする [5]
- コンプリケーション（ウォッチフェイス上の表示）と通知で何を見せるか：＜具体的に＞
- 常時表示（Always On）で手首を下げたとき： ＜表示内容。個人情報や細かい数値を出し続けない＞
- iPhoneが近くにないときの動作： ＜単独で動く範囲と、同期待ちの表示＞
- タップ対象は44×44pt（最小28×28pt）、文字は標準16pt・最小12ptを目安にする [6]

### アプリアイコン
- レイヤードアイコン（.icon）を **Icon Composer**（Xcode同梱のApple公式ツール）または **fresnel**（kajisho5/fresnel）で作成し、iOSの **Liquid Glass** スタイルにする [7][8][9]
- キャンバスは iOS / iPadOS / macOS が1024×1024px＜、watchOSは1088×1088px（円形にマスクされる。背景を黒にしない）＞。レイヤーは角丸・円形マスクを付けない正方形で渡し、前景はベクター（SVG / PDF）を優先する
- ハイライト・影・ぼかしなどの効果は描き込まず、システムの効果に任せる
- iOS / iPadOS / macOS はデフォルト／ダーク／クリア（ライト・ダーク）／ティント（ライト・ダーク）の外観をすべて用意し、それぞれで見え方を確認する
- アイコンに文字を入れない。小さいサイズでも判別できるシンプルなグリフにする [7]

### 品質・標準対応
- **ダークモード**: 色はアセットカタログまたはシステムカラーで定義し、ライト／ダーク両モードで表示を確認する
- **Dynamic Type**: システムの文字サイズ変更に対応し、最大サイズ（アクセシビリティサイズを含む）でもレイアウトが崩れない
- **アクセシビリティ**: 主要な操作要素にVoiceOverラベルを付け、読み上げ順序を画面の論理順に合わせる。テキストと背景のコントラスト比を両モードで確保する（17pt以下は4.5:1以上、18pt以上と太字は3:1以上）。隣接するコントロールの間に十分な余白をとる（目安： ベゼルありは周囲約12pt、ベゼルなしは約24pt）。カスタム書体でも最小サイズ（iPhone / iPad 11pt、Mac 10pt、Watch 12pt）を下回らない。色だけで情報を区別しない。「視差効果を減らす」がオンなら自動・反復アニメーションを抑え、「透明度を下げる」「コントラストを上げる」がオンでも文字が読めるようにする [6]
- **ローカライズ前提**: UI文字列はハードコードせず String Catalogs（.xcstrings）で管理する（初期言語は＜日本語＞）
- **権限拒否・空状態**: 権限が拒否された場合の代替導線（設定アプリへの誘導を含む）と、データが空の状態の画面を必ず用意する
- **プライバシーマニフェスト**: PrivacyInfo.xcprivacy を用意し、必須理由APIの申告を済ませる [10]
- **データ保持**: ユーザーデータはアプリのコンテナに保存してiCloudバックアップ対象とし、アップデートや機種変更でデータが消えない設計にする

### デモモックと成果物の形式
- 納品時、デモ用の画面モックを用意する: **iPhone / iPad ＜/ Mac＞＜/ Apple Watch＞ / iPhone Duo（iPhone 2台並び）**
- モックは主要画面を実機フレームで表示した、App Store掲載素材にも転用できる品質のものにする。スクリーンショットとして使う画像は App Store Connect の必須サイズで書き出す（透過なし。サイズは提出時に最新の仕様を確認）[11]
- **iPhone Duo（2台並び）モック**: 2画面の状態（時刻・データ内容・選択状態・ライト／ダーク）を一致させ、一覧と詳細、操作前と操作後のように役割分担が分かる並びにする。端末のサイズ・角度・余白を揃える。小さく表示しても文字が読めるようにする
- **モック・スクリーンショット・サンプルデータには、明らかに架空の人名・住所・電話番号・会社名を使う**（実在の人物・住所・企業を使わない）
- 確認する人はスマートフォン等で成果物を見ることが多い。**アイコンやモックなどの視覚成果物は、ベクター原版（SVG等）だけでなく、そのまま表示できるPNGのプレビューを必ず添えること**（表示環境によってはSVG単体を表示できないため）
- アイコンとモックの成果物はリポジトリ内の `deliverables/` フォルダにまとめ、READMEに一覧を載せる

### 作業環境・リポジトリ
- 成果物はGitHubの新規パブリックリポジトリ（名前: ＜リポジトリ名＞）で管理し、工程ごとにコミットしてプッシュする
- リポジトリは後日プライベートに変更する前提だが、公開期間があるため、APIキー・証明書・個人情報などの秘密情報は絶対にコミットしない（キーは .gitignore 済みのローカル設定や環境変数で扱い、手順をREADMEに書く）
- 提出用ビルドは、その時点で Apple が求める Xcode と SDK で作成する（提出要件は変わるため、提出前に最新の要件を確認する）[12]

### 審査・法務
- **ガイドライン4.3（スパム）対策**: テンプレートや部品を使い回しても、各アプリの機能・UI・訴求が実質的に異なるものにし、そのアプリ固有の価値を実装と掲載文の両方で明確にする。違いの分からない類似アプリを連続して提出しない [13]
- **商標と表現**: アプリ名・タイトル・サブタイトル・キーワード欄・説明文に、競合他社の名称・商標・製品名を使わない。根拠のない最上級表現や誇大表現（「No.1」「最速」「完全無料」など）を使わない

### 進め方
1. 最初に、プロジェクト構成と画面遷移の設計だけを提示し、私の確認を待つ。その際、バンドルIDとStoreKit商品IDの案も併せて提示する。推定開発日数に対して仕様が過大な場合は、設計を「コア機能／後回し可」に分けて提示する
2. 以後は機能ブロックごとに実装し、各ステップでビルドが通ることを確認してから次へ進む
3. 仕様に書いていない判断が必要になったら、勝手に範囲を広げず、選択肢と推奨案を提示して確認する

### 納品物
- ビルド可能なXcodeプロジェクト一式
- アプリアイコン一式（.icon と、各外観のPNGプレビュー）
- デモモック（対応プラットフォーム分、PNG添付）
- README.md（ビルド手順、差し替えが必要な定数の一覧、App Store Connect側で必要な作業のチェックリスト： IAP商品登録、プライバシーポリシーURLの用意、プライバシーラベルの入力、年齢区分の質問への回答、スクリーンショットの登録、アクセシビリティ・ニュートリションラベル（現時点は任意。対応した項目を申告）＜、EUで配信する場合はトレーダー情報の登録＞）[12][14]
- 動作確認レポート（主要フロー／権限拒否時／データ空時／ライト・ダーク／Dynamic Type最大サイズ／VoiceOver／視差効果を減らす・透明度を下げる／iPadの回転とウィンドウのリサイズ＜／Macのウィンドウのリサイズ＞＜／Watchの単独動作と常時表示＞を、実機またはシミュレータで確認した結果）
- App Store掲載文の下書き（タイトル30字以内、サブタイトル30字以内、説明文）

## 出典・参考

1. Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines
2. HIG — Layout: https://developer.apple.com/design/human-interface-guidelines/layout
3. TN3192: Migrating your app from the deprecated UIRequiresFullScreen key: https://developer.apple.com/documentation/technotes/tn3192-migrating-your-app-from-the-deprecated-uirequiresfullscreen-key
4. TN3208: Preparing your app’s launch screen to meet App Store requirements: https://developer.apple.com/documentation/technotes/tn3208-preparing-your-apps-launch-screen-to-meet-app-store-requirements
5. HIG — Designing for watchOS: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos
6. HIG — Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
7. HIG — App icons: https://developer.apple.com/design/human-interface-guidelines/app-icons
8. HIG — Materials（Liquid Glass）: https://developer.apple.com/design/human-interface-guidelines/materials
9. fresnel（アイコン作成ツール）: https://github.com/kajisho5/fresnel
10. Privacy manifest files: https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
11. Screenshot specifications: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
12. Upcoming requirements: https://developer.apple.com/news/upcoming-requirements/
13. App Store Review Guidelines（§4.3 Spam）: https://developer.apple.com/app-store/review/guidelines/
14. Overview of Accessibility Nutrition Labels: https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels
