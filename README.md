# ComfyUI Shadow/Outline Node

One node for ComfyUI that takes an `IMAGE` with alpha after background removal and returns either:
- shadow only
- outline only

## Install
1. Create this folder:
   `ComfyUI/custom_nodes/comfyui-shadow-outline`
2. Put these files into it:
   - `__init__.py`
   - `shadow_effect_node.py`
3. Restart ComfyUI

## Node location
`image/wps -> Shadow Or Outline From Alpha`

## Input
- `image` — PNG/IMAGE with alpha after rembg or any other background removal step

## Modes
- `shadow` — creates a separate shadow from the silhouette
- `outline` — creates a separate outline without the original subject

## General settings
- `threshold` — removes weak alpha noise before creating the effect

## Outline settings
- `outline_thickness` — outline thickness
- `outline_feather` — softens outline edges
- `outline_r/g/b` — outline color
- `outline_opacity` — outline opacity

## Shadow settings
- `shadow_blur` — shadow softness
- `shadow_expand` — silhouette expansion before blur
- `shadow_offset_x`, `shadow_offset_y` — shadow offset
- `shadow_opacity` — shadow opacity
- `shadow_r/g/b` — shadow color

## Recommended values

### For shadow
- `mode = shadow`
- `threshold = 10`
- `shadow_blur = 18`
- `shadow_expand = 4`
- `shadow_offset_x = 0`
- `shadow_offset_y = 16`
- `shadow_opacity = 0.28`
- `shadow_r/g/b = 0/0/0`

### For outline
- `mode = outline`
- `threshold = 10`
- `outline_thickness = 8`
- `outline_feather = 2`
- `outline_opacity = 1.0`
- `outline_r/g/b = 0/0/0`

## Important
This node expects the input image to already contain an alpha channel. If the image has no alpha channel, the effect will be generated from the full rectangular image area.

## Tips
- Increase `threshold` if rembg leaves faint edge noise.
- Increase `outline_feather` for softer sticker-like outlines.
- Increase `shadow_expand` for a wider shadow shape.
- Increase `shadow_blur` for a softer shadow.