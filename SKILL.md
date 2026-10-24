---
name: hig-design-skill
description: 'Design Apple-platform app interfaces that follow the Human Interface Guidelines: from an app idea or spec, produce a design spec (screens, navigation per platform, states, color and type tokens, SF Symbols, accessibility) and SVG mockups with PNG previews for iPhone, iPhone Duo (the foldable iPhone: outer and inner displays), iPad, Mac and Apple Watch, in light and dark. Canvas sizes match App Store screenshot specs; scripts frame devices, export opaque PNGs and check canvas size, minimum text size and contrast; the result is audited with design-check-skill until three consecutive passes find no new gaps. Uses only fictional sample data. Does not write app code. Use when the user asks to design, mock up or lay out screens for an iPhone, iPhone Duo, iPad, Mac or Apple Watch app, or for HIG-compliant app mockups or App Store screenshot mocks.'
---

# hig-design-skill

Appleの Human Interface Guidelines（HIG）に沿って、iPhone / iPhone Duo / iPad / Mac / Apple Watch のアプリ画面を**デザインする**スキルです。成果物は「デザイン設計書」と「SVGモック＋PNGプレビュー」。アプリのコード実装や、開発用プロンプトの作成はしません。

## 成果物

作業フォルダに `design/` を作り、次を置く。

```
design/
  design-spec.md          設計書（templates/design-spec.md を埋めたもの）
  mocks/
    iphone-S-01-light.svg / .png
    iphone-S-01-dark.svg  / .png
    iphone-duo-outer-S-01-light.svg / .png
    iphone-duo-inner-S-01-light.svg / .png
    ipad-landscape-S-01-light.svg / .png
    mac-S-01-light.svg / .png
    watch-ultra-S-01.svg / .png
```

- ファイル名は `<端末>-<画面ID>-<light|dark>.svg`。Apple Watch は黒背景のみなので `-light`／`-dark` を付けない（例： `watch-ultra-S-01.svg`）。端末名は `scripts/devices.py` の名前（`iphone`、`iphone-duo-outer`、`iphone-duo-inner`、`ipad-landscape`、`ipad-portrait`、`mac`、`watch-ultra` など）を使う。この名前でキャンバス寸法と書き出し倍率が決まる
- 完成例： `examples/hitokoto/`（架空のアプリ「ひとこと日記」）
- 以下の `<SKILL>` は、このスキルのフォルダ（例： `~/.claude/skills/hig-design-skill`）。スクリプトは作業フォルダから `python3 <SKILL>/scripts/...` で呼ぶ

## ワークフロー

1. **前提を固める** — ユーザーの説明から、アプリの目的、主な利用場面、対応プラットフォーム、画面の向きを決める。対応プラットフォームが書かれていなければ、iPhone＋iPhone Duo＋iPad を基本とし（iPhone アプリは iPhone Duo でも動くため）、Mac / Watch は利用場面に価値がある場合だけ提案する。機能の範囲やプラットフォームの追加など、ユーザーが決めるべきことは推測で埋めず、選択肢と推奨案を出す
2. **設計書を書く** — `templates/design-spec.md` を `design/design-spec.md` にコピーして埋める。数値は `references/hig-specs.md` から取る。部品（シート、アラート、メニュー、入力欄など）の決まりは同じファイルの §7、起動・読み込み・権限・課金・通知などの状態と文言は §8、Mac は §9、Watch は §10、標準アイコンは §11、特定の機能（ウィジェット、Apple Pay、ゲーム、CarPlay、タッチ決済、ヘルスケアなど）は §12 を見る
   - 画面一覧とプラットフォーム別のナビゲーション（iPhoneはタブバー、iPhone Duo は外側がタブバー・内側がサイドバー、iPadはタブバーかサイドバー、Macはサイドバー＋一覧＋詳細、Watchは浅い縦ページ）
   - 全画面の状態（空状態・読み込み中・エラー・権限拒否・無料版の上限）
   - 色はシステムカラーを基本とし、独自色はトークンとしてライト／ダークの値とコントラスト比を記録する
   - 文字は Text Styles で指定する（ポイント数を直接決めない）。アイコンは SF Symbols の名前で指定する
3. **主要画面からモックを描く** — まず iPhone の主要画面1つをライトで描いてユーザーに見せ、方向が合っているか確認してから全体に広げる（ユーザーが「おまかせ」と言っている場合は確認せず進め、最後にまとめて見せる）
   - **SVGは生成スクリプトで作るのを基本にする**。`<SKILL>/examples/hitokoto/build.py` を `design/build.py` にコピーし、色のトークン（ライト／ダーク）と部品（ステータスバー、タブバー、セル、ボタン）を書き換えて使う。ライトとダークを同じ部品から作るので、両モードの食い違いが起きない。画面が少なければ手書きのSVGでもよい
   - キャンバスは `references/hig-specs.md` の表のpt寸法で、ルートの `<svg>` に `width`／`height`／`viewBox` と、背景色を `data-bg` 属性で書く
   - 文字は Text Styles のサイズで組み、`font-family="-apple-system, 'SF Pro Text', 'Hiragino Sans', 'Noto Sans JP', 'Noto Sans CJK JP', sans-serif"` を指定する
   - カードやボタンの上に載る文字には、その背景色を `data-bg` で書く（コントラストの機械チェックに使う）
   - 文字サイズと色は**属性**（`font-size="17"`、`fill="#000000"`）で書く。`<style>` のクラスで書くと機械チェックで見られない
   - Liquid Glass はバーとコントロール（ボタンの形）にだけ使い、半透明の塗りで近似する。**バーの後ろに幅いっぱいの帯を描かず、コンテンツをバーの下まで描く**（上端・下端は薄いぼかしで近似）。コンテンツの層（カードなど）には Glass を使わない
   - ダークのシートやポップオーバーは、手前の面の色（高階調。`references/hig-specs.md` §5）で描く
   - Safe Area を守る： iPhoneは上端（ステータスバーとカメラ部分）と下端（ホームインジケータ）に操作要素を置かない
   - サンプルデータは**明らかに架空**の人名・住所・電話番号・会社名・日付の内容にする（実在の人物・住所・企業・作品を使わない）
   - アイコンは設計書に SF Symbols の名前を書く。モックには、Mac の SF Symbols アプリから書き出したSVGを使えるならそれを使い、使えない環境では単純な線画で代わりに描く（SF Symbols の利用条件は SF Symbols アプリと https://developer.apple.com/sf-symbols/ で確認する）
4. **全プラットフォーム・両モードに広げる** — 対応プラットフォームごとに主要画面をライトとダークで描く。ダークは色を反転するだけでなく、システムカラーのダーク値に置き換える
   - **iPhone Duo**（折りたたみ iPhone）： 外側（`iphone-duo-outer`、通常の iPhone と同じサイズクラス）と内側（`iphone-duo-inner`、横・縦とも regular）の両方を描く。詳細は `references/hig-specs.md` の「iPhone Duo」
     - **中央の折り目**： 折り目の予約領域は半分折ったときだけ現れる（完全に開いているときは幅0）。内側は Apple の図と同じ**横向きを主に描き**（`iphone-duo-inner-landscape`）、完全に開いた状態と、**半分折った状態**（`iphone-duo-inner-landscape-S-01-folded-light.svg` / `-dark.svg`）の両方を作る。半分折った状態では、中央（横向きでは縦一文字、縦向きでは横一文字。モックでは中央 ±13pt を目安）に見出し・ボタン・画像・顔・数値など重要な要素をかけず、左右に分ける配置は中央で均等にする。連続してスクロールする本文やリストはかかってもよい（Appleの指針）。グリッドは偶数列。縦向きで机に立てて置かれる使い方では、上半分に見る内容、下半分に操作を置く
     - **バーの位置**： 外側と内側の横向きでは、ふつう上下にあるものが後端（右端）に縦に並ぶ。外側は右上の角の丸いカメラ（Dynamic Island）から下へ ステータスバー → ツールバー → タブバー（**タブバーも下ではなく右端**）。内側の横向きは、一覧ペインの操作を一覧ペインの上に、詳細ペインの操作とステータスバーを右端に縦に置く（メールの例）。ツールバーの中は 戻る／閉じる → 強調操作 → 残り の順で、文字ではなく記号のボタンにする（文字のボタンは横向きのバーに残る）。内側の縦向きは通常の横向きのバーのまま。位置は近似で描き、設計書に「近似」と書く
     - **構成**： 外側は1段（一覧か詳細）、内側は一覧と詳細を並べる。向きではなくサイズクラスで組み替え、開閉・半分折ったときの組み替えは最小限にする
     - 内側の Split View（画面の左右どちらか半分）でも崩れないことを設計書に書く
   - **iPhone Duo の横向き**： アプリが横向きに対応する場合は外側の横向き（`iphone-duo-outer-landscape`）を描く。内側の横向き（`iphone-duo-inner-landscape`）は、内側の縦向きと構成が変わる場合だけ描く（テントのように立てて置かれるため、横向きの対応は推奨されている）
   - **iPad**： 横向き（`ipad-landscape`）を基本に、必要なら縦向きも描く。iPhone画面の引き伸ばしにしない。ウィンドウ表示（`ipad-narrow` など）ではツールバーの先頭にウィンドウコントロール（3つの丸、近似）が出るので、先頭にボタンを置かない
   - **Mac**： 1440 × 900 pt のデスクトップの中にウィンドウを置き、メニューバー（アプリ名・ファイル・編集・表示・ウインドウ・ヘルプ）も描く。「Designed for iPad」で動かす場合は、Mac専用のUIは描かず、iPad の画面をウィンドウに入れた形で描く。Mac Catalyst で iPad の見た目のまま動かす場合は 77% に縮小される（17pt が 13pt）ことを前提にする。主要な操作と情報はウインドウの上部とツールバーに置き、下部に置かない。メニューバーの並びは `references/hig-specs.md` §9
   - **CarPlay**（対応する場合）： 画面はシステムのテンプレートで iOS が描くので、モックは描かない。設計書の「該当する機能」に、使うテンプレートと載せる内容、エラーの出し方（CarPlay の画面に出す）を書く
   - **Apple Watch**： 一目で分かる1画面。標準の背景は黒（色の背景は情報を伝えるときだけ）。書体は SF Compact。本文は 40〜42mm で16pt、44〜49mm（Ultra を含む）で17pt、補足の文字は Caption / Footnote で12pt以上（表は `references/hig-specs.md` §2）。記号のボタンは横に3つまで、文字のボタンは横に2つまで。常時表示（手首を下げたとき）の画面も `watch-ultra-S-01-aod.svg` として描く（レイアウトは変えずに補足部分を暗くし、機密情報を隠し、操作できる部品は操作できない見た目にする）
   - **状態と条件のモック**（design-check-skill の C-03・C-13・C-14・C-16・I-02 に対応）： 主要画面について、少なくとも次も描く
     - 空状態： `iphone-S-01-empty-light.svg` / `-dark.svg`
     - 入力がある画面はキーボード表示時（入力欄と確定ボタンが隠れないこと）
     - 最大文字サイズ（AX5）： `iphone-S-01-light-ax5.svg`（行を省略せず縦に積む組み替えを見せる）。Watch は最大が AX3（Body 23pt）
     - iPad の細いウィンドウ： `ipad-narrow-S-01-light.svg` / `-dark.svg`（サイドバーを畳んだ状態など）
     - 権限を使うアプリは、システムのダイアログの前に出す説明画面（ボタン1つ、「続ける」）
   - **端末フレーム**： 掲載用に枠付きの画像が欲しい場合は `<SKILL>/scripts/frame.py iphone|duo-outer|duo-inner|ipad|mac|watch` で作り、出力名は `framed-<元の画面名>.svg` にする（スクリーンショット用の画面モックと区別するため）
   - **2台並びの掲載用画像（pair）**： 必要なら、描いた iPhone 画面2枚から `<SKILL>/scripts/frame.py pair` で作る（出力名は `pair-...`）。2枚は同じモード・同じ時刻・同じデータにし、一覧と詳細のように役割が分かる組み合わせにする
5. **書き出しと機械チェック** —
   ```bash
   python3 <SKILL>/scripts/export_png.py design/mocks      # SVG → 透過なしPNG（スクリーンショット寸法）
   python3 <SKILL>/scripts/check_mocks.py design/mocks     # 寸法・最小文字サイズ・コントラスト・はみ出し・ライト/ダークの対・PNG
   ```
   エラーが0になるまで直し、警告も確認する。依存： `pip install -r <SKILL>/requirements.txt`（Cairo 本体が必要： Mac は `brew install cairo`、Debian/Ubuntu は `sudo apt-get install libcairo2`）。和文の書体が入っていない環境では、PNGの日本語が表示されない（Noto Sans CJK JP かヒラギノを入れる）
6. **目で確認する** — 書き出したPNGを実際に開いて見る。機械チェックでは分からない、はみ出し・重なり・切れた文字・揃っていない余白・Safe Area への食い込みを直す
7. **design-check-skill で監査する** — 設計書とモックを design-check-skill（kajisho5/design-check-skill）で監査し、その終了条件（パスごとに毎回新しい観点で見直し、「新規の抜けゼロ」が3回連続）まで回す。結果は設計書の「監査結果」に貼る。design-check-skill が使えない環境では、`references/hig-specs.md` と設計書を1項目ずつ突き合わせる簡易チェックを行い、「design-check-skill による監査は未実施」と書く
8. **渡す** — 設計書とPNGをユーザーに渡す（SVGは原版としてフォルダに残す）。スマートフォンで見る人がいるので、PNGを必ず添える。最後に、監査の結果（総パス数・保留）を1〜2行で伝える

## デザインの原則（全プラットフォーム共通）

- **HIGに従う**。HIGと見た目の好みがぶつかったらHIGを優先する。標準のコンポーネント（タブバー、サイドバー、ツールバー、シート、リスト）を基本とし、独自UIは必要最小限にする
- **レイアウトはサイズクラスで考える**。iPhoneは縦固定でも、ウィンドウが細く・広くなっても崩れない構成にする。iPadとMacは最小ウィンドウでも主要機能が使えるようにする
- **ボタンの当たり判定は入力方法にかかわらず44×44pt以上**（見た目は Mac で28×28pt目安、最小の見た目は iPhone / iPad / Watch で28pt、Mac で20pt）。隣のコントロールとの間隔を取る
- **目立つ（塗りの）ボタンは1画面に2つまで**。破壊的な操作は赤で、プライマリにしない。確認のボタンは「OK」ではなく「削除」などの動詞
- **文字**は Text Styles で指定し、最小サイズ（iPhone / iPad 11pt、Mac 10pt、Watch 12pt）を下回らない。Dynamic Type の最大サイズで、横並びを縦に積むなどの組み替えを設計書に書く
- **コントラスト**は17pt以下で4.5:1、18pt以上と太字で3:1をライト・ダークの両方で満たす。システムの secondaryLabel（ライト）は17pt以下の文字では基準に届かないので、読ませたい文字には使わない
- **色だけで情報を区別しない**。同じ色に別の意味を持たせない
- **タブバーは移動専用**（検索タブは例外として可）。追加などの操作はツールバーやボタンに置く。別のセクションに移ってもタブバーは表示したまま（例外はタブバーを覆うモーダル）。タブのアイコンは塗り（fill）の記号
- **アプリ内にライト／ダークの切り替えを作らない**（システムの設定に従う）
- **シートとモーダル**： 1画面のシートは「キャンセル」を先頭、「完了」などを末尾。複数ステップのシートは2ステップ目以降の先頭が「戻る」で、「完了」は最後のステップで有効にする。編集中に閉じようとしたら確認する。モーダルを重ねない。つまみはサイズを変えられるシートだけ
- **ジェスチャだけの操作を作らない**（同じことができるボタンも置く）
- **無料版の制限**がある場合は、ぶつかる前に画面上で見える形にする（残り件数など）
- **起動画面（Launch Screen）**は最初の画面とほぼ同じ骨格にし、文字・広告・ロゴアニメ・待機演出を入れない（ライト／ダーク別）。Mac と Watch には起動画面がない
- **アイコン**を作る場合は、レイヤー（背景＋前景）をマスクなしの正方形SVGで描き、Icon Composer か fresnel（kajisho5/fresnel）で .icon にする前提で渡す。文字を入れない。外観は iOS / iPadOS / macOS でデフォルト／ダーク／クリア／ティントを確認する（watchOS は外観の種類がなく、円形にマスクされるので主要な形を中央に寄せる）。SF Symbols やそれに似せた形をアイコンに使わない（仕様は design-check-skill の A-01〜A-08・A-10）

## やらないこと

- アプリのコード実装、開発プロンプトの作成
- 実在の人物・住所・企業・作品・他社アプリの画面をモックに使うこと
- Appleの実機の写真や、特定の製品を精密に描いたフレームを使うこと（`frame.py` の枠は汎用の角丸形状）
- HIGで確認できない数値を、確認したように書くこと（近似値は「近似値」と書く）

## ファイル

- `references/hig-specs.md` — キャンバス寸法、Text Styles、コントロール、コントラスト、モック用の色の近似値、ナビゲーションの型（出典つき）
- `templates/design-spec.md` — 設計書の雛形
- `scripts/devices.py` — 端末名とキャンバス寸法・倍率・最小文字サイズ
- `scripts/frame.py` — 画面SVGを汎用の端末フレームに入れる（iPhone Duo の外側・内側を含む）。2台並びの掲載用画像（pair）を作る
- `scripts/export_png.py` — SVG → 透過なしPNG（スクリーンショット寸法）
- `scripts/check_mocks.py` — 寸法・最小文字サイズ・コントラスト・はみ出し（警告）・`<style>` の使用（警告）・ライト/ダークの対・PNGの有無と透過を確認
- `examples/hitokoto/` — 完成例（設計書・生成スクリプト・モック）。`bash examples/hitokoto/make.sh` で再生成と検査
