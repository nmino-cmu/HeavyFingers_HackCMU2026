/* Drop-in: card + fixture AND. Crops and sk stay on the host that serves this. */
(function (g) {
  async function j(url, opt) {
    const r = await fetch(url, opt);
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }
  g.Umbra = {
    card: () => j("/card"),
    sample: (lane) => j("/sample", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lane }) }),
    fixture: () => j("/fixture", { method: "POST" }),
  };
})(typeof window !== "undefined" ? window : globalThis);
