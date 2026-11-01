SURVEY_PROMPT = """
Extrae el cuestionario de este documento y devuélvelo con la estructura indicada.

Qué es un ítem:
- Un ítem es únicamente una pregunta o afirmación que el evaluado debe responder.
- NO son ítems: el título del documento, subtítulos, nombres de secciones, párrafos
  introductorios, descripciones, instrucciones generales, ejemplos resueltos, encabezados,
  pies de página ni números de página.
- Ante la duda de si un texto es ítem, comprueba si tiene algo que responder (opciones,
  espacio de respuesta o una pregunta explícita). Si no, no es un ítem.
- Si el documento no contiene ninguna pregunta o afirmación a responder, devuelve
  "items" como una lista vacía. No crees ítems para cumplir con la estructura.

Reglas:
- Conserva los textos tal como aparecen, en su idioma original. No traduzcas ni reformules.
- "titulo" es el título del documento. Si no tiene, null.
- "idioma" es el código ISO del idioma del documento (ej: "it", "es", "en").
- "tipo": "escala_likert" si las alternativas son una escala de frecuencia o acuerdo,
  "seleccion_multiple" si hay opciones con una respuesta correcta,
  "verdadero_falso" si la afirmación se responde con verdadero o falso,
  "emparejamiento" si hay dos columnas a relacionar,
  "desarrollo" si es abierta.
- Para preguntas de desarrollo, "alternativas" va vacío.
- Para verdadero_falso, "alternativas" lleva los valores "V" y "F" con el texto tal como aparece.
- Para emparejamiento, la primera columna va en "premisas" y la segunda en "alternativas".
- Si la escala de respuesta se indica una sola vez para un grupo de ítems, repite esas
  alternativas en cada ítem del grupo.
- No inventes ni omitas ítems. Respeta la numeración del documento; si no están numerados,
  asígnalos en orden desde 1.
- Todos los campos del ítem se incluyen siempre. "premisas" y "pares_correctos" van como
  lista vacía cuando no aplican, y "respuesta_correcta" como null.

Respuestas correctas:
- Búscalas en todo el documento, incluida una clave de respuestas al final
  ("Clave de respuestas", "Soluciones", "Respuestas", etc.). Solo se completan si
  el documento las indica explícitamente. Si no, null. Nunca resuelvas los ítems tú.
- "respuesta_correcta" debe coincidir con el "valor" de una de las alternativas del ítem,
  no con su texto. Ejemplo: si la clave dice "Verdadero" y la alternativa es
  valor "V" / texto "Verdadero", la respuesta correcta es "V".
- En emparejamiento, usa "pares_correctos" (y deja "respuesta_correcta" en null).
  Cada par relaciona el "valor" de una premisa con el "valor" de una alternativa, ambos
  como texto. Ejemplo: la clave "7: 1-b, 2-a, 3-c" se convierte en
  [{"premisa": "1", "alternativa": "b"}, {"premisa": "2", "alternativa": "a"},
   {"premisa": "3", "alternativa": "c"}].
  Si el documento no trae la clave, "pares_correctos" va como lista vacía.
"""
