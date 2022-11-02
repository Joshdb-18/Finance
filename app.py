import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

DISPLAY = {}
REGISTRANTS = {}
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", id)
    stocks = db.execute("SELECT symbol, SUM(shares) as shares FROM track WHERE id = ? GROUP BY symbol HAVING (SUM(shares)) > 0;", id)
    tot_cash = 0
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = stock["price"] * stock["shares"]
        tot_cash = tot_cash + stock["total"]

    sto_total = tot_cash + cash[0]["cash"]
    cash1 = 10000 - tot_cash
    al = cash1 + tot_cash
    return render_template("index.html", stocks=stocks, cash=cash1, total=al)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Ensure user enters via post
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares", type=int)
        # If symbol is not inputed
        if not symbol:
            return apology("Must enter symbol", 400)

        # If shares is not inputed
        elif not shares:
            return apology("Must enter shares", 400)

        # Check if shares is a positive integer
        elif shares < 1:
            return apology("Must enter a positive integer", 400)

        else:
            quoted = lookup(symbol)
            # if quote is not in our json file, return an apology
            if quoted is None:
                return apology("Invalid symbol", 400)
            price = quoted["price"]
            sym = quoted["symbol"]
            currentcash = db.execute("SELECT cash from users WHERE id = ?", session["user_id"])
            cash_amt = currentcash[0]["cash"]
            newprice = float(shares * price)
            if cash_amt < newprice:
                return apology("Sorry, Not enough cash to purchase stock", 400)

            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", newprice, session["user_id"])
            newcash = cash_amt - newprice
            name = quoted["name"]
            new_date = datetime.now()
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            db.execute("INSERT INTO track (id,name,shares,price,symbol,total,date,time) VALUES(?,?,?,?,?,?,?,?)",
                       session["user_id"], name, shares, price, sym, newprice, new_date, current_time)
            flash("Bought!")
            return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    stocks = db.execute("SELECT * FROM track WHERE id = ?", session["user_id"])
    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        name = request.form.get("username")
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Welcome!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # if request is via POST
    if request.method == "POST":

        # Get symbol
        quoted = lookup(request.form.get("symbol"))

        # If user doesn't include a symbol
        if quoted is None:
            return apology("must enter symbol", 400)

        else:
            # Else return price of stock
            return render_template("quoted.html", name=quoted["name"],
                                   price=quoted["price"],
                                   symbol=quoted["symbol"])

    # If request is via GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Ensure user enters via POST
    if request.method == "POST":

        # Get name
        name = request.form.get("username")

        # Get username check to know if name already exist
        usernameCheck = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide a name", 400)

        # Else if username already exists
        elif usernameCheck:
            return apology("Username already exists", 400)

        # Else if password was not submitted
        elif not request.form.get("password"):
            return apology("Must provide a password", 400)

        # Else if confirmation was not submitted
        elif not request.form.get("confirmation"):
            return apology("Must confirm Password")

        # Else if password is not the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password must match", 400)

        # Hash password
        password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Insert user into table
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", name, password)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        return redirect("/")
    # If user enters via GET
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    sym = db.execute("SELECT symbol FROM track WHERE id = ? GROUP BY symbol", session["user_id"])
    SYMBOLS = list()
    for x in sym:
        SYMBOLS.append(x["symbol"])
    """Sell shares of stock"""
    # Ensure user enters via post
    if request.method == "POST":
        # Get symbol
        symbol = request.form.get("symbol")
        # Get shares
        shares = request.form.get("shares", type=int)
        # Select user current share
        curr_shares = db.execute("SELECT shares FROM track WHERE id = ? and symbol = ?", session["user_id"], symbol)
        curr_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        current_shares = curr_shares[0]["shares"]
        # Conditions:
        if not symbol:
            return apology("Must enter a valid symbol", 400)
        elif shares < 1:
            return apology("Must enter a valid integer", 400)
        elif shares > current_shares:
            return apology("You don't have that much share", 400)
        quote = lookup(symbol)
        price = quote["price"]
        new_share = current_shares - shares
        total = price * new_share
        new_date = datetime.now()
        now = datetime.now()
        curr_time = now.strftime("%H:%M:%S")
        name = quote["name"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?", curr_cash[0]["cash"] + (shares * price), session["user_id"])
        db.execute("INSERT INTO track(id,name,shares,price,symbol,total,date,time) VALUES(?,?,?,?,?,?,?,?)",
                   session["user_id"], name, -shares, price, symbol, total, new_date, curr_time)
        flash("Sold!")
        return redirect("/")
    return render_template("sell.html", symbols=SYMBOLS)
