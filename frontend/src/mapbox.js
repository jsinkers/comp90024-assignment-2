import mapbox from 'mapbox-gl';

// https://docs.mapbox.com/help/glossary/access-token/
mapbox.accessToken = 'pk.eyJ1Ijoic2lua2VycyIsImEiOiJjazk1ZTU2Z3EwbTV4M2RudGo4ODRtZXpuIn0.NbpySvh4pkbr91I3SQKQIw';

const key = Symbol();

export { mapbox, key };