let currentTool = 'xiaoliuren';

function switchTool(name) {
  currentTool = name;
  document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('resultArea').classList.remove('show');
  document.getElementById('resultArea').innerHTML = '';
  renderForm(name);
}

function renderForm(name) {
  const area = document.getElementById('formArea');
  const forms = {
    xiaoliuren: `<div class="form-card">
      <h3 style="color:var(--g)">🖐 小六壬 · 掌诀定位</h3>
      <div class="row">
        <div><label>农历月</label><input id="xlr_m" type="number" value="1" min="1" max="12"></div>
        <div><label>农历日</label><input id="xlr_d" type="number" value="1" min="1" max="30"></div>
        <div><label>时辰</label><select id="xlr_h">${['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'].map(h=>`<option>${h}</option>`).join('')}</select></div>
      </div>
      <button class="btn" onclick="divineXiaoliuren()">掐指一算</button>
    </div>`,
    meihua: `<div class="form-card">
      <h3 style="color:var(--g)">🌸 梅花易数 · 万物起卦</h3>
      <label>起卦方式</label>
      <select id="mh_method" onchange="toggleMHMethod()">
        <option value="number">数字起卦</option><option value="time">时间起卦</option><option value="text">文字起卦</option>
      </select>
      <div id="mh_num"><label>输入2-3个数字(用逗号分隔)</label><input id="mh_nums" placeholder="例如: 37,5"></div>
      <div id="mh_time" style="display:none"><div class="row"><div><label>年</label><input id="mh_y" type="number" value="2026"></div><div><label>月</label><input id="mh_m" type="number" value="6"></div><div><label>日</label><input id="mh_d" type="number" value="13"></div><div><label>时</label><input id="mh_h" type="number" value="12"></div></div></div>
      <div id="mh_text" style="display:none"><label>输入任意文字</label><input id="mh_txt" placeholder="想到什么写什么"></div>
      <button class="btn" onclick="divineMeihua()">起卦</button>
    </div>`,
    liuyao: `<div class="form-card">
      <h3 style="color:var(--g)">🪙 六爻 · 铜钱摇卦</h3>
      <div class="coin-area"><div class="coin" onclick="flipCoin(0)">🪙</div><div class="coin" onclick="flipCoin(1)">🪙</div><div class="coin" onclick="flipCoin(2)">🪙</div></div>
      <p style="text-align:center;color:#888;font-size:0.8em" id="ly_status">点硬币翻面，然后点"记下这一爻"。摇第1次(共6次)</p>
      <div style="display:flex;gap:8px;margin:8px 0;flex-wrap:wrap" id="ly_result"></div>
      <button class="btn" id="ly_record" onclick="recordYao()">记下这一爻 (还剩6次)</button>
      <label>问什么事</label><select id="ly_type"><option>考试</option><option>求财</option><option>感情</option><option>健康</option><option>寻人</option><option>其他</option></select>
      <button class="btn" id="ly_submit" onclick="divineLiuyao()" style="display:none">开始占卜</button>
    </div>`,
  };
  area.innerHTML = forms[name] || '<p style="color:#888;text-align:center;padding:40px">即将推出</p>';
  if (name === 'liuyao') initLiuyao();
}

// ── 小六壬 ──
async function divineXiaoliuren() {
  const m = document.getElementById('xlr_m').value;
  const d = document.getElementById('xlr_d').value;
  const h = document.getElementById('xlr_h').value;
  showLoading();
  const res = await fetch('/api/xiaoliuren', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({month:parseInt(m),day:parseInt(d),hour_name:h})});
  const data = await res.json();
  hideLoading();
  if (data.success) {
    const d2 = data.data;
    let steps = d2.steps.map(s => `<p>→ ${s.action}：<b>${s.landing}</b></p>`).join('');
    document.getElementById('resultArea').innerHTML = `<div class="big-verdict">${d2.emoji} ${d2.result}</div><div class="poem">${d2.poem}</div><div class="steps">📐 推算过程：${steps}</div><div class="advice">💡 <em>讲人话就是：</em>${d2.advice}</div>`;
  } else { alert(data.error); }
  document.getElementById('resultArea').classList.add('show');
}

// ── 梅花 ──
function toggleMHMethod() {
  const m = document.getElementById('mh_method').value;
  document.getElementById('mh_num').style.display = m==='number'?'block':'none';
  document.getElementById('mh_time').style.display = m==='time'?'block':'none';
  document.getElementById('mh_text').style.display = m==='text'?'block':'none';
}

async function divineMeihua() {
  const method = document.getElementById('mh_method').value;
  let values = {};
  if (method==='number') values.numbers = document.getElementById('mh_nums').value.split(',').map(Number).filter(n=>!isNaN(n));
  else if (method==='time') values = {year:document.getElementById('mh_y').value|0,month:document.getElementById('mh_m').value|0,day:document.getElementById('mh_d').value|0,hour:document.getElementById('mh_h').value|0};
  else values.text = document.getElementById('mh_txt').value;
  showLoading();
  const res = await fetch('/api/meihua', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({method,values})});
  const data = await res.json();
  hideLoading();
  if (data.success) {
    const d = data.data;
    let steps = d.calc_steps.map(s => `<p>→ ${s}</p>`).join('');
    document.getElementById('resultArea').innerHTML = `<div class="big-verdict">${d.emoji} ${d.relation} · ${d.verdict}</div><p style="font-size:1.1em;color:#aaa">本卦：${d.upper_gua.symbol}${d.lower_gua.symbol} ${d.upper_gua.name}上${d.lower_gua.name}下</p><div class="steps">📐 推算过程：${steps}</div><div class="advice">💡 <em>讲人话就是：</em>${d.detail}</div>`;
  } else { alert(data.error); }
  document.getElementById('resultArea').classList.add('show');
}

// ── 六爻 ──
let lyCoins = [0,0,0], lyCount = 0, lyLines = [];

function initLiuyao() { lyCoins=[0,0,0]; lyCount=0; lyLines=[]; updateCoins(); document.getElementById('ly_record').style.display='block'; document.getElementById('ly_submit').style.display='none'; document.getElementById('ly_result').innerHTML=''; document.getElementById('ly_status').textContent='点硬币翻面，然后点"记下这一爻"。摇第1次(共6次)'; }

function flipCoin(i) { lyCoins[i]=1-lyCoins[i]; updateCoins(); }

function updateCoins() {
  document.querySelectorAll('.coin').forEach((c,i) => {
    c.textContent = lyCoins[i] ? '⚈' : '⚀';
    c.style.background = lyCoins[i] ? 'var(--g)' : 'var(--c2)';
    c.style.color = lyCoins[i] ? '#1a1a24' : '#aaa';
  });
}

function recordYao() {
  const heads = lyCoins.filter(c=>c===1).length;
  let result = heads===3?'老阳':heads===0?'老阴':heads===2?'少阳':'少阴';
  lyLines.push(result); lyCount++;
  document.getElementById('ly_result').innerHTML += `<span style="padding:4px 8px;background:var(--c2);border-radius:6px;font-size:0.8em">${lyCount}:${result}</span>`;
  if (lyCount>=6) { document.getElementById('ly_record').style.display='none'; document.getElementById('ly_submit').style.display='block'; document.getElementById('ly_status').textContent='6次完成！点击下方开始占卜'; }
  else { document.getElementById('ly_status').textContent=`已记下第${lyCount}次。点硬币翻面后点"记下这一爻"。还剩${6-lyCount}次`; }
  lyCoins=[0,0,0]; updateCoins();
}

async function divineLiuyao() {
  if (lyLines.length<6) return alert('先摇完6次');
  const qtype = document.getElementById('ly_type').value;
  showLoading();
  const res = await fetch('/api/liuyao', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lines:lyLines,question_type:qtype})});
  const data = await res.json();
  hideLoading();
  if (data.success) {
    const d = data.data;
    document.getElementById('resultArea').innerHTML = `<div class="big-verdict">🪙 ${d.hexagram}${d.moving_lines.length?' → '+d.changed_hexagram:''}</div><div class="hex-info">世爻: ${d.shi_pos} | 应爻: ${d.ying_pos} | 动爻: ${d.moving_lines.join(',')||'静卦'} | 用神: ${d.yong_shen_type}(${d.yong_shen_desc})</div><div class="advice">💡 <em>分析：</em>${d.analysis}</div>`;
  } else { alert(data.error); }
  document.getElementById('resultArea').classList.add('show');
}

function showLoading() { document.getElementById('loading').classList.add('show'); document.getElementById('resultArea').classList.remove('show'); }
function hideLoading() { document.getElementById('loading').classList.remove('show'); }

renderForm('xiaoliuren');
