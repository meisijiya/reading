/* ==========================================================================
   读书知识库 · 证据结构化
   --------------------------------------------------------------------------
   作用：把既有 Markdown 里已经存在、但样式上不可见的结构推导成视觉身份。
   硬约束：docs 下的 md 一个字不改。这个文件只在运行时读 DOM。

   三条规则，各自对应一个「不这样做就会出错」的事实：

   1) 卡片定位符有 4 种真实形态，chip 必须显示书自己的编号，绝不合成假卡号：
        Q3-1 …            → Q3-1        （智能体漫游指南 / AI Agents in Depth）
        Q1 …              → Q1          （民法典100问，无模块段）
        §3 第3章 …        → §3          （凤凰架构/微服务/DDD/橙皮书/AI Prompt）
        …？（第1章）      → 第1章       （Vibe Coding，编号藏在标题末尾）
      前 3 个是书的主编号；第 4 种是 Vibe Coding 的真实定位符，同样不是合成的。

   2) 📖 原文只吸收「连续的引用块」；🧭/➕ 才吸收其后的普通段落。
      依据：民法典100问 464 条 📖 但 0 条 🧭、0 条 ➕——它的卡片是
      「原文块 + 编者普通段落」。若按贪心规则让 📖 吸收后续一切，
      编者的白话就会被画进朱色衬线的原文带里，用视觉撒谎，
      正好违反本站最核心的契约（原文永不冒充归纳）。
      连续的引用块合并成一条带，但**只在定位符相同时合并**：
      ch03 §2.3 与 ch03 §2.3.1 是两处出处，共用一个标签就是谎报。

   3) 前缀括号有半角 (ch13) 与全角（§10.3.2）两种，且定位符可能缺失。
      只认半角会让解构领域驱动设计的 509 条 📖 丢掉定位符。

   4) 🧭/➕ 写在**引用块里**是真实存在的第四种形态（AI Prompt、橙皮书、
      Vibe、凤凰、微服务、解构 六本各 5~8 条/模块）。视觉签名服从标记语义，
      不服从 markdown 排版——否则「青色虚线 = 归纳」这条约定就有反例，
      而反例是读者看不见、只有数数才发现的那种。

   5) **一个 <blockquote> 里塞着多段。** Python-Markdown 把空行分隔的
      多个引用块并进同一个 blockquote，内部是多个 <p>。所以判定必须
      逐段做，不能只看第一段——详见 splitMarkedBlock 的注释。
   ========================================================================== */
(function () {
  'use strict';

  /* ---------------------------------------------------------------- 定位符 */

  var ID_PATTERNS = [
    { rx: /^Q(\d+)-(\d+)[\s　]/, fmt: function (m) { return 'Q' + m[1] + '-' + m[2]; } },
    { rx: /^§\s*(\d+)/, fmt: function (m) { return '§' + m[1]; } },
    { rx: /^Q(\d+)[\s　]/, fmt: function (m) { return 'Q' + m[1]; } },
    { rx: /[（(]\s*第\s*(\d+)\s*章\s*[）)]/, fmt: function (m) { return '第' + m[1] + '章'; } }
  ];

  function extractId(text) {
    for (var i = 0; i < ID_PATTERNS.length; i++) {
      var m = text.match(ID_PATTERNS[i].rx);
      if (m) return ID_PATTERNS[i].fmt(m);
    }
    return null;
  }

  /* -------------------------------------------------------------- 小工具 */

  function h2Text(h2) {
    var c = h2.cloneNode(true);
    var links = c.querySelectorAll('.headerlink');
    for (var i = 0; i < links.length; i++) links[i].remove();
    return (c.textContent || '').replace(/\s+/g, ' ').trim();
  }

  /* 找第一个不在括号内的冒号，半角全角都认 */
  function findColon(t, from) {
    var depth = 0;
    for (var i = from; i < t.length; i++) {
      var c = t.charAt(i);
      if (c === '（' || c === '(') depth++;
      else if (c === '）' || c === ')') depth--;
      else if (depth === 0 && (c === '：' || c === ':')) return i;
    }
    return -1;
  }

  /* 精确删除元素开头的 n 个码元（跨多个文本节点） */
  function stripLeading(el, n) {
    var remain = n;
    var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (var i = 0; i < nodes.length && remain > 0; i++) {
      var t = nodes[i];
      var take = Math.min(remain, t.nodeValue.length);
      t.nodeValue = t.nodeValue.slice(take);
      remain -= take;
    }
    /* 清掉被摘空后残留的 <strong>，否则留下一个空标签 */
    var strongs = el.querySelectorAll('strong');
    for (var j = 0; j < strongs.length; j++) {
      if (!strongs[j].textContent.trim()) strongs[j].remove();
    }
    if (el.firstChild && el.firstChild.nodeType === 3) {
      el.firstChild.nodeValue = el.firstChild.nodeValue.replace(/^[\s　]+/, '');
    }
  }

  var MARKERS = { '📖': 'src', '🧭': 'sum', '➕': 'add' };
  var NAMES = { src: '📖 原文', sum: '🧭 归纳', add: '➕ 补充' };

  /* 只读地读出段首标记，并把「📖 原文 (ch13) ：」拆成 label + 定位符。
     必须用捕获组 m[1]：emoji 在 BMP 之外，m[0] 是「空白 + emoji」，
     charAt(m[0].length - 1) 取到的是代理对低位而不是 emoji 本身。 */
  function peekMarker(p) {
    var t = p.textContent || '';
    var m = t.match(/^[\s　]*([📖🧭➕])/u);
    if (!m) return null;

    var ci = findColon(t, m[0].length);
    var head = ci >= 0 ? t.slice(0, ci + 1) : t.slice(0, m[0].length);
    var inner = head.replace(/[：:]\s*$/, '').trim();
    var lm = inner.match(/[（(]([^）)]*)[）)]\s*$/);
    var loc = lm ? lm[1].trim() : '';
    /* 名字必须从**括号之前**截。否则「📖 原文（ch03 §2.1）」的 name 会
       连括号一起带上，再拼一个 loc，标签就成了「原文（ch03 §2.1）· ch03 §2.1」。 */
    var base = lm ? inner.slice(0, lm.index) : inner;
    var name = base.replace(/[📖🧭➕]\s*/u, '').trim();

    return {
      kind: MARKERS[m[1]],
      loc: loc,
      label: m[0].trim() + ' ' + (name || '') + (loc ? ' · ' + loc : '')
    };
  }

  /* 读出段首标记**并把前缀从 DOM 里摘掉**。有副作用。 */
  function consumeMarker(p) {
    var info = peekMarker(p);
    if (!info) return null;
    var t = p.textContent || '';
    var m = t.match(/^[\s　]*([📖🧭➕])/u);
    var ci = findColon(t, m[0].length);
    stripLeading(p, ci >= 0 ? ci + 1 : m[0].length);
    return info;
  }

  /* ---------------------------------------------------------- 证据分带 */

  function laneKindOf(el) {
    if (el.nodeType !== 1) return null;
    var tag = el.tagName;
    var isQuote = tag === 'BLOCKQUOTE';
    if (!isQuote && tag !== 'P') return null;
    var t = (el.textContent || '').replace(/^[\s　]+/, '');
    var m = t.match(/^([📖🧭➕])/u);
    if (!m) return null;
    var kind = MARKERS[m[1]];
    /* 原文必须是引用块——普通段落自称 📖 的一律不认。 */
    if (kind === 'src') return isQuote ? 'src' : null;
    /* 🧭/➕ 段落形态和引用块形态都收，见文件头规则 4。 */
    return kind;
  }

  /* 把一个块级节点切成若干「同标记 + 同定位符」的段组。
     Python-Markdown 会把**空行分隔的多个引用块并进同一个 <blockquote>**，
     内部是多个 <p>。只认第一个 <p> 会同时犯三个错：
       ① 后面所有段首标记一个都摘不掉，页面上留下满屏「📖 原文（§7.1.1）：」；
       ② 跟在后面的 `> 🧭 归纳` 被当成原文，画进朱色衬线的原文带；
       ③ 解构一张卡里 17 段、跨 §7.1~§7.3.2 十一处出处，被谎报成一个标签。
     返回 [] 表示「整块不是证据」，交给中性区处理。 */
  function splitMarkedBlock(el) {
    if (el.tagName === 'BLOCKQUOTE' || el.tagName === 'P') {
      /* 取**全部后代 <p>**，不只是直接子。
         书里正文会出现裸 HTML——智能体漫游指南在讲「在 <section>、<article>、
         <p> 标签处切分」，markdown 照单渲染成真元素，引用块内部就成了
         blockquote > section > article > p 的畸形嵌套。只认直接子的话，
         嵌在里面的标记一个都摘不掉，页面上原样留着「📖 原文 (ch16 §16.4)：」。 */
      var ps = el.tagName === 'P' ? [el] : el.querySelectorAll('p');
      if (!ps.length) {
        /* 单段落形态。laneKindOf 守住「裸段落自称 📖 不认」这条规则；
           注意这里必须 consumeMarker 而不是 peekMarker——只读不摘的话
           `🧭 归纳：…` 会原样留在归纳带开头。 */
        if (!laneKindOf(el)) return [];
        var only = consumeMarker(el);
        return only ? [{ kind: only.kind, loc: only.loc, label: only.label, parts: [el], shell: false }] : [];
      }

      /* 先只读地定位「第一个带标记的段落」：万一首段没标记（罕见但存在），
         后面的标记段落不能因为前导段落的归属问题整个漏掉。 */
      var first = null;
      for (var k = 0; k < ps.length; k++) {
        var pm = peekMarker(ps[k]);
        if (pm) { first = pm; break; }
      }
      if (!first) return [];

      var groups = [];
      var cur = null;

      for (var i = 0; i < ps.length; i++) {
        var child = ps[i];
        var info = consumeMarker(child);
        var kind = info ? info.kind : (cur ? cur.kind : first.kind);
        var loc = info ? info.loc : (cur ? cur.loc : first.loc);
        if (!cur || cur.kind !== kind || cur.loc !== loc) {
          cur = {
            kind: kind,
            loc: loc,
            label: info ? info.label : (cur ? cur.label : first.label),
            parts: []
          };
          groups.push(cur);
        } else if (info && info.label && !cur.label) {
          cur.label = info.label;
        }
        cur.parts.push(child);
      }

      /* 整块只有一组时整块搬走，原样保留全部标记结构（含畸形嵌套），零改造成本。
         拆成多组时必须逐组套引用壳——注意**判据是「本块被拆过」而不是
         「本组有几段」**：拆开后只有一段的组照样要壳，否则那个 <p> 会被
         裸塞进证据带，衬线原文带里就混进了没引号的段落。 */
      if (groups.length === 1) {
        groups[0].parts = [el];
        groups[0].shell = false;
      } else {
        groups.forEach(function (g) { g.shell = true; });
      }
      return groups;
    }
    return [];
  }

  function buildLane(kind, label) {
    var div = document.createElement('div');
    div.className = 'rd-ev rd-ev--' + kind;
    var lab = document.createElement('span');
    lab.className = 'rd-ev-label';
    lab.textContent = label;
    div.appendChild(lab);
    return div;
  }

  /* 往已开着的带里塞一组，或另起一条带。两种情形共用，判定只差「已开的带是谁」。 */
  function emitGroups(groups, lanes, openRef) {
    for (var g = 0; g < groups.length; g++) {
      var grp = groups[g];
      var open = openRef.v;
      var lane;
      /* 同类同定位符才合并；§7.1 与 §7.1.1 是两处出处，不能共用标签。 */
      if (open && open.kind === grp.kind && open.loc === grp.loc) {
        lane = open.el;
      } else {
        lane = buildLane(grp.kind, grp.label || NAMES[grp.kind]);
        lanes.push(lane);
        open = { kind: grp.kind, loc: grp.loc, el: lane };
      }
      if (grp.shell) {
        /* 拆壳：每组一个引用壳，保留各自的引用视觉 */
        var bq = document.createElement('blockquote');
        grp.parts.forEach(function (x) { bq.appendChild(x); });
        lane.appendChild(bq);
      } else {
        lane.appendChild(grp.parts[0]);
      }
      openRef.v = open;
    }
  }

  /* 把一张卡片的内容节点分组成「头部 + 若干证据带 + 中性尾部」。
     铁律：**标记节点必须先进带，再谈要不要合并**。
     反过来写（先 append 到上一条带、再建新带）会把「新的 🧭 段落」塞进
     「上一条仍开着的 📖 带」——编者的话被画进朱色衬线的原文带，
     是本站最核心契约（原文永不冒充归纳）的反面。
     另外旧写法在 open 为空时把节点 push 进 head，导致**每张卡的第一个
     证据块永远留在卡片正文里没样式，带只剩一个空壳**。 */
  function partition(nodes) {
    var head = [];
    var tail = [];
    var lanes = [];
    var openRef = { v: null };

    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      if (el.tagName === 'HR') continue;

      var groups = splitMarkedBlock(el);

      if (groups.length) {
        /* 一个块可能拆出多组（如 §7.1 / §7.1.1 / 🧭归纳 挤在同一个 blockquote）。
           拆组时若原节点被拆空，必须把它从流里摘掉——restructure 之后
           article 只保留搬进 head/lanes/tail 的节点，漏摘就是页面上多一份原文。 */
        if (groups.length > 1) el.remove();
        emitGroups(groups, lanes, openRef);
        continue;
      }

      /* 普通节点：归纳/补充带开着就归它；原文带开着也**不**归它，
         一律留在中性区。见文件头规则 2。 */
      var open = openRef.v;
      if (open && open.kind !== 'src') open.el.appendChild(el);
      else if (open) tail.push(el);
      else head.push(el);
    }
    return { head: head, lanes: lanes, tail: tail };
  }

  /* 卡片之外仍有证据：解构的「篇N 第N篇」、AI Prompt 的「§A 附录…」
     （字母章号，不匹配数字章号那套定位符）、Vibe 的「导读·…」——
     这些 h2 不带定位符、不是卡，可它们下面照样压着 180 段
     📖/🧭/➕。不给签名，全站就有这一批证据长得跟别处不一样。
     所以同一套分带逻辑在这里再跑一遍；带外的中性节点**一律原地不动**。 */
  function hasMarkedBlock(el) {
    if (el.tagName !== 'BLOCKQUOTE' && el.tagName !== 'P') return false;
    if (peekMarker(el)) return true;
    var ps = el.querySelectorAll(':scope > p');
    for (var i = 0; i < ps.length; i++) if (peekMarker(ps[i])) return true;
    return false;
  }

  function bandLoose(article, wrap) {
    var loose = [].slice.call(article.children).filter(function (el) {
      if (wrap && el === wrap) return false;
      if (el.classList && el.classList.contains('rd-idstrip')) return false;
      return true;
    });

    var anchor = null;
    for (var i = 0; i < loose.length; i++) {
      if (hasMarkedBlock(loose[i])) { anchor = loose[i]; break; }
    }
    if (!anchor) return 0;

    var ph = document.createElement('span');
    article.insertBefore(ph, anchor);

    var lanes = [];
    var openRef = { v: null };
    for (var j = 0; j < loose.length; j++) {
      var el = loose[j];
      if (el.tagName === 'HR') continue;
      var groups = splitMarkedBlock(el);
      if (!groups.length) continue;            /* 没标记 = 原地不动 */
      if (groups.length > 1) el.remove();
      emitGroups(groups, lanes, openRef);
    }

    if (!lanes.length) { ph.remove(); return 0; }
    var box = document.createElement('div');
    box.className = 'rd-ev-loose';
    lanes.forEach(function (l) { box.appendChild(l); });
    ph.replaceWith(box);
    return lanes.length;
  }

  /* ------------------------------------------------------------ 卡片化 */

  function isCardHeading(h2) {
    return !!extractId(h2Text(h2));
  }

  function restructure(article) {
    var kids = Array.prototype.slice.call(article.children);
    var heads = [];
    for (var i = 0; i < kids.length; i++) {
      if (kids[i].tagName === 'H2' && isCardHeading(kids[i])) heads.push(kids[i]);
    }
    /* 少于 2 张卡就不动：INDEX / 速查表 / fulltext 都不该被改结构 */
    if (heads.length < 2) return null;

    /* 先插占位符再搬运节点。反过来做会炸：
       循环里把 h2 appendChild 进 card 之后，原来的 parentNode 已经变成 card 本身，
       parent.insertBefore(wrap, …) 就会抛 "new child element contains the parent"。 */
    var anchor = heads[0];
    var parent = anchor.parentNode;
    var placeholder = document.createElement('div');
    parent.insertBefore(placeholder, anchor);

    /* 卡片自带边框，卡之间那条 --- 变成冗余；导读块后那条同理 */
    var lead = anchor.previousElementSibling;
    if (lead && lead.tagName === 'HR') lead.remove();

    var cards = [];

    heads.forEach(function (h2, n) {
      var stop = n + 1 < heads.length ? heads[n + 1] : null;
      var slice = [];
      var collecting = false;
      for (var i = 0; i < kids.length; i++) {
        var el = kids[i];
        if (el === h2) { collecting = true; continue; }
        if (el === stop) break;
        if (!collecting) continue;
        if (el.tagName === 'HR') { el.remove(); break; }   /* 必须真删，不能只跳过 */
        slice.push(el);
      }

      var id = extractId(h2Text(h2));
      var parts = partition(slice);

      var card = document.createElement('article');
      card.className = 'rd-card';

      var head = document.createElement('div');
      head.className = 'rd-card-head';
      var chip = document.createElement('span');
      chip.className = 'rd-chip';
      chip.textContent = id;
      head.appendChild(chip);

      /* 从元数据列表里取「章节: xxx」作为卡片头部的定位信息 */
      var meta = null;
      for (var j = 0; j < parts.head.length; j++) {
        if (parts.head[j].tagName === 'UL') { meta = parts.head[j]; break; }
      }
      var srcText = '';
      if (meta) {
        var m = (meta.textContent || '').match(/章节\s*[:：]\s*([^\s（(]+)/);
        if (m) srcText = m[1];
      }
      if (srcText && srcText !== id) {
        var src = document.createElement('span');
        src.className = 'rd-src';
        src.textContent = srcText;
        head.appendChild(src);
      }

      card.appendChild(head);
      card.appendChild(h2);

      for (var k = 0; k < parts.head.length; k++) {
        var el2 = parts.head[k];
        if (el2 === meta) { el2.className = 'rd-card-meta'; el2.removeAttribute('start'); }
        card.appendChild(el2);
      }
      for (var l = 0; l < parts.lanes.length; l++) card.appendChild(parts.lanes[l]);
      for (var m2 = 0; m2 < parts.tail.length; m2++) card.appendChild(parts.tail[m2]);

      cards.push({ node: card, id: id, h2: h2 });
    });

    var wrap = document.createElement('div');
    wrap.className = 'rd-cards';
    cards.forEach(function (c) { wrap.appendChild(c.node); });
    parent.replaceChild(wrap, placeholder);

    return { wrap: wrap, cards: cards };
  }

  /* ------------------------------------------------------- 右栏卡号索引 */

  /* 右栏目录有两份 DOM 实例：桌面侧栏一份、移动抽屉一份。
       用 querySelector 只会改到**第一份**，移动端那份从头到尾保持
       「20 条长标题原样堆叠」的老样子，而且没有任何报错。 */
  function rewriteToc() {
    var navs = document.querySelectorAll('.md-nav--secondary');
    var total = 0;
    for (var n = 0; n < navs.length; n++) {
      var toc = navs[n];
      var links = toc.querySelectorAll('ul[data-md-component="toc"] > li > a.md-nav__link');
      var hits = 0;
      for (var i = 0; i < links.length; i++) {
        var span = links[i].querySelector('.md-ellipsis') || links[i];
        var text = (span.textContent || '').replace(/\s+/g, ' ').trim();
        var id = extractId(text);
        if (!id) continue;
        var rest = text.replace(/^Q\d+(-\d+)?[\s　]*/, '')
          .replace(/^§\s*\d+[\s　]*/, '')
          .replace(/[（(]\s*第\s*\d+\s*章\s*[）)]\s*$/, '')
          .trim();
        links[i].innerHTML = '';
        var b = document.createElement('b');
        b.className = 'rd-toc-id';
        b.textContent = id;
        var s = document.createElement('span');
        s.className = 'rd-toc-label';
        s.textContent = rest || text;
        links[i].appendChild(b);
        links[i].appendChild(s);
        hits++;
      }
      if (hits >= 2) toc.classList.add('rd-toc-index');
      total += hits;
    }
    return total;
  }

  /* ------------------------------------------------------ 移动端卡号横条 */

  function buildStrip(result) {
    if (!result || !result.cards.length) return;
    var strip = document.createElement('nav');
    strip.className = 'rd-idstrip';
    strip.setAttribute('aria-label', '卡号索引');

    var label = document.createElement('span');
    label.className = 'rd-idstrip-label';
    label.textContent = result.cards.length + ' 张卡';
    strip.appendChild(label);

    var track = document.createElement('div');
    track.className = 'rd-idstrip-track';
    result.cards.forEach(function (c) {
      var a = document.createElement('a');
      a.className = 'rd-chip';
      a.href = '#' + (c.h2.id || '');
      a.textContent = c.id;
      track.appendChild(a);
    });
    strip.appendChild(track);
    result.wrap.parentNode.insertBefore(strip, result.wrap);
  }

  /* ------------------------------------------------------------ 页面分类 */

  function decoratePage() {
    var article = document.querySelector('.md-typeset');
    if (!article || article.dataset.rdDone === '1') return;
    article.dataset.rdDone = '1';

    var path = decodeURIComponent(location.pathname);

    /* 原书档案页：与卡片页区分的表面 + 档案横幅 */
    if (/\/00-.*档案\/fulltext\//.test(path)) {
      article.classList.add('rd-archive');
      var h1 = article.querySelector('h1');
      var banner = document.createElement('div');
      banner.className = 'rd-archive-banner';
      banner.textContent = '逐字档案 · 非蒸馏结论 ｜ 公式与图表排版可能丢失，核对请对照原书';
      if (h1) h1.parentNode.insertBefore(banner, h1.nextSibling);
      else article.insertBefore(banner, article.firstChild);
      return;
    }

    /* 速查表：表头吸顶 */
    if (/\/99-速查表\/?$/.test(path)) {
      article.classList.add('rd-lookup');
      return;
    }

    var result = restructure(article);
    if (result) {
      rewriteToc();
      buildStrip(result);
    }
    bandLoose(article, result ? result.wrap : null);
  }

  /* -------------------------------------------- navigation.instant 兼容 */

  function schedule(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  }

  function onEachPage(fn) {
    /* Material 的 document$ 是全局 observable，但它由 bundle 在本页脚本之后
       才定义，直接用会 ReferenceError。这里轮询等待，超时后降级为一次执行。
       只订阅一次：subscribe 会「立即以当前页调用一次」，重复订阅等于跑两遍。 */
    var tries = 0;
    var iv = setInterval(function () {
      if (typeof window.document$ !== 'undefined') {
        clearInterval(iv);
        window.document$.subscribe(function () { schedule(fn); });
      } else if (++tries > 200) {
        clearInterval(iv);
        schedule(fn);
      }
    }, 50);
  }

  onEachPage(decoratePage);
})();