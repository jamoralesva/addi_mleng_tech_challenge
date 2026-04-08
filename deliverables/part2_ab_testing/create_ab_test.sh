#!/bin/bash

# Configuración de la URL (puedes cambiar localhost o el puerto aquí)
API_URL="http://localhost:1348/experiment"

# Definición del payload JSON
# Usamos un 'heredoc' para manejar las comillas internas sin problemas
JSON_PAYLOAD=$(cat <<EOF
{
  "name": "Metaprompting for bounce rate improvement",
  "hypothesis": "If we apply a metaprompting layer to the bot's initial prompt, then we will reduce the bounce rate of interactions by 10%, because metaprompting optimizes the structure of instructions, reduces hallucinations, and improves the model's adherence to system constraints.",
  "description": "Testing new initial prompt vs the baseline.",
  "variants": [
    { 
      "name": "control", 
      "control": true, 
      "traffic": 0.5,
      "config": { "prompt": "base_line" }
    },
    { 
      "name": "test", 
      "control": false, 
      "traffic": 0.5,
      "config": { "prompt": "test" }
    }
  ]
}
EOF
)

echo "Enviando configuración de experimento a: $API_URL..."

# Ejecución de CURL
# -s: Silent (no muestra barra de progreso)
# -w: Muestra el código de estado HTTP al final
response=$(curl -s -w "\nHTTP Status: %{http_code}\n" -X POST "$API_URL" \
     -H "Content-Type: application/json" \
     -d "$JSON_PAYLOAD")

echo "Respuesta del servidor:"
echo "$response"