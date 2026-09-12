/* Dark film grain. Seamless tile drift — no frame-swap, no loop snap. */
(function (g) {
  function noiseURL(size, mid, spread) {
    const c = document.createElement("canvas");
    c.width = c.height = size;
    const ctx = c.getContext("2d");
    const img = ctx.createImageData(size, size);
    const d = img.data;
    for (let i = 0; i < d.length; i += 4) {
      const n = (Math.random() + Math.random()) * 0.5;
      const v = mid + (n - 0.5) * spread;
      d[i] = v + 3;
      d[i + 1] = v - 6;
      d[i + 2] = v + 8;
      d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    ctx.filter = "blur(1.1px)";
    ctx.drawImage(c, 0, 0);
    return c.toDataURL("image/png");
  }

  function mount(host) {
    if (!host) return { destroy: function () {} };
    let layer = host.querySelector(".grain-layer");
    if (!layer) {
      layer = document.createElement("div");
      layer.className = "grain-layer";
      layer.innerHTML = '<i class="grain-film"></i><i class="grain-dust"></i>';
      host.appendChild(layer);
    }
    const film = layer.querySelector(".grain-film");
    const dust = layer.querySelector(".grain-dust");
    if (film) film.style.backgroundImage = "url(" + noiseURL(512, 88, 22) + ")";
    if (dust) dust.style.backgroundImage = "url(" + noiseURL(384, 96, 16) + ")";
    return {
      destroy: function () {
        layer.remove();
      },
    };
  }

  g.UmbraGrain = { mount };
})(typeof window !== "undefined" ? window : globalThis);
