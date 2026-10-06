
(function(){
  function sizeTitleNode(node, text){
    if (!node) return;
    node.classList.remove('is-long','is-very-long');
    const n = (text || node.textContent || '').trim().length;
    if (n >= 58) node.classList.add('is-very-long');
    else if (n >= 38) node.classList.add('is-long');
  }

  const blockedKeys = new Set(['a','c','s','u','p','x']);
  document.addEventListener('contextmenu', function(e){ e.preventDefault(); }, {passive:false});
  document.addEventListener('dragstart', function(e){ e.preventDefault(); }, {passive:false});
  document.addEventListener('selectstart', function(e){ e.preventDefault(); }, {passive:false});
  document.addEventListener('copy', function(e){ e.preventDefault(); }, {passive:false});
  document.addEventListener('cut', function(e){ e.preventDefault(); }, {passive:false});
  document.addEventListener('keydown', function(e){
    const key = (e.key || '').toLowerCase();
    if (e.key === 'F12' || (e.ctrlKey && e.shiftKey && ['i','j','c'].includes(key)) || ((e.ctrlKey || e.metaKey) && blockedKeys.has(key))) {
      e.preventDefault();
    }
  }, {passive:false});

  document.querySelectorAll('.selector-title').forEach(function(node){ sizeTitleNode(node, node.textContent); });
  document.querySelectorAll('.content-title').forEach(function(node){ sizeTitleNode(node, node.textContent); });

  document.querySelectorAll('[data-doc-switcher]').forEach(function(root){
    const cards = Array.from(root.querySelectorAll('[data-target]'));
    const panels = Array.from(document.querySelectorAll(root.getAttribute('data-panels')));
    const titleNode = document.querySelector(root.getAttribute('data-title-target') || '');
    function activate(id, pushHash){
      cards.forEach(function(card){
        const on = card.getAttribute('data-target') === id;
        card.classList.toggle('is-active', on);
        card.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      panels.forEach(function(panel){
        const on = panel.getAttribute('data-doc') === id;
        panel.classList.toggle('is-active', on);
      });
      const activeCard = cards.find(c => c.getAttribute('data-target') === id);
      if (titleNode && activeCard) {
        const txt = activeCard.getAttribute('data-title-full') || activeCard.querySelector('.selector-title')?.textContent || '';
        if (txt) { titleNode.textContent = txt; sizeTitleNode(titleNode, txt); }
      }
      if (pushHash) {
        try { history.replaceState(null, '', '#' + id); } catch (e) { location.hash = '#' + id; }
      }
    }
    cards.forEach(function(card){
      card.addEventListener('click', function(){ activate(card.getAttribute('data-target'), true); });
    });
    const fallback = cards[0] ? cards[0].getAttribute('data-target') : null;
    const hash = (location.hash || '').replace('#','');
    activate(cards.some(c => c.getAttribute('data-target') === hash) ? hash : fallback, false);
  });
})();
