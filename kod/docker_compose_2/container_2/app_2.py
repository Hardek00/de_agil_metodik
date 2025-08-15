from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Datalagring för ord
word_storage = []

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy", "service": "word-database"}

@app.route('/words', methods=['POST'])
def add_word():
    """Lägg till ord i databasen"""
    data = request.json
    word = data.get('word', '').strip()
    
    if not word:
        return {"error": "Inget ord skickat"}, 400
    
    # Lägg till ord med metadata
    entry = {
        "word": word,
        "timestamp": datetime.now().isoformat(),
        "length": len(word)
    }
    word_storage.append(entry)
    
    print(f"[DATABASE] Sparade ord: '{word}' (längd: {len(word)}) - Totalt: {len(word_storage)} ord")
    
    return {
        "message": "Ord sparat i databas",
        "word": word,
        "total_words": len(word_storage)
    }

@app.route('/words', methods=['GET'])
def get_words():
    """Hämta alla ord från databasen"""
    return {
        "words": word_storage,
        "count": len(word_storage)
    }

@app.route('/stats', methods=['GET'])
def get_stats():
    """Beräkna och returnera statistik"""
    if not word_storage:
        return {"message": "Inga ord i databasen ännu"}
    
    total_words = len(word_storage)
    total_chars = sum(entry['length'] for entry in word_storage)
    avg_length = total_chars / total_words if total_words > 0 else 0
    longest_word = max(word_storage, key=lambda x: x['length'])
    
    stats = {
        "total_words": total_words,
        "total_characters": total_chars,
        "average_length": round(avg_length, 2),
        "longest_word": longest_word['word'],
        "longest_length": longest_word['length']
    }
    
    print(f"[DATABASE] Statistik begärd - {total_words} ord, genomsnitt: {stats['average_length']}")
    
    return stats

@app.route('/clear', methods=['DELETE'])
def clear_database():
    """Rensa hela databasen (för testning)"""
    global word_storage
    old_count = len(word_storage)
    word_storage = []
    
    print(f"[DATABASE] Rensade databasen - tog bort {old_count} ord")
    
    return {"message": f"Databasen rensad - {old_count} ord borttagna"}

if __name__ == '__main__':
    print("=== Word Database Service startar ===")
    print("Container 2: Backend/Databas")
    print("Endpoints:")
    print("  POST   /words  - Lägg till ord")
    print("  GET    /words  - Hämta alla ord")
    print("  GET    /stats  - Hämta statistik")
    print("  DELETE /clear  - Rensa databas")
    print("  GET    /health - Hälsokontroll")
    
    app.run(host='0.0.0.0', port=5001, debug=True)