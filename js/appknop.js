/* WhatsApp-knop onderaan het scherm die op een telefoon meescrolt.

   De link komt uit de ronde knop in de kop, zodat het voorgevulde bericht en de
   taal per pagina op een plek staan. Een pagina zonder die knop (404, bedankt)
   krijgt niets. De knop verschijnt na een stukje scrollen en gaat weg zodra het
   formulier of de voet in beeld is, zodat hij niets afdekt.

   Zelfde bestand op draagmuurkoning.nl en keukenvoorbereid.nl. */
(function () {
  var bron = document.querySelector(".kop-contact a.wa");
  if (!bron) return;
  var engels = document.documentElement.lang.indexOf("en") === 0;

  var a = document.createElement("a");
  a.className = "appknop";
  a.href = bron.href;
  a.target = "_blank";
  a.rel = "noopener";
  a.innerHTML = bron.innerHTML;
  var tekst = document.createElement("span");
  tekst.textContent = engels ? "WhatsApp us" : "App ons";
  a.appendChild(tekst);
  document.body.appendChild(a);

  var inBeeld = new Set();
  function zet() {
    a.classList.toggle("zichtbaar", window.scrollY > 400 && inBeeld.size === 0);
  }
  if ("IntersectionObserver" in window) {
    var kijker = new IntersectionObserver(function (items) {
      items.forEach(function (i) {
        if (i.isIntersecting) inBeeld.add(i.target); else inBeeld.delete(i.target);
      });
      zet();
    });
    document.querySelectorAll("form, footer").forEach(function (el) { kijker.observe(el); });
  }
  window.addEventListener("scroll", zet, { passive: true });
  zet();
})();
