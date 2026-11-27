/* Melbourne visual insights: display-only charts derived from existing dashboard data. */
(function () {
  'use strict';

  function value(raw) {
    if (raw === null || raw === undefined || String(raw).trim() === '') return null;
    const n = Number(String(raw).replace(/[%*]/g, '').trim());
    return Number.isFinite(n) ? n : null;
  }

  function text(raw) {
    return String(raw === undefined || raw === null ? '' : raw)
      .replace(/[&<>"']/g, function (c) {
        return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
      });
  }

  function outs(raw) {
    const match = String(raw === undefined ? '' : raw).match(/^(\d+)\.([012])$/);
    return match ? Number(match[1]) * 3 + Number(match[2]) : null;
  }

  function total(rows, field) {
    if (!rows.length) return null;
    const vals = rows.map(function (r) { return value(r[field]); });
    return vals.some(function (v) { return v === null; })
      ? null : vals.reduce(function (a, b) { return a + b; }, 0);
  }

  function bar(label, amount, scale, displayed, alternate, performance) {
    if (!Number.isFinite(amount)) return '';
    const width = Math.max(0, Math.min(100, 100 * amount / Math.max(scale, 0.001)));
    const kind = alternate ? ' vis-muted-fill' :
      performance === 'better' ? ' vis-better-fill' :
      performance === 'worse' ? ' vis-worse-fill' :
      performance === 'equal' ? ' vis-muted-fill' : '';
    return '<div class="vis-bar-row"><span class="vis-label">' + text(label) +
      '</span><span class="vis-track" aria-hidden="true"><span class="vis-fill' + kind +
      '" style="width:' + width.toFixed(1) + '%"></span></span>' +
      '<strong class="vis-number">' + text(displayed) + '</strong></div>';
  }

  function card(title, explanation, body, full) {
    return '<section class="card vis-card' + (full ? ' vis-full' : '') + '">' +
      '<h3>' + text(title) + '</h3><p class="muted">' + text(explanation) + '</p>' +
      body + '</section>';
  }

  // Baseball-style rates display .255 and .729 rather than 0.255 and 0.729.
  function displayRate(amount, digits, baseballRate) {
    const result = amount.toFixed(digits);
    return baseballRate && result.startsWith('0.') ? result.slice(1) : result;
  }

  function paired(label, melbourne, pooled, digits, baseballRate) {
    if (melbourne === null || pooled === null || pooled <= 0) {
      return '<p class="muted">This comparison needs more verified team-level data.</p>';
    }
    const scale = Math.max(melbourne, pooled) * 1.07;
    return '<div class="vis-comparison"><h4>' + text(label) + '</h4>' +
      bar('Melbourne', melbourne, scale, displayRate(melbourne, digits, baseballRate), false) +
      bar('League', pooled, scale, displayRate(pooled, digits, baseballRate), true) + '</div>';
  }

  function peopleRows(rows, metric, limit, extras, ascending) {
    const eligible = rows
      .filter(function (r) {
        return !r['Team Total'] && Number.isFinite(value(r[metric])) && extras.qualifies(r);
      })
      .slice()
      .sort(function (a, b) {
        const diff = ascending ? value(a[metric]) - value(b[metric]) : value(b[metric]) - value(a[metric]);
        return diff || String(a.Player).localeCompare(String(b.Player));
      })
      .slice(0, limit);
    const leagueValue = extras.leagueValue;
    const hasLeague = Number.isFinite(leagueValue);
    const amounts = eligible.map(function (p) { return value(p[metric]); });
    if (hasLeague) amounts.push(leagueValue);
    const scale = (amounts.length ? Math.max.apply(null, amounts) : 1) * 1.07 || 1;
    let result = eligible.length ? eligible.map(function (p) {
      const amount = value(p[metric]);
      // Qualified hitters: OPS above League is green. Qualified pitchers:
      // ERA below League is green. Worse results are red, ties are gray.
      const performance = hasLeague
        ? (amount === leagueValue ? 'equal' :
          ((ascending ? amount < leagueValue : amount > leagueValue) ? 'better' : 'worse'))
        : null;
      return bar(String(p.Player) + ' · ' + extras.sample(p), amount, scale,
        displayRate(amount, extras.decimals, extras.baseballRate), false, performance);
    }).join('') : '<p class="muted">No players currently meet this qualification threshold.</p>';
    if (hasLeague) {
      result += '<div class="vis-league-row">' +
        bar('League ' + metric, leagueValue, scale,
          displayRate(leagueValue, extras.decimals, extras.baseballRate), true) + '</div>';
    }
    return result;
  }

  // Cumulative hit-type breakdowns; no ball-flight or spray coordinates are implied.
  const hitKinds = [
    { key: 'single', short: '1B', title: 'Singles' },
    { key: 'double', short: '2B', title: 'Doubles' },
    { key: 'triple', short: '3B', title: 'Triples' },
    { key: 'homeRun', short: 'HR', title: 'Home Runs' }
  ];

  function hitCounts(row) {
    const hits = value(row.H);
    const doubles = value(row['2B']);
    const triples = value(row['3B']);
    const homeRuns = value(row.HR);
    if ([hits, doubles, triples, homeRuns].some(function (v) {
      return v === null || v < 0 || !Number.isInteger(v);
    })) return null;
    const singles = hits - doubles - triples - homeRuns;
    if (singles < 0) return null;
    return { hits: hits, single: singles, double: doubles, triple: triples, homeRun: homeRuns };
  }

  function hitSegments(counts, denominator) {
    if (!counts || !denominator) return '';
    return hitKinds.map(function (type) {
      const count = counts[type.key];
      if (count === 0) return '';
      return '<span class="vis-hit-segment vis-hit-' + type.key +
        '" style="width:' + (count * 100 / denominator).toFixed(3) +
        '%" title="' + text(type.title + ': ' + count) + '"></span>';
    }).join('');
  }

  function hitLegend(counts) {
    return '<div class="vis-hit-legend">' + hitKinds.map(function (type) {
      const count = counts[type.key];
      return '<span><i class="vis-hit-key vis-hit-' + type.key +
        '"></i><strong>' + text(type.short) + '</strong> ' + text(count) +
        ' <span class="muted">(' + (count * 100 / counts.hits).toFixed(1) +
        '%)</span></span>';
    }).join('') + '</div>';
  }

  function renderHitBreakdown(teamRow) {
    const counts = hitCounts(teamRow);
    if (!counts || counts.hits === 0) {
      return '<p class="muted">No valid team hit breakdown is available.</p>';
    }
    return '<p class="vis-hit-summary"><strong>' + text(counts.hits) +
      ' Hits</strong> · ' + text(counts.single + counts.double + counts.triple + counts.homeRun) +
      ' Recorded by Hit Type</p>' +
      '<div class="vis-hit-track vis-hit-team" role="img" aria-label="' +
      text(hitKinds.map(function (type) { return type.title + ': ' + counts[type.key]; }).join(', ')) +
      '">' + hitSegments(counts, counts.hits) + '</div>' + hitLegend(counts) +
      '<p class="muted">Singles = Total Hits − Doubles − Triples − Home Runs.</p>';
  }

  function renderHitLeaders(batters) {
    const players = batters
      .filter(function (r) { return !r['Team Total']; })
      .map(function (r) { return { row: r, counts: hitCounts(r) }; })
      .filter(function (r) { return r.counts && r.counts.hits > 0; })
      .sort(function (a, b) {
        return b.counts.hits - a.counts.hits ||
          String(a.row.Player).localeCompare(String(b.row.Player));
      }).slice(0, 8);
    if (!players.length) return '<p class="muted">No player hits are currently available.</p>';
    const maxHits = players[0].counts.hits;
    return '<div class="vis-hit-players">' + players.map(function (p) {
      const player = String(p.row.Player);
      const pa = value(p.row.PA);
      const name = player + (pa === null ? '' : ' · ' + pa + ' PA');
      return '<div class="vis-hit-player"><span class="vis-hit-player-name">' +
        text(name) + '</span><span class="vis-hit-track" role="img" aria-label="' +
        text(player + ': ' + p.counts.hits + ' hits; ' +
          hitKinds.map(function (kind) { return kind.title + ': ' + p.counts[kind.key]; }).join(', ')) +
        '">' + hitSegments(p.counts, maxHits) + '</span><strong class="vis-number">' +
        text(p.counts.hits) + ' H</strong></div>';
    }).join('') + '</div><div class="vis-hit-legend vis-hit-legend-compact">' +
    hitKinds.map(function (type) {
      return '<span><i class="vis-hit-key vis-hit-' + type.key +
        '"></i>' + text(type.short) + '</span>';
    }).join('') + '</div>';
  }

  function renderMelbourneVisuals(d) {
    const root = document.getElementById('melbourneVisualsContent');
    if (!root) return;
    const m = d.melbourne || {};
    const batters = Array.isArray(m.batting) ? m.batting : [];
    const pitchers = Array.isArray(m.pitching) ? m.pitching : [];
    const mb = batters.find(function (r) { return r['Team Total']; });
    const mp = pitchers.find(function (r) { return r['Team Total']; });
    const official = d.metadata || {};
    const games = value(official.melbourneGames) || value(official.melbournePlayerGames);
    if (!mb || !mp || !games) {
      root.innerHTML = '<p class="muted">The Melbourne cumulative totals are not yet available for charts.</p>';
      return;
    }

    const teamBat = batters.concat((d.opponents || {}).batting || []).filter(function (r) { return r['Team Total']; });
    const teamPit = pitchers.concat((d.opponents || {}).pitching || []).filter(function (r) { return r['Team Total']; });
    const ab = total(teamBat, 'AB');
    const h = total(teamBat, 'H');
    const bb = total(teamBat, 'BB');
    const doubles = total(teamBat, '2B');
    const triples = total(teamBat, '3B');
    const hr = total(teamBat, 'HR');
    const pooledAvg = ab && h !== null ? h / ab : null;
    const pooledSlg = ab && [h, doubles, triples, hr].every(function (v) { return v !== null; })
      ? (h + doubles + 2 * triples + 3 * hr) / ab : null;
    const pooledObp = ab !== null && bb !== null && h !== null && ab + bb > 0
      ? (h + bb) / (ab + bb) : null;
    const pooledOps = pooledObp === null || pooledSlg === null ? null : pooledObp + pooledSlg;

    const validOuts = teamPit.map(function (r) { return outs(r.IP); });
    const pooledIp = validOuts.length && validOuts.every(function (v) { return v !== null; })
      ? validOuts.reduce(function (a, b) { return a + b; }, 0) / 3 : null;
    const ph = total(teamPit, 'H');
    const pbb = total(teamPit, 'BB');
    const per = total(teamPit, 'ER');
    const pooledEra = pooledIp && per !== null ? 9 * per / pooledIp : null;
    const pooledWhip = pooledIp && ph !== null && pbb !== null ? (ph + pbb) / pooledIp : null;

    const record = String(official.melbourneRecord || '').split(/[–—-]/).map(Number);
    const wins = record.length === 3 && record.every(Number.isFinite) ? record[0] : null;
    const losses = wins !== null ? record[1] : null;
    const draws = wins !== null ? record[2] : null;
    const rf = value(official.melbourneRF);
    const ra = value(official.melbourneRA);
    let season = '';
    if (wins !== null && wins + losses + draws > 0) {
      const n = wins + losses + draws;
      season += '<div class="vis-record" role="img" aria-label="' +
        text(wins + ' wins, ' + losses + ' losses and ' + draws + ' draws') + '">' +
        '<span class="vis-wins" style="width:' + (100 * wins / n).toFixed(1) + '%"></span>' +
        '<span class="vis-losses" style="width:' + (100 * losses / n).toFixed(1) + '%"></span>' +
        '<span class="vis-draws" style="width:' + (100 * draws / n).toFixed(1) + '%"></span></div>' +
        '<p class="vis-legend"><span><i class="vis-key vis-wins"></i>' + wins + ' Wins</span>' +
        '<span><i class="vis-key vis-losses"></i>' + losses + ' Losses</span>' +
        '<span><i class="vis-key vis-draws"></i>' + draws + ' Draws</span></p>';
    }
    if (rf !== null && ra !== null) {
      const made = rf / games, allowed = ra / games, scale = Math.max(made, allowed) * 1.07;
      season += '<h4>Runs per Official Game</h4>' +
        bar('Scored', made, scale, made.toFixed(2), false) +
        bar('Allowed', allowed, scale, allowed.toFixed(2), true) +
        '<p class="muted">Run Differential: ' + (rf - ra > 0 ? '+' : '') + text(rf - ra) +
        ' across ' + text(games) + ' games. Official ladder data, not summed partial boxes.</p>';
    }

    const battingCompare = paired('OPS', value(mb.OPS), pooledOps, 3, true) +
      paired('AVG', value(mb.AVG), pooledAvg, 3, true);
    const pitchingCompare = paired('ERA', value(mp.ERA), pooledEra, 2, false) +
      paired('WHIP', value(mp.WHIP), pooledWhip, 2, false);
    const minPa = Math.ceil(2 * games);
    const minOuts = Math.ceil(games);
    const hitterRows = peopleRows(batters, 'OPS', 6, {
      qualifies: function (r) { return value(r.PA) >= minPa; },
      sample: function (r) { return String(r.PA) + ' PA'; },
      decimals: 3,
      baseballRate: true,
      leagueValue: pooledOps
    }, false);
    const pitcherRows = peopleRows(pitchers, 'ERA', 6, {
      qualifies: function (r) { return outs(r.IP) !== null && outs(r.IP) >= minOuts; },
      sample: function (r) { return String(r.IP) + ' IP'; },
      decimals: 2,
      baseballRate: false,
      leagueValue: pooledEra
    }, true);

    root.innerHTML =
      card('Season Record & Run Balance', 'Official standings through ' + games + ' games.', season, true) +
      card('Melbourne Batting vs. League',
        'Team AVG & OPS compared to league totals', battingCompare, false) +
      card('Melbourne Pitching vs. League',
        'Team ERA & WHIP compared to league totals', pitchingCompare, false) +
      card('Qualified Melbourne Hitters - OPS',
        'Top six by OPS; at least ' + minPa + ' PA (2 PA per Melbourne game). Includes qualified players only.', hitterRows, false) +
      card('Qualified Melbourne Pitchers - ERA',
        'Sorted by ERA; at least ' + minOuts + ' recorded outs (' + Math.floor(minOuts / 3) +
        '.' + (minOuts % 3) + ' IP).', pitcherRows, false) +
      card('Melbourne Hit Distribution',
        'Season hit types from the Melbourne cumulative batting totals.',
        renderHitBreakdown(mb), false) +
      card('Melbourne Hit Leaders',
        'Top eight players by hits; bars show singles, doubles, triples and home runs.',
        renderHitLeaders(batters), false);

    const note = document.getElementById('melbourneVisualsSources');
    if (note) {
      note.textContent = 'Charts recalculate from the current uploaded data. League comparisons use ' +
        teamBat.length + ' uploaded team totals, including Melbourne, not all 16 VSBL teams. ' +
        'Historical OBP/OPS calculation limitations, incomplete opponent game coverage, provisional early-game pitching, ' +
        'and small samples affect interpretation. No unsupported game-by-game trends are shown.';
    }
  }

  window.renderMelbourneVisuals = renderMelbourneVisuals;
}());
