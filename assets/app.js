/* app.js：把 catalog 渲染成可查的列表 + 详情（DOM 部分；纯逻辑在 catalog-core.js）。 */
(function () {
  'use strict';
  const core = window.HACore;
  const $ = (id) => document.getElementById(id);
  const esc = (s) =>
    String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const hl = (text, q) =>
    core.highlight(text, q).map((p) => (p.hit ? '<mark>' + esc(p.text) + '</mark>' : esc(p.text))).join('');

  /** effective view：实况优先、定义兜底（与导出器 effective_view 同规则，前端自算一份）。 */
  function viewOf(cap) {
    const def = cap.definition || {};
    const live = cap.live || {};
    const out = {};
    for (const key of Object.keys(def)) {
      const v = live[key];
      out[key] = v === undefined || v === '' || v === null ? def[key] : v;
    }
    for (const key of Object.keys(live)) if (!(key in out)) out[key] = live[key];
    out.providers = live.providers || [];
    return out;
  }

  const state = { q: '', group: '', kind: '', provider: '', status: 'all', sort: 'relevance', id: '' };
  const KEYS = ['q', 'group', 'kind', 'provider', 'status', 'sort', 'id'];
  let CATALOG = null;

  function readUrl() {
    const p = new URLSearchParams(location.search);
    for (const k of KEYS) if (p.has(k)) state[k] = p.get(k);
    if (!state.status) state.status = 'all';
  }

  function writeUrl() {
    const p = new URLSearchParams();
    for (const k of KEYS) {
      if (k === 'status' && state[k] === 'all') continue;
      if (state[k]) p.set(k, state[k]);
    }
    const qs = p.toString();
    history.replaceState(null, '', qs ? '?' + qs : location.pathname);
  }

  function fillSelect(el, items, value, label) {
    el.innerHTML =
      `<option value="">${label}</option>` +
      items.map((it) => `<option value="${esc(it.name)}">${esc(it.name)} (${it.count})</option>`).join('');
    el.value = value || '';
  }

  function renderStats(summary) {
    const s = summary || {};
    $('stats').innerHTML = [
      ['能力', s.capabilities],
      ['在线', s.live],
      ['声明未上线', s.declared_not_live],
      ['线上未声明', s.live_not_declared],
      ['能力包', s.extensions],
    ]
      .map(([label, value]) => `<div class="stat"><b>${value == null ? '–' : value}</b><span>${label}</span></div>`)
      .join('');
  }

  function cardHtml(row, q) {
    const cap = row.cap;
    const view = row.view;
    const chips = [`<span class="chip chip--group">${esc(view.group || '(未分类)')}</span>`];
    if (view.kind) chips.push(`<span class="chip">${esc(view.kind)}</span>`);
    if (view.composition === 'composite') chips.push('<span class="chip">composite</span>');
    if (cap.in_live) chips.push('<span class="chip chip--ok">在线</span>');
    if ((cap.reconcile || {}).declared_not_live) chips.push('<span class="chip chip--warn">声明未上线</span>');
    if ((cap.reconcile || {}).live_not_declared) chips.push('<span class="chip chip--warn">线上未声明</span>');
    if (cap.availability && cap.availability.has_checker) chips.push('<span class="chip">有探测</span>');
    const providers = core.providerNames(cap, view).join('、');
    if (providers) chips.push(`<span class="chip">${esc(providers)}</span>`);
    const trig = (view.typical_triggers || [])[0];
    return `<article class="card${state.id === cap.capability_id ? ' active' : ''}" data-id="${esc(cap.capability_id)}">
      <div class="card__top"><span class="card__id mono">${hl(cap.capability_id, q)}</span>
        ${view.role ? `<span class="card__role">${hl(view.role, q)}</span>` : ''}</div>
      <div class="card__meta">${chips.join('')}</div>
      ${trig ? `<div class="card__trig">「${hl(trig, q)}」</div>` : ''}
    </article>`;
  }

  function paramsTable(schema, q) {
    const keys = Object.keys(schema || {});
    if (!keys.length) return '<div class="muted small">（无）</div>';
    return (
      '<table><thead><tr><th>参数</th><th>类型</th><th>必填</th><th>说明</th></tr></thead><tbody>' +
      keys
        .map((k) => {
          const s = schema[k] || {};
          return `<tr><td class="mono">${hl(k, q)}</td><td>${esc(s.type || '')}</td><td>${
            s.required ? '是' : '否'
          }</td><td>${hl(s.description || '', q)}</td></tr>`;
        })
        .join('') +
      '</tbody></table>'
    );
  }

  function detailHtml(cap, q) {
    const view = viewOf(cap);
    const flags = [
      `<span class="chip chip--group">${esc(view.group || '(未分类)')}</span>`,
      `<span class="chip">kind ${esc(view.kind || '-')}</span>`,
      `<span class="chip">${esc(view.composition || 'atomic')}</span>`,
    ];
    if (cap.in_live) flags.push('<span class="chip chip--ok">在线</span>');
    if ((cap.reconcile || {}).declared_not_live) flags.push('<span class="chip chip--warn">声明未上线</span>');
    if ((cap.reconcile || {}).live_not_declared) flags.push('<span class="chip chip--warn">线上未声明</span>');
    if (cap.reconcile && cap.reconcile.live_differs) flags.push('<span class="chip">实况≠定义</span>');

    const list = (arr) =>
      arr && arr.length ? '<ul>' + arr.map((t) => `<li>${hl(t, q)}</li>`).join('') + '</ul>' : '<div class="muted small">（无）</div>';
    const providers = (view.providers || [])
      .map((p) => `<li>${esc(p.edge_name || '')} <span class="muted mono">${esc(p.service_id || '')}</span></li>`)
      .join('');
    const docs = (cap.docs || [])
      .map(
        (d) =>
          `<li><a href="https://github.com/kaulie/home-agent-os/blob/main/${esc(d)}" target="_blank" rel="noreferrer">${esc(
            d
          )}</a></li>`
      )
      .join('');
    const cfg = (cap.config_keys || []).map((k) => `<li class="mono">${esc(k)}</li>`).join('');
    const decl = []
      .concat((cap.declared_by || []).map((s) => `<li class="mono">service: ${esc(s)}</li>`))
      .concat((cap.declared_lists || []).map((s) => `<li class="mono">条件声明: ${esc(s)}</li>`))
      .concat((cap.packages || []).map((s) => `<li class="mono">package: plugins/${esc(s)}/</li>`))
      .join('');

    return `<h2 class="mono">${hl(cap.capability_id, q)}</h2>
      <div class="muted small">${esc([view.display_name, view.role].filter(Boolean).join(' · '))}</div>
      <div class="card__meta">${flags.join('')}</div>
      ${view.planner_recognize ? `<h3>规划器怎么认它</h3><div>${hl(view.planner_recognize, q)}</div>` : ''}
      ${view.prefer_when ? `<h3>优先本能力</h3><div>${hl(view.prefer_when, q)}</div>` : ''}
      <h3>典型触发语</h3>${list(view.typical_triggers)}
      <h3>不要派给它</h3>${list(view.do_not_dispatch)}
      ${(view.decomposes_to || []).length ? `<h3>分解为</h3>${list(view.decomposes_to)}` : ''}
      <h3>入参</h3>${paramsTable(view.input_schema, q)}
      <h3>出参</h3>${paramsTable(view.output_schema, q)}
      <h3>谁提供</h3>${providers ? `<ul>${providers}</ul>` : '<div class="muted small">（当前无在线节点）</div>'}
      ${decl ? `<h3>声明 / 归属</h3><ul>${decl}</ul>` : ''}
      ${cfg ? `<h3>相关配置</h3><ul>${cfg}</ul>` : ''}
      ${docs ? `<h3>文档</h3><ul>${docs}</ul>` : ''}
      <h3>可用性</h3>
      <div class="small">执行前探测：${cap.availability && cap.availability.has_checker ? '有' : '无'} · 当前在线：${
      cap.in_live ? '是' : '否'
    }</div>
      <p class="small"><a href="capabilities/${esc(cap.capability_id)}.md">静态页（md）</a></p>`;
  }

  function render() {
    const caps = CATALOG.capabilities || [];
    const rows = core.filterCaps(caps, {
      viewOf,
      query: state.q,
      group: state.group,
      kind: state.kind,
      provider: state.provider,
      status: state.status,
      sort: state.sort,
    });
    $('count').textContent = `显示 ${rows.length} / ${caps.length} 条能力`;
    $('list').innerHTML = rows.length
      ? rows.map((r) => cardHtml(r, state.q)).join('')
      : '<div class="empty">没有匹配的能力。试试清空关键词 / 换 group。</div>';
    if (state.id) {
      const cap = caps.find((c) => c.capability_id === state.id);
      $('detail').innerHTML = cap ? detailHtml(cap, state.q) : '<div class="empty">未找到 ' + esc(state.id) + '</div>';
    }
    $('group').value = state.group;
    $('kind').value = state.kind;
    $('provider').value = state.provider;
    $('status').value = state.status;
    $('sort').value = state.sort;
    writeUrl();
  }

  function bind() {
    $('q').addEventListener('input', (e) => {
      state.q = e.target.value;
      render();
    });
    for (const id of ['group', 'kind', 'provider', 'status', 'sort']) {
      $(id).addEventListener('change', (e) => {
        state[id] = e.target.value;
        render();
      });
    }
    $('reset').addEventListener('click', () => {
      Object.assign(state, { q: '', group: '', kind: '', provider: '', status: 'all', sort: 'relevance', id: '' });
      $('q').value = '';
      render();
    });
    $('list').addEventListener('click', (e) => {
      const card = e.target.closest('[data-id]');
      if (!card) return;
      state.id = card.dataset.id;
      render();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement !== $('q')) {
        e.preventDefault();
        $('q').focus();
      } else if (e.key === 'Escape' && document.activeElement === $('q') && state.q) {
        state.q = '';
        $('q').value = '';
        render();
      }
    });
  }

  async function main() {
    readUrl();
    $('q').value = state.q;
    bind();
    try {
      const resp = await fetch('catalog/capabilities.json', { cache: 'no-store' });
      CATALOG = await resp.json();
    } catch (err) {
      $('list').innerHTML = '<div class="empty">读不到 catalog/capabilities.json —— 先跑 scripts/sync.sh 生成目录。</div>';
      return;
    }
    const src = CATALOG.source || {};
    $('source').textContent =
      `来源 ${src.repo || ''} @ ${src.commit || '-'} · 边缘 ${src.edge || '-'} · 生成于 ${CATALOG.generated_at || '-'}` +
      ` · 实况 ${src.live_source || '(未拉取)'}（${src.live_count || 0} 条）`;
    renderStats(CATALOG.summary);
    const f = core.facets(CATALOG.capabilities || [], viewOf);
    fillSelect($('group'), f.groups, state.group, '全部 group');
    fillSelect($('kind'), f.kinds, state.kind, '全部 kind');
    fillSelect($('provider'), f.providers, state.provider, '全部设备');
    render();
  }

  main();
})();


