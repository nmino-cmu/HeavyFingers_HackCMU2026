/* Static dark-purple grain. Fixed texture — no drift, no white specks. */
(function (g) {
  function noiseURL(size) {
    const c = document.createElement("canvas");
    c.width = c.height = size;
    const ctx = c.getContext("2d");
    const img = ctx.createImageData(size, size);
    const d = img.data;
    for (let i = 0; i < d.length; i += 4) {
      const n = (Math.random() + Math.random()) * 0.5;
      d[i] = 12 + n * 38;
      d[i + 1] = 4 + n * 24;
      d[i + 2] = 24 + n * 46;
      d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    ctx.filter = "blur(0.8px)";
    ctx.drawImage(c, 0, 0);
    return c.toDataURL("image/png");
  }

  function mount(host) {
    if (!host) return { destroy: function () {} };
    let layer = host.querySelector(".grain-layer");
    if (!layer) {
      layer = document.createElement("div");
      layer.className = "grain-layer";
      layer.innerHTML = '<i class="grain-film"></i>';
      host.appendChild(layer);
    }
    const film = layer.querySelector(".grain-film");
    if (film) film.style.backgroundImage = "url(" + noiseURL(512) + ")";
    return {
      destroy: function () {
        layer.remove();
      },
    };
  }

  g.UmbraGrain = { mount };
})(typeof window !== "undefined" ? window : globalThis);
