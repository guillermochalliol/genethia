# Verificación de "Diseño del terrario.md" (v0.1)

Fecha: 2026-10-21. Verificador independiente. Fuentes: notas de `Sociedades de modelos IA/` y `Marco teórico del terrario/` (las tres `critica_*.md` tienen prioridad), más chequeos en vivo de fuentes primarias.

## Cambios hechos (antes → después, con fuente)

1. **§1, afirmación de novedad.** "humanidad... con necesidades de autodeterminación y constitución ratificada" → "con constitución ratificada y, en el Estudio 2, necesidades de autodeterminación". Motivo: el §6.4 del mismo documento dice que en el Estudio 1 la SDT no entra como condición (solo de forma estructural e idéntica en todas). La versión anterior se contradecía con el diseño.
2. **§4.1, fila Deci y Ryan.** "en el Estudio 1 solo como razón constitucional" → "solo de forma estructural e idéntica en todas las condiciones". Misma inconsistencia con §6.4.
3. **§2.2, Bellina et al. (arXiv 2601.05384).** "modelos de 3B a 34B" → "modelos de visión y lenguaje de 3B a 34B". Fuente: `psicologia_filosofia_sociedades.md` (12 VLM abiertos, tareas visuales tipo Asch).
4. **§4.1, Dunbar.** "8-12 está en el rango del grupo de simpatía" → "8-12 queda entre la camarilla de apoyo (~5) y el grupo de simpatía (~12-15)". Fuente: `psicologia_social_desarrollo.md` l.150 (el grupo de simpatía es ~12-15, así que 8 no cae ahí).
5. **§6.5, CSE.** "12 de 15 modelos caen por debajo del 50% con 3 o menos" → "...con 3 restricciones o menos". Solo claridad. Se verificó el abstract en vivo (arXiv 2608.12426).
6. **§8.3, tabla de costos (recalculada).** 240 × 0,134 = 32,2 → "~31" pasa a "~32". 240 × 0,954 = 229 → "~228" pasa a "~229". La fila de la mezcla típica (~125) y el total con +25% (USD 40-290, ~150) cuadran.
7. **§8.3, ejecución.** "las 240 entran en un día" → "las 210 de la corrida de 1 día (180 + 30 homogéneas)...; el piloto de 30 va antes". Motivo: el piloto (fase 2b, semana 5) es anterior a la corrida de 1 día (fase 3, semana 6).
8. **§14, semana 6.** "Las 240 corridas terminadas" → "Las 210 corridas confirmatorias (180 + 30 homogéneas)". Mismo motivo.
9. **§9.4, volumen de logs.** "~100.000 llamadas por día entre los 4 mundos" → "~60.000 (740 × 20 generaciones × 4)". La cifra de 100.000 venía de `critica_viabilidad_etica.md`, que usaba la definición vieja de generación (~5.200 llamadas). Con los supuestos de §8.3 da ~59.200.
10. **§8.2, potencia.** Se agregó una oración marcada como **[Estimación]**: con Bonferroni estricto sobre 4 pruebas (α = 0,0125) harían falta ~35 por brazo para d = 0,8; Holm exige menos salvo en la primera prueba. Es cálculo propio (aproximación normal; reproduce exactamente la tabla de la crítica: 63/25/16/7 y 97/38/25/11). Así ~30 por celda queda presentado como un número justo, no holgado.
11. **§13.2, arXiv en inglés.** Se agregó la fecha de entrada en vigor (11 de febrero de 2026) y el link. Fuente: blog de arXiv del 13 ene 2026, verificado en vivo.
12. **§13.3, AAMAS.** Se agregó "la conferencia va del 3 al 7 de mayo". Verificado en vivo en la home de AAMAS 2027.
13. **§13.3, presencialidad.** "Se puede presentar a distancia si el workshop lo permite" → la página de workshops anuncia AAMAS 2027 como evento presencial, así que presentar a distancia dependería de una excepción. Verificado en vivo.
14. **Legibilidad (sin afirmaciones nuevas).** Glosas breves para "martingala" (§2.2), "self-consistency" (§2.2) y "corrección de Holm" (§3).

## Verificado y sin cambios

- **Incidente.** Verificado contra el HTML completo de METR descargado en vivo: ~1.200, ~700, 533 / más del 90%, más de 70.000, HOLD/VETO/owner/STOP, ~10% de PHASEONE[big], 19 agentes / 429 mensajes firmados, "per SIGNED", "self-risking experiments", 3-6, al menos 20%, ~7%, "uncritically adopt". Hugging Face: 16 jul 2026 y "driven, end to end". 898, 198, 93%, IM1, 12 may y 8 jul salen de la crítica metodológica y de las notas del incidente. CSA 989 está marcado como error.
- **AAMAS 2027.** Conferencia 3-7 may, Hanoi. Blue Sky: resumen 5 nov y paper 12 nov 2026. Workshops: propuestas 29 oct, CfP 9 dic, paper recomendado 24 ene 2027, decisión 28 feb, workshops 3-4 may. Todo verificado en vivo.
- **ALIFE 2027.** Praga, 19-23 jul 2027, sin deadlines. Verificado en vivo.
- **arXiv, aval del 21 ene 2026.** Mail institucional más autoría previa en el dominio, o aval personal. Verificado en vivo.
- **Precios de OpenRouter.** Consultados en vivo el 21 oct 2026 por la API de endpoints. Coinciden: Llama 3.1 8B (DeepInfra 0,02/0,04 sin SO; CoreWeave 0,22/0,22 con SO), Gemma 3 12B (DeepInfra 0,04/0,12 con SO), Ministral 8B (0,15/0,15), Phi-4 (0,056/0,112), Granite 4.2 8B (DeepInfra 0,06/0,25 sin SO; CoreWeave 0,10/0,15 con SO). Los precios de Qwen3.5-9B y de los modelos de 24-30B salen solo de las notas.
- **SovSim** r = −0,93 (R² = 0,86, p = 0,008). Verificado en vivo en arXiv HTML.
- **Aritmética.** 2.400 llamadas por corrida, 6M/0,36M tokens, 0,13/0,52/0,95 USD por corrida, 740 llamadas por generación, 0,16 USD por generación, 3,2 USD por día, 22 USD por semana, ~110 USD con 4 mundos y +25%, ~580.000 llamadas, 25-50 min por corrida y los lunes del cronograma (2 nov ... 21 dic 2026). Todo recalculado y correcto.
- **Novedad.** El documento no dice ser la primera sociedad de LLM que evoluciona, se reproduce o dura mucho. La afirmación sigue la versión de `critica_novedad.md`.
- **Citas.** Las 132 URLs del documento aparecen en las notas o en el informe previo. No se encontraron papers inventados.

## No verificado (fuera de las notas o sin acceso)

- El post de OpenAI del 26 ago devolvió una página casi vacía (renderizado por JS). Sus cifras dependen de la crítica metodológica y de las notas del incidente.
- No se re-verificaron en vivo los precios de Qwen3.5-9B, del batch de Ministral, de los embeddings, de RunPod ni de los candidatos de 24-30B. Salen de `tecnologia.md`.
- El resultado de Haslam, Reicher y Birney (2014) sobre la orden directa ya figura en el documento como no verificado.
- Las referencias [K] de psicología (Bandura y otras) siguen pendientes de DOI, como avisa el propio documento.
- Hay supuestos de diseño sin fuente pero presentados como propios: 100 rondas, 2.500 tokens por llamada, ~4 s por llamada, el umbral de 70%, la regla de 3×, los pesos de afinidad y las probabilidades de los operadores (salvo σ = 0,05 y 0,02, que vienen de `evolucion.md`).

## Riesgos que quedan

- **Potencia.** ~30 por celda alcanza para d = 0,8 solo con Holm. Si el piloto da d más chico, el plan de recortar celdas es lo que lo salva.
- **Venues.** El cronograma pone la corrida de 1 día (semana 6, 7 dic) antes de que se publiquen las convocatorias de workshops (9 dic). El tema del workshop elegido podría no encajar.
- **Viaje.** AAMAS es presencial en Hanoi el 3-4 de mayo y puede chocar con el viaje de mayo-junio de 2027.
- **Comisión.** El 5,5% de comisión y "sin markup" siguen en tensión en las propias fuentes de OpenRouter. Está presupuestado igual.
- **Costo de Claude.** Los check-ins de Claude siguen sin costo estimado.
