# HIG 数値・仕様リファレンス

デザインを作るときに参照する数値です。出典は末尾。**2026年10月時点で一次情報を確認**しています（確認できなかったものは「近似値」と明記）。OSのメジャーアップデート時は再確認してください。

## 1. モックのキャンバス寸法

App Store Connect のスクリーンショット仕様（ピクセル）を、端末の倍率で割ってポイント（pt）にしています。モックはこのpt寸法で描き、書き出し時に倍率を掛けてPNGにします。そうすればそのままスクリーンショットに使えます [1]。

| 用途 | キャンバス（pt） | 書き出し倍率 | PNG（px） | 備考 |
|---|---|---|---|---|
| iPhone（標準・既定） | 402 × 874 | @3x | 1206 × 2622 | Dynamic Island 搭載の中サイズ。**スクリーンショット必須枠** |
| iPhone（標準・小） | 393 × 852 | @3x | 1179 × 2556 | 同じ必須枠の別サイズ |
| iPhone（大） | 440 × 956 | @3x | 1320 × 2868 | 大画面枠（任意） |
| iPhone Duo 外側（閉じた状態）縦 | 466 × 678 | @3x（推定） | 1398 × 2034 | 5.4インチ。iPhone Duo のスクリーンショット枠（現時点は任意）|
| iPhone Duo 内側（開いた状態）縦 | 669 × 951 | @3x（推定） | 2007 × 2853 | 7.6インチ。横向き（951 × 669 / 2853 × 2007 px）もある |
| iPad 13インチ 横 | 1376 × 1032 | @2x | 2752 × 2064 | **iPad対応アプリの必須枠** |
| iPad 13インチ 縦 | 1032 × 1376 | @2x | 2064 × 2752 | 同上 |
| Mac | 1440 × 900 | @2x | 2880 × 1800 | 16:10。この中にウィンドウを置く |
| iPad 細いウィンドウ（例） | 600 × 1032 | @2x | 1200 × 2064 | スクリーンショット枠ではない。ウィンドウは自由にリサイズされるので、細い幅での崩れを確認する見本 |
| Apple Watch Ultra 3 | 211 × 257 | @2x | 422 × 514 | Watchの枠は機種別 |
| Apple Watch Series 7〜9 | 198 × 242 | @2x | 396 × 484 | |

- スクリーンショットは1サイズにつき最大10枚、PNG / JPEG、**透過なし** [1]
- iPhone Duo のpt寸法はAppleが公開していないため、スクリーンショットのピクセル値を@3xと仮定して割った推定値。比率（約0.69〜0.70）はスクリーンショット仕様どおり [1]
- iPhone Duo のスクリーンショットは現時点では任意。ただし **2027年4月以降、iOS 27.1 SDK以降でビルドしたアプリは必須** になる。提出すると製品ページに「iPhone Duo 向けに最適化」のバッジが付く [1]
- 2台の iPhone を並べた掲載用画像（pair）は、スクリーンショット枠ではない横長キャンバス（1600 × 1000 pt、@2x）に iPhone（402 × 874 pt）を2台並べて作る

## 1-2. iPhone Duo（折りたたみ iPhone、2026年9月発表）

| 項目 | 内容 | 出典 |
|---|---|---|
| 画面 | 外側 5.4インチ、内側 7.6インチ。2画面は同じ縦横比で、開閉すると内容が比例して拡大・縮小する | [12] |
| サイズクラス | 外側の縦向き＝横 compact・縦 regular（通常の iPhone と同じ）。外側の横向き＝横 compact・縦 compact。**内側＝横 regular・縦 regular**（サイドバーを置ける） | [13] |
| 向き | 外側はアプリが対応する向きに従う。**内側は対応する向きの指定に従わず**、アプリを拡大して表示する。向きでレイアウトを決めない。テントのように置かれるので横向きの対応を推奨 | [13] |
| Split View | 内側で2つのアプリを左右に並べられる（iPhoneで初）。アプリは画面の左右どちら側にも置かれる | [12][13] |
| バーとボタン | **外側と、内側の横向き**では、ふつう上下にあるものが画面の後端（右側）に**縦に並ぶ**。外側の並びは上から **Dynamic Island → ステータスバー → ツールバー → タブバー**（タブバーも横側に来る）。ツールバーの中は上から 戻る／閉じる → 完了などの強調操作 → 残りのグループ。**内側の縦向きは例外で、通常の横向きのバーのまま**。Split View では各アプリが自分の外側の端に操作を置く。記号だけのボタンにも題名を付ける（あふれたときのメニューで使われる）。**文字のボタンは横向きのバーに残るので、なるべく記号にする**。あふれる項目は下から上へシステムのあふれメニュー（…）に入る。独自のあふれメニューは作らず、… は あふれメニュー専用にする。場所が足りないとき、移動が中心の画面はタブバーを残してツールバーを畳み、作業が中心の画面はタブバーを畳んでツールバーを残す。ペインに属する操作はそのペインの上に置く（例： メールの一覧の操作は左ペインの上） | [15] |
| システムUI | 外側の前面カメラは角にあり、常に見えていて、横側の操作と縦に揃う。内側の前面カメラは画面の下にあり、カメラを使うときだけ現れて、UIがよける。Dynamic Island・ステータスバーは操作と同じく横側に来る | [15] |
| **折り目（中央）** | 半分折った状態では、内側の画面の中央が「折り目の予約領域」になり、画面が2つの領域に分かれる。**折り目の向きは、内側の横向きでは縦（左右に分かれる。本のように持つ）、内側の縦向きでは横（上下に分かれる。小さなノートPCのように置ける）**（※向きは、2画面が同じ縦横比で、内側を上下に分けた半分が外側を横にした大きさに相当することからの推定）。**重要な文字・操作・画像は中央にまたがせない**。システムの部品（アラート、メニュー、シート、Split View）は自動でよける。独自の部品は `ReservedRegion` で中央を避ける。グリッドは偶数列にして中央で分かれるようにする。**連続してスクロールする内容（記事・リスト・文書）はずらさなくてよい**。折ったときの組み替えは最小限にする（操作が大きく動くと見失う） | [15][16] |
| 全幅のレイアウト | バーが要らない、スクロールしない没入型の画面（例： 計算機）は画面の全幅を使ってよい。Dynamic Island とステータスバーにだけはぶつけない。外側は他の iPhone より横に広く縦に短い（計算機は外側で5列×4行） | [15] |
| 2画面の構成 | 外側は1段（一覧か詳細）、内側は一覧と詳細を並べる（例： メール）。内側の横向きで左右に分ける配置は、中央の折り目で分かれる左右均等にする。内側の縦向きで机に立てて置かれたときは、上の領域を見る内容、下の領域を操作に使う | [15][16] |
| タブ | タブは両方の画面に出て、必要に応じて縦に並ぶ。内側ではサイドバーにすることを推奨 | [13] |
| シート | 外側ではボタンが縦に並び、内側では画面の中央に表示される | [13] |
| Safe Area | 左右・上下で非対称なことが多い。操作できる要素は Safe Area の内側、背景は外まで伸ばす | [13] |
| 確認方法 | Xcode 27.1 の iPhone Duo シミュレータと Device Hub で、開閉・回転・折り曲げと、Split View の左右を確認する | [13] |

- **pt寸法、Split View の幅、折り目の領域の幅、Dynamic Island の正確な位置はAppleが公開していない**（2026年10月時点）。モックではシステムUIの位置を近似で描き、「近似」と明記する。折り目の幅は、モックでは中央 ±12pt を避ける目安にする（Appleの数値ではない。内側の縦向きは y = 475.5 付近、横向きは x = 475.5 付近）
- モックは最低限、外側の主要画面と、内側の主要画面を描く。内側の Split View（画面の半分）と、半分折った状態でも崩れないことを設計書に書く

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

| 状況 | iPhone | iPhone Duo | iPad | Mac | Watch |
|---|---|---|---|---|---|
| 主要な区分が少ない（目安5以下） | 画面下に浮くタブバー（Liquid Glass）[6] | 外側はタブバーが横側に縦に並ぶ。内側の縦向きは通常の横向きのバー [15] | 画面上部のタブバー。サイドバーへの切り替えも可 [6] | サイドバー、またはツールバー | 縦方向のページ移動（Digital Crown）[8] |
| 区分が多い・階層が深い | タブバー＋各タブ内の階層 | 外側は1段（一覧か詳細）。内側は一覧と詳細を並べる。横向きでは中央の折り目で分かれる左右均等の配置にする [15] | サイドバー（階層は2段まで。それより深ければ一覧列を足す）[9] | サイドバー＋一覧＋詳細 | 階層を浅くする |
| 一時的な作業 | シート（中間の高さ可、つまみを付け、スワイプで閉じる）[10] | 外側はシート（ボタンは縦並び）。内側は中央のシート [13] | ページ／フォームシート [10] | ウィンドウに付くシート [10] | 全画面のモーダル |

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
12. Apple Newsroom — Apple unveils iPhone Duo（2026-09-10）: https://www.apple.com/my/newsroom/2026/09/apple-unveils-iphone-duo/
13. Apple Developer Tech Talk — Prepare your app for iPhone Duo: https://developer.apple.com/videos/play/tech-talks/111461/
14. TidBITS — Apple Unfolds the iPhone Duo（2026-09-11、表示の挙動の補足）: https://tidbits.com/2026/09/11/apple-unfolds-the-iphone-duo/
15. HIG — Designing for iPhone Duo: https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo
16. Apple Developer Tech Talk — Strike a Pose with Adaptive Layouts on iPhone Duo: https://developer.apple.com/videos/play/tech-talks/111463/
