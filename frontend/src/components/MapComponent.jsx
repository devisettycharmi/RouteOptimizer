import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';

// Fix for default marker icons in Leaflet with Webpack/Vite
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Component to dynamically fit map bounds to locations
const MapBounds = ({ locations }) => {
  const map = useMap();
  useEffect(() => {
    if (locations && locations.length > 0) {
      const bounds = L.latLngBounds(locations.map(loc => [loc.lat, loc.lng]));
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [locations, map]);
  return null;
};

const MapComponent = ({ locations = [], routeData = null }) => {
  // New York approx center
  const center = [40.7128, -74.0060];

  // Helper to get location by ID
  const getLoc = (id) => locations.find(l => l.id === id);

  return (
    <MapContainer 
      center={center} 
      zoom={11} 
      className="w-full h-full"
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      
      <MapBounds locations={locations} />

      {/* Render all available locations */}
      {locations.map(loc => (
        <Marker key={loc.id} position={[loc.lat, loc.lng]}>
          <Popup className="bg-slate-800 text-white rounded-lg border-none shadow-xl">
            <div className="font-sans">
              <strong className="block text-indigo-400 mb-1">{loc.name} ({loc.id})</strong>
              <span className="text-xs text-slate-300">Type: {loc.type}</span>
            </div>
          </Popup>
        </Marker>
      ))}

      {/* Render Route (Path) */}
      {routeData && routeData.path && routeData.path.length > 1 && (
        <Polyline 
          positions={routeData.path.map(id => {
            const loc = getLoc(id);
            return loc ? [loc.lat, loc.lng] : null;
          }).filter(Boolean)} 
          color="#3b82f6" // blue-500
          weight={4}
          opacity={0.8}
          dashArray="10, 10"
          className="animate-[dash_1s_linear_infinite]"
        />
      )}

      {/* Render MST Edges */}
      {routeData && routeData.edges && routeData.edges.length > 0 && (
        <>
          {routeData.edges.map((edge, idx) => {
            const source = getLoc(edge.source);
            const target = getLoc(edge.target);
            if (source && target) {
              return (
                <Polyline 
                  key={idx}
                  positions={[[source.lat, source.lng], [target.lat, target.lng]]}
                  color="#10b981" // emerald-500
                  weight={3}
                  opacity={0.7}
                />
              );
            }
            return null;
          })}
        </>
      )}
    </MapContainer>
  );
};

export default MapComponent;
