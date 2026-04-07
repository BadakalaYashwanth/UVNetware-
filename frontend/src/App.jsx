import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from 'recharts';
import { 
  LayoutDashboard, Database, Zap, Activity, Globe, Monitor, Users, 
  TrendingUp, AlertTriangle, Target, DollarSign, Clock, MapPin, 
  ChevronRight, RefreshCw, Layers, Terminal, User, Moon, Sun
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000/api';

const COLORS = ['#0ea5e9', '#6366f1', '#f43f5e', '#10b981', '#f59e0b', '#8b5cf6'];

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({ input: null, output: null });
  const [activeTab, setActiveTab] = useState('overview');
  const [lastUpdated, setLastUpdated] = useState(new Date().toLocaleTimeString());
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'system');

  const applyTheme = (t) => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');

    let applied = t;
    if (t === 'system') {
      applied = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    
    root.classList.add(applied);
    localStorage.setItem('theme', t);
  };

  useEffect(() => {
    applyTheme(theme);
    
    // Listen for system theme changes if set to system
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const listener = (e) => applyTheme('system');
      mediaQuery.addListener(listener);
      return () => mediaQuery.removeListener(listener);
    }
  }, [theme]);

  const fetchData = async () => {
    try {
      const [inputRes, outputRes] = await Promise.all([
        axios.get(`${API_BASE}/input`),
        axios.get(`${API_BASE}/output`)
      ]);
      setData({ input: inputRes.data, output: outputRes.data });
      setLastUpdated(new Date().toLocaleTimeString());
      setLoading(false);
    } catch (err) {
      console.error("Fetch Error:", err);
      // Fallback or error state
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  if (loading) return (
    <div className="flex h-screen w-full items-center justify-center bg-transparent text-slate-200">
      <div className="flex flex-col items-center gap-4">
        <RefreshCw className="h-10 w-10 animate-spin text-primary-400" />
        <p className="text-xl font-medium tracking-tight animate-pulse text-slate-400">Booting Analytics Engine...</p>
      </div>
    </div>
  );

  const input = data.input || {};
  const output = data.output || {};

  // Transformation for visualizations
  const deviceData = input.aggregated?.deviceBreakdown?.map(d => ({ name: d.device, value: d.count })) || 
                     (output.user_behavior_insights?.top_devices ? Object.entries(output.user_behavior_insights.top_devices).map(([k, v]) => ({ name: k, value: v })) : []);
  
  const trafficData = input.aggregated?.hourlyTraffic?.map(t => ({ name: `${t.hour}:00`, sessions: t.sessions, conv: t.conversions })) || [];
  
  const funnelData = output.funnel_analytics?.avg_conversion_rates ? 
    output.funnel_analytics.avg_conversion_rates.map((rate, i) => ({ name: `Step ${i+1}`, rate: rate * 100 })) : [];
  
  const roiData = Array.isArray(output.channel_performance) ? 
    output.channel_performance.map(item => ({ name: item.channel, roi: item.ROI || item.roi })) : [];

  const StatCard = ({ title, value, icon: Icon, trend, color = "primary" }) => (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass p-6 rounded-2xl relative overflow-hidden group border-white/5 hover:border-white/10 transition-all"
    >
       <div className={`absolute -right-4 -bottom-4 opacity-5 group-hover:opacity-10 transition-opacity`}>
         <Icon size={120} />
       </div>
       <div className="flex justify-between items-start mb-4">
         <div className={`p-3 rounded-xl bg-${color}-500/10 text-${color}-400`}>
           <Icon size={24} />
         </div>
         {trend && (
           <span className="text-xs px-2 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-medium">
             +{trend}%
           </span>
         )}
       </div>
       <p className="text-slate-400 text-sm font-medium mb-1">{title}</p>
       <h3 className="text-2xl font-bold font-display">{value}</h3>
    </motion.div>
  );

  const ChartWrapper = ({ title, children, icon: Icon }) => (
    <div className="glass p-6 rounded-2xl flex flex-col h-full bg-white dark:bg-slate-900 overflow-hidden">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 rounded-lg bg-slate-100 dark:bg-white/5">
          {Icon && <Icon size={18} className="text-primary-400" />}
        </div>
        <h4 className="text-lg font-semibold text-slate-900 dark:text-slate-100">{title}</h4>
      </div>
      <div className="flex-1 min-h-[250px]">
        {children}
      </div>
    </div>
  );

  return (
    <div className="min-h-screen text-slate-900 dark:text-slate-200 selection:bg-primary-500/30">
      {/* Sidebar */}
      <div className="fixed top-0 left-0 h-full w-64 bg-slate-50 dark:bg-slate-900/50 border-r border-slate-200 dark:border-white/5 p-6 z-50 hidden lg:block">
        <div className="flex items-center gap-3 mb-10 px-2">
          <div className="h-10 w-10 bg-gradient-to-tr from-primary-600 to-secondary rounded-lg flex items-center justify-center text-white shadow-lg shadow-primary-500/20">
            <Layers size={24} />
          </div>
          <div>
            <h1 className="font-bold text-lg leading-tight font-display tracking-tight">UV NETWARE <span className="text-primary-400 italic">.AI</span></h1>
            <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">Analytics Engine v2.0</p>
          </div>
        </div>

        <nav className="space-y-1 mb-8">
          {[
            { id: 'overview', label: 'Overview', icon: LayoutDashboard },
            { id: 'input', label: 'Live Input Stream', icon: Database },
            { id: 'insights', label: 'Predictive Insights', icon: Zap },
            { id: 'funnels', label: 'Conversion Funnels', icon: Target },
            { id: 'geo', label: 'Geo Analysis', icon: Globe },
          ].map(item => (
            <button
               key={item.id}
               onClick={() => setActiveTab(item.id)}
               className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                 activeTab === item.id 
                 ? 'bg-primary-500/10 text-primary-400 border-l-2 border-primary-500 font-medium' 
                 : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 hover:text-primary-500 dark:hover:text-slate-200'
               }`}
            >
              <item.icon size={20} />
              {item.label}
            </button>
          ))}
        </nav>

        <div className="space-y-4 px-2">
           <p className="text-[10px] uppercase tracking-widest text-slate-400 font-bold mb-2">Display Theme</p>
           <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl">
             {[
               { id: 'light', icon: Sun },
               { id: 'dark', icon: Moon },
               { id: 'system', icon: Monitor }
             ].map(opt => (
               <button
                 key={opt.id}
                 onClick={() => setTheme(opt.id)}
                 className={`flex-1 flex items-center justify-center py-2 rounded-lg transition-all ${
                   theme === opt.id 
                   ? 'bg-white dark:bg-slate-700 text-primary-500 shadow-sm' 
                   : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-200'
                 }`}
               >
                 <opt.icon size={16} />
               </button>
             ))}
           </div>
        </div>

        <div className="absolute bottom-10 left-6 right-6">
           <div className="p-4 rounded-2xl bg-gradient-to-br from-slate-800 to-slate-900 border border-white/5">
              <div className="flex items-center gap-2 mb-2">
                <div className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></div>
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">System Live</span>
              </div>
              <p className="text-xs text-slate-500 mb-3">Syncing every 5 seconds... Last: {lastUpdated}</p>
              <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: '0%' }}
                  animate={{ width: '100%' }}
                  transition={{ duration: 5, repeat: Infinity, ease: 'linear' }}
                  className="h-full bg-primary-500"
                />
              </div>
           </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="lg:ml-64 p-8 min-h-screen">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
          <div>
            <h2 className="text-3xl font-bold font-display text-slate-900 dark:text-white mb-2">
              {activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Dashboard
            </h2>
            <p className="text-slate-500 dark:text-slate-400">Welcome back! Here's what's happening with your traffic and conversions today.</p>
          </div>
          
          <div className="flex items-center gap-4">
             <div className="flex -space-x-2">
                {[1,2,3].map(i => (
                  <div key={i} className="h-10 w-10 rounded-full border-2 border-slate-900 overflow-hidden">
                    <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${i + 20}`} alt="user" />
                  </div>
                ))}
             </div>
             <button className="bg-primary-600 hover:bg-primary-500 text-white px-6 py-2.5 rounded-xl font-semibold shadow-lg shadow-primary-500/20 transition-all flex items-center gap-2">
               Generate Report <ChevronRight size={18} />
             </button>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {activeTab === 'overview' && (
            <motion.div 
              key="overview"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-8"
            >
              {/* Summary Stats */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard 
                  title="Total Sessions" 
                  value={input.aggregated?.traffic?.totalSessions?.toLocaleString()} 
                  icon={Activity} 
                  trend={12.5} 
                />
                <StatCard 
                  title="Avg Sessions Time" 
                  value={`${input.aggregated?.traffic?.avgSessionTime?.toFixed(2)}m`} 
                  icon={Clock} 
                  color="indigo" 
                />
                <StatCard 
                  title="Returning Users" 
                  value={input.aggregated?.traffic?.returningUsers?.toLocaleString()} 
                  icon={Users} 
                  color="rose" 
                />
                <StatCard 
                  title="Estimated Revenue" 
                  value={`$${(output.predicted_revenue?.total_predicted_revenue || output.weekly_summary?.total_revenue || 0).toLocaleString()}`} 
                  icon={DollarSign} 
                  color="emerald" 
                />
              </div>

              {/* Charts Row 1 */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <ChartWrapper title="Hourly Traffic Distribution" icon={TrendingUp}>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={trafficData}>
                      <defs>
                        <linearGradient id="colorSessions" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#0ea5e9" stopOpacity={0.3}/>
                          <stop offset="95%" stopColor="#0ea5e9" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                      <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px', fontSize: '12px' }} />
                      <Area type="monotone" dataKey="sessions" stroke="#0ea5e9" fillOpacity={1} fill="url(#colorSessions)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </ChartWrapper>

                <ChartWrapper title="Device Segmentation" icon={Monitor}>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={deviceData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {deviceData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px', fontSize: '12px' }} />
                    </PieChart>
                  </ResponsiveContainer>
                  <div className="grid grid-cols-2 gap-2 mt-4">
                    {deviceData.map((d, i) => (
                      <div key={i} className="flex items-center gap-2">
                        <div className="h-3 w-3 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }}></div>
                        <span className="text-xs text-slate-400 capitalize">{d.name} ({d.value})</span>
                      </div>
                    ))}
                  </div>
                </ChartWrapper>

                <ChartWrapper title="Channel ROI Prediction" icon={Target}>
                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={roiData}>
                      <PolarGrid stroke="#ffffff10" />
                      <PolarAngleAxis dataKey="name" stroke="#64748b" fontSize={10} />
                      <PolarRadiusAxis stroke="#64748b" fontSize={10} />
                      <Radar name="ROI" dataKey="roi" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.6} />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px', fontSize: '12px' }} />
                    </RadarChart>
                  </ResponsiveContainer>
                </ChartWrapper>
              </div>

              {/* Advanced Insights Section */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* AI Analysis Card */}
                <div className="glass p-8 rounded-3xl border-primary-500/20 bg-gradient-to-br from-primary-900/10 via-slate-900/50 to-indigo-900/10">
                   <div className="flex items-center gap-4 mb-6">
                      <div className="h-14 w-14 rounded-2xl bg-primary-500 flex items-center justify-center text-white shadow-xl shadow-primary-500/40">
                        <Zap size={28} />
                      </div>
                      <div>
                        <h3 className="text-xl font-bold font-display">AI Intelligence Engine</h3>
                        <p className="text-slate-400 text-sm">Real-time predictive analysis of your pipeline.</p>
                      </div>
                   </div>
                   
                   <div className="space-y-4">
                      <div className="p-4 rounded-xl bg-white/5 border border-white/5">
                        <div className="flex justify-between mb-2">
                           <span className="text-sm font-medium text-slate-300 flex items-center gap-2">
                             <AlertTriangle size={16} className="text-amber-400" /> Anomaly Probability
                           </span>
                           <span className="text-sm text-primary-400 font-bold">14% - Low Risk</span>
                        </div>
                        <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                           <motion.div initial={{ width: 0 }} animate={{ width: '14%' }} className="h-full bg-amber-400" />
                        </div>
                      </div>

                      <div className="p-4 rounded-xl bg-white/5 border border-white/5">
                        <div className="flex justify-between mb-2">
                           <span className="text-sm font-medium text-slate-300 flex items-center gap-2">
                             <TrendingUp size={16} className="text-emerald-400" /> Predicted Conv. Rate
                           </span>
                           <span className="text-sm text-emerald-400 font-bold">{(output.conversion_rate?.average_conversion_rate * 100 || 0).toFixed(2)}%</span>
                        </div>
                        <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                           <motion.div initial={{ width: 0 }} animate={{ width: '42%' }} className="h-full bg-emerald-400" />
                        </div>
                      </div>

                      <div className="flex gap-4 mt-6">
                        <div className="flex-1 p-4 rounded-xl bg-slate-800/50 border border-white/5">
                           <p className="text-[10px] uppercase font-bold text-slate-500 mb-1">Recommended Budget</p>
                           <p className="text-2xl font-bold text-white font-display">${output.budget_recommendations?.total_recommended_budget?.toLocaleString()}</p>
                        </div>
                        <div className="flex-1 p-4 rounded-xl bg-slate-800/50 border border-white/5">
                           <p className="text-[10px] uppercase font-bold text-slate-500 mb-1">Weekly Trends</p>
                           <p className="text-2xl font-bold text-white font-display">Positive</p>
                        </div>
                      </div>
                   </div>
                </div>

                {/* Funnel Dropoff */}
                <ChartWrapper title="Conversion Funnel Performance" icon={Target}>
                   <ResponsiveContainer width="100%" height={300}>
                     <BarChart layout="vertical" data={funnelData} margin={{ left: 10 }}>
                        <XAxis type="number" hide />
                        <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={12} width={100} />
                        <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px', fontSize: '12px' }} />
                        <Bar dataKey="rate" fill="#0ea5e9" radius={[0, 4, 4, 0]} barSize={20} />
                     </BarChart>
                   </ResponsiveContainer>
                </ChartWrapper>
              </div>
            </motion.div>
          )}

          {activeTab === 'input' && (
            <motion.div 
              key="input"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-6"
            >
               <div className="glass p-6 rounded-2xl border-white/5">
                  <div className="flex items-center justify-between mb-6">
                     <div className="flex items-center gap-3">
                        <Terminal className="text-primary-400" size={24} />
                        <h3 className="text-xl font-bold font-display">Raw Input Stream</h3>
                     </div>
                     <span className="text-xs text-slate-500 font-mono italic">real_world_input.json</span>
                  </div>
                  <div className="bg-slate-900/50 rounded-xl p-6 font-mono text-sm text-slate-300 overflow-auto max-h-[600px] border border-white/5">
                    <pre>{JSON.stringify(input, null, 2)}</pre>
                  </div>
               </div>
            </motion.div>
          )}

          {activeTab === 'insights' && (
            <motion.div 
              key="insights"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="grid grid-cols-1 lg:grid-cols-2 gap-8"
            >
               <div className="glass p-8 rounded-3xl border-white/5 col-span-2">
                  <h3 className="text-2xl font-bold font-display mb-6 flex items-center gap-3">
                    <Zap className="text-amber-400" /> Advanced Insights Summary
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {Object.entries(output.advanced_insights || {}).map(([key, val], idx) => (
                      <div key={idx} className="p-6 rounded-2xl bg-white/5 border border-white/5">
                         <p className="text-xs uppercase font-bold text-slate-500 mb-2">{key.replace(/_/g, ' ')}</p>
                         <div className="text-white">
                            {typeof val === 'object' ? JSON.stringify(val) : val}
                         </div>
                      </div>
                    ))}
                  </div>
               </div>

               <ChartWrapper title="ROI vs CPC Comparison" icon={DollarSign}>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={roiData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                      <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
                      <YAxis stroke="#64748b" fontSize={12} />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px', fontSize: '12px' }} />
                      <Line type="monotone" dataKey="roi" stroke="#6366f1" strokeWidth={3} dot={{ fill: '#6366f1', r: 4 }} />
                    </LineChart>
                  </ResponsiveContainer>
               </ChartWrapper>

               <div className="glass p-8 rounded-3xl border-white/5">
                 <h3 className="text-xl font-bold font-display mb-6">Channel Recommendations</h3>
                 <div className="space-y-4">
                    {Array.isArray(output.budget_recommendations?.increase) ? output.budget_recommendations.increase.map((chan, idx) => (
                      <div key={idx} className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                        <div className="flex items-center gap-3">
                          <div className={`h-2 w-2 rounded-full bg-emerald-500`}></div>
                          <span className="font-semibold capitalize">{chan}</span>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-bold text-emerald-400">Increase Budget</p>
                          <p className="text-[10px] text-slate-500">High performing channel</p>
                        </div>
                      </div>
                    )) : <p className="text-slate-500 text-sm italic">No active budget updates</p>}
                 </div>
               </div>
            </motion.div>
          )}

          {activeTab === 'geo' && (
            <motion.div 
               key="geo"
               initial={{ opacity: 0, x: 20 }}
               animate={{ opacity: 1, x: 0 }}
               className="space-y-8"
            >
               <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="glass p-8 rounded-3xl border-white/5">
                    <h3 className="text-xl font-bold font-display mb-6 flex items-center gap-2">
                       <MapPin className="text-rose-500" /> Geography Highlights
                    </h3>
                    <div className="space-y-6">
                       <div className="flex justify-between items-center">
                          <span className="text-slate-400">Top Country</span>
                          <span className="text-white font-bold">{input.meta?.geoLocation?.country || 'USA'}</span>
                       </div>
                       <div className="flex justify-between items-center">
                          <span className="text-slate-400">Top City</span>
                          <span className="text-white font-bold">{input.meta?.geoLocation?.city || 'New York'}</span>
                       </div>
                    </div>
                  </div>
                  
                  <div className="glass p-8 rounded-3xl border-white/5">
                    <h3 className="text-xl font-bold font-display mb-6 flex items-center gap-2">
                       <Monitor className="text-indigo-400" /> OS Breakdown
                    </h3>
                    <div className="space-y-6">
                       <div className="flex justify-between items-center">
                          <span className="text-slate-400">Primary OS</span>
                          <span className="text-white font-bold">{input.meta?.os || 'Windows'}</span>
                       </div>
                       <div className="flex justify-between items-center">
                          <span className="text-slate-400">Primary Browser</span>
                          <span className="text-white font-bold">{input.meta?.browser || 'Chrome'}</span>
                       </div>
                    </div>
                  </div>
               </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

export default Dashboard;
