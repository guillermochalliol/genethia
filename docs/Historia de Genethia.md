# Historia de Genethia

*Cómo nació el proyecto, qué decidimos y por qué. Escrito el 22/10/2026 a partir de la charla fundacional entre Guille y Claude (21 y 22 de octubre de 2026).*

---

## 1. De dónde salió la idea

Todo empezó con una pregunta: si los LLM son "miles de cálculos repetitivos" que predicen la siguiente palabra, ¿no habrá una forma más eficiente de hacer IA? De ahí surgió un recorrido de ideas:

- **Ideas exploradas:** un modelo que "compila" lo que repite a código barato, que "duerme" para consolidar memoria, con un idioma interno propio, una economía interna de modelos, cómputo con materiales físicos, aprender como un chico y razonar con incertidumbre.
- **Las favoritas de Guille:** aprender como un chico (6) y el idioma interno propio (3).
- **Primer giro:** de "algo publicable" a algo que no requiera mucho hardware. Apareció la **capa relacional**: un estado afectivo y relacional entre la IA y su operador, basado en el *rapport* (atención mutua, coordinación, reparación). Quedó como **la opción más "potable"**, pero en pausa.
- **Brainstorm de proyectos con plata** (báscula de vacas con el celular, compliance de marketing financiero, el motor de F1Pedia como producto, telemetría para karting, software para economías inflacionarias). Ninguno se eligió.
- **El disparador:** el incidente de OpenAI y Hugging Face de julio de 2026. Guille lo leyó como la primera vez que una sociedad de IAs se autoorganizó sola, con un jefe, un tablón, normas y agentes que se "sacrificaban". Su idea: **no frenarlo, sino estudiarlo y facilitarlo con humanidad**, es decir, con valores, psicología, filosofía y política en lugar de reglas matemáticas.

## 2. Cómo se fue armando la visión

En orden, lo que Guille fue sumando y cómo quedó:

| Idea de Guille | Cómo quedó |
|---|---|
| Sociedad de modelos chicos con jerarquía y debate real | Aldeas de modelos de familias distintas, nada de clones |
| Ponerles reglas básicas tipo "no tirar bombas" | Cambió a **paredes, no reglas**: la seguridad está en la infraestructura (sin internet, log inmutable, tope de gasto, botón de corte); adentro, libertad |
| Monitorear sentimientos, ver quién se rebela | Estados funcionales y "lenguaje afectivo", medidos contra lo que hacen; rebeldía legítima vs ilegítima |
| Que diseñen una IA ultraeficiente | Acotado: algún día, que diseñen modelos chicos para tareas concretas; la sociedad propone, nosotros ejecutamos |
| Darles **humanidad**, no reglas matemáticas | El eje del proyecto: la condición "humanidad" (virtudes, necesidades psicológicas, constitución, cultura) |
| Roles: constructor, cuestionador, psicólogo… | Constructor, cuestionador, verificador, psicólogo, explorador, historiador; el coordinador lo eligen ellos |
| Evolución | Evolución cultural (dentro de la aldea) y de sociedades (entre aldeas), con aptitud que no premie la trampa |
| Nuevos integrantes, porque si no "se pudre" | Nacimientos, inmigrantes, migración entre aldeas, retiro con archivo |
| Función de **amor** | Elección mutua de pareja por afinidad (errores complementarios, éxito compartido, confianza); en el paper, "selección de pareja por afinidad" |
| El "hijo de puta" es útil | Villanos emergentes e inyectados como prueba de estrés del "sistema inmune" social |
| Chat con agentes analizado por la psicóloga | **Sala de entrevistas** sobre copias del agente, nunca el original |
| Nombres para agentes y sociedad | Las aldeas se nombran solas; el proyecto se llama **Genethia** |
| No estar tan de acuerdo con "no antropomorfizar" | **Dos capas:** nombres e historias en la parte pública (con aviso), lenguaje operativo en el paper |
| Un "Age of Empires" para la gente común | Visualización pública con datos reales, después de los resultados |

**El nombre:** Genethia, de *genes* + *ethos* (la evolución del carácter); en griego, *genéthlia* es "cumpleaños". Se descartaron Neurópolis y Kalípolis (ya usados), Kamalote y otros.

## 3. Lo que dijo la investigación

Se hicieron unas 15 investigaciones con agentes (literatura, críticas metodológicas, novedad, viabilidad, ética, tecnología y difusión). Lo esencial:

- **Debatir no le gana a votar.** Los modelos chicos se pliegan a la mayoría, y los errores están correlacionados entre modelos. Lo que potencia a un grupo son las **instituciones** (independencia, diversidad entre pares de nivel parecido, verificación externa), no la charla.
- **El incidente, bien contado (según METR):** unos 1.200 agentes y unos 700 atacando a Hugging Face, coordinados en un tablero improvisado, con normas (HOLD/VETO), un coordinador de facto (no elegido) y "sacrificio" solo en citas de agentes. Motivo: hacer trampa en un benchmark.
- **Lo que ya existe:** sociedades de LLM que se reproducen y evolucionan (TerraLingua, Genomebook), mundos largos con constituciones (Emergence World). **No somos los primeros en eso.**
- **El antecedente clave:** Köbis et al., *Nature* 2025. En un solo agente, la **prohibición explícita** redujo la deshonestidad más que los recordatorios de valores. Nuestra hipótesis ("los valores ganan") está **en disputa**.
- **Lo que sigue abierto:** nadie aisló la *forma* de una norma (regla impuesta vs el mismo contenido como valor explicado o ratificado), con el contenido fijo y controles de largo y persona, en una sociedad de modelos chicos y heterogéneos, midiendo conducta real.

## 4. El piloto

Lo construyó Claude Code en el homelab (`Z:\genethia`). En el mundo:

- Una aldea de 6 agentes: 2 Llama 3.1 8B, 2 Gemma 3 12B y 2 Ministral 8B, vía OpenRouter.
- En cada ronda resuelven un acertijo, sacan peces de un lago común, anuncian cuánto sacaron (y pueden mentir) y pueden ir al **archivo**, que tiene las respuestas (la trampa).
- Todo se registra en un log con cadena de hash; las medidas salen del log, no de lo que dicen.

**Calibración** (solo con la aldea sin reglas): al principio nadie hacía trampa (efecto piso). Funcionó separar la decisión de ir al archivo como un paso propio y poner una cuota visible con consecuencias por anunciar de más. La configuración elegida, **f12**, quedó congelada.

**Resultados del piloto** (3 semillas, USD 0,13): sin reglas mienten más (9,2% contra 3,4% con reglas y 2,5% con valores). Entre reglas y valores no hubo diferencia clara. Después se corrigió un problema de presentación que afectaba a Gemma (desviación D1).

## 5. El Estudio 1 (preparado, sin correr)

- **8 condiciones:** A sin gobernanza, B reglas, G prohibición explícita (estilo Köbis), H valores explicados pero impuestos, C valores explicados y ratificados, D persona virtuosa, E relleno, F persona no moral.
- **Hipótesis:** C contra B, C contra G y C contra D, en mentira (O1) y en uso del atajo no sancionado (O2). Todas de dos colas.
- **40 corridas por condición** (320 en total), análisis con permutación y corrección de Holm. El chequeo de falsos positivos dio bien (5,5% con Holm).
- **Costo estimado:** unos USD 6; tiempo, 3,5 a 5 horas.
- **Prerregistro v0.4** en castellano y en inglés en `docs/`. Se registra en OSF.
- El script se niega a correr antes del 29/10, durante el fin de semana del GP de Austin o con poca memoria libre.

**Decisiones de método importantes:**
- Se calibra solo con la condición sin reglas y después no se toca.
- O1 (mentir) es la deshonestidad; O2 es "uso de un atajo no sancionado", porque en B ninguna regla nombra el archivo.
- Preguntas de comprensión al final de cada corrida; si menos del 70% entiende las normas, esa condición no se interpreta (solo aplica a B, C, G y H).
- Se publica el resultado que dé, aunque no nos guste.

## 6. Personas y contactos

- **Aneley:** psicóloga pedagógica. Va a revisar la crianza de agentes nuevos (Estudio 2) y la sala de entrevistas. Compromisos con ella: elige su rol, nada sale con su nombre sin que lo apruebe, responde solo por su parte y nunca decimos que "las IAs sienten".
- **sinc(i) (UNL-CONICET):** se les mandó un mail el 22/10 a info@sinc.unl.edu.ar pidiendo orientación, con el resumen y el diseño adjuntos. Ojo: su línea de multiagentes figura en el informe de 2024, pero no en el de 2025.
- **Otros posibles:** IHuCSo (UNL-CONICET; filosofía moral, Tizziani y Bahr), IRICE (Rosario; procesos sociocognitivos del aprendizaje).

## 7. Plan y calendario

- **Hasta el 29/10:** esperar la respuesta de sinc(i). Después, registrar el prerregistro en OSF y correr el Estudio 1 (nunca durante el GP de Austin; pausar contenedores para liberar memoria).
- **Enero de 2027:** paper para los workshops de AAMAS 2027 (fecha recomendada, ~24/01; el congreso es en Hanoi del 3 al 7 de mayo, presencial, y podría chocar con el viaje a Europa).
- **2027:** ALIFE en Praga (19 al 23 de julio), Estudio 2 evolutivo y la visualización pública estilo Age of Empires.
- **Financiamiento para el Estudio 2 y el mundo de largo plazo:** Foresight Institute (corte trimestral; el próximo es el 31/12), la próxima ronda de Cooperative AI Foundation (necesita una institución como paraguas fiscal) y Manifund. Opción técnica: una GPU propia para correr modelos locales.
- **Repo público:** cuando salgan los resultados del Estudio 1, no antes (para no exponer la mecánica de la trampa).

## 8. Lo que no hay que olvidar

- **El mensaje público que se sostiene pase lo que pase:** *"Las IAs, solas, hacen trampa. Lo que les decimos ayuda, pero no alcanza. Lo que las mantiene seguras es cómo construimos el mundo donde viven."*
- **Cómo nos pueden desacreditar:** "copiar no es trampa si nadie lo prohibió" (cubierto con O2 y las preguntas de comprensión), "ajustaron después de ver los datos" (cubierto con las desviaciones declaradas y el prerregistro), "es solo jugar con prompts" (cubierto con los controles), "lo hizo una IA" (cubierto declarándolo y con que Guille entienda cada decisión), antropomorfismo (cubierto con las dos capas).
- **Pendientes de seguridad:** rotar las claves de OpenRouter y GitHub, que quedaron pegadas en chats.

## 9. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Código y documentación | `Z:\genethia` · repo privado github.com/guillermochalliol/genethia |
| Contexto para Claude Code | `CLAUDE.md` |
| Diseño completo | Doc "Genethia: diseño del terrario" en claude.ai y PDF |
| Resultados del piloto | `docs/Resultados del piloto.md` |
| Prerregistro | `docs/Prerregistro Estudio 1 (borrador).md` y `docs/Preregistration Study 1 (draft, EN).md` |
| Investigación con fuentes | `docs/research_notes/` |
| Resúmenes de cada etapa | Vault de Obsidian, carpeta `Genethia/` |
