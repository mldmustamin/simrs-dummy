import { apiFetch } from '../lib/api';
import { useState, useEffect } from 'react';
import { 
  Pill, RefreshCw, CheckCircle2, AlertTriangle, X, User, 
  ShoppingBag, Plus, Trash2, Search, Printer, 
  MapPin, CheckSquare, ShieldAlert 
} from 'lucide-react';

export default function Apotek() {
  const [activeTab, setActiveTab] = useState<'ANTREAN' | 'OTC'>('ANTREAN');
  
  // Antrean E-Resep States
  const [antrean, setAntrean] = useState<any[]>([]);
  const [depos, setDepos] = useState<any[]>([]);
  const [selectedDepos, setSelectedDepos] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Stok Override States


  // OTC / Resep Bebas States
  const [namaPembeli, setNamaPembeli] = useState('Pasien Mandiri');
  const [selectedOtcDepo, setSelectedOtcDepo] = useState('');
  const [searchKeyword, setSearchKeyword] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [cart, setCart] = useState<any[]>([]);
  const [submittingOtc, setSubmittingOtc] = useState(false);
  const [successOtcReceipt, setSuccessOtcReceipt] = useState<any>(null);

  // Fetch Antrean and Depo
  const fetchAntreanAndDepo = async () => {
    setLoading(true);
    setError('');
    try {
      const [resAntrean, resDepo] = await Promise.all([
        apiFetch('http://localhost:3000/farmasi/antrean-resep'),
        apiFetch('http://localhost:3000/farmasi/depo')
      ]);

      if (resAntrean.ok) {
        setAntrean(await resAntrean.json());
      }
      if (resDepo.ok) {
        const dataDepo = await resDepo.json();
        setDepos(dataDepo);
        if (dataDepo.length > 0) {
          setSelectedOtcDepo(dataDepo[0].kd_bangsal);
        }
      }
    } catch (err) {
      setError('Gagal terhubung ke API Farmasi.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAntreanAndDepo();
    const interval = setInterval(fetchAntreanAndDepo, 15000); 
    return () => clearInterval(interval);
  }, []);

  // Handle medicine search for OTC
  const handleSearchObat = async (keyword: string) => {
    setSearchKeyword(keyword);
    if (!keyword.trim()) {
      setSearchResults([]);
      return;
    }
    try {
      const res = await apiFetch(`http://localhost:3000/farmasi/obat?keyword=${keyword}`);
      if (res.ok) {
        setSearchResults(await res.json());
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Add item to OTC cart
  const addToCart = (obat: any) => {
    const existing = cart.find(item => item.kode_brng === obat.kode_brng);
    if (existing) {
      setCart(cart.map(item => item.kode_brng === obat.kode_brng ? { ...item, jml: item.jml + 1 } : item));
    } else {
      setCart([...cart, { ...obat, jml: 1 }]);
    }
    setSearchKeyword('');
    setSearchResults([]);
  };

  const updateCartQuantity = (kode_brng: string, jml: number) => {
    if (jml <= 0) {
      setCart(cart.filter(item => item.kode_brng !== kode_brng));
    } else {
      setCart(cart.map(item => item.kode_brng === kode_brng ? { ...item, jml } : item));
    }
  };

  const removeFromCart = (kode_brng: string) => {
    setCart(cart.filter(item => item.kode_brng !== kode_brng));
  };

  // Process OTC checkout
  const handleOtcCheckout = async () => {
    if (!selectedOtcDepo) {
      alert('Pilih depo pengeluaran obat terlebih dahulu.');
      return;
    }
    if (cart.length === 0) {
      alert('Keranjang obat kosong.');
      return;
    }

    setSubmittingOtc(true);
    setError('');
    try {
      const payload = {
        nama_pembeli: namaPembeli,
        kd_bangsal_asal: selectedOtcDepo,
        items: cart.map(item => ({ kode_brng: item.kode_brng, jml: item.jml }))
      };

      const res = await apiFetch('http://localhost:3000/farmasi/resep-bebas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const result = await res.json();
        setSuccessOtcReceipt(result.data);
        setCart([]);
        setNamaPembeli('Pasien Mandiri');
        alert('Transaksi penjualan obat bebas (OTC) sukses!');
      }
    } catch (err: any) {
      alert(`Transaksi gagal: ${err.message}`);
    } finally {
      setSubmittingOtc(false);
    }
  };

  // Validasi & Serahkan E-Resep standard
  const serahkanObat = async (no_resep: string, overridePin?: string) => {
    const targetDepo = selectedDepos[no_resep];
    if (!targetDepo) {
      alert('Pilih Depo pengeluaran sebelum menyerahkan obat.');
      return;
    }

    try {
      const payload: any = { 
        no_resep,
        kd_bangsal_asal: targetDepo
      };
      if (overridePin) payload.pin_override = overridePin;

      const res = await apiFetch('http://localhost:3000/farmasi/serahkan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        alert('Resep sukses diserahkan dan diselesaikan!');
        fetchAntreanAndDepo();
      } else {
        const errData = await res.json();
        if (errData.code === 'STOK_KURANG' || errData.message?.includes('Insufficient Stock')) {
          alert(`Stok tidak mencukupi di depo pilihan Anda.`);
        } else {
          alert(`Gagal: ${errData.message || 'Terjadi kesalahan'}`);
        }
      }
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  const selectDepoForResep = (resepId: string, depoId: string) => {
    setSelectedDepos(prev => ({ ...prev, [resepId]: depoId }));
  };

  const calculateOtcTotal = () => {
    return cart.reduce((sum, item) => sum + ((item.ralan || 0) * item.jml), 0);
  };

  return (
    <div className="space-y-6">
      
      {/* Top Header bar */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <Pill className="w-6 h-6 text-[#004d40]" /> Pelayanan Farmasi & Apotek
          </h1>
          <p className="text-sm text-slate-500 mt-1">Sistem validasi obat rawat jalan terpadu, antrean resep, dan penjualan obat bebas.</p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={fetchAntreanAndDepo}
            className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2.5 rounded-lg text-sm font-semibold transition-colors flex items-center gap-2 border border-slate-200"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-[#004d40]' : ''}`} /> Refresh Data
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 p-1 bg-slate-100 rounded-lg w-fit border border-slate-200">
        <button 
          onClick={() => setActiveTab('ANTREAN')}
          className={`px-6 py-2 text-sm font-bold rounded-md transition-all ${activeTab === 'ANTREAN' ? 'bg-[#004d40] text-white shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
        >
          Antrean E-Resep Klinik
        </button>
        <button 
          onClick={() => setActiveTab('OTC')}
          className={`px-6 py-2 text-sm font-bold rounded-md transition-all ${activeTab === 'OTC' ? 'bg-[#004d40] text-white shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
        >
          Penjualan Obat Bebas (OTC)
        </button>
      </div>

      {error && (
        <div className="bg-rose-50 text-rose-600 p-4 rounded-xl border border-rose-200 text-sm font-medium flex items-center gap-2 animate-pulse">
          <AlertTriangle className="w-5 h-5" /> {error}
        </div>
      )}

      {/* View: ANTREAN E-RESEP */}
      {activeTab === 'ANTREAN' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {antrean.map((resep) => {
            const isUmum = resep.reg_periksa?.kd_pj === 'A01';
            const isBelumBayar = resep.reg_periksa?.status_bayar === 'Belum_Bayar';
            const isBlocked = isUmum && isBelumBayar;
            const currentSelectedDepo = selectedDepos[resep.no_resep] || '';

            return (
              <div 
                key={resep.no_resep} 
                className={`bg-white border rounded-xl shadow-sm hover:shadow-md transition-all flex flex-col overflow-hidden relative ${isBlocked ? 'border-amber-200 opacity-95' : 'border-slate-200'}`}
              >
                {/* Visual Status Indicator */}
                <div className={`h-1.5 w-full ${isBlocked ? 'bg-amber-400' : 'bg-[#004d40]'}`}></div>

                {isBlocked && (
                  <div className="absolute right-4 top-4 z-10">
                    <span className="text-[10px] font-bold bg-amber-100 text-amber-800 px-2 py-0.5 rounded border border-amber-200 flex items-center gap-1 shadow-sm">
                      <ShieldAlert className="w-3.5 h-3.5" /> BELUM LUNAS (KASIR)
                    </span>
                  </div>
                )}

                <div className="p-5 flex-1 flex flex-col">
                  <div className="flex justify-between items-start mb-3 pb-3 border-b border-slate-100">
                    <div className="min-w-0 pr-8">
                      <h3 className="font-bold text-slate-800 flex items-center gap-1.5 truncate">
                        <User className="w-4 h-4 text-slate-500" /> {resep.reg_periksa?.pasien?.nm_pasien || 'Pasien Anonim'}
                      </h3>
                      <p className="text-[10px] text-slate-400 font-mono mt-0.5">Rawat: {resep.no_rawat}</p>
                    </div>
                  </div>

                  <div className="space-y-4 flex-1">
                    <div className="flex justify-between text-xs font-semibold text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                      <span>Dokter: dr. {resep.dokter?.nm_dokter}</span>
                      <span className="font-mono text-slate-500">{String(resep.jam).substring(11, 16)} WIB</span>
                    </div>

                    {/* Depo selection (Required!) */}
                    <div className="space-y-1">
                      <label className="block text-[10px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-teal-600" /> Depo Asal Obat
                      </label>
                      <select 
                        value={currentSelectedDepo}
                        onChange={(e) => selectDepoForResep(resep.no_resep, e.target.value)}
                        className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-[#004d40]/20 focus:border-[#004d40] bg-white appearance-none"
                      >
                        <option value="">-- Pilih Depo --</option>
                        {depos.map(d => (
                          <option key={d.kd_bangsal} value={d.kd_bangsal}>{d.nm_bangsal}</option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-2 max-h-[140px] overflow-y-auto pr-1">
                      {resep.resep_dokter?.map((item: any, i: number) => (
                        <div key={i} className="flex justify-between items-center text-xs border-b border-slate-100 pb-2 last:border-0 last:pb-0">
                          <div className="min-w-0 pr-2">
                            <span className="font-bold text-[#004d40] mr-2 bg-slate-100 px-1 rounded border border-slate-200">{item.jml}x</span>
                            <span className="text-slate-700 font-medium truncate">{item.databarang?.nama_brng}</span>
                          </div>
                          <span className="text-[9px] font-bold text-slate-400 bg-slate-100 px-2 py-0.5 rounded shrink-0">{item.aturan_pakai}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Submission and Locks */}
                  <div className="pt-4 border-t border-slate-100 mt-auto">
                    {isBlocked ? (
                      <div className="w-full p-2 bg-amber-50 text-amber-800 rounded-lg text-[10px] font-semibold text-center border border-amber-200">
                        Dispensing terkunci. Pasien harus melunasi tagihan resep terlebih dahulu di Kasir.
                      </div>
                    ) : (
                      <button 
                        onClick={() => serahkanObat(resep.no_resep)}
                        disabled={!currentSelectedDepo}
                        className="w-full py-2 bg-[#004d40] hover:bg-[#00332a] disabled:opacity-50 text-white text-xs font-bold rounded-lg shadow-sm transition-colors flex justify-center items-center gap-1.5"
                      >
                        <CheckSquare className="w-4 h-4" /> Validasi & Serahkan
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
          
          {antrean.length === 0 && !loading && (
            <div className="col-span-full py-16 text-center bg-white rounded-xl border border-dashed border-slate-300">
              <Pill className="w-12 h-12 mx-auto mb-3 text-slate-200 animate-bounce" />
              <p className="text-sm text-slate-500 font-medium">Tidak ada antrean resep saat ini.</p>
            </div>
          )}
        </div>
      )}

      {/* View: PENJUALAN OBAT BEBAS (OTC) */}
      {activeTab === 'OTC' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main shopping area */}
          <div className="lg:col-span-2 bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-6">
            <h2 className="text-lg font-bold text-slate-800 flex items-center gap-2">
              <ShoppingBag className="w-5 h-5 text-[#004d40]" /> Cari & Tambahkan Obat Bebas
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-xs font-semibold text-slate-600">Nama Pembeli / Umum</label>
                <input 
                  type="text" 
                  value={namaPembeli}
                  onChange={(e) => setNamaPembeli(e.target.value)}
                  className="w-full px-3.5 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#004d40]/20 focus:border-[#004d40] bg-white font-medium text-slate-800"
                />
              </div>

              <div className="space-y-1.5">
                <label className="block text-xs font-semibold text-slate-600">Depo Asal Pengeluaran</label>
                <select 
                  value={selectedOtcDepo}
                  onChange={(e) => setSelectedOtcDepo(e.target.value)}
                  className="w-full px-3.5 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#004d40]/20 focus:border-[#004d40] bg-white appearance-none"
                >
                  {depos.map(d => (
                    <option key={d.kd_bangsal} value={d.kd_bangsal}>{d.nm_bangsal}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Medicine Search Box */}
            <div className="space-y-2 relative">
              <label className="block text-xs font-semibold text-slate-600">Cari Obat di Inventori</label>
              <div className="relative">
                <Search className="absolute left-3.5 top-2.5 w-5 h-5 text-slate-400" />
                <input 
                  type="text"
                  value={searchKeyword}
                  onChange={(e) => handleSearchObat(e.target.value)}
                  placeholder="Ketik nama obat bebas (contoh: Paracetamol)..."
                  className="w-full pl-11 pr-4 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#004d40]/20 focus:border-[#004d40] bg-white"
                />
              </div>

              {searchResults.length > 0 && (
                <div className="absolute left-0 right-0 top-full mt-1 bg-white border border-slate-200 rounded-lg shadow-xl max-h-[220px] overflow-y-auto z-10 divide-y divide-slate-100">
                  {searchResults.map(obat => (
                    <div 
                      key={obat.kode_brng}
                      onClick={() => addToCart(obat)}
                      className="p-3 hover:bg-slate-50 cursor-pointer flex justify-between items-center transition-colors text-sm"
                    >
                      <div>
                        <span className="font-bold text-slate-800">{obat.nama_brng}</span>
                        <span className="text-xs text-slate-400 ml-2">({obat.kode_brng})</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-mono font-bold text-[#004d40]">Rp {Number(obat.ralan).toLocaleString()}</span>
                        <span className="p-1 bg-teal-50 text-teal-700 rounded-md"><Plus className="w-4 h-4" /></span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Receipt Modal Success OTC */}
            {successOtcReceipt && (
              <div className="p-5 bg-teal-50 border border-teal-200 rounded-xl space-y-4 animate-fade-in">
                <div className="flex justify-between items-center pb-3 border-b border-teal-200/60">
                  <h3 className="text-sm font-bold text-teal-800 flex items-center gap-1.5">
                    <Printer className="w-4 h-4" /> Transaksi Terakhir Berhasil
                  </h3>
                  <button 
                    onClick={() => setSuccessOtcReceipt(null)}
                    className="p-1 text-teal-600 hover:bg-teal-150 rounded-full"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <div className="bg-white border border-slate-200 rounded-lg p-5 text-slate-900 font-mono text-xs max-w-sm mx-auto shadow-sm space-y-3">
                  <div className="text-center border-b border-dashed border-slate-300 pb-2">
                    <h4 className="font-extrabold">APOTEK HARAPAN UTAMA</h4>
                    <p className="text-[9px] text-slate-400">NOTA PENJUALAN OBAT BEBAS (OTC)</p>
                  </div>
                  <div className="space-y-1">
                    <div>No. Resep: {successOtcReceipt.id.substring(0, 8).toUpperCase()}</div>
                    <div>Tanggal: {new Date(successOtcReceipt.tgl_jual).toLocaleDateString()}</div>
                    <div>Pembeli: {successOtcReceipt.nama_pembeli}</div>
                  </div>
                  <div className="border-t border-b border-slate-200 py-2 space-y-2">
                    {successOtcReceipt.details?.map((d: any, idx: number) => (
                      <div key={idx} className="flex justify-between text-[11px]">
                        <span>{d.kode_brng} x{d.jumlah}</span>
                        <span>Rp {d.total.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-between font-extrabold text-sm text-[#004d40]">
                    <span>Total Lunas:</span>
                    <span>Rp {successOtcReceipt.total_bayar.toLocaleString()}</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Cart sidebar */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-col h-fit">
            <h3 className="font-bold text-slate-800 text-base mb-4 pb-3 border-b border-slate-100 flex items-center justify-between">
              <span>Keranjang Belanja</span>
              <span className="text-xs bg-[#004d40]/10 text-[#004d40] px-2.5 py-0.5 rounded-full font-extrabold">{cart.length} Item</span>
            </h3>

            <div className="space-y-3 overflow-y-auto max-h-[300px] mb-4 pr-1 scrollbar-thin scrollbar-thumb-slate-100">
              {cart.map(item => (
                <div key={item.kode_brng} className="flex items-start gap-3 bg-slate-50 border border-slate-100 p-3 rounded-lg text-xs">
                  <div className="flex-1 min-w-0">
                    <h5 className="font-bold text-slate-800 truncate">{item.nama_brng}</h5>
                    <div className="text-slate-400 font-mono mt-0.5">@ Rp {Number(item.ralan).toLocaleString()}</div>
                    <div className="text-[#004d40] font-bold mt-1.5 font-mono">Total: Rp {((item.ralan || 0) * item.jml).toLocaleString()}</div>
                  </div>

                  <div className="flex flex-col items-end gap-2 shrink-0">
                    <button 
                      onClick={() => removeFromCart(item.kode_brng)}
                      className="text-slate-400 hover:text-red-500 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <div className="flex items-center gap-1.5 bg-white border border-slate-200 rounded-md p-1 shadow-sm">
                      <button 
                        onClick={() => updateCartQuantity(item.kode_brng, item.jml - 1)}
                        className="w-5 h-5 flex items-center justify-center bg-slate-100 text-slate-600 rounded active:scale-90 font-bold"
                      >
                        -
                      </button>
                      <span className="w-6 text-center font-extrabold text-slate-800">{item.jml}</span>
                      <button 
                        onClick={() => updateCartQuantity(item.kode_brng, item.jml + 1)}
                        className="w-5 h-5 flex items-center justify-center bg-slate-100 text-slate-600 rounded active:scale-90 font-bold"
                      >
                        +
                      </button>
                    </div>
                  </div>
                </div>
              ))}

              {cart.length === 0 && (
                <div className="text-center py-12 text-slate-400 space-y-2">
                  <ShoppingBag className="w-10 h-10 text-slate-200 mx-auto" />
                  <p className="text-xs">Keranjang masih kosong.</p>
                </div>
              )}
            </div>

            <div className="border-t border-slate-100 pt-4 space-y-4">
              <div className="flex justify-between items-center text-sm font-extrabold text-slate-800">
                <span>Total Tagihan:</span>
                <span className="font-mono text-lg text-[#004d40]">Rp {calculateOtcTotal().toLocaleString()}</span>
              </div>

              <button 
                onClick={handleOtcCheckout}
                disabled={cart.length === 0 || submittingOtc || !selectedOtcDepo}
                className="w-full py-3 bg-[#004d40] hover:bg-[#00332a] disabled:opacity-50 text-white font-bold rounded-lg text-sm shadow-sm transition-all flex items-center justify-center gap-2"
              >
                {submittingOtc ? <RefreshCw className="w-4 h-4 animate-spin" /> : (
                  <>
                    <CheckCircle2 className="w-5 h-5" /> Proses & Selesaikan OTC
                  </>
                )}
              </button>
            </div>
          </div>

        </div>
      )}


    </div>
  );
}
