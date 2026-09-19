/* app.js：能力集市 UI。
 *
 * 数据源二选一（自动）：
 *   1) **marketplace 服务**（有数据库时）：走 /api/v1/*，服务端查询 + 集市注解编辑；
 *   2) **静态**（GitHub Pages / 纯静态托管）：读 ../catalog/capabilities.json，只读。
 * 两种模式 UI 一致，页头标明当前数据源。
 */
(function () {
  'use strict';
  const core = window.HACore;
  const $ = (id) => document.getElementById(id);
  const esc = (s) =>
    String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const hl = (text, q) =>
    core.highlight(text, q).map((p) => (p.hit ? '<mark>' + esc(p.text) + '</mark>' : esc(p.text))).join('');

  /** effective view：实况优先、定义兜底（与后端/导出器同规则）。 */
  function viewOf(cap) {
    const def = cap.definition || {};
    const live = cap.live || {};
    const out = {};
    for (const key of Object.keys(def)) {
      const v = live[key];
      out[key] = v === undefined || v === '' || v === null ? def[key] : v;
    }
    for (const key of Object.keys(live)) if (!(key in out)) out[key] = live[key];
    out.providers = live.providers || cap.providers || [];
    return out;
  }

  const state = { q: '', group: '', kind: '', provider: '', status: 'all', review: '', sort: 'relevance', id: '' };
  const KEYS = ['q', 'group', 'kind', 'provider', 'status', 'review', 'sort', 'id'];

  const SOURCE = { api: false, label: '加载中…', stats: null, facets: null, imports: [] };
  let CAPS = [];

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

  async function getJSON(url) {
    const r = await fetch(url, { cache: 'no-store', headers: { Accept: 'application/json' } });
    if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
    return r.json();
  }

  /** 先试服务（DB），失败退回静态 JSON。 */
  async function loadData() {
    try {
      const [stats, caps, facets, imports] = await Promise.all([
        getJSON('/api/v1/stats'),
        getJSON('/api/v1/capabilities?limit=2000'),
        getJSON('/api/v1/facets'),
        getJSON('/api/v1/imports?limit=5'),
      ]);
      if (stats && stats.ok) {
        SOURCE.api = true;
        SOURCE.label = `数据源：marketplace 服务 / SQLite（schema v${stats.schema_version}）`;
        SOURCE.stats = stats;
        SOURCE.facets = facets;
        SOURCE.imports = imports.imports || [];
        CAPS = caps.capabilities || [];
        return;
      }
    } catch (e) {
      /* 落到静态 */
    }
    const catalog = await getJSON('../catalog/capabilities.json');
    SOURCE.api = false;
    SOURCE.label = `数据源：静态 catalog（只读）· 由 ${catalog.generated_by || '导出器'} 生成`;
    CAPS = catalog.capabilities || [];
    SOURCE.stats = Object.assign({}, catalog.summary || {}, { last_import: catalog.source || {} });
    SOURCE.facets = null;
    SOURCE.imports = [];
  }

  function fillSelect(el, items, value, label) {
    el.innerHTML =
      `<option value="">${label}</option>` +
      items.map((it) => `<option value="${esc(it.name)}">${esc(it.name)} (${it.count})</option>`).join('');
    el.value = value || '';
  }

  function renderStats() {
    const s = SOURCE.stats || {};
    const last = s.last_import || {};
    const items = [
      ['能力', s.capabilities],
      ['在线', s.live],
      ['声明未上线', s.declared_not_live],
      ['线上未声明', s.live_not_declared],
      s.annotated != null ? ['集市注解', s.annotated] : null,
      SOURCE.api ? ['导入次数', s.imports] : null,
      SOURCE.api ? ['已下线', s.not_in_catalog] : null,
    ].filter(Boolean);
    $('stats').innerHTML = items
      .map(([label, value]) => `<div class="stat"><b>${value == null ? '–' : value}</b><span>${label}</span></div>`)
      .join('');
    const src = last && (last.source_commit || last.commit);
    $('source').textContent =
      SOURCE.label +
      (src ? ` · 代码 ${src}` : '') +
      (last && last.source_commit && last.imported_at ? ` · 导入于 ${last.imported_at}` : '');
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
    if ((cap.reconcile || {}).not_in_catalog) chips.push('<span class="chip chip--err">已下线</span>');
    if (cap.has_checker) chips.push('<span class="chip">有探测</span>');
    if (cap.owner) chips.push(`<span class="chip">owner: ${esc(cap.owner)}</span>`);
    if (cap.status && cap.status !== 'active') chips.push(`<span class="chip chip--warn">${esc(cap.status)}</span>`);
    for (const tag of (cap.tags || []).slice(0, 3)) chips.push(`<span class="chip">#${esc(tag)}</span>`);
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

  function annotationEditor(cap) {
    if (!SOURCE.api) {
      return '<h3>集市字段</h3><div class="muted small">静态托管下只读 —— 起本机 marketplace 服务后可在此维护（status / owner / tags / notes）。</div>';
    }
    const tags = (cap.tags || []).join(', ');
    return `<h3>集市字段（可维护）</h3>
      <div class="form">
        <label>status
          <select id="ann-status">
            ${['active', 'planned', 'deprecated', 'blocked']
              .map((s) => `<option value="${s}"${cap.status === s ? ' selected' : ''}>${s}</option>`)
              .join('')}
          </select></label>
        <label>owner <input id="ann-owner" type="text" value="${esc(cap.owner || '')}" placeholder="谁负责" /></label>
        <label>tags <input id="ann-tags" type="text" value="${esc(tags)}" placeholder="逗号分隔" /></label>
        <label>notes <textarea id="ann-notes" rows="2" placeholder="备注/评审结论">${esc(cap.notes || '')}</textarea></label>
        <div class="form__actions">
          <button class="btn" id="ann-save">保存</button>
          <span id="ann-msg" class="small muted">${cap.reviewed_at ? '上次维护 ' + esc(cap.reviewed_at) : '还没人维护过'}</span>
        </div>
      </div>`;
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
    if ((cap.reconcile || {}).not_in_catalog) flags.push('<span class="chip chip--err">代码里已下线</span>');

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
    const events = (cap.events || [])
      .map((e) => `<li class="mono">${esc(e.at)} ${esc(e.field)}: ${esc(e.old_value)} → ${esc(e.new_value)}（${esc(e.actor)}）</li>`)
      .join('');

    return `<h2 class="mono">${hl(cap.capability_id, q)}</h2>
      <div class="muted small">${esc([view.display_name, view.role].filter(Boolean).join(' · '))}</div>
      <div class="card__meta">${flags.join('')}</div>
      ${cap.notes ? `<p class="note">${esc(cap.notes)}</p>` : ''}
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
      ${annotationEditor(cap)}
      ${events ? `<h3>维护历史</h3><ul>${events}</ul>` : ''}
      <h3>可用性</h3>
      <div class="small">执行前探测：${cap.has_checker ? '有' : '无'} · 当前在线：${cap.in_live ? '是' : '否'}</p></div>
      <p class="small"><a href="../capabilities/${esc(cap.capability_id)}.md">静态页（md）</a></p>`;
  }

  /** 过滤：有服务就走数据库查询，否则退回客户端过滤（两者语义一致）。 */
  async function applyFilters() {
    if (SOURCE.api) {
      const p = new URLSearchParams({ limit: '500' });
      if (state.q) p.set('q', state.q);
      if (state.group) p.set('group', state.group);
      if (state.kind) p.set('kind', state.kind);
      if (state.provider) p.set('edge', state.provider);
      if (state.review) p.set('status', state.review === 'annotated' ? '' : state.review);
      if (state.status === 'live') p.set('live', 'live');
      else if (state.status === 'declared_not_live') p.set('live', 'declared_not_live');
      else if (state.status === 'live_not_declared') p.set('live', 'live_not_declared');
      else if (state.status === 'checker') p.set('has_checker', '1');
      if (state.sort) p.set('sort', state.sort);
      try {
        const data = await getJSON('/api/v1/capabilities?' + p.toString());
        return (data.capabilities || []).map((cap) => ({ cap, view: viewOf(cap) }));
      } catch (e) {
        /* 服务抖了就退回客户端过滤 */
      }
    }
    return core
      .filterCaps(CAPS, {
        viewOf,
        query: state.q,
        group: state.group,
        kind: state.kind,
        provider: state.provider,
        status: state.status,
        sort: state.sort,
      })
      .filter((row) => {
        if (!state.review) return true;
        if (state.review === 'annotated') {
          const c = row.cap;
          return c.owner || c.notes || (c.tags || []).length || (c.status && c.status !== 'active');
        }
        return row.cap.status === state.review;
      });
  }

  let renderToken = 0;
  async function render() {
    const token = ++renderToken;
    const rows = await applyFilters();
    if (token !== renderToken) return;
    $('count').textContent = `显示 ${rows.length} / ${CAPS.length} 条能力`;
    $('list').innerHTML = rows.length
      ? rows.map((r) => cardHtml(r, state.q)).join('')
      : '<div class="empty">没有匹配的能力。试试清空关键词 / 换 group。</div>';
    if (state.id) {
      const cap = CAPS.find((c) => c.capability_id === state.id);
      $('detail').innerHTML = cap ? detailHtml(cap, state.q) : '<div class="empty">未找到 ' + esc(state.id) + '</div>';
      bindAnnotation(cap);
    }
    for (const id of ['group', 'kind', 'provider', 'status', 'review', 'sort']) $(id).value = state[id] || (id === 'status' ? 'all' : '');
    $('imports').textContent = SOURCE.imports.length
      ? '最近导入：' +
        SOURCE.imports
          .slice(0, 2)
          .map((i) => `#${i.import_id} ${i.source_commit || '?'}（+${(i.added || []).length}/-${(i.removed || []).length}/~${(i.changed || []).length}）`)
          .join('；')
      : '';
    writeUrl();
  }

  function bindAnnotation(cap) {
    const save = $('ann-save');
    if (!save || !cap) return;
    save.addEventListener('click', async () => {
      const msg = $('ann-msg');
      msg.textContent = '保存中…';
      const body = {
        status: $('ann-status').value,
        owner: $('ann-owner').value,
        tags: $('ann-tags').value,
        notes: $('ann-notes').value,
      };
      try {
        const r = await fetch('/api/v1/capabilities/' + encodeURIComponent(cap.capability_id), {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body),
        });
        const data = await r.json();
        if (!r.ok || !data.ok) throw new Error(data.error || r.statusText);
        const idx = CAPS.findIndex((c) => c.capability_id === cap.capability_id);
        if (idx >= 0) CAPS[idx] = data.capability;
        SOURCE.stats = SOURCE.stats || {};
        msg.textContent = '已保存 ' + (data.capability.reviewed_at || '');
        await render();
      } catch (e) {
        msg.textContent = '保存失败：' + e.message;
      }
    });
  }

  let debounce = null;
  function scheduleRender() {
    clearTimeout(debounce);
    debounce = setTimeout(render, 180);
  }

  function bind() {
    $('q').addEventListener('input', (e) => {
      state.q = e.target.value;
      scheduleRender();
    });
    for (const id of ['group', 'kind', 'provider', 'status', 'review', 'sort']) {
      $(id).addEventListener('change', (e) => {
        state[id] = e.target.value;
        render();
      });
    }
    $('reset').addEventListener('click', () => {
      Object.assign(state, { q: '', group: '', kind: '', provider: '', status: 'all', review: '', sort: 'relevance', id: '' });
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
      await loadData();
    } catch (err) {
      $('list').innerHTML =
        '<div class="empty">读不到数据：起本机 marketplace 服务（`python3 server/catalog_cli.py serve`），或先跑 `scripts/sync.sh` 生成 catalog。</div>';
      return;
    }
    renderStats();
    const f = SOURCE.facets || core.facets(CAPS, viewOf);
    fillSelect($('group'), f.groups || [], state.group, '全部 group');
    fillSelect($('kind'), f.kinds || [], state.kind, '全部 kind');
    fillSelect($('provider'), f.edges || f.providers || [], state.provider, '全部设备');
    render();
  }

  main();
})();



