#!/usr/bin/env bash
# random-joke.sh – Säg ett slumpvalt skämt

# Definiera en array med 10 skämt
jokes=(
  "Varför kan inte cyklar stå upp själva? – De är två-hjuliga!"
  "Hur får man en fisk att skratta? – Man kittlar den under fenorna!"
  "Vad sa den ena väggen till den andra? – Vi ses på hörnet!"
  "Varför går spöken i skolan? – För att lära sig boo-kföring!"
  "Hur organiserar man ett utrymmefest? – Man planet-erar den!"
  "Varför är elefanter dåliga på datorer? – För många ‘ele-fel’!"
  "Varför kastade boken in handduken? – Den hade för många kapitel!"
  "Vad gör klockor i skolan? – De tickar av tiden!"
  "Hur håller man ett hav kallt? – Man använder en skumbox!"
  "Vad kallar man en kanin med en gaffel? – En hungrig hoppare!"
)

# Räkna antal skämt
count=${#jokes[@]}

# Välj ett slumpindex mellan 0 och count-1
index=$(( RANDOM % count ))

# Skriv ut skämtet
echo ""
echo "🎲 Dagens skämt: ${jokes[$index]}"
echo ""