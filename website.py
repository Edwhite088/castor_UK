from flask import Flask, request, redirect, url_for, render_template_string
import json
import os

app = Flask(__name__)
QUOTES_FILE = "quotes.json"

def load_quotes():
    if not os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "w") as f:
            json.dump({"quotes": []}, f)
    with open(QUOTES_FILE, "r") as f:
        data = json.load(f)
    return data.get("quotes", [])

def save_quotes(quotes):
    with open(QUOTES_FILE, "w") as f:
        json.dump({"quotes": quotes}, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    quotes = load_quotes()

    if request.method == "POST":
        if "add" in request.form:
            new_quote = request.form.get("quote", "").strip()
            if new_quote:
                quotes.append(new_quote)
                save_quotes(quotes)
        elif "delete" in request.form:
            index = int(request.form.get("delete"))
            if 0 <= index < len(quotes):
                quotes.pop(index)
                save_quotes(quotes)
        return redirect(url_for("index"))

    html = """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <title>Quote Collector</title>
      <style>
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          max-width: 600px;
          margin: 40px auto;
          padding: 0 20px;
          background: #f9f9f9;
          color: #333;
        }
        h1, h2 {
          text-align: center;
          color: #2c3e50;
        }
        form {
          margin-bottom: 30px;
          text-align: center;
        }
        input[type="text"] {
          width: 70%;
          padding: 10px;
          font-size: 1em;
          border: 2px solid #3498db;
          border-radius: 5px;
          box-sizing: border-box;
          transition: border-color 0.3s;
        }
        input[type="text"]:focus {
          border-color: #2980b9;
          outline: none;
        }
        button {
          padding: 10px 20px;
          font-size: 1em;
          border: none;
          border-radius: 5px;
          background-color: #3498db;
          color: white;
          cursor: pointer;
          transition: background-color 0.3s;
          margin-left: 10px;
        }
        button:hover {
          background-color: #2980b9;
        }
        ul {
          list-style: none;
          padding: 0;
        }
        li {
          background: white;
          margin-bottom: 10px;
          padding: 12px 15px;
          border-radius: 5px;
          box-shadow: 0 1px 4px rgba(0,0,0,0.1);
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        li form {
          margin: 0;
        }
        li button {
          background-color: #e74c3c;
          padding: 6px 12px;
          font-size: 0.9em;
          margin-left: 0;
        }
        li button:hover {
          background-color: #c0392b;
        }
      </style>
    </head>
    <body>
      <h1>Quote Collector</h1>
      <form method="post" action="/">
        <input type="text" name="quote" placeholder="Enter your quote" required />
        <button type="submit" name="add">Add Quote</button>
      </form>

      <h2>Quotes:</h2>
      <ul>
        {% for quote in quotes %}
          <li>
            <span>{{ quote }}</span>
            <form method="post" action="/">
              <button type="submit" name="delete" value="{{ loop.index0 }}" onclick="return confirm('Delete this quote?');">Delete</button>
            </form>
          </li>
        {% endfor %}
      </ul>
    </body>
    </html>
    """
    return render_template_string(html, quotes=quotes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
