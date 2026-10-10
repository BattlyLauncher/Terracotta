# Terracotta para BattlyWorlds

Terracotta, copyright burningtnt, se distribuye bajo AGPL-3.0; véase `LICENSE`.
La distribución Windows es `0.4.2-battly.2`; Linux conserva `0.4.2-battly.1`, basada en el commit
`74364326038f9a33306777a56ed9bb6664799a1d` de
https://github.com/burningtnt/Terracotta (la misma base que Battly para Android).

Las fuentes parcheadas están en https://github.com/BattlyLauncher/Terracotta.
La release `v0.4.2-battly.2` contiene `terracotta-battly.exe`, su manifiesto SHA-256,
la licencia y el parche de Battly. GitHub ofrece el archivo de fuentes de este tag.
El launcher ya no distribuye un ZIP de fuentes; conserva la licencia y la referencia
al repositorio público. `README.upstream.md` conserva la documentación original.

Cambios de Battly:

- Permitir el relé de EasyTier cuando P2P no funciona, igual que el parche de Android.
- Mantener Scaffolding y `NoTun`: no instalar una VPN ni modificar rutas del sistema.
- Mostrar «BattlyWorlds - pulsa para entrar» en el anuncio LAN.
- Aislar bloqueo, procesos temporales y registros mediante `BATTLY_TERRACOTTA_ROOT`.
- En Windows, conservar EasyTier bajo `BATTLY_EASYTIER_DIR` entre sesiones. Sus
  archivos se comparan con los bytes del archivo integrado antes de reutilizarlos;
  los archivos correctos no se reescriben ni se eliminan al salir. La ruta estable
  evita generar una nueva identidad de ejecutable para el firewall en cada sala.
- Vincular la API a 127.0.0.1 y exigir el secreto de proceso
  `BATTLY_TERRACOTTA_SECRET` en la cabecera `X-Battly-Terracotta`.

El ejecutable incluye EasyTier `v2.5.0-terracotta.2`, descargado por el build
original desde https://github.com/burningtnt/EasyTier. Se ejecuta como proceso
independiente; el token de la cuenta Battly no se entrega a Terracotta.

La distribución contiene Windows x86_64 y Linux x86_64 (musl estático en
`linux-x64/`). Cada binario se verifica contra el `manifest.json` de su carpeta.
Linux usa `--hmcl`, Windows `--hmcl2`. macOS no está incluido.

## Reconstruir

Desde el proyecto, ejecutar `powershell -File scripts/build-terracotta.ps1`.
Requiere Rust nightly, MSVC y Windows SDK, además de acceso a las dependencias de
Cargo y a la versión fijada de EasyTier. La versión del compilador utilizada
para este binario se registra en `manifest.json`.

En Linux: instalar Rust nightly-2026-08-18, el target
`x86_64-unknown-linux-musl`, musl-tools y unzip; ejecutar
`sh scripts/build-terracotta-linux.sh`. Conserva las mismas fuentes y licencia.
