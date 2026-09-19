// catalog-core 单测：查询/筛选/排序是这页的核心行为，用 node --test 跑。
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const core = require('../web/assets/catalog-core.js');

const viewOf = (cap) => ({ ...(cap.definition || {}), ...(cap.live || {}), providers: (cap.live || {}).providers || [] });

const CAPS = [
  {
    capability_id: 'display.audio',
    in_ads: true,
    in_live: true,
    availability: { has_checker: false, live: true },
    reconcile: { declared_not_live: false, live_not_declared: false },
    docs: ['plugins/xiaomi-tv-display/capability.md'],
    declared_by: ['xiaomi.tv.display'],
    definition: {
      kind: 'output',
      group: 'display',
      role: '音频投电视播放器',
      planner_recognize: '把 audio Asset 交给电视 DLNA 出声',
      typical_triggers: ['把最新的音频在小米电视上放出来'],
      do_not_dispatch: ['投图', '点歌放歌'],
      input_schema: { asset_ref: { type: 'object', required: true, description: '必填 AssetRef' } },
    },
    live: { providers: [{ edge_name: '客厅 · Mac Edge', service_id: 'xiaomi.tv.display' }] },
  },
  {
    capability_id: 'camera.capture',
    in_ads: true,
    in_live: false,
    availability: { has_checker: true, live: false },
    reconcile: { declared_not_live: true, live_not_declared: false },
    docs: ['plugins/gopro-camera/capability.md'],
    definition: { kind: 'input', group: 'camera', role: '拍照', typical_triggers: ['拍一张'], do_not_dispatch: [] },
    live: {},
  },
  {
    capability_id: 'xiaodu.play',
    in_ads: false,
    in_live: true,
    availability: { has_checker: false, live: true },
    reconcile: { declared_not_live: false, live_not_declared: true },
    docs: [],
    definition: {},
    live: { kind: 'action', group: 'voice', role: '小度播放', providers: [{ edge_name: '客厅 · Mac Edge', service_id: 'xiaodu.speaker' }] },
  },
];

const ids = (rows) => rows.map((r) => r.cap.capability_id);

test('关键词命中触发语 / 参数说明 / 设备名', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: '电视' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: 'asset_ref' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: '小度' })), ['xiaodu.play']);
});

test('空格分隔 = AND', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: '电视 音频' })).length, 1);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: '电视 拍照' })).length, 0);
});

test('按 group / kind / 设备 / 状态筛选', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, group: 'display' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, kind: 'input' })), ['camera.capture']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, provider: '客厅 · Mac Edge' })).sort(), ['display.audio', 'xiaodu.play']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'live' })).sort(), ['display.audio', 'xiaodu.play']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'declared_not_live' })), ['camera.capture']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'live_not_declared' })), ['xiaodu.play']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'checker' })), ['camera.capture']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'no_docs' })), ['xiaodu.play']);
});

test('相关性排序把 id 命中排在前面；group 排序可用', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: 'camera' })), ['camera.capture']);
  const byGroup = ids(core.filterCaps(CAPS, { viewOf, sort: 'group' }));
  assert.deepEqual(byGroup, ['camera.capture', 'display.audio', 'xiaodu.play']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, sort: 'live' }))[0] !== 'camera.capture', true);
});

test('facets 统计 group/kind/设备', () => {
  const f = core.facets(CAPS, viewOf);
  assert.deepEqual(f.groups.map((g) => g.name), ['camera', 'display', 'voice']);
  assert.deepEqual(f.kinds.map((k) => k.name).sort(), ['action', 'input', 'output']);
  assert.deepEqual(f.providers, [{ name: '客厅 · Mac Edge', count: 2 }]);
});

test('高亮切片段并可合并', () => {
  assert.deepEqual(core.highlight('display.audio', 'audio'), [
    { text: 'display.', hit: false },
    { text: 'audio', hit: true },
  ]);
  assert.deepEqual(core.highlight('audio audio', 'audio'), [
    { text: 'audio', hit: true },
    { text: ' ', hit: false },
    { text: 'audio', hit: true },
  ]);
  assert.deepEqual(core.highlight('nothing', 'zzz'), [{ text: 'nothing', hit: false }]);
});
