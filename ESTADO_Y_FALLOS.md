# Estado y fallos pendientes

## Último reporte del usuario, después de v.4

- **Slime gigante:** el tamaño visual sigue sin ajustarse a su caja de colisión. NO resuelto.
- **Magma gigante:** ahora aparece, pero golpeó al jugador cuando parecía estar muy lejos. Posible desajuste visual/colisión/alcance; causa aún no demostrada.
- **Devastador:** se ven los cuernos, pero el torso sigue desubicado. NO resuelto.
- **Zombi gigante:** ahora se ven correctamente las texturas, pero no encaja visualmente con la colisión. El reporte anterior era muerte atribuida a un gigante no visible.
- **Araña abisal:** en v.3 parecía carecer de ojos. v.4 cambió el material a `spider`; aún no hay confirmación explícita del usuario sobre los ojos.
- **Comportamiento, solo registrar por ahora:** slime hace saltitos pequeños; zombi gigante tarda en subir un bloque y hace saltitos repetidos. El usuario pidió no abordar todavía este tema.

## Confirmado previamente en el móvil del usuario

Arranque, `/pd:status`, menú por mesa de trabajo agachado, administración, bloqueo de receta por día, cambio al día 40, cuatro espacios sellados, fabricación de Reliquia del Fin y desbloqueo al llevarla. Al soltarla vuelven los bloqueos y al recogerla desaparecen. Estado conservado al salir y entrar. Muerte permanente pasa a espectador. Conversión en supervivencia observada: 17 conversiones y 0 errores contados en una captura. El contador solo recoge excepciones que maneja el script; NO detecta todos los fallos visuales.

En v.2 el usuario confirmó que cerdos, pollos y ovejas adquirían aspecto normal tras unos segundos. No significa que todos los demás animales estén validados. Esqueletos disparaban, pero sin arco visible en v.0.1. v.1 añadió arco geométrico y apuntado; la sincronización con cada flecha sigue pendiente.

## Historial breve

- 0.1: implementación parcial; modelos genéricos y muchas limitaciones.
- v.1: arco geométrico y postura de apuntado en cinco variantes a distancia; etiquetas de versión visibles.
- v.2: modelos de siete animales comunes basados en referencias oficiales; correcciones de atlas y animaciones.
- v.3: intento de mejorar araña, slime, magma y devastador. Las pruebas reales demostraron que no bastó.
- v.4: materiales `magma_cube` y `spider`; torso/cuerno del devastador pasan de rotación por cubo a huesos hijos; slime/magma usan raíz fija [2,2.4,2] y retiran deformaciones; zombi cambia atlas 64x64 a 64x32; texturas de referencia incluidas. Los últimos reportes indican fallos de escala/posición persistentes.

## Datos relevantes para investigar

Definiciones BP actuales (no cambiarlas automáticamente):

| Entidad | collision_box ancho × alto | minecraft:scale |
|---|---:|---:|
| giga_slime | 3 × 3.6 | 3 |
| giga_magma | 3 × 3.6 | 3 |
| giant_zombie | 1.8 × 5.4 | 3 |
| ultra_ravager | 1.2 × 1.44 | 1.2 |
| abyssal_spider | 1.4 × 1.12 | 1.4 |

La v.4 calculó 8/16 × 3 × raíz [2,2.4,2] para producir 3 × 3.6 bloques en los cubos. **El usuario indica que el resultado real no coincide**. No reutilizar ese cálculo como prueba de éxito: investigar cómo se combinan material, animación, geometría, escala de cliente y escala de entidad en el motor.

Las texturas TGA de magma y araña usan alfa para efectos especiales: con `entity_alphatest`, magma quedaba oculto y los ojos de araña se descartaban. Los materiales de v.4 interpretan esos datos de otra manera. Slime usa `slime` interior y `entity_alphablend` exterior. Revisar también la jerarquía al aplicar animaciones a múltiples geometrías/controladores.

Modelo de devastador: atlas 128×128; torso/cuerno en huesos hijos con rotaciones negativas. Hace falta revisar posición/pivote/orientación reales, no solo que los nombres de huesos existan.

## Otros pendientes ya detectados

Equipo y postura de ataque de esqueleto infernal y emperador wither; postura del zombi gigante; animación precisa de cada disparo; correspondencia de todos los buffs con las clases y días del JAR. Animaciones de rugido/mordida y saltos no equivalentes al original. Variantes de color, esquilado y crianza de animales convertidos incompletas.

No hubo validación en PS5. No se dispone de Minecraft ejecutable en el entorno de desarrollo anterior. No hay logs de contenido del motor en este traspaso ni grabaciones. No confundir previsualizaciones geométricas offline con pruebas dentro del juego.

## Comandos de inspección

Con trucos, mundo de copia y creativo para evitar muertes durante inspección:

```
/gamemode creative
/summon permadeath:abyssal_spider ~ ~ ~8
/summon permadeath:giga_slime ~ ~ ~8
/summon permadeath:giga_magma ~ ~ ~8
/summon permadeath:ultra_ravager ~ ~ ~8
/summon permadeath:giant_zombie ~ ~ ~12
/pd:status
/pd:admin
```

Revivir mediante Administración → Revivir jugador conectado para borrar la marca persistente de muerte; cambiar solo el modo de juego no basta. El mundo de prueba estaba en día 40 pausado. Deathtrain puede seguir activo.
