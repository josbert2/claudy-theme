# Claudy Theme

Tema oscuro para VSCode con sintaxis cálida y acento violeta.

**Claudy Dark** toma el look de los IDE JetBrains —fondos profundos, resaltado de
sintaxis cálido, estética limpia— y lo rebrandea con el violeta de Claudy.

## Instalación

Desde el Marketplace: buscá **"Claudy Theme"**.

Manual (`.vsix`):

```
code --install-extension claudy-dark-0.1.0.vsix
```

Después, activá el tema: `Ctrl+K Ctrl+T` → elegí **Claudy Dark**.

## Paleta

| Elemento | Color |
|---|---|
| Fondo | `#18171e` |
| Texto | `#bcbec4` |
| Acento (UI) | `#8a6cf0` |
| Keywords | `#cf8e6d` |
| Strings | `#6aab73` |
| Funciones | `#5c9ef0` |
| Tipos / clases | `#c77dbb` |
| Números | `#2aacb8` |
| Comentarios | `#7a7e85` |

## Glass Mode (opcional)

Claudy Dark trae además un **modo glass**: paneles flotantes con esquinas
redondeadas, bordes de vidrio y sombras —el look de los IDE modernos.

Es **activable** y se apoya en la extensión
[Custom UI Style](https://marketplace.visualstudio.com/items?itemName=subframe7536.custom-ui-style),
que inyecta CSS en VSCode.

### Instalar

```
./glass/install-glass.sh
```

El script instala la extensión Custom UI Style. Después:

1. Abrí tu `settings.json` (Command Palette → *Preferences: Open User Settings (JSON)*).
2. Pegá adentro el contenido de [`glass/claudy-glass.jsonc`](glass/claudy-glass.jsonc).
3. Command Palette → **Custom UI Style: Enable** → recargá VSCode.

### Activar / desactivar

El glass se prende y apaga sin tocar nada más:

- **Apagar:** Command Palette → *Custom UI Style: Disable* → recargar.
- **Encender:** Command Palette → *Custom UI Style: Enable* → recargar.

> Custom UI Style parchea VSCode, así que vas a ver una advertencia de
> "instalación corrupta". Es esperado — descartala. Tras cada update de VSCode
> hay que volver a hacer *Enable*.

## Créditos

Claudy Dark deriva de [Islands Dark](https://github.com/bwya77/vscode-dark-islands)
de **bwya77** (licencia MIT), que a su vez se inspira en JetBrains Islands Dark.
La estructura del tema y la paleta de sintaxis cálida vienen de ahí; el acento
violeta y el tinte de fondo son propios de Claudy.

## Licencia

MIT — ver [LICENSE](LICENSE).
