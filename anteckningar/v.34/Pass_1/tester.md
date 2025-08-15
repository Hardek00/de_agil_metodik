# Grundläggande Testing för Utvecklare

## Vad är tester och varför behöver vi dem?

**Ett test** är kod som verifierar att din andra kod fungerar som förväntat.

### Problemet utan tester:
```
Du skriver kod → Den verkar fungera → Du ändrar något → Något annat slutar fungera → 😱
```

### Lösningen med tester:
```
Du skriver kod → Du skriver tester → Testerna passerar → Du ändrar något → Testerna säger om något gick sönder → 😌
```

### Fördelar med tester:
- ✅ **Självförtroende** - Du vet att din kod fungerar
- ✅ **Snabbare utveckling** - Hittar buggar direkt, inte efter veckor
- ✅ **Bättre design** - Testbar kod är oftast bättre struktur
- ✅ **Dokumentation** - Tester visar hur koden ska användas

---

## Ditt första test

Låt oss börja med en enkel funktion och dess test.

### 1. Koden som ska testas (`calculator.py`):
```python
def add(a, b):
    """Adderar två tal"""
    return a + b

def subtract(a, b):
    """Subtraherar b från a"""
    return a - b

def multiply(a, b):
    """Multiplicerar två tal"""
    return a * b

def divide(a, b):
    """Dividerar a med b"""
    if b == 0:
        raise ValueError("Kan inte dividera med noll!")
    return a / b
```

### 2. Testerna (`test_calculator.py`):
```python
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    # Arrange (Förbered)
    a = 2
    b = 3
    
    # Act (Utför)
    result = add(a, b)
    
    # Assert (Kontrollera)
    assert result == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(4, 3) == 12

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    # Testar att rätt exception kastas
    with pytest.raises(ValueError, match="Kan inte dividera med noll!"):
        divide(10, 0)
```

### 3. Kör testerna:
```bash
# Installera pytest
pip install pytest

# Kör alla tester
pytest

# Kör med mer information
pytest -v

# Kör specifik testfil
pytest test_calculator.py
```

**Förväntad output:**
```
========================= test session starts =========================
collected 6 items

test_calculator.py::test_add PASSED                           [ 16%]
test_calculator.py::test_add_negative_numbers PASSED         [ 33%]
test_calculator.py::test_subtract PASSED                     [ 50%]
test_calculator.py::test_multiply PASSED                     [ 66%]
test_calculator.py::test_divide PASSED                       [ 83%]
test_calculator.py::test_divide_by_zero PASSED               [100%]

========================= 6 passed in 0.02s =========================
```

---

## Teststruktur: AAA-mönstret

Varje test bör följa **AAA**-mönstret:

### **Arrange** (Förbered)
```python
# Sätt upp data och objekt
user = User("Anna", 25)
expected_greeting = "Hej Anna!"
```

### **Act** (Utför)
```python
# Kör funktionen du vill testa
result = user.get_greeting()
```

### **Assert** (Kontrollera)
```python
# Verifiera att resultatet är korrekt
assert result == expected_greeting
```

**Komplett exempel:**
```python
def test_user_greeting():
    # Arrange
    user = User("Anna", 25)
    expected_greeting = "Hej Anna!"
    
    # Act
    result = user.get_greeting()
    
    # Assert
    assert result == expected_greeting
```

---

## Typer av tester

### 1. **Unit Tests** (Enhets-tester)
Testar **en enda funktion** i isolation.

```python
def test_calculate_area():
    # Testar bara area-funktionen
    assert calculate_area(5, 10) == 50
```

**Karakteristik:**
- Snabba (< 1ms per test)
- Testar en sak åt gången
- Inga externa beroenden (databaser, nätverk, filer)

### 2. **Integration Tests** (Integrations-tester)
Testar att **flera komponenter fungerar tillsammans**.

```python
def test_save_and_load_user():
    # Testar databas + användarlogik tillsammans
    user = User("Anna", 25)
    user_id = database.save_user(user)
    
    loaded_user = database.load_user(user_id)
    assert loaded_user.name == "Anna"
```

**Karakteristik:**
- Långsammare (sekunder per test)
- Testar kommunikation mellan delar
- Kan använda riktiga databaser, APIs, etc.

### 3. **End-to-End Tests** (E2E)
Testar **hela applikationen** från användarens perspektiv.

```python
def test_complete_user_registration():
    # Simulerar en användare som registrerar sig
    response = client.post('/register', data={
        'username': 'anna',
        'email': 'anna@example.com',
        'password': 'säkert123'
    })
    
    assert response.status_code == 201
    assert 'Välkommen Anna!' in response.text
```

---

## Vanliga pytest-assert metoder

```python
# Grundläggande jämförelser
assert result == expected_value          # Lika med
assert result != wrong_value            # Inte lika med
assert result > 0                       # Större än
assert result in [1, 2, 3]             # Finns i lista

# Sanningsvärden
assert is_valid                         # True
assert not is_invalid                   # False

# Typer
assert isinstance(result, str)          # Är en string
assert isinstance(result, int)          # Är ett heltal

# Exceptions
with pytest.raises(ValueError):         # Förväntar sig ValueError
    risky_function()

# Approximationer (för decimaler)
assert result == pytest.approx(3.14159, rel=1e-5)

# Listor och dictionaries
assert len(result_list) == 3
assert 'key' in result_dict
assert result_list[0] == expected_first_item
```

---

## Test-driven Development (TDD)

TDD är en utvecklingsmetod där du **skriver testet först**, sedan koden.

### TDD-cykeln: Red → Green → Refactor

#### 1. **Red**: Skriv ett test som misslyckas
```python
def test_user_can_withdraw_money():
    account = BankAccount(balance=100)
    account.withdraw(30)
    assert account.balance == 70
```
**Kör test:** ❌ FAIL (funktionen finns inte än)

#### 2. **Green**: Skriv minimal kod för att testet passerar
```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        self.balance -= amount  # Enklaste möjliga implementation
```
**Kör test:** ✅ PASS

#### 3. **Refactor**: Förbättra koden utan att ändra beteendet
```python
class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Belopp måste vara positivt")
        if amount > self.balance:
            raise ValueError("Otillräckligt saldo")
        self.balance -= amount
```
**Kör test:** ✅ PASS (fortfarande)

### Fördelar med TDD:
- Du skriver bara kod som behövs
- Koden blir automatiskt testbar
- Du tänker på design innan implementation
- 100% test coverage från start

---

## Testning i CI/CD

Kom ihåg hur vi integrerade tester i GitHub Actions? Här är varför det är så kraftfullt:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      run: |
        pytest tests/ -v --tb=short
```

**Vad händer:**
1. **Varje git push** → Tester körs automatiskt
2. **Tester misslyckas** → PR blockeras, ingen dålig kod kommer in
3. **Alla tester passerar** → Koden kan mergas säkert

**Real-world workflow:**
```
Utvecklare pushes kod → GitHub Actions kör tester → 
✅ Alla tester OK → Kod mergas → Deploy till produktion
❌ Tester misslyckas → Utvecklaren fixar → Repeat
```
