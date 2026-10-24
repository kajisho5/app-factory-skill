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
| システムUI | 外側： ヒンジは左端、前面カメラは右上の角の丸い予約領域で常に見えている（ライブアクティビティのときは Dynamic Island に広がる）。その下に後端に沿って ステータスバー → ツールバー → タブバー。内側（横向き）： 前面カメラは右半分の上にあり、カメラを使うときだけ現れて、UIがよける。ステータスバーと詳細ペインの操作は右端に縦に並び、一覧ペインの操作は一覧ペインの上に置く（メールの例） | [15] |
| **折り目（中央）** | 折り目の予約領域は**半分折ったときだけ**現れ、完全に開いているときは幅0（無効）。半分折ると内側の画面の中央が除外され、2つの領域に分かれる。Apple の図では内側は**横向きで描かれ、ヒンジは中央の縦一文字**（縦向きに持てば横一文字になる）。**半分折った状態では重要な文字・操作・画像を中央にかけない**。システムの部品（アラート、メニュー、シート、Split View）は自動でよけ、分割ビューは左右均等になる（メモの例： 開いているときは一覧が狭く、半分折ると一覧と本文が同じ幅）。独自の部品は `ReservedRegion` で中央を避ける。グリッドは偶数列。連続してスクロールする内容（記事・リスト・文書）はずらさなくてよい（この点は Tech Talk [16]）。折ったときの組み替えは最小限にする | [15][16] |
| 全幅のレイアウト | バーが要らない、スクロールしない没入型の画面（例： 計算機）は画面の全幅を使ってよい。Dynamic Island とステータスバーにだけはぶつけない。外側は他の iPhone より横に広く縦に短い（計算機は外側で5列×4行） | [15] |
| 2画面の構成 | 外側は1段（一覧か詳細）、内側は一覧と詳細を並べる（例： メール）。内側の横向きで左右に分ける配置は、中央の折り目で分かれる左右均等にする。内側の縦向きで机に立てて置かれたときは、上の領域を見る内容、下の領域を操作に使う（この点は Tech Talk [16]） | [15][16] |
| タブ | タブは両方の画面に出て、必要に応じて縦に並ぶ。内側ではサイドバーにすることを推奨 | [13] |
| シート | 外側ではボタンが縦に並び、内側では画面の中央に表示される | [13] |
| Safe Area | 左右・上下で非対称なことが多い。操作できる要素は Safe Area の内側、背景は外まで伸ばす | [13] |
| 確認方法 | Xcode 27.1 の iPhone Duo シミュレータと Device Hub で、開閉・回転・折り曲げと、Split View の左右を確認する | [13] |

- **pt寸法、Split View の幅、折り目の領域の幅、Dynamic Island の正確な位置はAppleが公開していない**（2026年10月時点）。モックではシステムUIの位置を近似で描き、「近似」と明記する。折り目の幅は、モックでは中央 ±13pt を避ける目安にする（Appleの数値ではない。Apple の図では帯の幅が画面幅の約3%で、内側の横向きなら約27pt に相当。横向きは x = 475.5 付近、縦向きは y = 475.5 付近）
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

### watchOS [2]
- システムフォントは **SF Compact**（コンプリケーションは SF Compact Rounded）。Watch のモックは `font-family="'SF Compact Text', 'SF Compact Rounded', 'Hiragino Sans', 'Noto Sans JP', 'Noto Sans CJK JP', sans-serif"` にする
- 既定の文字サイズは機種で違う。40/41/42mm は「Large」、44/45/49mm（Ultra を含む）は「xLarge」が既定

| スタイル | Large（40〜42mm） | xLarge（44〜49mm） |
|---|---|---|
| Body / Headline | 16 | 17 |
| Title 3 | 19 | 20 |
| Caption 1 | 15 | 16 |
| Caption 2 | 14 | 15 |
| Footnote 1 | 13 | 14 |
| Footnote 2 | 12 | 13 |

- 「本文16pt」は本文の標準値で、すべての文字の下限ではない。補足の文字は Caption / Footnote を使い、最小12ptを下回らない [3]

### 最小サイズ（カスタム書体でも下回らない）[3]
iOS / iPadOS 11pt、macOS 10pt、watchOS 12pt

### 文字の扱い [2][3]
- **macOS は Dynamic Type に対応していない**（最大文字サイズのモックは iPhone / iPad / Watch で作る）。文字は 200% 以上（watchOS は 140% 以上）に拡大できるのが理想
- 細いウェイト（Ultralight / Thin / Light）は避ける。使うなら推奨より大きくする
- 3行以上の文は行送りを詰めない。文字が大きくなったら列数を減らし、重要な内容を上に置く

### モックで使う書体
- 欧文・数字は SF Pro（Apple Design Resources から入手）、和文はヒラギノ角ゴシック。SVGでは `font-family="-apple-system, 'SF Pro Text', 'Hiragino Sans', 'Noto Sans JP', sans-serif"` と書く
- SF Pro が無い環境でPNGを書き出すと代替書体になり、文字幅が少し変わる。最終確認用のPNGは、可能ならMacで書き出す

## 3. コントロールと間隔 [3]

| プラットフォーム | 標準のコントロールサイズ | 最小 |
|---|---|---|
| iOS / iPadOS | 44 × 44 pt | 28 × 28 pt |
| macOS | 28 × 28 pt | 20 × 20 pt |
| watchOS | 44 × 44 pt | 28 × 28 pt |

- **ボタンの当たり判定（ヒット領域）は、入力方法にかかわらず 44 × 44 pt 以上**（Buttons [17]）。上の「最小」は見た目の大きさの下限で、小さく描くときも当たり判定は 44pt まで広げる
- 目立つスタイル（塗りの強調）のボタンは1画面に2つまで。推奨の選択肢は大きさではなくスタイルで区別する [17]
- ボタンの役割（通常／プライマリ／キャンセル／破壊的）を決める。破壊的な操作をプライマリにしない（システムの赤を使う）。カスタムボタンには押された状態を描く [17]

- 間隔の目安： ベゼルのあるコントロールは周囲に約12pt、ベゼルのないものは見た目の端から約24pt [3]

## 4. コントラスト [3]

| 文字サイズ | ウェイト | 最小コントラスト比 |
|---|---|---|
| 17pt以下 | すべて | 4.5:1 |
| 18pt以上 | すべて | 3:1 |
| すべて | 太字 | 3:1 |

ライトとダークの両方で満たす。満たせない場合でも、「コントラストを上げる」がオンのときに高コントラスト配色を出す [3]。

- Dark Mode のページは「色同士のコントラスト比は最低 4.5:1、**独自の前景色・背景色は 7:1 を目指す**（特に小さい文字）」としている [18]。18pt 以上で 3:1 という上の表（Accessibility のページ）より厳しいので、独自色は 7:1 を目標にする
- 画像の上に文字を載せるときは、影か背景の層でコントラストを確保する（機械チェックでは測れないので目で確認する）

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
| 3次背景 tertiarySystemBackground | #FFFFFF | #2C2C2E |
| ダークの手前の面（高階調）systemBackground | ― | #1C1C1E |
| ダークの手前の面（高階調）secondarySystemBackground | ― | #2C2C2E |

- **ダークには「ベース」と「高階調（elevated）」の2組の背景がある**。シートやポップオーバーのように手前に出る面は自動で高階調（明るい側）になるので、ダークのシートは上の「高階調」の値で描く（値は近似）[18]
- 独自色は、ライト／ダークそれぞれに「コントラストを上げる」用の値も用意する。外観を1つしか用意しないアプリでも、Liquid Glass のためにライトとダークの両方の色を用意する [4]
- **アプリ内にライト／ダークの切り替えを作らない**（システムの設定に従う）。システム全体の設定（アクセシビリティなど）をアプリの設定に複製しない [18][19]
- アクセントカラーは主要な操作と状態の表示（選択中のタブ、未読など）に絞り、ブランドの色はコンテンツ側に入れる。ロゴを常に表示しない [20]
- Mac では、アプリのアクセントカラーはシステム設定のアクセントカラーが「マルチカラー」のときだけ効き、それ以外はユーザーが選んだ色に置き換わる（Mac のモックは「マルチカラー時」と書く）[4]

- **注意： システムの secondaryLabel（ライト、#3C3C43・不透明度60%）は白背景で約3.4:1** で、17pt以下の文字の基準（4.5:1）に届かない（計算値）。17pt以下で読ませる必要がある文字は、label を使うか、不透明度を約80%に上げた独自色（アセットカタログで定義）にする。ダーク（#EBEBF5・60%）は基準を満たす
- 同じ色に別の意味を持たせない。色だけで情報を区別しない [4]
- Liquid Glass のバー（タブバー・ツールバー）の上では、コンテンツと似た色をラベルに使わない [6][7]
- Liquid Glass への色付けは控えめにする。強調する操作は記号や文字ではなく背景に色を付ける（例：「完了」の背景をアクセントカラー）。複数のコントロールの背景に色を付けない [4]
- **Liquid Glass はバーとコントロールだけに使い、コンテンツの層には使わない**。バーの後ろに幅いっぱいの不透明・半透明の帯を描かず、コンテンツをバーの下まで描く（読みやすさはスクロールエッジエフェクトで保つ。モックでは上端・下端の薄いぼかしで近似）。写真や動画の上に浮かべる部品は clear を使い、下が明るいときは不透明度35%の暗い層を敷く [21][22]

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

## 7. 部品ごとの決まり（HIG 各ページの要点）

| 部品 | 決まり | 出典 |
|---|---|---|
| ツールバー | 戻る／閉じるは標準の記号（文字の「戻る」は使わない）。システムの記号は枠なしで表示。グループは3つ程度まで、強調する操作は1つで後端 | [7] |
| タブバー | 別のセクションに移っても表示したまま（例外はタブバーを覆うモーダル）。タブを無効化・非表示にしない。はみ出して「その他」タブができる状態を避ける。アイコンは塗り（fill）の記号。バッジは重要な情報だけ | [6] |
| シート | iOS は「キャンセル」を先頭、「完了」などを末尾。「完了」は必ず「キャンセル」か「戻る」と組にし、3つ全部は並べない。メイン画面から出すシートは一度に1つ。編集中にスワイプで閉じようとしたらアクションシートで確認する。長い・複雑な流れは全画面のモーダル。**つまみ（グラバー）はサイズを変えられるシートにだけ**付ける | [10][23] |
| モーダル全般 | タスク名のタイトルを付ける。モーダルの上にモーダルを重ねない。アラートを同時に2つ出さない | [23] |
| ポップオーバー | iPhone や細いウィンドウ（compact）では出さず、シートにする。同時に1つだけ。警告には使わない | [24] |
| アラート | ボタンは最大3つ、タイトルは2行まで。確認のボタンは「OK」ではなく「削除」などの動詞、取り消しは「キャンセル」。強調するボタンは横並びの後端・縦並びの一番上、キャンセルは横並びの先頭・縦並びの一番下。起動時に出さない。よく使う取り消し可能な削除では確認しない | [25] |
| アクションシート | ユーザーが始めた操作の選択肢に使う。キャンセルは一番下、破壊的な操作は一番上で赤。タイトルは1行、スクロールさせない。Watch はキャンセルを含めて4つまで | [26] |
| メニュー／プルダウン | 使えない項目は淡色にしてメニュー自体は開けるままにする（コンテキストメニューは逆に非表示）。サブメニューは1階層。グループ内のアイコンは全部付けるか全部付けない。追加の入力が要る項目は末尾に「…」。画面の主要な操作を「…」の中にしまわない。項目が1〜2個ならボタンやトグルにする | [27] |
| コンテキストメニュー | 項目は少なく、区切りのグループは3つ以下。破壊的な項目は末尾で赤。ショートカットは表示しない。項目はメインのUIからも使えるようにする | [28] |
| セグメントコントロール | iPhone は約5個まで、広い画面で5〜7個まで。文字と画像を混ぜない。幅をそろえる。ラベルは名詞。別のセクションの切り替えにはタブバーを使う | [29] |
| トグル | iOS のスイッチはリストの行の中だけで使う。オン／オフを色の違いだけで示さない。Mac のラジオボタンは5つ程度まで | [30] |
| リスト | 詳細へ進む行にはシェブロン。情報ボタン（i）は詳細表示専用。長い文字は中央を省略して先頭と末尾を残す。iOS の箱（カード）は入れ子にしない | [31] |
| 分割ビュー | 詳細に至るまでの各ペインで選択中の項目を常に強調表示する。iOS では regular の幅でだけ使う。Mac の区切り線は 1pt、パネルは隠せて、ツールバーのボタンとメニュー（ショートカット付き）で再表示できる | [32] |
| ピッカー | 短い選択肢はプルダウンにする。ピッカーのために画面を切り替えず、編集中の欄の近くかポップオーバーに出す。分の刻みは60を割り切れる間隔 | [33] |
| 入力欄 | プレースホルダとは別に項目のラベルを付ける。内容に合ったキーボードの種類と内容の種類（メール、電話番号など）を指定し、検索なら Return を「検索」にする。必須項目が埋まるまで「次へ」を押せないようにする。できるだけ選択式にする | [34][35] |
| ページコントロール | 下部中央に横向き。点が10個を超えたら別の方法にする。点に色を付けない | [36] |
| スクロール | 同じ方向のスクロールを入れ子にしない。スクロールエッジエフェクトは浮いたバーの後ろだけで1ビューに1つ。iPad・Mac の分割ビューでは各ペインの高さをそろえる | [37] |
| 検索 | 検索が重要なら主要な位置に置く。タブバーのあるアプリは検索を専用のタブにしてよい（タブバーは移動専用の例外）。iPhone は下の方、iPad と Mac はツールバーの末尾。iPad の細いウィンドウでも検索を残す。iPad で仮想キーボードしかないときは自動でフォーカスしない | [38] |
| ジェスチャ | カスタムジェスチャを重要な操作の唯一の手段にしない（ボタンも置く）。標準のジェスチャに別の意味を割り当てない | [39] |
| 共有 | 共有は square.and.arrow.up のボタンから開く。iPhone はシート、iPad はポップオーバー | [40] |
| モーション・触覚 | 重要な情報をアニメーションだけで伝えない。アニメーションの終了を待たせない。触覚は控えめにし、オフでも使えるようにする | [41] |

## 8. 状態・流れ・文言

| 場面 | 決まり | 出典 |
|---|---|---|
| 起動画面 | 最初の画面とほぼ同じ骨格にし、**文字を入れない**（ローカライズされないため）。ライト／ダークと向きに合わせる。ロゴは最初の画面にも出し続ける場合だけ。macOS と watchOS には起動画面がない | [42] |
| 読み込み | 内容はできるだけ早く出し、プレースホルダから順に置き換える。所要時間が分かるなら確定的、分からないなら不確定的なインジケータ（途中で種類を変えない）。「読み込んでいます」のような曖昧な文言を避ける。可能ならキャンセルを出す。時間のかかるボタンは、ボタンの中にインジケータを出してラベルも変える（例：「送信中…」）| [43][17] |
| 空状態 | 次の操作のボタンやリンクを置く。空状態は一時的なので、重要な情報を空状態にだけ置かない | [44] |
| エラー | 問題のそば（入力欄の横など）に出し、直し方を書く。実行できない操作は、その旨と理由を伝える。取り返しのつかないデータ損失の前には警告する | [44][45] |
| 権限 | その機能を使う時点で求める（起動時に求めない）。用途の説明文は能動態で具体的に。システムのダイアログの前に出す説明画面はボタン1つ（「続ける」「次へ」。「許可」は不可）で、閉じるボタンを置かない | [19] |
| オンボーディング | 起動が終わってから行う。短く、スキップできる。スキップしたら次回から出さず、ヘルプや設定から見直せる。評価や購入のお願いは、しばらく使ってもらってから | [46] |
| 評価の依頼 | システムの依頼画面を使う（表示は365日で3回まで）。初回起動時やオンボーディング中に出さない | [47] |
| サインイン | できるだけ後に回す。Apple でサインインを使わないならパスキーを優先。認証方法を名前で示す（例：「Face ID でサインイン」）| [48] |
| アカウント削除 | アプリ内から簡単に削除できるようにする（できなければ、削除用 Web ページへの直接リンクを見つけやすい場所に）。サブスクリプションは削除後も請求が続くことを説明する | [48] |
| 課金画面 | 名前・期間・各期間の内容・現地通貨の金額・購入の復元（またはサインイン）・利用規約とプライバシーポリシーへのリンク・無料トライアルの期間と終了後の価格を載せる。解約を見つけにくい場所に置かない。Apple の確認シートをまねない | [49] |
| 通知 | 機密情報を入れない。プレビュー非表示のときの汎用の文（例：「新規コメント」）を用意する。アクションは最大4つで、アプリを開くだけのアクションは置かない。タイトルにアプリ名を入れない。エラーは通知ではなくアラート | [50] |
| バッジ | 未読の数だけに使う（天気・日付などには使わない）。重要な情報をバッジだけで伝えない。バッジに似せた独自の部品を作らない | [50] |
| 状態の保存 | 現在の状態を保存し、再起動後もスクロール位置やウィンドウの位置まで戻す | [42][51] |
| 文言 | 呼びかけは「あなた」。「私たち」は使わない。端末に合った語にする（タッチ端末で「クリック」と書かない）。ボタンは動詞。「次へ」と「続ける」はどちらかに統一。専門用語は説明なしに使わない | [44][52] |
| 人物の表現 | 性別を不要に表現しない。人物は多様に描き、職業などのステレオタイプを避ける（架空のサンプルデータでも）| [52] |
| アクセシビリティの補足 | 画面ごとに固有のタイトル、セクションに見出し。装飾だけの画像は読み上げから外す。関係する要素はまとめて読ませる。時間で自動的に消える表示を避ける。開始・停止の操作なしに音声や動画を自動再生しない | [3][53] |

## 9. Mac の決まり

| 項目 | 決まり | 出典 |
|---|---|---|
| メニューバーの並び | アプリ名 → ファイル → 編集 → フォーマット → 表示 → アプリ固有のメニュー → ウインドウ → ヘルプ。「ウインドウ」はウィンドウが1つでも必須（「しまう」「拡大／縮小」を入れる）。「表示」はフルスクリーンの項目だけでも用意する。実行できない項目は隠さず無効にする。メニュー名は短い1語 | [11] |
| 配置 | 主要な操作と情報はウインドウの上部とツールバーに置き、**下部に置かない**（ウィンドウの下端は画面外に出やすい）。独自のウィンドウ枠を作らない。入れ子とモーダルを減らす | [8][54] |
| ショートカット | 独自のショートカットは Command を主に、Shift を2つ目に使う（Control は避け、Option は控えめに）。表示順は Control・Option・Shift・Command。既存のショートカットに修飾キーを足して無関係な機能を作らない。取り消し／やり直しは編集メニューの上部で ⌘Z / ⇧⌘Z | [55][56] |
| ボタン | 別のウィンドウや画面を開くボタンは題名の末尾に「…」。ヘルプボタン（?）は1ウィンドウに1つで、ツールバーに置かない | [17] |
| サイドバー | 既定で隠さない。ウィンドウを縮めたら自動で畳む。下部に重要な情報や操作を置かない。「表示」メニューに「サイドバーを表示／非表示」を入れる | [9] |
| 設定ウインドウ | アプリメニューの「設定…」から開き、ツールバーに設定ボタンを置かない。最小化・拡大は使えなくする。パネル切り替えのツールバーは選択中のパネルを示し、ウィンドウの題名はパネル名。最後に開いたパネルを復元する | [19] |
| フルスクリーン | システムのフルスクリーン機能を使い、ウィンドウのボタン・「表示」メニュー・⌃⌘F で切り替える | [57] |
| 表とアウトライン | 列見出しのクリックで並べ替え、列の幅を変えられる。複数列の表は行の色を交互に。階層は最初の列だけ | [31] |
| Mac Catalyst | iPad の見た目のまま動かす設定では表示が 77% に縮小される（17pt が 13pt）。タブバーはサイドバー付きの分割ビューなどに置き換え、画面の端のボタンはツールバーへ移す | [58] |

## 10. Apple Watch の決まり

| 項目 | 決まり | 出典 |
|---|---|---|
| 背景 | 標準は黒。色の背景は情報を伝えるときだけ使い、ワークアウト中のように長く表示される画面では全面の背景色を使わない | [4][59] |
| ボタンの並べ方 | 記号のボタンは横に3つまで、文字のボタンは横に2つまで。文字のボタンは基本的に画面幅いっぱい | [8] |
| 縦のページ | 1ページは画面の高さに収まる量。高さが変わるページは固定高のページの後ろに置く。Digital Crown でする移動はタッチでもできるようにする（Crown を押す操作はアプリで使えない）| [37][60] |
| ダブルタップ | ビューで最もよく使うボタンを主アクションにする。リスト・スクロール・縦タブのビューには付けない | [39] |
| 読み込み | 読み込みの表示はできるだけ出さない。1〜2秒かかるときだけ空白より優先して出す。長い処理は終わったら通知で知らせる | [43][45] |
| 常時表示 | レイアウトは変えずに、補足の文字・画像・塗りを暗くする。銀行残高や健康データなどの機密情報を隠す（ワークアウト中のペースのように一目で見られると喜ばれる情報もある）。操作できる部品は消さずに操作できない見た目にする。更新頻度を下げる | [61] |
| 通知 | ショートルック（タイトルに機密情報を入れない）とロングルック（アクションは最大4つ、下に「閉じる」）の2段階 | [50] |
| 設定 | アプリの設定はシステムの設定アプリに入らない。メイン画面の下部か「詳細」メニューに少数だけ置く | [19] |
| コンプリケーション | できるだけすべてのファミリーに対応する。それぞれ別のディープリンクにする。淡色モードでも色だけで情報を伝えない。線の幅は 2pt 以上 | [62] |

## 11. よく使う操作の標準アイコン（SF Symbols）[63]

| 操作 | シンボル | 操作 | シンボル |
|---|---|---|---|
| 完了 | checkmark | キャンセル | xmark |
| 追加 | plus | 削除 | trash |
| 共有 | square.and.arrow.up | その他（あふれ） | ellipsis |
| コピー | document.on.document | ペースト | document.on.clipboard |
| フィルタ | line.3.horizontal.decrease | アカウント | person.crop.circle |
| 取り消す | arrow.uturn.backward | 検索 | magnifyingglass |

- 同じ操作はどの画面でも同じシンボルにする。シンボルの太さは隣の文字に合わせる。iOS のタブバーは塗り（.fill）、ツールバーとリストは線
- **SF Symbols やそれに似せた形を、アプリアイコンやロゴに使わない**（利用規約）[64]

## 12. 特定の機能がある場合の数値

| 機能 | 決まり | 出典 |
|---|---|---|
| ウィジェット（iPhone 393×852pt）| 小 158×158、中 338×158、大 338×354、ロック画面 円形 72×72・長方形 160×72・インライン 234×26pt。余白は標準16pt（詰めるとき11pt）、文字は11pt以上。ライト／ダーク／クリア／淡色の外観を確認し、読み込み中のプレースホルダを描く | [65] |
| ライブアクティビティ | 8時間以内の作業に使う。広告や機密情報を出さない。ロック画面の余白14pt | [66] |
| Apple でサインイン | ボタンは最小 140×30pt、周囲の余白はボタンの高さの1/10以上。他のサインインボタンより小さくしない。スタイルは白／白（輪郭線）／黒 | [67] |
| Apple Pay | ボタンは Apple の API で作り、最小 100×30pt。デジタル商品やサブスクリプションはアプリ内課金で売る | [68] |
| 地図 | Apple のロゴと権利表示を隠さない（余白の目安 左右7pt・上下10pt）| [69] |
| グラフ | タイトルや要約で目的を先に伝える。色だけで系列を区別しない。棒グラフの縦軸は0から。各要素か要約にアクセシビリティのラベルを付ける | [70] |
| 生成AI | AIを使っている場所を示す。結果の近くに編集・元に戻す・再試行を置く。生成中は何をしているかを具体的に書く。削除や購入を自動で実行しない | [71] |
| ホーム画面のクイックアクション | 4つまで。SF Symbols を使い、タイトルにアプリ名を入れない | [72] |
| ゲームの画面上の操作 | ホームインジケータ・Dynamic Island と重ねない。よく使うもの 44×44pt 以上、メニューなど 28×28pt 以上。補助の操作は上部。押された状態は指で隠れても見せる。A／X／R1 の表記を絵に使わない。移動は左、カメラは右 | [74] |
| ゲームコントローラ・キーボード | 標準の操作（タッチ／キーボード・マウス）でも遊べるようにする。UIでは A＝実行、B＝戻る、ショルダー＝セクション移動、メニュー＝設定・一時停止、ホーム＝システム予約。表記は接続中のコントローラに合わせたシンボル。キーボードは1キーのコマンドを優先し、割り当てを変更できる。watchOS はコントローラ非対応 | [74] |
| CarPlay（iOS のみ）| システムのテンプレートで iOS が描く（自由なレイアウトにしない）。ロック中でも動く。エラーは CarPlay の画面に出す。重要なものは画面の上半分。ライト／ダーク両対応。アイコン @2x 120×120px・@3x 180×180px、背景を黒にしない | [75] |
| iPhoneのタッチ決済（iOS のみ）| ラベル「iPhoneのタッチ決済」／「タッチ決済」、記号は wave.3.right.circle(.fill)、Apple ロゴなし。最終金額は決済画面の前に決める。準備中・承認中は進捗表示。失敗時は別の方法か再試行 | [76] |
| ID確認（iOS のみ）| ボタン「年齢を確認」／「本人であると確認」。通信方式の記号と Apple ロゴを入れない。必要なデータだけ求める | [77] |
| ヘルスケアデータ・CareKit（iOS / iPadOS）| 使う時点で許可を求める。標準の許可画面をまねない。共有の管理はシステム設定。グラフは単位を軸に、凡例を付ける。薬は商品名 | [78] |
| ResearchKit（iOS / iPadOS）| 概要 → 参加資格 → 同意 → データへのアクセス許可 の順。アンケートは1問1画面、問題数と所要時間を先に示す | [79] |
| ShazamKit | 録音はできるだけ早く止める。iCloud のライブラリへの保存は先に許可を取る | [80] |

## 13. 画像の書き出し [73]
- PNG はカラープロファイル（sRGB、広色域なら Display P3）を埋め込み、インターレースなしで書き出す（`scripts/export_png.py` は sRGB を埋め込む）

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
17. HIG — Buttons: https://developer.apple.com/design/human-interface-guidelines/buttons
18. HIG — Dark Mode: https://developer.apple.com/design/human-interface-guidelines/dark-mode
19. HIG — Privacy / Settings: https://developer.apple.com/design/human-interface-guidelines/privacy
20. HIG — Branding: https://developer.apple.com/design/human-interface-guidelines/branding
21. HIG — Materials: https://developer.apple.com/design/human-interface-guidelines/materials
22. HIG — Layout: https://developer.apple.com/design/human-interface-guidelines/layout
23. HIG — Sheets / Modality: https://developer.apple.com/design/human-interface-guidelines/modality
24. HIG — Popovers: https://developer.apple.com/design/human-interface-guidelines/popovers
25. HIG — Alerts: https://developer.apple.com/design/human-interface-guidelines/alerts
26. HIG — Action sheets: https://developer.apple.com/design/human-interface-guidelines/action-sheets
27. HIG — Menus / Pull-down buttons: https://developer.apple.com/design/human-interface-guidelines/menus
28. HIG — Context menus: https://developer.apple.com/design/human-interface-guidelines/context-menus
29. HIG — Segmented controls: https://developer.apple.com/design/human-interface-guidelines/segmented-controls
30. HIG — Toggles: https://developer.apple.com/design/human-interface-guidelines/toggles
31. HIG — Lists and tables: https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
32. HIG — Split views: https://developer.apple.com/design/human-interface-guidelines/split-views
33. HIG — Pickers: https://developer.apple.com/design/human-interface-guidelines/pickers
34. HIG — Text fields: https://developer.apple.com/design/human-interface-guidelines/text-fields
35. HIG — Entering data / Virtual keyboards: https://developer.apple.com/design/human-interface-guidelines/entering-data
36. HIG — Page controls: https://developer.apple.com/design/human-interface-guidelines/page-controls
37. HIG — Scroll views: https://developer.apple.com/design/human-interface-guidelines/scroll-views
38. HIG — Search fields / Searching: https://developer.apple.com/design/human-interface-guidelines/search-fields
39. HIG — Gestures: https://developer.apple.com/design/human-interface-guidelines/gestures
40. HIG — Activity views: https://developer.apple.com/design/human-interface-guidelines/activity-views
41. HIG — Motion / Playing haptics: https://developer.apple.com/design/human-interface-guidelines/motion
42. HIG — Launching: https://developer.apple.com/design/human-interface-guidelines/launching
43. HIG — Loading / Progress indicators: https://developer.apple.com/design/human-interface-guidelines/loading
44. HIG — Writing: https://developer.apple.com/design/human-interface-guidelines/writing
45. HIG — Feedback: https://developer.apple.com/design/human-interface-guidelines/feedback
46. HIG — Onboarding: https://developer.apple.com/design/human-interface-guidelines/onboarding
47. HIG — Ratings and reviews: https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews
48. HIG — Managing accounts / Sign in with Apple: https://developer.apple.com/design/human-interface-guidelines/managing-accounts
49. HIG — In-app purchase: https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase
50. HIG — Notifications: https://developer.apple.com/design/human-interface-guidelines/notifications
51. HIG — Multitasking: https://developer.apple.com/design/human-interface-guidelines/multitasking
52. HIG — Inclusion: https://developer.apple.com/design/human-interface-guidelines/inclusion
53. HIG — VoiceOver: https://developer.apple.com/design/human-interface-guidelines/voiceover
54. HIG — Designing for macOS: https://developer.apple.com/design/human-interface-guidelines/designing-for-macos
55. HIG — Keyboards: https://developer.apple.com/design/human-interface-guidelines/keyboards
56. HIG — Undo and redo: https://developer.apple.com/design/human-interface-guidelines/undo-and-redo
57. HIG — Going full screen: https://developer.apple.com/design/human-interface-guidelines/going-full-screen
58. HIG — Mac Catalyst: https://developer.apple.com/design/human-interface-guidelines/mac-catalyst
59. HIG — Designing for watchOS: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos
60. HIG — Digital Crown: https://developer.apple.com/design/human-interface-guidelines/digital-crown
61. HIG — Always On: https://developer.apple.com/design/human-interface-guidelines/always-on
62. HIG — Complications: https://developer.apple.com/design/human-interface-guidelines/complications
63. HIG — Icons: https://developer.apple.com/design/human-interface-guidelines/icons
64. HIG — SF Symbols: https://developer.apple.com/design/human-interface-guidelines/sf-symbols
65. HIG — Widgets: https://developer.apple.com/design/human-interface-guidelines/widgets
66. HIG — Live Activities: https://developer.apple.com/design/human-interface-guidelines/live-activities
67. HIG — Sign in with Apple: https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple
68. HIG — Apple Pay: https://developer.apple.com/design/human-interface-guidelines/apple-pay
69. HIG — Maps: https://developer.apple.com/design/human-interface-guidelines/maps
70. HIG — Charting data: https://developer.apple.com/design/human-interface-guidelines/charting-data
71. HIG — Generative AI: https://developer.apple.com/design/human-interface-guidelines/generative-ai
72. HIG — Home Screen quick actions: https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions
73. HIG — Images: https://developer.apple.com/design/human-interface-guidelines/images
74. HIG — Game controls: https://developer.apple.com/design/human-interface-guidelines/game-controls
75. HIG — CarPlay: https://developer.apple.com/design/human-interface-guidelines/carplay
76. HIG — Tap to Pay on iPhone: https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone
77. HIG — ID Verifier: https://developer.apple.com/design/human-interface-guidelines/id-verifier
78. HIG — CareKit: https://developer.apple.com/design/human-interface-guidelines/carekit
79. HIG — ResearchKit: https://developer.apple.com/design/human-interface-guidelines/researchkit
80. HIG — ShazamKit: https://developer.apple.com/design/human-interface-guidelines/shazamkit
