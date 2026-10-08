# Traspaso de Permadeath a Copilot

Estado al 8 de octubre de 2026. Base: v.4 de prueba, NO lista para una partida definitiva.

## Objetivo y restricciones del usuario

Adaptar el mod Fabric Java adjunto a Minecraft Bedrock **26.52**, priorizando una buena experiencia en móvil. PS5 conectada al móvil es un objetivo posterior. No se exige equivalencia perfecta con Java. Respetar los límites de simulación y aparición de Bedrock; sin mantener chunks cargados artificialmente.

Trabajar en tandas pequeñas: el usuario tiene pocos tokens. No pedirle que pruebe uno por uno todos los mobs; investigar primero los fallos compartidos. Usar español. No prometer trabajo en segundo plano.

Modificar únicamente mobs y mecánicas contemplados explícitamente por el Java original. No extender buffs, estadísticas ni comportamientos a contenido ajeno o posterior. No inferir que todo mob hostil debe recibir mejoras. Las fechas/versiones mencionadas no sustituyen inspeccionar el JAR para decidir qué toca.

El usuario pidió registrar los problemas de salto, pero **no arreglar el comportamiento ahora**. Prioridad inmediata: renderizado, torso desubicado, visibilidad y correspondencia entre modelo y colisión. Antes de cambiar la colisión física, determinar qué tamaño exige el original y explicar el cambio.

## Contenido

- `originales/`: los dos archivos adjuntos conservados byte por byte.
- `pack/Permadeath_BP`, `pack/Permadeath_RP`: fuentes extraídas directamente del `.mcaddon` adjunto, no reconstruidas desde una versión anterior.
- `ESTADO_Y_FALLOS.md`: resultados reales y pendientes.
- `PROMPT_PARA_COPILOT.txt`: texto para iniciar la continuación.
- `work/`: pruebas con API simulada y validación estática heredadas. No arrancan Minecraft.
- `referencia/bytecode/`: desensamblado anterior de clases Java, ayuda de consulta. Verificar contra el JAR adjunto antes de tratarlo como autoridad.
- `empaquetar.py`: crea un `.mcaddon` con el contenido actual de `pack/` sin modificar archivos ni versiones.
- `SHA256_originales.json`: huellas de los archivos originales.

## Cómo continuar

1. Abrir esta carpeta en VS Code con GitHub Copilot; leer este archivo y el estado.
2. Inspeccionar materiales, texturas, atlas, jerarquías y transformaciones de huesos, escalas y cajas de colisión. Distinguir hipótesis de causas confirmadas.
3. Preparar una corrección acotada y verificar el paquete. La siguiente entrega debe mostrar **v.5** en comportamiento, recursos, menú, mensaje inicial y `/pd:status`.
4. Mantener los UUID de los manifiestos: no perder las propiedades guardadas de mundos existentes. Subir versiones de cabecera, módulos y dependencia UUID del RP de forma consistente. No subir por error versiones de módulos API.
5. No declarar resuelto un fallo visual por pasar pruebas de sintaxis. Se necesita confirmar en Minecraft Bedrock 26.52.

## Arquitectura

BP: `scripts/main.js` gestiona reloj, eventos, forja, inventario, conversión y expedición. `rules.js` contiene fórmulas y recetas; `islands.js` contiene estructuras. RP: `entity/`, `models/entity/`, `animations/`, `render_controllers/`, `textures/`.

API declarada: `@minecraft/server` 2.10.0, `@minecraft/server-ui` 2.0.0. Manifest min_engine_version [1,26,50]; el usuario prueba en 26.52. La v.4 usa [4,0,0] en las versiones de los paquetes. Mantener APIs estables y evitar experimentos sin motivo verificado.

Conversión de mobs solo cerca de un jugador vivo en supervivencia o aventura. Radio predeterminado 44; opción 96. Cola máxima 192 y procesamiento de hasta 8 entidades por tick. Las invocaciones directas de entidades personalizadas sí permiten inspección en creativo. Pausar el día NO pausa conversiones, IA ni Deathtrain.

Persistencia principal: `pd:state_v1`, más propiedades de jugador y entidad. La adaptación empieza en día 0 y usa bloques de 24 h reales por defecto, incluido el tiempo cerrado; opción tiempo jugado y pausa. El Java analizado usa fecha de calendario, empieza en día 1 y tiene modo speedrun: no afirmar identidad exacta.

Hay 19 entidades personalizadas y 24 piezas de armadura. La adaptación es parcial: Beginning se representa en una zona apartada del End; no es una dimensión nueva equivalente a Java. Muchos sistemas originales, botines, IA y fases siguen incompletos. No presentar v.4 como port completo.

## Verificación local

Desde esta carpeta:

```
python3 work/validate.py
node work/test.mjs
node work/check_exclusions.mjs
python3 empaquetar.py --salida dist/Permadeath_Bedrock_26.52_v.5.mcaddon
```

Python 3 con Pillow para validar imágenes; Node.js para las pruebas. `test.mjs` genera `work/runtime-test.mjs`; ejecutar ese test antes de `check_exclusions.mjs`.

Las 15 pruebas heredadas verifican lógica con mocks; los 70 casos de exclusión cubren siete identificadores en diez días, con Deathtrain. No certifican motor, renderizado, física, IA real ni equivalencia con Java. El identificador `unknown_future_mob` es sintético. Esas exclusiones no demuestran que los mobs restantes estén correctamente tratados según el original.

Los LEEME_v1…v4 dentro del BP documentan INTENCIONES e hipótesis de cada versión. El reporte más reciente del usuario en ESTADO_Y_FALLOS.md prevalece sobre cualquier texto anterior que diga «corregido».
