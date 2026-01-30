(() => {
  const deck = document.querySelector('[data-deck]');
  let currentView = document.querySelector('[data-view]');

  if (!deck || !currentView) return;

  const sameOrigin = (url) => {
    try {
      const u = new URL(url, window.location.href);
      return u.origin === window.location.origin;
    } catch {
      return false;
    }
  };

  const normalizePath = (path) => {
    if (!path) return '/';
    const u = new URL(path, window.location.href);
    return u.pathname || '/';
  };

  const setActiveNav = (path) => {
    const p = normalizePath(path);

    document.querySelectorAll('[data-nav]').forEach((a) => {
      try {
        const ap = normalizePath(a.getAttribute('href') || '/');
        if (ap === p) {
          a.setAttribute('aria-current', 'page');
        } else {
          a.removeAttribute('aria-current');
        }
      } catch {
        a.removeAttribute('aria-current');
      }
    });
  };

  const swapView = async (href, { push = true } = {}) => {
    if (!href) return;

    const url = new URL(href, window.location.href);
    if (!sameOrigin(url)) {
      window.location.href = url.href;
      return;
    }

    const nextPath = url.pathname;

    try {
      const res = await fetch(url.href, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
          'X-Butterfly-Deck': '1',
        },
      });

      if (!res.ok) {
        window.location.href = url.href;
        return;
      }

      const html = await res.text();
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const next = doc.querySelector('[data-view]');

      if (!next) {
        window.location.href = url.href;
        return;
      }

      const nextTitle = doc.querySelector('title');
      if (nextTitle && nextTitle.textContent) {
        document.title = nextTitle.textContent;
      }

      currentView.classList.remove('is-active');

      const incoming = document.createElement('section');
      incoming.className = 'view-card is-active';
      incoming.setAttribute('data-view', '');
      incoming.setAttribute('aria-live', 'polite');
      incoming.setAttribute('aria-atomic', 'true');
      incoming.innerHTML = next.innerHTML;

      deck.appendChild(incoming);

      window.requestAnimationFrame(() => {
        incoming.classList.add('is-active');
      });

      window.setTimeout(() => {
        currentView.remove();
        incoming.classList.remove('is-entering');
        setActiveNav(nextPath);

        const focusTarget = incoming.querySelector('h1, h2, a, button, input, [tabindex]');
        if (focusTarget && typeof focusTarget.focus === 'function') {
          focusTarget.focus({ preventScroll: true });
        }

        currentView = incoming;
      }, 260);

      if (push) {
        window.history.pushState({ path: nextPath }, '', nextPath);
      }
    } catch {
      window.location.href = url.href;
    }
  };

  document.addEventListener('click', (e) => {
    const a = e.target && e.target.closest ? e.target.closest('a[data-nav]') : null;
    if (!a) return;

    const href = a.getAttribute('href');
    if (!href) return;

    if (a.target === '_blank') return;

    e.preventDefault();
    swapView(href, { push: true });
  });

  window.addEventListener('popstate', (e) => {
    const path = (e.state && e.state.path) || window.location.pathname;
    swapView(path, { push: false });
  });

  setActiveNav(window.location.pathname);
})();
