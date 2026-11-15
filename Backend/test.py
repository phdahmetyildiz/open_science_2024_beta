# This file is being archived on 15.11.2026 and is not part of the new version.
from flask import Flask, request, jsonify, render_template
import sqlite3
import os




def add_article(title, author, content):
        conn = get_db_connection()
        if conn is not None:
            try:
                conn.execute('''
                    INSERT INTO articles (title, author, content) VALUES (?, ?, ?)
                ''', (title, author, content))
                conn.commit()
                print(f"Artikel '{title}' wurde hinzugefügt.")
                conn.close()
            except sqlite3.Error as e:
                print(f"Fehler beim Hinzufügen des Artikels: {e}")
        else:
            print("Verbindung zur Datenbank konnte nicht hergestellt werden.")

def search_articles(keyword):
        conn = get_db_connection()
        if conn is not None:
            try:
                cursor = conn.execute('''
                    SELECT * FROM articles WHERE title LIKE ? OR content LIKE ?
                ''', ('%' + keyword + '%', '%' + keyword + '%'))
                results = cursor.fetchall()
                conn.close()
                if results:
                    print(f"Gefundene Artikel mit dem Stichwort '{keyword}':") ######################
                    for i, article in enumerate(results, start=1):
                        print(f"{i}. Titel: {article['title']}, Autor: {article['author']}")
                else:
                    print(f"Keine Artikel gefunden mit dem Stichwort '{keyword}'.")
            except sqlite3.Error as e:
                print(f"Fehler bei der Artikelsuche: {e}")
        else:
            print("Verbindung zur Datenbank konnte nicht hergestellt werden.")

def display_articles():
        conn = get_db_connection()
        if conn is not None:
            try:
                cursor = conn.execute('SELECT * FROM articles')
                articles = cursor.fetchall()
                conn.close()
                if articles:
                    print("Liste der Artikel:")
                    for i, article in enumerate(articles, start=1):
                        print(f"{i}. Titel: {article['title']}, Autor: {article['author']}") #####################
                else:
                    print("Keine Artikel in der Bibliothek.")
            except sqlite3.Error as e:
                print(f"Fehler beim Anzeigen der Artikel: {e}")
        else:
            print("Verbindung zur Datenbank konnte nicht hergestellt werden.")

