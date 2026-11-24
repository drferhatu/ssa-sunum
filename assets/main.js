(() => {
  const prefersReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const slides = Array.from(document.querySelectorAll('.slide'));
  const pad = (n) => String(n).padStart(2, '0');

  // PDF için sayfa numaraları
  slides.forEach((s, i) => {
    if (i === 0) return;
    const n = document.createElement('span');
    n.className = 'pageno';
    n.textContent = pad(i + 1) + ' / ' + pad(slides.length);
    s.appendChild(n);
  });

  // Kaydırınca belirme
  const revealTargets = document.querySelectorAll('.reveal');
  if (prefersReduce || !('IntersectionObserver' in window)) {
    revealTargets.forEach(el => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });
    revealTargets.forEach(el => io.observe(el));
  }

  // Hangi slayttayız?
  const counter = document.querySelector('.counter');
  const progress = document.querySelector('.progress');
  const current = () => {
    const mid = window.scrollY + window.innerHeight / 2;
    let idx = 0;
    slides.forEach((s, i) => { if (s.offsetTop <= mid) idx = i; });
    return idx;
  };
  const update = () => {
    const i = current();
    if (counter) counter.textContent = pad(i + 1) + ' / ' + pad(slides.length);
    if (progress) progress.style.width = ((i + 1) / slides.length * 100) + '%';
  };
  window.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();

  const go = (i) => {
    const t = slides[Math.max(0, Math.min(slides.length - 1, i))];
    window.scrollTo({ top: t.offsetTop, behavior: prefersReduce ? 'auto' : 'smooth' });
  };

  // Klavye / sunum kumandası: → PageDown Boşluk = ileri, ← PageUp = geri, F = tam ekran
  window.addEventListener('keydown', (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ') { e.preventDefault(); go(current() + 1); }
    else if (k === 'ArrowLeft' || k === 'PageUp') { e.preventDefault(); go(current() - 1); }
    else if (k === 'Home') { e.preventDefault(); go(0); }
    else if (k === 'End') { e.preventDefault(); go(slides.length - 1); }
    else if (k === 'f' || k === 'F') {
      if (document.fullscreenElement) document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
    }
  });

  // Sayfa içi bağlantılar
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const target = document.getElementById(a.getAttribute('href').slice(1));
      if (!target) return;
      e.preventDefault();
      window.scrollTo({ top: target.offsetTop, behavior: prefersReduce ? 'auto' : 'smooth' });
      history.replaceState(null, '', '#' + target.id);
    });
  });
})();
