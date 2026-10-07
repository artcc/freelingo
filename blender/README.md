# Lingu Lighting Preview

`lingu-lighting-preview.html` lets you preview the model and adjust its lighting locally, without changing the app or deploying anything.

## Open the preview

Install the frontend dependencies first (`frontend/node_modules`) and use a browser with WebGL support.

From the repository root, start a static server:

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000/blender/lingu-lighting-preview.html>. Stop the server with `Ctrl+C` in the terminal.

## Controls

- **Dark / Light** switches between FreeLingo's dark and light background colors.
- The sliders adjust hemisphere, key, and fill light intensity, as well as exposure.
- The color pickers change the light colors.
- Choose an animation from the menu and click **Play animation** to preview it.
- Click **Copy values** to copy the current lighting settings as formatted JSON.
- **Reset to app values** restores the lighting values currently used by the app.

Changes are temporary: they are not saved and do not affect production. The page loads `frontend/public/models/lingu.glb` and Three.js from `frontend/node_modules`.
