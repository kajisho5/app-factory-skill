# HIG 数値・仕様リファレンス

デザインを作るときに参照する数値です。出典は末尾。**2026年10月時点で一次情報を確認**しています（確認できなかったものは「近似値」と明記）。OSのメジャーアップデート時は再確認してください。

## 1. モックのキャンバス寸法

App Store Connect のスクリーンショット仕様（ピクセル）を、端末の倍率で割ってポイント（pt）にしています。モックはこのpt寸法で描き、書き出し時に倍率を掛けてPNGにします。そうすればそのままスクリーンショットに使えます [1]。

| 用途 | キャンバス（pt） | 書き出し倍率 | PNG（px） | 備考 |
|---|---|---|---|---|
| iPhone（標準・既定） | 402 × 874 | @3x | 1206 × 2622 | Dynamic Island 搭載の中サイズ。**スクリーンショット必須枠** |
| iPhone（標準・小） | 393 × 852 | @3x | 1179 × 2556 | 同じ必須枠の別サイズ |
| iPhone（大） | 440 × 956 | @3x | 1320 × 2868 | 大画面枠（任意） |
| iPad 13インチ 横 | 1376 × 1032 | @2x | 2752 × 2064 | **iPad対応アプリの必須枠** |
| iPad 13インチ 縦 | 1032 × 1376 | @2x | 2064 × 2752 | 同上 |
| Mac | 1440 × 900 | @2x | 2880 × 1800 | 16:10。この中にウィンドウを置く |
| Apple Watch Ultra 3 | 211 × 257 | @2x | 422 × 514 | Watchの枠は機種別 |
| Apple Watch Series 7〜9 | 198 × 242 | @2x | 396 × 484 | |

- スクリーンショットは1サイズにつき最大10枚、PNG / JPEG、**透過なし** [1]
- iPhone Duo（2台並び）は掲載用の提示画像なので、スクリーンショット枠ではなく、横長キャンバス（例： 1600 × 1000 pt、@2x）に iPhone（402 × 874 pt）を2台並べる

## 2. 文字（Text Styles）

### iOS / iPadOS（Dynamic Type の既定サイズ＝Large）[2]

| スタイル | ウェイト | サイズ | 行送り | 強調時 |
|---|---|---|---|---|
| Large Title | Regular | 34 | 41 | Bold |
| Title 1 | Regular | 28 | 34 | Bold |
| Title 2 | Regular | 22 | 28 | Bold |
| Title 3 | Regular | 20 | 25 | Semibold |
| Headline | Semibold | 17 | 22 | Semibold |
| Body | Regular | 17 | 22 | Semibold |
| Callout | Regular | 16 | 21 | Semibold |
| Subhead | Regular | 15 | 20 | Semibold |
| Footnote | Regular | 13 | 18 | Semibold |
| Caption 1 | Regular | 12 | 16 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

最大のアクセシビリティサイズ（AX5）では Body が53pt、Large Title が60pt になる。最大サイズのモックではこの値で組んで崩れないことを確認する [2]。

### macOS [2]

| スタイル | ウェイト | サイズ | 行の高さ |
|---|---|---|---|
| Large Title | Regular | 26 | 32 |
| Title 1 | Regular | 22 | 26 |
| Title 2 | Regular | 17 | 22 |
| Title 3 | Regular | 15 | 20 |
| Headline | Bold | 13 | 16 |
| Body | Regular | 13 | 16 |
| Callout | Regular | 12 | 15 |
| Subheadline | Regular | 11 | 14 |
| Footnote | Regular | 10 | 13 |
| Caption 1 / 2 | Regular / Medium | 10 | 13 |

### watchOS
- 文字の標準は16pt、最小は12pt [3]。text styleの表は機種ごとに異なるので、HIGの Typography > watchOS を参照する [2]

### 最小サイズ（カスタム書体でも下回らない）[3]
iOS / iPadOS 11pt、macOS 10pt、watchOS 12pt

### モックで使う書体
- 欧文・数字は SF Pro（Apple Design Resources から入手）、和文はヒラギノ角ゴシック。SVGでは `font-family="-apple-system, 'SF Pro Text', 'Hiragino Sans', 'Noto Sans JP', sans-serif"` と書く
- SF Pro が無い環境でPNGを書き出すと代替書体になり、文字幅が少し変わる。最終確認用のPNGは、可能ならMacで書き出す

## 3. コントロールと間隔 [3]

| プラットフォーム | 標準のコントロールサイズ | 最小 |
|---|---|---|
| iOS / iPadOS | 44 × 44 pt | 28 × 28 pt |
| macOS | 28 × 28 pt | 20 × 20 pt |
| watchOS | 44 × 44 pt | 28 × 28 pt |

- 間隔の目安： ベゼルのあるコントロールは周囲に約12pt、ベゼルのないものは見た目の端から約24pt [3]

## 4. コントラスト [3]

| 文字サイズ | ウェイト | 最小コントラスト比 |
|---|---|---|
| 17pt以下 | すべて | 4.5:1 |
| 18pt以上 | すべて | 3:1 |
| すべて | 太字 | 3:1 |

ライトとダークの両方で満たす。満たせない場合でも、「コントラストを上げる」がオンのときに高コントラスト配色を出す [3]。

## 5. 色

- **実装ではシステムカラー（label / secondaryLabel / systemBackground / systemBlue など）を使う**。モックのSVGに書くHEX値は**近似値**（HIGは色見本を画像で載せており、正確な値は Apple Design Resources の素材で確認する）[4][5]
- モック用の近似値（ライト / ダーク）：

| 名前 | ライト | ダーク |
|---|---|---|
| 背景 systemBackground | #FFFFFF | #000000 |
| 2次背景 secondarySystemBackground | #F2F2F7 | #1C1C1E |
| グループ背景 systemGroupedBackground | #F2F2F7 | #000000 |
| グループ内のセル secondarySystemGroupedBackground | #FFFFFF | #1C1C1E |
| 文字 label | #000000 | #FFFFFF |
| 2次文字 secondaryLabel | #3C3C43（不透明度60%） | #EBEBF5（不透明度60%） |
| 区切り線 separator | #3C3C43（不透明度29%） | #545458（不透明度60%） |
| アクセント systemBlue | #0088FF | #0091FF |
| 赤 systemRed | #FF383C | #FF4245 |
| 緑 systemGreen | #34C759 | #30D158 |

- **注意： システムの secondaryLabel（ライト、#3C3C43・不透明度60%）は白背景で約3.4:1** で、17pt以下の文字の基準（4.5:1）に届かない（計算値）。17pt以下で読ませる必要がある文字は、label を使うか、不透明度を約80%に上げた独自色（アセットカタログで定義）にする。ダーク（#EBEBF5・60%）は基準を満たす
- 同じ色に別の意味を持たせない。色だけで情報を区別しない [4]
- Liquid Glass のバー（タブバー・ツールバー）の上では、コンテンツと似た色をラベルに使わない [6][7]

## 6. ナビゲーションの型

| 状況 | iPhone | iPad | Mac | Watch |
|---|---|---|---|---|
| 主要な区分が少ない（目安5以下） | 画面下に浮くタブバー（Liquid Glass）[6] | 画面上部のタブバー。サイドバーへの切り替えも可 [6] | サイドバー、またはツールバー | 縦方向のページ移動（Digital Crown）[8] |
| 区分が多い・階層が深い | タブバー＋各タブ内の階層 | サイドバー（階層は2段まで。それより深ければ一覧列を足す）[9] | サイドバー＋一覧＋詳細 | 階層を浅くする |
| 一時的な作業 | シート（中間の高さ可、つまみを付け、スワイプで閉じる）[10] | ページ／フォームシート [10] | ウィンドウに付くシート [10] | 全画面のモーダル |

- タブバーは移動専用で、操作（追加など）を置かない。タブは無効化・非表示にしない。ラベルは1語で、SF Symbolsを使う [6]
- ツールバーのグループは最大3つ程度。確定操作（完了など）は1つだけ強調し、後端に置く [7]
- ウィンドウやバーのタイトルにアプリ名を使わない。15文字程度までの短い名前にする [7]
- Mac・iPadでは、ツールバーの操作をすべてメニューバーのコマンドにも出す [7][11]

## 出典

1. App Store Connect Help — Screenshot specifications: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
2. HIG — Typography（Specifications）: https://developer.apple.com/design/human-interface-guidelines/typography
3. HIG — Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility
4. HIG — Color: https://developer.apple.com/design/human-interface-guidelines/color
5. Apple Design Resources: https://developer.apple.com/design/resources/
6. HIG — Tab bars: https://developer.apple.com/design/human-interface-guidelines/tab-bars
7. HIG — Toolbars: https://developer.apple.com/design/human-interface-guidelines/toolbars
8. HIG — Designing for watchOS: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos
9. HIG — Sidebars: https://developer.apple.com/design/human-interface-guidelines/sidebars
10. HIG — Sheets: https://developer.apple.com/design/human-interface-guidelines/sheets
11. HIG — The menu bar: https://developer.apple.com/design/human-interface-guidelines/the-menu-bar
