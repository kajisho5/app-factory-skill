---
name: app-factory-skill
description: 'Design Apple-platform app interfaces that follow the Human Interface Guidelines: from an app idea or spec, produce a design spec (screens, navigation per platform, states, color and type tokens, SF Symbols, accessibility) and SVG mockups with PNG previews for iPhone, iPhone Duo (two-iPhone presentation), iPad, Mac and Apple Watch, in light and dark. Canvas sizes match App Store screenshot specs; includes scripts to frame devices, export opaque PNGs and check canvas size, minimum text size and contrast; then audits the result with design-check-skill until three consecutive passes find no new gaps. Uses only fictional sample data. Does not write app code or development prompts. Use when the user asks to design, mock up or lay out screens for an iPhone, iPad, Mac or Apple Watch app, or for HIG-compliant app mockups or App Store screenshot mocks.'
---

# app-factory-skill

Appleの Human Interface Guidelines（HIG）に沿って、iPhone / iPhone Duo / iPad / Mac / Apple Watch のアプリ画面を**デザインする**スキルです。成果物は「デザイン設計書」と「SVGモック＋PNGプレビュー」。アプリのコード実装や、開発用プロンプトの作成はしません。

## 成果物

作業フォルダに `design/` を作り、次を置く。

```
design/
  design-spec.md          設計書（templates/design-spec.md を埋めたもの）
  mocks/
    iphone-S-01-light.svg / .png
    iphone-S-01-dark.svg  / .png
    iphone-duo-S-01-S-02-light.svg / .png
    ipad-landscape-S-01-light.svg / .png
    mac-S-01-light.svg / .png
    watch-ultra-S-01.svg / .png
```

- ファイル名は `<端末>-<画面ID>-<light|dark>.svg`。端末名は `scripts/devices.py` の名前（`iphone`、`ipad-landscape`、`ipad-portrait`、`mac`、`watch-ultra` など）を使う。この名前でキャンバス寸法と書き出し倍率が決まる
- 完成例： `examples/hitokoto/`（架空のアプリ「ひとこと日記」）

## ワークフロー

1. **前提を固める** — ユーザーの説明から、アプリの目的、主な利用場面、対応プラットフォーム、画面の向き、iPhone Duo の要否を決める。対応プラットフォームが書かれていなければ、iPhone＋iPad を基本とし、Mac / Watch は利用場面に価値がある場合だけ提案する。機能の範囲やプラットフォームの追加など、ユーザーが決めるべきことは推測で埋めず、選択肢と推奨案を出す
2. **設計書を書く** — `templates/design-spec.md` を `design/design-spec.md` にコピーして埋める。数値は `references/hig-specs.md` から取る
   - 画面一覧とプラットフォーム別のナビゲーション（iPhoneはタブバー、iPadはタブバーかサイドバー、Macはサイドバー＋一覧＋詳細、Watchは浅い縦ページ）
   - 全画面の状態（空状態・読み込み中・エラー・権限拒否・無料版の上限）
   - 色はシステムカラーを基本とし、独自色はトークンとしてライト／ダークの値とコントラスト比を記録する
   - 文字は Text Styles で指定する（ポイント数を直接決めない）。アイコンは SF Symbols の名前で指定する
3. **主要画面からモックを描く** — まず iPhone の主要画面1つをライトで描いてユーザーに見せ、方向が合っているか確認してから全体に広げる（ユーザーが「おまかせ」と言っている場合は確認せず進め、最後にまとめて見せる）
   - キャンバスは `references/hig-specs.md` の表のpt寸法で、ルートの `<svg>` に `width`／`height`／`viewBox` と、背景色を `data-bg` 属性で書く
   - 文字は Text Styles のサイズで組み、`font-family="-apple-system, 'SF Pro Text', 'Hiragino Sans', 'Noto Sans JP', 'Noto Sans CJK JP', sans-serif"` を指定する
   - カードやボタンの上に載る文字には、その背景色を `data-bg` で書く（コントラストの機械チェックに使う）
   - Safe Area を守る： iPhoneは上端（ステータスバーとカメラ部分）と下端（ホームインジケータ）に操作要素を置かない
   - サンプルデータは**明らかに架空**の人名・住所・電話番号・会社名・日付の内容にする（実在の人物・住所・企業・作品を使わない）
   - アイコンは設計書に SF Symbols の名前を書く。モックには、Mac の SF Symbols アプリから書き出したSVGを使えるならそれを使い、使えない環境では単純な線画で代わりに描く（SF Symbols の利用条件は SF Symbols アプリと https://developer.apple.com/sf-symbols/ で確認する）
4. **全プラットフォーム・両モードに広げる** — 対応プラットフォームごとに主要画面をライトとダークで描く。ダークは色を反転するだけでなく、システムカラーのダーク値に置き換える
   - **iPad**： 横向き（`ipad-landscape`）を基本に、必要なら縦向きも描く。iPhone画面の引き伸ばしにしない
   - **Mac**： 1440 × 900 pt のデスクトップの中にウィンドウを置き、メニューバー（アプリ名・ファイル・編集・表示・ウインドウ・ヘルプ）も描く
   - **Apple Watch**： 一目で分かる1画面。背景は黒、文字は標準16pt以上
   - **端末フレーム**： 掲載用に枠付きの画像が欲しい場合は `scripts/frame.py iphone|ipad|mac|watch` で作り、出力名は `framed-<元の画面名>.svg` にする（スクリーンショット用の画面モックと区別するため）
   - **iPhone Duo**： 描いた iPhone 画面2枚から `scripts/frame.py duo` で作る。2枚は同じモード・同じ時刻・同じデータにし、一覧と詳細、操作前と操作後のように役割が分かる組み合わせにする
5. **書き出しと機械チェック** —
   ```bash
   python3 scripts/export_png.py design/mocks      # SVG → 透過なしPNG（スクリーンショット寸法）
   python3 scripts/check_mocks.py design/mocks     # 寸法・最小文字サイズ・コントラスト・ライト/ダークの対・PNG
   ```
   エラーが0になるまで直す。依存： `pip install cairosvg pillow`。和文の書体が入っていない環境では、PNGの日本語が表示されない（Noto Sans CJK JP かヒラギノを入れる）
6. **目で確認する** — 書き出したPNGを実際に開いて見る。機械チェックでは分からない、はみ出し・重なり・切れた文字・揃っていない余白・Safe Area への食い込みを直す
7. **design-check-skill で監査する** — 設計書とモックを design-check-skill（kajisho5/design-check-skill）で監査し、その終了条件（観点を変えたパスで「新規の抜けゼロ」が3回連続）まで回す。結果は設計書の「監査結果」に貼る。design-check-skill が使えない環境では、`references/hig-specs.md` と設計書を1項目ずつ突き合わせる簡易チェックを行い、「design-check-skill による監査は未実施」と書く
8. **渡す** — 設計書とPNGをユーザーに渡す（SVGは原版としてフォルダに残す）。スマートフォンで見る人がいるので、PNGを必ず添える。最後に、監査の結果（総パス数・保留）を1〜2行で伝える

## デザインの原則（全プラットフォーム共通）

- **HIGに従う**。HIGと見た目の好みがぶつかったらHIGを優先する。標準のコンポーネント（タブバー、サイドバー、ツールバー、シート、リスト）を基本とし、独自UIは必要最小限にする
- **レイアウトはサイズクラスで考える**。iPhoneは縦固定でも、ウィンドウが細く・広くなっても崩れない構成にする。iPadとMacは最小ウィンドウでも主要機能が使えるようにする
- **タップ対象**は iPhone / iPad / Watch で44×44pt以上、Macは28×28pt目安。隣のコントロールとの間隔を取る
- **文字**は Text Styles で指定し、最小サイズ（iPhone / iPad 11pt、Mac 10pt、Watch 12pt）を下回らない。Dynamic Type の最大サイズで、横並びを縦に積むなどの組み替えを設計書に書く
- **コントラスト**は17pt以下で4.5:1、18pt以上と太字で3:1をライト・ダークの両方で満たす。システムの secondaryLabel（ライト）は17pt以下の文字では基準に届かないので、読ませたい文字には使わない
- **色だけで情報を区別しない**。同じ色に別の意味を持たせない
- **タブバーは移動専用**。追加などの操作はツールバーやボタンに置く
- **無料版の制限**がある場合は、ぶつかる前に画面上で見える形にする（残り件数など）
- **起動画面**に広告・ロゴアニメ・待機演出を入れない
- **アイコン**を作る場合は、レイヤー（背景＋前景）をマスクなしの正方形SVGで描き、Icon Composer か fresnel（kajisho5/fresnel）で .icon にする前提で渡す。文字を入れない。外観はデフォルト／ダーク／クリア／ティントで確認する（仕様は design-check-skill の A-01〜A-08）

## やらないこと

- アプリのコード実装、開発プロンプトの作成
- 実在の人物・住所・企業・作品・他社アプリの画面をモックに使うこと
- Appleの実機の写真や、特定の製品を精密に描いたフレームを使うこと（`frame.py` の枠は汎用の角丸形状）
- HIGで確認できない数値を、確認したように書くこと（近似値は「近似値」と書く）

## ファイル

- `references/hig-specs.md` — キャンバス寸法、Text Styles、コントロール、コントラスト、モック用の色の近似値、ナビゲーションの型（出典つき）
- `templates/design-spec.md` — 設計書の雛形
- `scripts/devices.py` — 端末名とキャンバス寸法・倍率・最小文字サイズ
- `scripts/frame.py` — 画面SVGを汎用の端末フレームに入れる。iPhone Duo を作る
- `scripts/export_png.py` — SVG → 透過なしPNG（スクリーンショット寸法）
- `scripts/check_mocks.py` — 寸法・最小文字サイズ・コントラスト・ライト/ダークの対・PNGの有無と透過を確認
- `examples/hitokoto/` — 完成例（設計書・生成スクリプト・モック）
