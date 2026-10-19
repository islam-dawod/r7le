// R7LE — interactions: mobile nav + FAQ accordion
(function () {
  "use strict";
  var toggle = document.querySelector(".nav-toggle");
  var mnav = document.getElementById("mobile-nav");
  if (toggle && mnav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      mnav.hidden = open;
    });
    mnav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        toggle.setAttribute("aria-expanded", "false");
        mnav.hidden = true;
      });
    });
  }
  var head = document.querySelector(".site-head");
  if (head) {
    var onScroll = function () {
      head.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }
  document.querySelectorAll(".acc__btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      btn.setAttribute("aria-expanded", String(!open));
      if (panel) panel.hidden = open;
      var icn = btn.querySelector(".acc__ic");
      if (icn) icn.textContent = open ? "+" : "–";
    });
  });

  // Prefill the order summary from ?dest=&pkg= (auto destination, no login)
  var box = document.getElementById("order-summary");
  if (box) {
    var params = new URLSearchParams(location.search);
    var dest = params.get("dest");
    var pkg = params.get("pkg");
    if (dest || pkg) {
      var pkgEl = document.getElementById("order-pkg");
      var destEl = document.getElementById("order-dest");
      if (pkgEl) pkgEl.textContent = pkg || "باقة";
      if (destEl) { if (dest) destEl.textContent = dest; else destEl.hidden = true; }
      var di = document.getElementById("order-dest-input");
      var pi = document.getElementById("order-pkg-input");
      if (di) di.value = dest || "";
      if (pi) pi.value = pkg || "";
      box.hidden = false;
    }
  }
})();
