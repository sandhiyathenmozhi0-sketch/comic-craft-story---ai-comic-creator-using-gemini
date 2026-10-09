def build_comic_layout(outline: list[dict], image_paths: list[str]) -> list[dict]:
    layout = []
    for index, panel in enumerate(outline):
        layout.append({
            "panel_number": panel.get("panel_number", index + 1),
            "title": panel.get("title", f"Panel {index + 1}"),
            "scene_description": panel.get("scene_description", ""),
            "image_prompt": panel.get("image_prompt", ""),
            "caption": panel.get("caption", ""),
            "narration": panel.get("narration", ""),
            "dialogue": panel.get("dialogue", ""),
            "image_path": image_paths[index] if index < len(image_paths) else "",
        })
    return layout
