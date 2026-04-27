import React, { useState } from 'react';
import { Settings2, Map, Truck, BarChart2 } from 'lucide-react';

const Sidebar = ({ locations, onCalculateRoute, routeData }) => {
  const [startPoint, setStartPoint] = useState('');
  const [endPoint, setEndPoint] = useState('');
  const [algorithm, setAlgorithm] = useState('dijkstra');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!startPoint) return;
    
    // For MST we only need startPoint, but we use start for others as well.
    onCalculateRoute({
      start: startPoint,
      end: algorithm !== 'mst' ? endPoint : '',
      algorithm: algorithm
    });
  };

  return (
    <aside className="w-80 h-full bg-slate-800/80 backdrop-blur-xl border-r border-slate-700/50 flex flex-col pt-6 z-20 shadow-2xl">
      <div className="px-6 mb-8 flex items-center gap-3 text-blue-400">
        <Truck className="w-8 h-8" />
        <h1 className="text-xl font-bold tracking-tight text-white">Route<span className="text-blue-500">Optima</span></h1>
      </div>

      <div className="px-6 space-y-6 flex-1 overflow-y-auto">
        <form onSubmit={handleSubmit} className="space-y-4 bg-slate-900/50 p-5 rounded-xl border border-slate-700/50">
          <div className="flex items-center gap-2 mb-2">
            <Settings2 className="w-4 h-4 text-slate-400" />
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Configure Route</h2>
          </div>
          
          <div className="space-y-1">
            <label className="text-xs text-slate-400 font-medium">Algorithm</label>
            <select 
              className="w-full bg-slate-800 border border-slate-600 text-sm rounded-lg px-3 py-2 text-slate-200 outline-none focus:border-blue-500 transition-colors"
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
            >
              <option value="dijkstra">Dijkstra's (Shortest Path)</option>
              <option value="floyd_warshall">Floyd-Warshall (All Pairs)</option>
              <option value="mst">Minimum Spanning Tree (Network)</option>
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs text-slate-400 font-medium">Source / Start Node</label>
            <select 
              className="w-full bg-slate-800 border border-slate-600 text-sm rounded-lg px-3 py-2 text-slate-200 outline-none focus:border-blue-500 transition-colors"
              value={startPoint}
              onChange={(e) => setStartPoint(e.target.value)}
            >
              <option value="">Select location...</option>
              {locations.map(loc => (
                <option key={loc.id} value={loc.id}>{loc.name} ({loc.id})</option>
              ))}
            </select>
          </div>

          {algorithm !== 'mst' && (
            <div className="space-y-1">
              <label className="text-xs text-slate-400 font-medium">Destination</label>
              <select 
                className="w-full bg-slate-800 border border-slate-600 text-sm rounded-lg px-3 py-2 text-slate-200 outline-none focus:border-blue-500 transition-colors"
                value={endPoint}
                onChange={(e) => setEndPoint(e.target.value)}
              >
                <option value="">Select location...</option>
                {locations.map(loc => (
                  <option key={loc.id} value={loc.id}>{loc.name} ({loc.id})</option>
                ))}
              </select>
            </div>
          )}

          <button 
            type="submit"
            className="w-full mt-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium py-2.5 rounded-lg shadow-[0_0_15px_rgba(79,70,229,0.4)] transition-all hover:scale-[1.02] active:scale-[0.98]"
          >
            Calculate Optimal Route
          </button>
        </form>

        {routeData && (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 bg-slate-900/50 p-5 rounded-xl border border-slate-700/50">
            <div className="flex items-center gap-2 mb-4">
              <BarChart2 className="w-4 h-4 text-emerald-400" />
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">Analytics</h2>
            </div>
            
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                <p className="text-xs text-slate-400">Total Distance</p>
                <p className="text-xl font-bold text-emerald-400">
                  {routeData.distance !== undefined ? 
                    routeData.distance.toFixed(1) : 
                    routeData.total_cost !== undefined ? 
                      routeData.total_cost.toFixed(1) : 'N/A'
                  } <span className="text-sm font-medium text-slate-500">km</span>
                </p>
              </div>
              <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700">
                <p className="text-xs text-slate-400">Algorithm Used</p>
                <p className="text-sm font-bold text-blue-400 break-words flex items-center h-full pb-1">
                  {routeData.algorithm === 'floyd_warshall' ? 'Floyd-W.' : routeData.algorithm}
                </p>
              </div>
            </div>

            {routeData.path && routeData.path.length > 0 && (
              <div className="space-y-2">
                <p className="text-xs text-slate-400 font-medium mb-2">Route Path</p>
                <div className="flex flex-wrap items-center gap-2">
                  {routeData.path.map((nodeId, idx) => (
                    <React.Fragment key={idx}>
                      <span className="px-2 py-1 bg-slate-800 text-slate-200 text-xs font-medium rounded border border-slate-600">
                        {nodeId}
                      </span>
                      {idx < routeData.path.length - 1 && (
                        <span className="text-slate-500">→</span>
                      )}
                    </React.Fragment>
                  ))}
                </div>
              </div>
            )}
            
            {routeData.edges && routeData.edges.length > 0 && (
              <div className="space-y-2 max-h-32 overflow-y-auto pr-1">
                <p className="text-xs text-slate-400 font-medium mb-1">MST Edges</p>
                {routeData.edges.map((edge, idx) => (
                  <div key={idx} className="flex justify-between items-center bg-slate-800/50 p-2 rounded text-xs border border-slate-700/50">
                    <span className="text-slate-300">{edge.source} <span className="text-slate-500">↔</span> {edge.target}</span>
                    <span className="text-emerald-400 font-medium">{edge.weight.toFixed(1)} km</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
