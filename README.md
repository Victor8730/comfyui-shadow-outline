# ComfyUI Shadow/Outline Node

One node for ComfyUI that takes `IMAGE` with alpha after remove background / rembg
and returns separately or:
- shadow only
- stroke only

## Install
1. Create folder:
   `ComfyUI/custom_nodes/comfyui-shadow-outline`
2. Put the files there:
   - `__init__.py`
   - `shadow_effect_node.py`
3. reboot ComfyUI

## Where to look for a node
`image/wps -> Shadow Or Outline From Alpha`

## Enter
- `image` — PNG/IMAGE with alpha after rembg

## Type
- `shadow` — builds a separate shadow from the silhouette
- `outline` — builds a separate stroke without the animal itself

## Settings outline
- `outline_thickness` — outline thickness
  - `outline_r/g/b` — outline color
- `outline_opacity` — outline transparency

## Settings shadow
- `shadow_blur` — shadow blur
- `shadow_expand` — silhouette expansion before blur
- `shadow_offset_x`, `shadow_offset_y` — shadow shift
- `shadow_opacity` — shadow transparency
- `shadow_r/g/b` — shadow color

## Recommended values
### For shadow
- `mode = shadow`
- `shadow_blur = 18`
- `shadow_expand = 4`
- `shadow_offset_x = 0`
- `shadow_offset_y = 16`
- `shadow_opacity = 0.28`
- `shadow_r/g/b = 0/0/0`

### For outline
- `mode = outline`
- `outline_thickness = 8`
- `outline_opacity = 1.0`
- `outline_r/g/b = 0/0/0`

## Important
This node expects that the input already has an alpha channel. If the image has no alpha, the effect will be built from the entire rectangle.
