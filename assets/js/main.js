/* =============================================================================
   LEAP – interactions
   Vanilla JS, no dependencies. Respects prefers-reduced-motion.
   ========================================================================== */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Preview aid: ?allin reveals every section immediately (e.g. for screenshots or print).
  var showAll = window.location.search.indexOf("allin") !== -1;

  /* ---------- Scroll reveal ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if (showAll || reduce || !("IntersectionObserver" in window)) {
    reveals.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Nav: solid on scroll; hero letters shift a few pixels ---------- */
  var nav = document.getElementById("nav");
  var word = document.querySelector(".hero__word");
  var ticking = false;
  function onScroll() {
    var y = window.pageYOffset;
    if (nav) nav.classList.toggle("scrolled", y > 60);
    if (word && !reduce && y < window.innerHeight) {
      word.style.setProperty("--shift", Math.round(y * 0.04) + "px");   // about 6px over the first 150px, capped by the hero height
    }
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Hero letters: tap shows the archival source (hover does it in CSS) ---------- */
  var letters = document.querySelectorAll(".hero__letter");
  letters.forEach(function (el) {
    el.addEventListener("click", function () {
      var on = el.classList.contains("show");
      letters.forEach(function (o) { o.classList.remove("show"); });
      if (!on) el.classList.add("show");
    });
  });

  /* ---------- Films: swap a still for its YouTube video, only when a visitor asks ---------- */
  document.querySelectorAll("a.film[data-video]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + a.getAttribute("data-video") + "?autoplay=1&rel=0";
      f.title = (a.getAttribute("aria-label") || "Video").replace(/^Play /, "");
      f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
      f.allowFullscreen = true;
      f.className = a.getAttribute("data-frame") || "film-frame";
      a.replaceWith(f);
    });
  });

  /* ---------- Mobile menu ---------- */
  var toggle = document.getElementById("navToggle");
  var menu = document.getElementById("menu");
  function setMenu(open) {
    menu.classList.toggle("open", open);
    menu.setAttribute("aria-hidden", String(!open));
    toggle.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () { setMenu(!menu.classList.contains("open")); });
    menu.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  }
})();
