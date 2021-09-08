// TO MAKE THE MAP APPEAR YOU MUST
// ADD YOUR ACCESS TOKEN FROM
// https://account.mapbox.com
mapboxgl.accessToken = 'pk.eyJ1IjoiYXBhcG91dHNpcyIsImEiOiJja3NzZ2Q0bmgwd2tkMm5wdWtteHVvd3M5In0.YfOjhqgCT00v9ggsxACvfA';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [145.004795728903, -37.82661008356922], // starting position [lng, lat]
    zoom: 15 // starting zoom
});