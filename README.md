# Finance
### A website via which users can “buy” and “sell” stocks as per cs50 finance specifications
![Finanve Image](https://cs50.harvard.edu/x/2021/psets/9/finance/finance.png)

## Configuring
### Before getting started on this, we’ll need to register for an API key in order to be able to query IEX’s data. To do so, follow these steps:
- Visit: [IEX cloud website](https://iexcloud.io/cloud-login#/register/)
- Select the “Individual” account type, then enter your email address and a password, and click “Create account”.
- Once registered, scroll down to “Get started for free” and click “Select Start” to choose the free plan
- Once you’ve confirmed your account via a confirmation email, visit https://iexcloud.io/console/tokens.
- Copy the key that appears under the Token column (it should begin with pk_).
- In a terminal, execute: `$ export API_KEY=value`

***where `value` is that (pasted) value, without any space immediately before or after the =. You also may wish to paste that value in a text document somewhere, in case you need it again later.***

## Background
Indeed, IEX lets you download stock quotes via their API (application programming interface) using URLs like https://cloud.iexapis.com/stable/stock/nflx/quote?token=API_KEY. Notice how Netflix’s symbol (NFLX) is embedded in this URL; that’s how IEX knows whose data to return. That link won’t actually return any data because IEX requires you to use an API key, but if it did, you’d see a response in JSON (JavaScript Object Notation) format like this:

```
{
   "symbol": "NFLX",
   "companyName": "Netflix, Inc.",
   "primaryExchange": "NASDAQ",
   "calculationPrice": "close",
   "open": 317.49,
   "openTime": 1564752600327,
   "close": 318.83,
   "closeTime": 1564776000616,
   "high": 319.41,
   "low": 311.8,
   "latestPrice": 318.83,
   "latestSource": "Close",
   "latestTime": "August 2, 2019",
   "latestUpdate": 1564776000616,
   "latestVolume": 6232279,
   "iexRealtimePrice": null,
   "iexRealtimeSize": null,
   "iexLastUpdated": null,
   "delayedPrice": 318.83,
   "delayedPriceTime": 1564776000616,
   "extendedPrice": 319.37,
   "extendedChange": 0.54,
   "extendedChangePercent": 0.00169,
   "extendedPriceTime": 1564876784244,
   "previousClose": 319.5,
   "previousVolume": 6563156,
   "change": -0.67,
   "changePercent": -0.0021,
   "volume": 6232279,
   "iexMarketPercent": null,
   "iexVolume": null,
   "avgTotalVolume": 7998833,
   "iexBidPrice": null,
   "iexBidSize": null,
   "iexAskPrice": null,
   "iexAskSize": null,
   "marketCap": 139594933050,
   "peRatio": 120.77,
   "week52High": 386.79,
   "week52Low": 231.23,
   "ytdChange": 0.18907500000000002,
   "lastTradeTime": 1564776000616
}
```

***Notice how, between the curly braces, there’s a comma-separated list of key-value pairs, with a colon separating each key from its value.***

## Running
### Start Flask’s built-in web server (within Finance/):
`` flask run``
Visit the URL outputted by flask

## Features
- `Register and Login`
- `Quote`: It allows a user to look up a stock’s current price.
- `Buy`: It enables a user to buy stocks. Renders an apology if the input is blank or the symbol does not exist (as per the return value of lookup) and so on...
- `Sell`: It enables a user to sell shares of a stock (that he or she owns). Renders an apology if the user fails to select a stock or if (somehow, once submitted) the user does not own any shares of that stock and so on...
- `Index`: Displays an HTML table summarizing, for the user currently logged in, which stocks the user owns, the numbers of shares owned, the current price of each stock, and the total value of each holding (i.e., shares times price). Also displays the user’s current cash balance along with a grand total (i.e., stocks’ total value plus cash)
- `History`: Displays an HTML table summarizing all of a user’s transactions ever, listing row by row each and every buy and every sell. For each row, it makes clear whether a stock was bought or sold and include the stock’s symbol, the (purchase or sale) price, the number of shares bought or sold, and the date and time at which the transaction occurred.

## Hints:
- You should use [SQLAlchemy Core](http://docs.sqlalchemy.org/en/latest/index.html) or [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/) (i.e., [SQLAlchemy ORM](http://docs.sqlalchemy.org/en/latest/index.html)) instead of cs50.SQL.
- You may find [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/) or [Jinja documentation](http://jinja.pocoo.org/docs/dev/) helpful
- You’re welcome to alter the aesthetics of the sites, as via:
   - [Bootswatch](https://bootswatch.com/)
   - [Bootstrap content](https://getbootstrap.com/docs/4.1/content/)
   - [Bootstrap components](https://getbootstrap.com/docs/4.1/components/) and/or
   - [Memegen.link](https://memegen.link/)
 
 
## Personal touch to implement
- Allow users to change their passwords.
- Allow users to add additional cash to their account.
- Allow users to buy more shares or sell shares of stocks they already own via index itself, without having to type stocks’ symbols manually.
- Require users’ passwords to have some number of letters, numbers, and/or symbols.
- Implement some other feature of comparable scope.
- Have fun :wink:

## FAQ
### OSError: [Errno 98] Address already in use
If, upon running flask, you see this error, odds are you (still) have flask running in another tab. Be sure to kill that other process, as with ctrl-c, before starting flask again. If you haven’t any such other tab, execute fuser -k 8080/tcp to kill any processes that are (still) listening on TCP port 8080.
### ImportError: No module named ‘application’
By default, flask looks for a file called application.py in your current working directory (because we’ve configured the value of FLASK_APP, an environment variable, to be application.py). If seeing this error, odds are you’ve run flask in the wrong directory!


# <span style="color:red;">WARNING!!!</span> 🔴❎
## You shouldn't use this projects as your assignment on CS50 or you risk being removed from the program
