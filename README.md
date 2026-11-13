# Tokyo Stock Exchange Daily Candles: Toyota 7203 and Sony 6758

To build a daily candlestick chart for a Tokyo-listed stock, request a `1d` series with `market=JP` and a full symbol such as `TSE:7203`. Display the candle's session date in `Asia/Tokyo`; midnight in your server's time zone is not the Tokyo trading date.

日本株の日足サンプル。トヨタ自動車は `TSE:7203`、ソニーグループは `TSE:6758`。取引日は日本時間で扱います。  
日股日线示例：用东京时区标记每根 K 线的交易日，并保留证券代码的字母。

## Check a Tokyo-listed security

```bash
python3 tokyo-daily.py catalog 7203
```

The public lookup returns Toyota's catalog entry. The code accepts four-character securities codes as text, including letters. [JPX began issuing some alphanumeric codes in 2024](https://www.jpx.co.jp/english/sicc/code-pr/index.html); don't coerce new listings to integers.

## Read a daily OHLC series

After setting `ZAFEED_HTTP_BASE_URL` and `ZAFEED_API_KEY` for Japan:

```bash
python3 tokyo-daily.py candles TSE:6758
```

This requests the last 10 returned daily bars through [`GET /v1/klines`](https://www.zafeed.com/docs-kline.html). The example prints the response; use its documented timestamp and OHLC fields in your chart. Keep exchange closures as gaps in the data. Use the [JPX holiday calendar](https://www.jpx.co.jp/english/corporate/about-jpx/calendar/) and [TSE cash equity hours](https://www.jpx.co.jp/english/equities/trading/domestic/01.html) when checking an apparent gap. Osaka derivatives have separate sessions.

The public symbol lookup was tested. Authenticated history requires a provisioned Japan service. See the [shared quickstart](https://github.com/ZaFeed/stock-market-data-api) for Java, Node.js, Go and cURL clients.
