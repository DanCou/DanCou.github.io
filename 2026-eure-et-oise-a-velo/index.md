---
layout: default
title: Eure et Oise à vélo
date: 17 - 21 juin 2026
show_title: true
---

<img src="./images/eric.jpg" alt="Eric" class="center-img">

## Eure et Oise à vélo : 239 km +1750 m / -1750 m



<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<div style="position:relative;height:460px;border-radius:8px;overflow:hidden;margin:1em 0;">
  <div style="position:absolute;top:0;left:0;right:0;height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;background:#fff;z-index:1000;box-sizing:border-box;">
    <span id="rv-ts" style="font:600 16px sans-serif;color:#333">Loading…</span>
    <div style="display:flex;gap:6px;">
      <button onclick="rvStop();rvShow(rvPos-1)" style="width:32px;height:32px;border:1px solid #ddd;border-radius:4px;background:#fff;cursor:pointer;font-size:15px;">‹</button>
      <button id="rv-play" onclick="rvPlayStop()" style="width:32px;height:32px;border:1px solid #ddd;border-radius:4px;background:#fff;cursor:pointer;font-size:15px;">▶</button>
      <button onclick="rvStop();rvShow(rvPos+1)" style="width:32px;height:32px;border:1px solid #ddd;border-radius:4px;background:#fff;cursor:pointer;font-size:15px;">›</button>
    </div>
  </div>
  <div id="rv-map" style="position:absolute;top:44px;left:0;bottom:0;right:0;"></div>
</div>

<script>
var rvMap = L.map('rv-map', { maxZoom: 12 }).setView([49.247196274221494, 1.585768450655383], 9);
L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors &copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
  subdomains: 'abc', maxZoom: 17
}).addTo(rvMap);



var rvData = {}, rvFrames = [], rvPos = 0, rvTimer = false, rvLayer = null, rvLoading = false, rvCache = {};
var RV_OPACITY = 0.8, RV_DELAY = 500, RV_TSIZE = window.devicePixelRatio >= 2 ? 512 : 256;

function rvWrap(p) { while (p >= rvFrames.length) p -= rvFrames.length; while (p < 0) p += rvFrames.length; return p; }
function rvFmt(ts) { return new Date(ts * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); }
function rvNewLayer(f) { return new L.TileLayer(rvData.host + f.path + '/' + RV_TSIZE + '/{z}/{x}/{y}/2/1_1.png', { tileSize: 256, opacity: 0.001, maxNativeZoom: 7, maxZoom: 12 }); }

function rvClearCache() {
  rvStop();
  for (var p in rvCache) { if (parseInt(p) !== rvPos) { rvMap.removeLayer(rvCache[p]); delete rvCache[p]; } }
}

function rvStop() {
  if (rvTimer) { clearTimeout(rvTimer); rvTimer = false; document.getElementById('rv-play').innerHTML = '▶'; return true; }
  return false;
}

function rvPlay() { rvTimer = true; document.getElementById('rv-play').innerHTML = '⏸'; rvShow(rvPos + 1); }
function rvPlayStop() { if (!rvStop()) rvPlay(); }

function rvShow(pos) {
  if (rvLoading) return;
  pos = rvWrap(pos);
  var f = rvFrames[pos];
  document.getElementById('rv-ts').innerHTML = rvFmt(f.time);
  var old = rvLayer;
  if (rvCache[pos]) {
    if (old) old.setOpacity(0);
    rvCache[pos].setOpacity(RV_OPACITY); rvLayer = rvCache[pos]; rvPos = pos;
    if (rvTimer) rvTimer = setTimeout(rvPlay, RV_DELAY);
    return;
  }
  rvLoading = true;
  var layer = rvNewLayer(f);
  layer.on('load', function () {
    layer.setOpacity(RV_OPACITY);
    if (old) old.setOpacity(0);
    rvCache[pos] = layer; rvLayer = layer; rvPos = pos; rvLoading = false;
    if (rvTimer) rvTimer = setTimeout(rvPlay, RV_DELAY);
  });
  layer.addTo(rvMap);
}

function rvInit(api) {
  rvClearCache(); rvLayer = null; rvFrames = []; rvPos = 0;
  if (!api || !api.radar || !api.radar.past) return;
  rvFrames = api.radar.past;
  rvShow(rvFrames.length - 1);
}

rvMap.on('movestart', rvClearCache);
var rvReq = new XMLHttpRequest();
rvReq.open('GET', 'https://api.rainviewer.com/public/weather-maps.json', true);
rvReq.onload = function () { rvData = JSON.parse(rvReq.response); rvInit(rvData); };
rvReq.send();

['gisors-larocheguyon.gpx', 'gournayenbray-gisors.gpx', 'larocheguyon-lesandelys.gpx',
 'lesandelys-lyonslaforet.gpx', 'lyonslaforet-gournayenbray.gpx' ]
  .forEach(function(name) {
    fetch('./files/' + name)
      .then(function(r) { return r.text(); })
      .then(function(text) {
        var pts = Array.from(new DOMParser().parseFromString(text, 'text/xml')
          .getElementsByTagName('trkpt'))
          .map(function(p) { return [+p.getAttribute('lat'), +p.getAttribute('lon')]; })
          .filter(function(p) { return !isNaN(p[0]) && !isNaN(p[1]); });
        L.polyline(pts, { color: '#e63946', weight: 3, opacity: 0.9 }).addTo(rvMap);
      });
  });
</script>




## 1 - mercredi 17 juin : Paris ⟶ Gisors ⟶ La Roche Guyon

<div class="trip-note trip-train">🚆 Paris 08:17 - 09:36 Gisors</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/paris-gisors.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<iframe id="widget_autocomplete_preview"  width="150" height="300" frameborder="0" src="https://meteofrance.com/widget/prevision/272840##3D6AA2" title="Gisors"> </iframe>
</div>

<div class="trip-note trip-bike">🚲 <a href="./files/gisors-larocheguyon.gpx">Gisors - La Roche Guyon GPX</a> . 42 km, 265 D+, 300 D-</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/gisors-larocheguyon.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/gisors-larocheguyon-d.png" alt="Parcours">
</div>


<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/7trkwBDdTcvqHRBLA">Hotel Les Bords de Seine, 21 rue du Docteur Duval, 95780 La Roche-Guyon</a> · <a href="https://www.booking.com/hotel/fr/les-bords-de-seine.html">Booking</a></div>



<div style="display: flex; justify-content: center; align-items: center;">
<iframe id="widget_autocomplete_preview"  width="150" height="300" frameborder="0" src="https://meteofrance.com/widget/prevision/955230##3D6AA2" title="La Roche Guyon"> </iframe>
</div>


## 2 - jeudi 18 juin, La Roche Guyon ⟶ Les Andelys

<div class="trip-note trip-bike">🚲 <a href="./files/larocheguyon-lesandelys.gpx">La Roche Guyon - Les Andelys GPX</a> . 42 km, 222 D+, 222 D-</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/larocheguyon-lesandelys.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/larocheguyon-lesandelys-d.png" alt="Parcours">
</div>

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/8VnMDgUiGyf8azD79">Hotel Les Iris, 8-10 rue Georges Clémenceau, 27700 Les Andelys</a>· <a href="https://www.booking.com/hotel/fr/les-iris-les-andelys.html">Booking</a>
<ul>
<li>Chambre 1 : 2 lits jumeaux</li>
<li>Chambre 2 : 2 lits jumeaux</li>
</ul>
</div>


<div style="display: flex; justify-content: center; align-items: center;">
<iframe id="widget_autocomplete_preview"  width="150" height="300" frameborder="0" src="https://meteofrance.com/widget/prevision/270160##3D6AA2" title="Les Andelys"> </iframe>
</div>



## 3 - vendredi 19 juin, Les Andelys ⟶ Lyons La Forêt

<div class="trip-note trip-bike">🚲 <a href="./files/lesandelys-lyonslaforet.gpx">Les Andelys - Lyons La Foret GPX</a> . 57 km, 290 D+, 195 D-</div>


<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/lesandelys-lyonslaforet.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/lesandelys-lyonslaforet-d.png" alt="Parcours">
</div>

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/bkXUkUPyxbVwWpxbA">Camping Saint Paul,
2 Rte Saint-Paul, 27480 Lyons-la-Forêt</a> . <a href="https://campingsaintpaul-27.fr">Site web</a></div>

<div style="display: flex; justify-content: center; align-items: center;">
<iframe id="widget_autocomplete_preview"  width="150" height="300" frameborder="0" src="https://meteofrance.com/widget/prevision/273770##3D6AA2" title="Lyons la Forêt"> </iframe>
</div>



## 4 - samedi 20 juin, Lyons La Forêt ⟶ Gournay en Bray

<div class="trip-note trip-bike">🚲 <a href="./files/lyonslaforet-gournayenbray.gpx">Lyons La Foret - Gournay en Bray GPX</a> . 64 km, 664 D+, 673 D-</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/lyonslaforet-gournayenbray.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/lyonslaforet-gournayenbray-d.png" alt="Parcours">
</div>


<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/EmV4ZVb5BUa5gztA7">Hotel de Normandie, 21 place nationale, 76220 Gournay-en-Bray</a> . <a href="https://www.booking.com/hotel/fr/de-normandie-gournay-en-bray.html">Booking</a>
<ul>
<li>Chambre 1 : chambre double</li>
<li>Chambre 2 : chambre triple</li>
</ul>
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<iframe id="widget_autocomplete_preview"  width="150" height="300" frameborder="0" src="https://meteofrance.com/widget/prevision/763120##3D6AA2" title="Gournay en Bray"> </iframe>
</div>


## 5 - dimanche 21 juin, Gournay en Bray ⟶ Gisors ⟶ Paris

<div class="trip-note trip-bike">🚲 <a href="./files/gournayenbray-gisors.gpx">Gournay en Bray - Gisors GPX</a> . 35 km, 313 D+, 353 D-</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/gournayenbray-gisors.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/gournayenbray-gisors-d.png" alt="Parcours">
</div>

<div class="trip-note trip-train">🚆 Gisors 15:55 - 17:16 Paris</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/gisors-paris.png" alt="Parcours">
</div>
