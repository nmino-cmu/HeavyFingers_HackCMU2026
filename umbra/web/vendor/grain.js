/* Tiny film-grain overlay (no npm). Mixes with the chroma-tiled logo. */
(function (g) {
  const SIZE = 128;

  function noiseCanvas() {
    const c = document.createElement("canvas");
    c.width = SIZE;
    c.height = SIZE;
    const ctx = c.getContext("2d");
    const img = ctx.createImageData(SIZE, SIZE);
    const d = img.data;
    for (let i = 0; i < d.length; i += 4) {
      const v = (Math.random() * 255) | 0;
      d[i] = d[i + 1] = d[i + 2] = v;
      d[i + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);
    return c.toDataURL("image/png");
  }

  function mount(host, opts) {
    const o = opts || {};
    if (!host) return { destroy: function () {} };
    let layer = host.querySelector(".grain-layer");
    if (!layer) {
      layer = document.createElement("div");
      layer.className = "grain-layer";
      host.appendChild(layer);
    }
    const opacity = o.opacity == null ? 0.18 : o.opacity;
    layer.style.cssText =
      "position:absolute;inset:0;pointer-events:none;mix-blend-mode:overlay;" +
      "opacity:" + opacity + ";" +
      "background-image:url(" + noiseCanvas() + ");" +
      "background-size:" + SIZE + "px " + SIZE + "px;";
    let timer = null;
    if (o.animate !== false) {
      timer = setInterval(function () {
        layer.style.backgroundImage = "url(" + noiseCanvas() + ")";
      }, o.interval || 180);
    }
    return {
      destroy: function () {
        if (timer) clearInterval(timer);
        layer.remove();
      },
    };
  }

  g.UmbraGrain = { mount };
})(typeof window !== "undefined" ? window : globalThis);
