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
            "content":