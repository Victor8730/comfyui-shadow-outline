import numpy as np
from PIL import Image, ImageFilter
import torch


class ShadowOrOutlineFromAlpha:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mode": (["shadow", "outline"], {"default": "shadow"}),
                "threshold": ("INT", {"default": 10, "min": 0, "max": 255, "step": 1}),
                "outline_thickness": ("INT", {"default": 8, "min": 1, "max": 128, "step": 1}),
                "outline_feather": ("INT", {"default": 2, "min": 0, "max": 64, "step": 1}),
                "outline_r": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "outline_g": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "outline_b": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "outline_opacity": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "shadow_blur": ("INT", {"default": 18, "min": 0, "max": 128, "step": 1}),
                "shadow_expand": ("INT", {"default": 4, "min": 0, "max": 64, "step": 1}),
                "shadow_offset_x": ("INT", {"default": 0, "min": -512, "max": 512, "step": 1}),
                "shadow_offset_y": ("INT", {"default": 16, "min": -512, "max": 512, "step": 1}),
                "shadow_opacity": ("FLOAT", {"default": 0.28, "min": 0.0, "max": 1.0, "step": 0.01}),
                "shadow_r": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "shadow_g": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "shadow_b": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("effect_image", "effect_mask")
    FUNCTION = "make_effect"
    CATEGORY = "image/wps"

    @staticmethod
    def _tensor_to_rgba_pil(image_tensor):
        arr = image_tensor[0].cpu().numpy()
        arr = np.clip(arr, 0.0, 1.0)

        if arr.shape[-1] == 4:
            rgba = (arr * 255).astype(np.uint8)
            return Image.fromarray(rgba, mode="RGBA")

        rgb = (arr[:, :, :3] * 255).astype(np.uint8)
        alpha = np.full((rgb.shape[0], rgb.shape[1], 1), 255, dtype=np.uint8)
        rgba = np.concatenate([rgb, alpha], axis=2)
        return Image.fromarray(rgba, mode="RGBA")

    @staticmethod
    def _pil_rgba_to_tensor(img):
        arr = np.array(img).astype(np.float32) / 255.0
        return torch.from_numpy(arr)[None,]

    @staticmethod
    def _pil_l_to_mask_tensor(img):
        arr = np.array(img).astype(np.float32) / 255.0
        return torch.from_numpy(arr)[None,]

    @staticmethod
    def _apply_opacity(mask_img, opacity):
        alpha_np = np.array(mask_img).astype(np.float32)
        alpha_np = np.clip(alpha_np * float(opacity), 0, 255).astype(np.uint8)
        return Image.fromarray(alpha_np, mode="L")

    @staticmethod
    def _shift_mask(mask_img, offset_x, offset_y):
        shifted = Image.new("L", mask_img.size, 0)
        shifted.paste(mask_img, (int(offset_x), int(offset_y)))
        return shifted

    @staticmethod
    def _threshold_alpha(alpha, threshold):
        alpha_np = np.array(alpha).astype(np.uint8)
        alpha_np[alpha_np < int(threshold)] = 0
        return Image.fromarray(alpha_np, mode="L")

    def _make_outline_mask(self, alpha, thickness, feather):
        expanded = alpha.filter(ImageFilter.MaxFilter(size=thickness * 2 + 1))
        orig_np = np.array(alpha).astype(np.int16)
        exp_np = np.array(expanded).astype(np.int16)
        outline_np = np.clip(exp_np - orig_np, 0, 255).astype(np.uint8)
        outline = Image.fromarray(outline_np, mode="L")

        if feather > 0:
            outline = outline.filter(ImageFilter.GaussianBlur(radius=feather))

        return outline

    def _make_shadow_mask(self, alpha, expand, blur, offset_x, offset_y):
        if expand > 0:
            alpha = alpha.filter(ImageFilter.MaxFilter(size=expand * 2 + 1))

        if blur > 0:
            alpha = alpha.filter(ImageFilter.GaussianBlur(radius=blur))

        if offset_x != 0 or offset_y != 0:
            alpha = self._shift_mask(alpha, offset_x, offset_y)

        return alpha

    def make_effect(
        self,
        image,
        mode,
        threshold,
        outline_thickness,
        outline_feather,
        outline_r,
        outline_g,
        outline_b,
        outline_opacity,
        shadow_blur,
        shadow_expand,
        shadow_offset_x,
        shadow_offset_y,
        shadow_opacity,
        shadow_r,
        shadow_g,
        shadow_b,
    ):
        rgba = self._tensor_to_rgba_pil(image)
        alpha = rgba.getchannel("A")
        alpha = self._threshold_alpha(alpha, threshold)

        if mode == "outline":
            effect_mask = self._make_outline_mask(alpha, outline_thickness, outline_feather)
            effect_mask = self._apply_opacity(effect_mask, outline_opacity)
            color = (int(outline_r), int(outline_g), int(outline_b), 0)
        else:
            effect_mask = self._make_shadow_mask(
                alpha,
                shadow_expand,
                shadow_blur,
                shadow_offset_x,
                shadow_offset_y,
            )
            effect_mask = self._apply_opacity(effect_mask, shadow_opacity)
            color = (int(shadow_r), int(shadow_g), int(shadow_b), 0)

        effect_rgba = Image.new("RGBA", rgba.size, color)
        effect_rgba.putalpha(effect_mask)

        return (self._pil_rgba_to_tensor(effect_rgba), self._pil_l_to_mask_tensor(effect_mask))


NODE_CLASS_MAPPINGS = {
    "ShadowOrOutlineFromAlpha": ShadowOrOutlineFromAlpha,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShadowOrOutlineFromAlpha": "Shadow Or Outline From Alpha",
}