from flask import Flask, request, jsonify, render_template_string
import requests
import time

app = Flask(__name__)

# URL till databas-containern (Container 2)
DATABASE_URL = "http://word-database:5001"

# Enkel HTML-template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Word Manager</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        input[type="text"] { padding: 10px; font-size: 16px; width: 300px; margin-right: 10px; }
        button { padding: 10px 20px; font-size: 16px; background: #007acc; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #005fa3; }
        .stats { background: white; padding: 15px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #007acc; }
        .words { background: white; padding: 15px; margin: 20px 0; border-radius: 5px; max-height: 200px; overflow-y: auto; }
        .word-item { padding: 5px; border-bottom: 1px solid #eee; }
        .error { color: red; font-weight: bold; }
        .success { color: green; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔤 Word Manager</h1>
        <p>Frontend Container (Container 1) - Skickar data till Database Container (Container 2)</p>
        
        <form id="wordForm">
            <input type="text" id="wordInput" placeholder="Skriv ett ord..." required>
            <button type="submit">Lägg till ord</button>
        </form>
        
        <div id="message"></div>
        
        <div id="stats" class="stats">
            <h3>📊 Statistik</h3>
            <div id="statsContent">Laddar...</div>
        </div>
        
        <div id="words" class="words">
            <h3>📝 Alla ord</h3>
            <div id="wordsContent">Laddar...</div>
        </div>
    </div>

    <script>
        // Ladda statistik och ord när sidan laddas
        loadStats();
        loadWords();
        
        // Hantera formulär
        document.getElementById('wordForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const word = document.getElementById('wordInput').value.trim();
            
            if (!word) return;
            
            try {
                const response = await fetch('/add-word', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ word: word })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById('message').innerHTML = 
                        '<div class="success">✅ ' + result.message + '</div>';
                    document.getElementById('wordInput').value = '';
                    loadStats();
                    loadWords();
                } else {
                    document.getElementById('message').innerHTML = 
                        '<div class="error">❌ ' + result.error + '</div>';
                }
            } catch (error) {
                document.getElementById('message').innerHTML = 
                    '<div class="error">❌ Fel vid kommunikation med databas</div>';
            }
        });
        
        async function loadStats() {
            try {
                const response = await fetch('/stats');
                const stats = await response.json();
                
                if (stats.message) {
                    document.getElementById('statsContent').innerHTML = stats.message;
                } else {
                    document.getElementById('statsContent').innerHTML = `
                        <p><strong>Totalt antal ord:</strong> ${stats.total_words}</p>
                        <p><strong>Totalt antal tecken:</strong> ${stats.total_characters}</p>
                        <p><strong>Genomsnittlig ordlängd:</strong> ${stats.average_length}</p>
                        <p><strong>Längsta ordet:</strong> "${stats.longest_word}" (${stats.longest_length} tecken)</p>
                    `;
                }
            } catch (error) {
                document.getElementById('statsContent').innerHTML = 'Fel vid laddning av statistik';
            }
        }
        
        async function loadWords() {
            try {
                const response = await fetch('/words');
                const data = await response.json();
                
                if (data.words.length === 0) {
                    document.getElementById('wordsContent').innerHTML = 'Inga ord ännu...';
                } else {
                    const wordsHtml = data.words.map(entry => 
                        `<div class="word-item"><strong>${entry.word}</strong> (${entry.length} tecken) - ${entry.timestamp.split('T')[1].split('.')[0]}</div>`
                    ).join('');
                    document.getElementById('wordsContent').innerHTML = wordsHtml;
                }
            } catch (error) {
                document.getElementById('wordsContent').innerHTML = 'Fel vid laddning av ord';
            }
        }
        
        // Uppdatera automatiskt var 5:e sekund
        setInterval(() => {
            loadStats();
            loadWords();
        }, 5000);
    </script>
</body>
</html>
"""

def wait_for_database():
    """Vänta tills databas-containern är tillgänglig"""
    print("🔍 Väntar på att Database Container ska starta...")
    
    for attempt in range(30):
        try:
            response = requests.get(f"{DATABASE_URL}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Database Container är redo!")
                return True
        except requests.exceptions.RequestException:
            print(f"   Försök {attempt + 1}/30...")
            time.sleep(1)
    
    print("❌ Kunde inte ansluta till Database Container")
    return False

@app.route('/')
def index():
    """Visa webbgränssnitt"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/add-word', methods=['POST'])
def add_word():
    """Lägg till ord via databas-containern"""
    try:
        data = request.json
        word = data.get('word', '').strip()
        
        if not word:
            return {"error": "Inget ord skickat"}, 400
        
        # Skicka till databas-container
        response = requests.post(f"{DATABASE_URL}/words", json={"word": word})
        
        if response.status_code == 200:
            result = response.json()
            return {"message": f"Ord '{word}' sparat! (Totalt: {result['total_words']} ord)"}
        else:
            return {"error": "Fel vid sparande i databas"}, 500
            
    except requests.exceptions.RequestException:
        return {"error": "Kan inte ansluta till databas"}, 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Hämta statistik från databas-containern"""
    try:
        response = requests.get(f"{DATABASE_URL}/stats")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Kan inte ansluta till databas"}, 500

@app.route('/words', methods=['GET'])
def get_words():
    """Hämta alla ord från databas-containern"""
    try:
        response = requests.get(f"{DATABASE_URL}/words")
        return response.json()
    except requests.exceptions.RequestException:
        return {"error": "Kan inte ansluta till databas"}, 500

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy", "service": "word-frontend"}

if __name__ == '__main__':
    print("=== Word Manager Frontend startar ===")
    print("Container 1: Frontend/Webbgränssnitt")
    print("Väntar på Database Container...")
    
    # Vänta på databas (valfritt för utveckling)
    # wait_for_database()
    
    print("Startar webbserver på http://localhost:5050")
    app.run(host='0.0.0.0', port=5050, debug=True)