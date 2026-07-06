---
layout: default
title: The Dingle Way
date: 13 - 19 juillet 2026
show_title: true
---

## The Dingle Way : 115 km +2440 m / -2410 m (131 ke)


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
var rvMap = L.map('rv-map', { maxZoom: 12 }).setView([52.207965722919376, -10.014874863280404], 10);
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

['tralee-camp.gpx', 'camp-annascaul.gpx', 'annascaul-dingle.gpx',
 'feothanach-cloghan.gpx', 'cloghan-annascaul.gpx', 'ventry%20-%20dingle.gpx']
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


## 1 - Lundi 13 juillet : Cork ⟶ Tralee

<div class="trip-note trip-train">🚆 Cork 16:57 - 18:58 Tralee</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/cork-tralee-train.png" alt="Cork-Tralee">
</div>

{% comment %}
{% include hourly-weather.html
   id="1-cork"
   cityid="2965140"
   appid="e799e26275aa824e9c4a5e897c2dfd8c"
%}
{% endcomment %}

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/LcPY8piburQajFs16">Tralee Townhouse,
1 High Street, Tralee</a> · <a href="https://www.booking.com/hotel/ie/tralee-townhouse.fr.html">Booking</a>
<ul>
<li>L2</li>
<li>L2</li>
<li>L1 + L1</li>
<li>L1 + L1 + L1</li>
</ul>
</div>


## 2 - mardi 14 juillet - Tralee ⟶ Camp

{% comment %}
{% include hourly-weather.html
   id="2-tralee"
   cityid="2961123"
   appid="e799e26275aa824e9c4a5e897c2dfd8c"
%}
{% endcomment %}

<div class="trip-note trip-hike"> 🥾 <a href="./files/tralee-camp.gpx">Tralee - Camp GPX</a> . 20 km, 350 D+, 280 D- (22 ke)</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/tralee-camp.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/tralee-camp-d.png" alt="Parcours">
</div>

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/LUnHQSR6yqHLQRZ57">Camp Cross, Camp Coach Field Camp, Camp,</a>· <a href="https://www.booking.com/hotel/ie/coach-field-camp.fr.html">Booking</a>
<ul>
<li>1 coach 6 personnes</li>
<li>1 coach 4 personnes</li>
</ul>
</div>



## 3 - mercredi 15 juillet - Camp ⟶ Annascaul

<div class="trip-note trip-hike">🥾 <a href="./files/camp-annascaul.gpx">Camp - Annascaul GPX</a> . 17 km, 310 D+, 350 D- (19 ke)</div>


<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/camp-annascaul.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/camp-annascaul-d.png" alt="Parcours">
</div>

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/Mbf269Ez1o78f9fm9">Lower Main Street Annascaul</a> . <a href="https://www.booking.com/hotel/ie/lavarna-house.fr.html">Booking</a>
<ul>
<li>L1 + L2</li>
<li>L1 + L1</li>
<li>L2</li>
</ul>
</div>

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/Bs12DmdWYYZLQY6w9">Main Street, Ardrinane, Annascaul</a> . <a href="https://www.airbnb.fr/rooms/1561716437968515833">AirBnB</a>
<ul>
<li>L2</li>
<li>L1 + L2</li>
</ul>
</div>




## 4 - jeudi 16 juillet - Annascaul ⟶ Dingle

{% comment %}
{% include hourly-weather.html
   id="3-dingle"
   cityid="2964782"
   appid="e799e26275aa824e9c4a5e897c2dfd8c"
%}
{% endcomment %}

<div class="trip-note trip-hike">🥾 <a href="./files/annascaul-dingle.gpx">Annascaul - Dingle GPX</a> . 22.5 km, 360 D+, 380 D- (25 ke)</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/annascaul-dingle.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/annascaul-dingle-d.png" alt="Parcours">
</div>


<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/cDaNdRzwGLYCsUsj7">Captain's House, the Mall, Dingle</a> . <a href="https://www.airbnb.fr/rooms/27215697">AirBnB</a>
<ul>
<li>contacter l'hôte Mary en sonnant à la porte sous le panneau Captain’s House. Si absente, code 1429 de la boîte à clés (+353 66 915 153)</li>
<li>L2</li>
<li>L2</li>
<li>L1 + L1</li>
</ul>
</div>

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/wXUzPXMsLRAc6i1S8">Dingle Sea Horse Apartment, 6 B Orchard Lane, Dingle</a> . <a href="https://www.airbnb.fr/rooms/10952918">AirBnB</a>
<ul>
<li>L2</li>
<li>L1 + L1</li>
</ul>
</div>


## 5 - vendredi 17 juillet - Dingle ⟶ Ventry ⟶ Dingle

<div class="trip-note trip-train">🚌 Dingle 12:40 - 12:55 Ventry</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/dingle-ventry-bus.png" alt="Parcours">
</div>

<div class="trip-note trip-hike">🥾 <a href="./files/ventry-dingle.gpx">Ventry - Dingle GPX</a> . 12 km, 140 D+, 140 D- (13 ke)</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/ventry-dingle.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/ventry-dingle-d.png" alt="Parcours">
</div>


## 6 - samedi 18 juillet - Dingle ⟶ Feothanach ⟶ Cloghan

<div class="trip-note trip-train">🚌 Dingle 09:15 - 09:40 Feothanach</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/dingle-feothanach-bus.png" alt="Parcours">
</div>

<div class="trip-note trip-bike">🥾 <a href="./files/feothanach-cloghan.gpx">Feothanach - Cloghan GPX</a> . 26 km, 800 D+, 800 D- (31 ke)</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/feothanach-cloghan.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/feothanach-cloghan-d.png" alt="Parcours">
</div>

<div class="trip-note trip-stay">🏨 <a href="https://maps.app.goo.gl/J8qxcPbWyUajRGGP9">O'Connor's Bar & Guesthouse, Main Street, An Clochán</a> . <a href="https://bookingengine.myguestdiary.com/1566/">Web site</a>
<ul>
<li>L2 + L1 + L1</li>
<li>L2 + L1</li>
<li>L1 + L1</li>
</ul>
</div>


## 7 - dimanche 19 juillet - Cloghan ⟶ Annascaul

<div class="trip-note trip-bike">🥾 <a href="./files/cloghan-annascaul.gpx">Cloghan - Annascaul GPX</a> . 18 km, 480 D+, 460 D- (21 ke)</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/cloghan-annascaul.png" alt="Parcours">
</div>

<div style="display: flex; justify-content: center; align-items: center;">
<img src="./images/cloghan-annascaul-d.png" alt="Parcours">
</div>

