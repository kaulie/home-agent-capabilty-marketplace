/**
 * catalog-core：目录的纯逻辑（无 DOM）—— 搜索 / 筛选 / 排序 / 高亮。
 * 集市只登记**声明**（谁声明、参数、触发语、条件挂载），不含实时状态。
 * 拆出来是为了能用 `node --test` 测：查询与过滤是这页的核心行为。
 * 浏览器挂到 globalThis.HACore；Node 里可 require。
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.HACore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  function schemaText(schema) {
    if (!schema || typeof schema !== 'object') return '';
    const out = [];
    for (const key of Object.keys(schema)) {
      const spec = schema[key] || {};
      out.push(key, spec.type || '', spec.description || '');
    }
    return out.join(' ');
  }

  /** 一条能力的可搜索文本（含参数说明：用户常按「投屏」「音量」「asset_ref」找）。 */
  function searchBlob(cap, view) {
    const v = view || {};
    const parts = [
      cap.capability_id,
      v.display_name,
      v.role,
      v.group,
      v.kind,
      v.planner_recognize,
      (v.typical_triggers || []).join(' '),
      (v.do_not_dispatch || []).join(' '),
      (v.decomposes_to || []).join(' '),
      (cap.declared_by || []).join(' '),
      (cap.conditional_lists || []).join(' '),
      (cap.packages || []).join(' '),
      (cap.config_keys || []).join(' '),
      (cap.hosts_effective || []).join(' '),
      cap.description,
      (cap.keywords || []).join(' '),
      schemaText(v.input_schema),
      schemaText(v.output_schema),
    ];
    return parts.filter(Boolean).join('  ').toLowerCase();
  }

  /** 关键词命中：空格分隔 = AND（「电视 音频」这类组合查询）。 */
  function matchesQuery(cap, view, query) {
    const q = (query || '').trim().toLowerCase();
    if (!q) return true;
    const blob = searchBlob(cap, view);
    return q.split(/\s+/).every((token) => blob.includes(token));
  }

  /** 声明特征（静态）：all / conditional 条件声明 / preflight 执行前自检 / composite 组合能力 / unowned 无服务归属 / no_docs 缺文档 */
  function matchesStatus(cap, status) {
    switch (status) {
      case 'conditional':
        return !!(cap.conditional_lists || []).length;
      case 'preflight':
        return !!(cap.has_preflight || cap.has_checker);
      case 'composite':
        return cap.composition === 'composite';
      case 'unowned':
        return !(cap.declared_by || []).length;
      case 'no_docs':
        return !(cap.docs || cap.declaration && cap.declaration.docs || []).length;
      default:
        return true;
    }
  }

  const kindOf = (cap, view) => (view && view.kind) || cap.kind || '';
  const groupOf = (cap, view) => (view && view.group) || cap.group || '(未分类)';

  /** 谁声明了这个能力（服务/能力包）—— 静态归属，不是在线设备。 */
  function serviceNames(cap) {
    const decl = cap.declaration || {};
    const src = (cap.declared_by || decl.declared_by || []).concat(
      (cap.packages || decl.packages || []).map((p) => 'plugins/' + p)
    );
    return Array.from(new Set(src.filter(Boolean))).sort();
  }

  const cmp = (a, b) => (String(a) < String(b) ? -1 : String(a) > String(b) ? 1 : 0);

  /** 相关性启发式：id 精确/前缀 > id 命中 > 显示名 > 角色。 */
  function score(row, q) {
    const id = String(row.cap.capability_id || '').toLowerCase();
    const name = String((row.view && row.view.display_name) || '').toLowerCase();
    const role = String((row.view && row.view.role) || '').toLowerCase();
    let s = 0;
    if (id === q) s += 100;
    if (id.startsWith(q)) s += 40;
    if (id.includes(q)) s += 20;
    if (name.includes(q)) s += 10;
    if (role.includes(q)) s += 6;
    return s;
  }

  /** 过滤 + 排序；viewOf: (cap) => effective view。返回 [{cap, view}]。 */
  function filterCaps(caps, opts) {
    const o = opts || {};
    const viewOf = o.viewOf || (() => ({}));
    const out = [];
    for (const cap of caps) {
      const view = viewOf(cap);
      if (o.group && groupOf(cap, view) !== o.group) continue;
      if (o.kind && kindOf(cap, view) !== o.kind) continue;
      if (o.service && !serviceNames(cap).includes(o.service)) continue;
      if (o.keyword && !(cap.keywords || []).includes(o.keyword)) continue;
      if (o.host && !(cap.hosts_effective || []).includes(o.host)) continue;
      if (o.described && !String(cap.description || '').trim()) continue;
      if (!matchesStatus(cap, o.status || 'all')) continue;
      if (!matchesQuery(cap, view, o.query)) continue;
      out.push({ cap, view });
    }
    return sortRows(out, o.sort, o.query);
  }

  function sortRows(rows, sort, query) {
    const s = sort || 'relevance';
    const copy = rows.slice();
    if (s === 'group') {
      copy.sort(
        (a, b) => cmp(groupOf(a.cap, a.view), groupOf(b.cap, b.view)) || cmp(a.cap.capability_id, b.cap.capability_id)
      );
    } else if (s === 'updated') {
      copy.sort(
        (a, b) => cmp(b.cap.updated_at || '', a.cap.updated_at || '') || cmp(a.cap.capability_id, b.cap.capability_id)
      );
    } else if (s === 'relevance' && (query || '').trim()) {
      const q = query.trim().toLowerCase();
      copy.sort((a, b) => score(b, q) - score(a, q) || cmp(a.cap.capability_id, b.cap.capability_id));
    } else {
      copy.sort((a, b) => cmp(a.cap.capability_id, b.cap.capability_id));
    }
    return copy;
  }

  const inc = (map, key) => map.set(key, (map.get(key) || 0) + 1);

  /** 汇总 facet（筛选下拉/分组标签用）。 */
  function facets(caps, viewOf) {
    const groups = new Map();
    const kinds = new Map();
    const services = new Map();
    const kws = new Map();
    const hosts = new Map();
    for (const cap of caps) {
      const view = viewOf(cap);
      inc(groups, groupOf(cap, view));
      inc(kinds, kindOf(cap, view) || '(未标注)');
      for (const name of serviceNames(cap)) inc(services, name);
      for (const k of cap.keywords || []) inc(kws, k);
      for (const h of cap.hosts_effective || []) inc(hosts, h);
    }
    const toList = (m) =>
      Array.from(m.entries())
        .sort((a, b) => b[1] - a[1] || cmp(a[0], b[0]))
        .map(([name, count]) => ({ name, count }));
    return {
      groups: toList(groups),
      kinds: toList(kinds),
      services: toList(services),
      keywords: toList(kws),
      hosts: toList(hosts),
    };
  }

  /** 命中高亮：返回 [{text, hit}]，调用方负责转义/包裹。 */
  function highlight(text, query) {
    const raw = String(text == null ? '' : text);
    const q = (query || '').trim();
    if (!q || !raw) return [{ text: raw, hit: false }];
    const lower = raw.toLowerCase();
    const tokens = q.split(/\s+/).filter(Boolean).map((t) => t.toLowerCase());
    const hits = [];
    for (const token of tokens) {
      let from = 0;
      while (from < lower.length) {
        const at = lower.indexOf(token, from);
        if (at < 0) break;
        hits.push([at, at + token.length]);
        from = at + token.length;
      }
    }
    if (!hits.length) return [{ text: raw, hit: false }];
    hits.sort((a, b) => a[0] - b[0]);
    const merged = [];
    for (const [s, e] of hits) {
      const last = merged[merged.length - 1];
      if (last && s <= last[1]) last[1] = Math.max(last[1], e);
      else merged.push([s, e]);
    }
    const out = [];
    let cursor = 0;
    for (const [s, e] of merged) {
      if (s > cursor) out.push({ text: raw.slice(cursor, s), hit: false });
      out.push({ text: raw.slice(s, e), hit: true });
      cursor = e;
    }
    if (cursor < raw.length) out.push({ text: raw.slice(cursor), hit: false });
    return out;
  }

  return {
    schemaText,
    searchBlob,
    matchesQuery,
    matchesStatus,
    filterCaps,
    sortRows,
    facets,
    highlight,
    groupOf,
    kindOf,
    serviceNames,
  };
});

