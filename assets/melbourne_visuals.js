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

  function bar(label, amount, scale, displayed, alternate) {
    if (!Number.isFinite(amount)) return '';
    const width = Math.max(0, Math.min(100, 100 * amount / Math.max(scale, 0.001)));
    const kind = alternate ? ' vis-muted-fill' : '';
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

  function paired(label, melbourne, pooled, digits, lowerBetter) {
    if (melbourne === null || pooled === null || pooled <= 0) {
      return '<p class="muted">This comparison needs more verified team-level data.</p>';
    }
    const scale = Math.max(melbourne, pooled) * 1.07;
    return '<div class="vis-comparison"><h4>' + text(label) +
      ' <span class="muted">(' + (lowerBetter ? 'lower' : 'higher') + ' is better)</span></h4>' +
      bar('Melbourne', melbourne, scale, melbourne.toFixed(digits), false) +
      bar('Uploaded teams', pooled, scale, pooled.toFixed(digits), true) + '</div>';
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
    if (!eligible.length) return '<p class="muted">No players currently meet this qualification threshold.</p>';
    const scale = Math.max.apply(null, eligible.map(function (p) { return value(p[metric]); })) * 1.07 || 1;
    return eligible.map(function (p) {
      const amount = value(p[metric]);
      return bar(String(p.Player) + ' · ' + extras.sample(p), amount, scale,
        amount.toFixed(extras.decimals), false);
    }).join('');
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
        '<p class="vis-legend"><span><i class="vis-key vis-wins"></i>' + wins + ' wins</span>' +
        '<span><i class="vis-key vis-losses"></i>' + losses + ' losses</span>' +
        '<span><i class="vis-key vis-draws"></i>' + draws + ' draws</span></p>';
    }
    if (rf !== null && ra !== null) {
      const made = rf / games, allowed = ra / games, scale = Math.max(made, allowed) * 1.07;
      season += '<h4>Runs per official game</h4>' +
        bar('Scored', made, scale, made.toFixed(2), false) +
        bar('Allowed', allowed, scale, allowed.toFixed(2), true) +
        '<p class="muted">Run differential: ' + (rf - ra > 0 ? '+' : '') + text(rf - ra) +
        ' across ' + text(games) + ' games. Official ladder data, not summed partial boxes.</p>';
    }

    const battingCompare = paired('OPS (estimated)', value(mb.OPS), pooledOps, 3, false) +
      paired('AVG', value(mb.AVG), pooledAvg, 3, false);
    const pitchingCompare = paired('ERA', value(mp.ERA), pooledEra, 2, true) +
      paired('WHIP', value(mp.WHIP), pooledWhip, 2, true);
    const minPa = Math.ceil(2 * games);
    const minOuts = Math.ceil(games);
    const hitterRows = peopleRows(batters, 'OPS', 6, {
      qualifies: function (r) { return value(r.PA) >= minPa; },
      sample: function (r) { return String(r.PA) + ' PA'; },
      decimals: 3
    }, false);
    const pitcherRows = peopleRows(pitchers, 'ERA', 6, {
      qualifies: function (r) { return outs(r.IP) !== null && outs(r.IP) >= minOuts; },
      sample: function (r) { return String(r.IP) + ' IP'; },
      decimals: 2
    }, true);

    root.innerHTML =
      card('Season record & run balance', 'Official standings through ' + games + ' games.', season, true) +
      card('Melbourne batting vs uploaded teams',
        'Team AVG and estimated OPS. Higher is better.', battingCompare, false) +
      card('Melbourne pitching vs uploaded teams',
        'Team ERA and WHIP. Lower is better.', pitchingCompare, false) +
      card('Qualified Melbourne hitters · OPS',
        'Top six by OPS; at least ' + minPa + ' PA (2 PA per Melbourne game). Includes qualified players only.', hitterRows, false) +
      card('Qualified Melbourne pitchers · ERA',
        'Lowest ERA first; at least ' + minOuts + ' recorded outs (' + Math.floor(minOuts / 3) +
        '.' + (minOuts % 3) + ' IP). Smaller ERA is better.', pitcherRows, false);

    const note = document.getElementById('melbourneVisualsSources');
    if (note) {
      note.textContent = 'Charts recalculate from the current uploaded data. Pooled comparisons use ' +
        teamBat.length + ' uploaded team totals, including Melbourne, not all 16 VSBL teams. ' +
        'Historical OBP/OPS estimates, incomplete opponent game coverage, provisional early-game pitching, ' +
        'and small samples affect interpretation. No unsupported game-by-game trends are shown.';
    }
  }

  window.renderMelbourneVisuals = renderMelbourneVisuals;
}());
