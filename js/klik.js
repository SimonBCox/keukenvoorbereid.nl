/* Klikken op bellen, mailen en WhatsApp tellen, met de pagina erbij.

   GoatCounter telt een klik op een link met data-goatcounter-click, maar zet
   als verwijzer de site waar de bezoeker vandaan kwam en niet de pagina waarop
   hij klikte. Dit script zet die pagina erbij. Een link zonder naam (een
   telefoonnummer in een lopende tekst) krijgt hier een naam naar de plek waar
   hij staat: wa-kop, bel-voet, mail-contact of wa-tekst. Zo hoeft niet elke
   link met de hand een naam te krijgen.

   Zelfde bestand op coxadvies.nl (in tellen.js), draagmuurkoning.nl en
   keukenvoorbereid.nl. Zet geen cookies en bewaart niets. */
(function () {
  function soort(h) {
    if (h.indexOf("tel:") === 0) return "bel";
    if (h.indexOf("mailto:") === 0) return "mail";
    if (/wa\.me\/|whatsapp\.com\//.test(h)) return "wa";
    return null;
  }
  function plek(a) {
    if (a.closest("header, nav")) return "kop";
    if (a.closest("footer")) return "voet";
    if (a.closest("form, #contact, .contact")) return "contact";
    return "tekst";
  }
  function titel(a) {
    var t = (a.textContent || "").replace(/\s+/g, " ").trim();
    return (t || a.getAttribute("aria-label") || "").slice(0, 100);
  }
  function klik(e) {
    var a = e.target && e.target.closest ? e.target.closest("a[href]") : null;
    if (!a) return;
    if (a.hasAttribute("data-goatcounter-click")) {
      // GoatCounter telt deze zelf; alleen de pagina en een leesbare titel erbij.
      a.setAttribute("data-goatcounter-referrer", location.pathname);
      a.setAttribute("data-goatcounter-title", titel(a));
      return;
    }
    var s = soort(a.getAttribute("href") || "");
    if (!s || !window.goatcounter || !window.goatcounter.count) return;
    window.goatcounter.count({
      event: true,
      path: s + "-" + plek(a),
      title: titel(a),
      referrer: location.pathname
    });
  }
  // In de vangfase, zodat de verwijzer staat voordat GoatCounter zijn eigen
  // luisteraar op de link afhandelt.
  document.addEventListener("click", klik, true);
  document.addEventListener("auxclick", klik, true);
})();
