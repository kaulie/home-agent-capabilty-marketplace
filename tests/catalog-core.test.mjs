// catalog-core 单测：搜索/筛选（**声明维度**）/排序/高亮。
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const core = require('../web/assets/catalog-core.js');

const viewOf = (cap) => ({ ...(cap.definition || {}) });

const CAPS = [
  {
    capability_id: 'display.audio',
    in_ads: true,
    declared_by: ['xiaomi.tv.display'],
    conditional_lists: ['AUDIO_DISPLAY_CAPABILITIES'],
    packages: ['xiaomi-tv-display'],
    has_preflight: false,
    status: 'active', owner: '', tags: [], notes: '',
    docs: ['plugins/xiaomi-tv-display/capability.md'],
    definition: {
      kind: 'output', composition: 'atomic', group: 'display', role: '音频投电视播放器',
      planner_recognize: '把 audio Asset 交给电视 DLNA 出声',
      typical_triggers: ['把最新的音频在小米电视上放出来'],
      do_not_dispatch: ['投图', '点歌放歌'],
      input_schema: { asset_ref: { type: 'object', required: true, description: '必填 AssetRef' } },
    },
  },
  {
    capability_id: 'camera.capture',
    in_ads: true,
    declared_by: ['gopro.camera'], conditional_lists: [], packages: ['gopro-camera'],
    has_preflight: true, docs: ['plugins/gopro-camera/capability.md'],
    definition: { kind: 'input', composition: 'atomic', group: 'camera', role: '拍照', typical_triggers: ['拍一张'], do_not_dispatch: [] },
  },
  {
    capability_id: 'chat.smalltalk',
    in_ads: true,
    declared_by: [], conditional_lists: [], packages: [], has_preflight: false, docs: [],
    definition: { kind: 'action', composition: 'atomic', group: 'chat', role: '闲聊', typical_triggers: [], do_not_dispatch: [] },
  },
];

const ids = (rows) => rows.map((r) => r.cap.capability_id);

test('关键词命中触发语 / 参数说明 / 服务归属', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: '电视' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: 'asset_ref' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: 'xiaomi.tv.display' })), ['display.audio']);
});

test('空格分隔 = AND', () => {
  assert.equal(core.filterCaps(CAPS, { viewOf, query: '电视 音频' }).length, 1);
  assert.equal(core.filterCaps(CAPS, { viewOf, query: '电视 拍照' }).length, 0);
});

test('按 group / kind / 声明服务筛选', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, group: 'display' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, kind: 'input' })), ['camera.capture']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, service: 'gopro.camera' })), ['camera.capture']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, service: 'plugins/xiaomi-tv-display' })), ['display.audio']);
});

test('按声明特征筛选（条件挂载 / 执行前自检 / 无归属 / 缺文档）', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'conditional' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'preflight' })), ['camera.capture']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'unowned' })), ['chat.smalltalk']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'no_docs' })), ['chat.smalltalk']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, status: 'all' })).sort(), ['camera.capture', 'chat.smalltalk', 'display.audio']);
});

test('排序：按 group / 相关性', () => {
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, sort: 'group' })), ['camera.capture', 'chat.smalltalk', 'display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: 'camera' }))[0], 'camera.capture');
});

test('facets 统计 group/kind/服务', () => {
  const f = core.facets(CAPS, viewOf);
  assert.deepEqual(f.groups.map((g) => g.name), ['camera', 'chat', 'display']);
  assert.deepEqual(f.kinds.map((k) => k.name).sort(), ['action', 'input', 'output']);
  assert.deepEqual(f.services.map((s) => s.name), ['gopro.camera', 'plugins/gopro-camera', 'plugins/xiaomi-tv-display', 'xiaomi.tv.display']);
});

test('serviceNames：服务 + 能力包', () => {
  const cap = CAPS[0];
  assert.deepEqual(core.serviceNames(cap), ['plugins/xiaomi-tv-display', 'xiaomi.tv.display']);
});

test('高亮切片段并可合并', () => {
  assert.deepEqual(core.highlight('display.audio', 'audio'), [
    { text: 'display.', hit: false },
    { text: 'audio', hit: true },
  ]);
  assert.deepEqual(core.highlight('nothing', 'zzz'), [{ text: 'nothing', hit: false }]);
});

test('适用宿主：能按宿主筛、进 facets、能搜到', () => {
  const CAPS = [
    {
      capability_id: 'display.audio', declared_by: [], packages: [], keywords: [],
      hosts_effective: ['mac'], runs_on: ['mac'],
      definition: { group: 'display', kind: 'output' },
    },
    {
      capability_id: 'asset.inventory', declared_by: [], packages: [], keywords: [],
      hosts_effective: ['brain'], runs_on: ['brain'],
      definition: { group: 'asset', kind: 'system' },
    },
  ];
  const viewOf = (cap) => ({ ...(cap.definition || {}) });
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, host: 'mac' })), ['display.audio']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, host: 'brain' })), ['asset.inventory']);
  assert.deepEqual(ids(core.filterCaps(CAPS, { viewOf, query: 'brain' })), ['asset.inventory']);
  assert.deepEqual(core.facets(CAPS, viewOf).hosts.map((h) => h.name), ['brain', 'mac']);
});
