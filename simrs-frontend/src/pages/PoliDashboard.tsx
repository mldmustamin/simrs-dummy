import { apiFetch } from '../lib/api';
import { useEffect, useState } from 'react';
import { Users, Clock, CheckCircle2, User, Activity, AlertCircle, Building, CalendarDays } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function PoliDashboard() {
  const [queues, setQueues] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // For Poliklinik Umum (UMU) or U0009. We use U0009 based on DB.
  const kdPoli = 'U0009'; 

  useEffect(() => {
    fetchPoliQueues();
    const interval = setInterval(fetchPoliQueues, 10000); // refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const fetchPoliQueues = async () => {
    try {
      const res = await apiFetch(`http://localhost:3000/api/queues/poli/${kdPoli}`);
      const data = await res.json();
      setQueues(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const periksaPasien = (no_rawat: string) => {
    // Navigate to RME with no_rawat as query parameter
    navigate(`/rme?no_rawat=${encodeURIComponent(no_rawat)}`);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-black text-slate-800 flex items-center gap-2">
            <Building className="w-7 h-7 text-[#004d40]" /> Dashboard Dokter Poli Umum
          </h1>
          <p className="text-sm text-slate-500 mt-1 flex items-center gap-2">
            <CalendarDays className="w-4 h-4" /> {new Date().toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
          </p>
        </div>
        <div className="bg-[#004d40]/10 text-[#004d40] px-4 py-2 rounded-lg border border-[#004d40]/20 flex items-center gap-3">
          <Users className="w-5 h-5" />
          <div className="text-sm">
            <span className="font-bold text-lg">{queues.length}</span> Pasien Hari Ini
          </div>
        </div>
      </div>

      {/* Queue List */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-5 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
          <h2 className="font-bold text-slate-800">Daftar Antrean Pemeriksaan</h2>
          <button onClick={fetchPoliQueues} className="text-xs font-semibold text-[#004d40] hover:underline flex items-center gap-1">
            <Activity className="w-4 h-4" /> Refresh
          </button>
        </div>
        
        <div className="p-0">
          {loading ? (
            <div className="text-center py-12 text-slate-400">Loading antrean...</div>
          ) : queues.length === 0 ? (
            <div className="text-center py-12 flex flex-col items-center justify-center">
              <AlertCircle className="w-12 h-12 text-slate-200 mb-3" />
              <p className="text-slate-500 font-medium">Belum ada pasien yang mendaftar ke Poli Umum hari ini.</p>
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {queues.map((q, idx) => (
                <div key={q.no_rawat} className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:bg-slate-50 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center text-slate-400 font-bold text-xl border border-slate-200 shrink-0">
                      {idx + 1}
                    </div>
                    <div>
                      <h3 className="font-bold text-slate-800 text-lg mb-1">{q.pasien?.nm_pasien}</h3>
                      <div className="flex flex-wrap items-center gap-3 text-xs text-slate-500">
                        <span className="font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-600">{q.no_rawat}</span>
                        <span className="flex items-center gap-1"><User className="w-3.5 h-3.5" /> NIK: {q.pasien?.no_ktp}</span>
                        <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {new Date(q.tgl_registrasi).toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}</span>
                      </div>
                      <div className="mt-2 text-xs font-semibold">
                        {q.stts === 'Belum' ? (
                          <span className="text-amber-600 bg-amber-50 px-2 py-1 rounded-md border border-amber-200">Menunggu Diperiksa</span>
                        ) : (
                          <span className="text-emerald-700 bg-emerald-50 px-2 py-1 rounded-md border border-emerald-200">Selesai</span>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex sm:flex-col gap-2 shrink-0">
                    <button className="flex-1 sm:flex-none bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg text-sm font-bold transition-colors">
                      Panggil
                    </button>
                    <button 
                      onClick={() => periksaPasien(q.no_rawat)}
                      className="flex-1 sm:flex-none bg-[#004d40] hover:bg-[#00332a] text-white px-6 py-2 rounded-lg text-sm font-bold shadow-sm transition-colors flex items-center justify-center gap-2"
                    >
                      <CheckCircle2 className="w-4 h-4" /> Periksa RME
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
