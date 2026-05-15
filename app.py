from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DATA_FILE = "entries.json"


def load_entries():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except:
            return []


def save_entries(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)


entries = load_entries()


@app.route('/')
def index():
    return render_template("index.html", entries=entries)


@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    entry = next((e for e in entries if e["id"] == entry_id), None)

    if not entry:
        return "Запись не найдена", 404

    return render_template("detail.html", entry=entry)


@app.route('/add', methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        new_id = max([e["id"] for e in entries], default=0) + 1

        new_entry = {
            "id": new_id,
            "title": title,
            "content": content,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        entries.append(new_entry)

        save_entries(entries)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route('/edit/<int:entry_id>', methods=["GET", "POST"])
def edit_entry(entry_id):
    entry = next((e for e in entries if e["id"] == entry_id), None)

    if not entry:
        return "Запись не найдена", 404

    if request.method == "POST":
        entry["title"] = request.form["title"]
        entry["content"] = request.form["content"]

        save_entries(entries)

        return redirect(url_for("index"))

    return render_template("edit.html", entry=entry)


@app.route('/delete/<int:entry_id>', methods=["POST"])
def delete_entry(entry_id):
    global entries

    entries = [e for e in entries if e["id"] != entry_id]

    save_entries(entries)

    return redirect(url_for("index"))


@app.route('/search')
def search():
    query = request.args.get("q", "").lower()

    filtered_entries = [
        e for e in entries
        if query in e["title"].lower()
    ]

    return render_template("index.html", entries=filtered_entries)


@app.route('/filter/week')
def filter_week():
    week_ago = datetime.now() - timedelta(days=7)

    filtered_entries = []

    for entry in entries:
        entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")

        if entry_date >= week_ago:
            filtered_entries.append(entry)

    return render_template("index.html", entries=filtered_entries)


if __name__ == '__main__':
    app.run(debug=True)