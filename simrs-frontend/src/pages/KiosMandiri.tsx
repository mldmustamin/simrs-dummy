import { useState, useEffect } from 'react';
import { apiFetch } from '../lib/api';
import { 
  Building, User, CreditCard, Search, CheckCircle, ArrowLeft, ArrowRight, 
  Printer, RefreshCw, UserCheck 
} from 'lucide-react';

export default function KiosMandiri() {
  const [step, setStep] = useState<'WELCOME' | 'INPUT_RM' | 'VERIFY' | 'SELECT_SERVICE' | 'SELECT_PAYMENT' | 'SUCCESS'>('WELCOME');
  const [searchInput, setSearchInput] = useState('');
  const [patientData, setPatientData] = useState<any>(null);
  
  // Schedules and selections
  const [schedules, setSchedules] = useState<{ poliklinik: any[]; dokter: any[] }>({ poliklinik: [], dokter: [] });
  const [selectedPoli, setSelectedPoli] = useState<any>(null);
  const [selectedDokter, setSelectedDokter] = useState<any>(null);
  const [selectedPj, setSelectedPj] = useState<string>('A01'); // Default UMUM

  // Search and loading states
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successReg, setSuccessReg] = useState<any>(null);

  // Load schedules once Kios is opened
  useEffect(() => {
    async function loadSchedules() {
      try {
        const res = await apiFetch('http://localhost:3000/api/kiosk/active-schedules');
        const data = await res.json();
        setSchedules(data);
      } catch (err) {
        console.error('Gagal memuat jadwal dokter/poliklinik', err);
      }
    }
    loadSchedules();
  }, []);

  // Virtual Keyboard Keys helper
  const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', 'RM'];
  const handleKeyClick = (key: string) => {
    setErrorMsg('');
    if (key === 'RM') {
      setSearchInput('');
    } else {
      setSearchInput(prev => prev + key);
    }
  };

  const handleBackspace = () => {
    setSearchInput(prev => prev.slice(0, -1));
  };

  const handlePatientSearch = async () => {
    if (!searchInput.trim()) {
      setErrorMsg('Masukkan NIK atau Nomor RM Anda terlebih dahulu.');
      return;
    }
    setLoading(true);
    setErrorMsg('');
    try {
      const res = await apiFetch(`http://localhost:3000/api/kiosk/check-patient?q=${searchInput.trim()}`);
      const result = await res.json();
      if (result.exists) {
        setPatientData(result.data);
        setSelectedPj(result.data.kd_pj);
        setStep('VERIFY');
      } else {
        setErrorMsg('Data pasien tidak ditemukan. Silakan hubungi loket pendaftaran fisik untuk registrasi baru.');
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Terjadi kesalahan sistem pendaftaran.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegistration = async () => {
    if (!patientData || !selectedPoli || !selectedDokter) return;
    setLoading(true);
    setErrorMsg('');
    try {
      const payload = {
        no_rkm_medis: patientData.no_rkm_medis,
        kd_poli: selectedPoli.kd_poli,
        kd_dokter: selectedDokter.kd_dokter,
        kd_pj: selectedPj,
      };

      const res = await apiFetch('http://localhost:3000/api/kiosk/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        const result = await res.json();
        setSuccessReg(result);
        setStep('SUCCESS');
      } else {
        const err = await res.json();
        setErrorMsg(err.message || 'Pendaftaran gagal.');
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Gagal mendaftar. Koneksi terputus.');
    } finally {
      setLoading(false);
    }
  };

  const resetKiosk = () => {
    setStep('WELCOME');
    setSearchInput('');
    setPatientData(null);
    setSelectedPoli(null);
    setSelectedDokter(null);
    setSelectedPj('A01');
    setSuccessReg(null);
    setErrorMsg('');
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col font-sans select-none">
      {/* Header bar Kiosk */}
      <header className="bg-slate-950/80 backdrop-blur-md border-b border-slate-800/60 py-5 px-8 flex justify-between items-center shrink-0 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-teal-500 rounded-xl flex items-center justify-center shadow-md shadow-teal-500/20">
            <Building className="w-6 h-6 text-slate-900" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-teal-400 to-emerald-400 bg-clip-text text-transparent">
              ANJUNGAN PENDAFTARAN MANDIRI
            </h1>
            <p className="text-xs text-slate-400 font-semibold uppercase tracking-wider mt-0.5">RS Medika Utama Mandiri</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-sm font-bold text-teal-400">STATUS ONLINE</div>
          <div className="text-xs text-slate-500 mt-0.5 font-medium">Sistem Integrasi SIMRS</div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 flex flex-col items-center justify-center p-8 overflow-y-auto max-w-6xl mx-auto w-full">
        
        {/* Step: WELCOME */}
        {step === 'WELCOME' && (
          <div className="text-center max-w-2xl space-y-8 animate-fade-in py-10">
            <div className="space-y-4">
              <span className="bg-teal-500/10 text-teal-400 text-xs px-4 py-1.5 rounded-full font-bold uppercase tracking-wider border border-teal-500/20">
                Selamat Datang di Layanan Mandiri
              </span>
              <h2 className="text-4xl sm:text-5xl font-black text-slate-100 tracking-tight leading-none">
                Daftar & Berobat Lebih <br />
                <span className="text-teal-400">Cepat Tanpa Antre</span>
              </h2>
              <p className="text-slate-400 text-base max-w-lg mx-auto font-medium">
                Pendaftaran kunjungan rawat jalan pasien umum secara mandiri hanya dalam 3 langkah mudah.
              </p>
            </div>

            <div className="pt-6">
              <button 
                onClick={() => setStep('INPUT_RM')}
                className="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 active:scale-95 text-slate-950 font-black text-xl py-6 px-12 rounded-2xl shadow-xl shadow-teal-500/20 transition-all duration-200 flex items-center gap-4 mx-auto"
              >
                MULAI PENDAFTARAN MANDIRI
                <ArrowRight className="w-6 h-6 stroke-[3]" />
              </button>
            </div>

            <div className="grid grid-cols-3 gap-6 pt-10 text-center text-xs font-semibold text-slate-500 border-t border-slate-800/40">
              <div className="space-y-2">
                <div className="w-10 h-10 rounded-full bg-slate-800/60 border border-slate-700/40 flex items-center justify-center text-teal-400 mx-auto font-bold text-sm">1</div>
                <div>Masukkan NIK / No RM</div>
              </div>
              <div className="space-y-2">
                <div className="w-10 h-10 rounded-full bg-slate-800/60 border border-slate-700/40 flex items-center justify-center text-teal-400 mx-auto font-bold text-sm">2</div>
                <div>Pilih Poli & Dokter</div>
              </div>
              <div className="space-y-2">
                <div className="w-10 h-10 rounded-full bg-slate-800/60 border border-slate-700/40 flex items-center justify-center text-teal-400 mx-auto font-bold text-sm">3</div>
                <div>Cetak Tiket Antrean</div>
              </div>
            </div>
          </div>
        )}

        {/* Step: INPUT_RM */}
        {step === 'INPUT_RM' && (
          <div className="w-full max-w-2xl bg-slate-950/40 border border-slate-800 rounded-3xl p-8 shadow-2xl animate-fade-in space-y-6">
            <div className="flex justify-between items-center">
              <button onClick={resetKiosk} className="flex items-center gap-2 text-sm text-slate-400 hover:text-white font-bold transition-colors">
                <ArrowLeft className="w-4 h-4" /> BATALKAN
              </button>
              <div className="text-xs font-bold text-teal-400 tracking-wider">LANGKAH 1 DARI 4</div>
            </div>

            <div className="space-y-2">
              <h3 className="text-2xl font-black text-slate-100">Ketik NIK atau Nomor RM Anda</h3>
              <p className="text-sm text-slate-400">Silakan isi menggunakan keyboard layar sentuh di bawah ini.</p>
            </div>

            {/* Input Box Display */}
            <div className="relative">
              <Search className="absolute left-4 top-4.5 w-6 h-6 text-teal-400" />
              <input 
                type="text" 
                value={searchInput}
                readOnly
                placeholder="Contoh: 327409xxxxxxxxxx atau 000001" 
                className="w-full bg-slate-900 border-2 border-slate-700 rounded-2xl py-4.5 pl-14 pr-16 text-xl font-extrabold text-teal-300 tracking-wider focus:outline-none focus:border-teal-500 transition-colors shadow-inner"
              />
              {searchInput.length > 0 && (
                <button 
                  onClick={handleBackspace}
                  className="absolute right-4 top-4 bg-slate-800 hover:bg-slate-700 active:scale-95 text-slate-300 p-2 rounded-lg text-xs font-bold transition-all"
                >
                  HAPUS
                </button>
              )}
            </div>

            {errorMsg && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl text-sm font-bold text-center">
                {errorMsg}
              </div>
            )}

            {/* Touch screen keyboard */}
            <div className="grid grid-cols-3 gap-3">
              {keys.map(key => (
                <button 
                  key={key} 
                  onClick={() => handleKeyClick(key)}
                  className="bg-slate-850 hover:bg-slate-750 active:scale-95 text-slate-100 font-extrabold text-2xl py-5 rounded-2xl border border-slate-800 transition-all duration-100 shadow-md active:bg-slate-700 flex items-center justify-center"
                >
                  {key}
                </button>
              ))}
            </div>

            <div className="flex gap-4 pt-2">
              <button 
                onClick={() => setSearchInput('')}
                className="flex-1 bg-slate-800 hover:bg-slate-700 active:scale-95 text-slate-300 font-extrabold py-4 rounded-xl text-sm transition-all"
              >
                RESET KOSONGKAN
              </button>
              <button 
                onClick={handlePatientSearch}
                disabled={loading}
                className="flex-2 bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 active:scale-95 disabled:opacity-50 text-slate-950 font-black py-4 rounded-xl text-lg shadow-lg shadow-teal-500/10 transition-all flex items-center justify-center gap-2"
              >
                {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : 'VERIFIKASI DATA'}
              </button>
            </div>
          </div>
        )}

        {/* Step: VERIFY */}
        {step === 'VERIFY' && patientData && (
          <div className="w-full max-w-2xl bg-slate-950/40 border border-slate-800 rounded-3xl p-8 shadow-2xl animate-fade-in space-y-6">
            <div className="flex justify-between items-center">
              <button onClick={() => setStep('INPUT_RM')} className="flex items-center gap-2 text-sm text-slate-400 hover:text-white font-bold transition-colors">
                <ArrowLeft className="w-4 h-4" /> KEMBALI
              </button>
              <div className="text-xs font-bold text-teal-400 tracking-wider">LANGKAH 2 DARI 4</div>
            </div>

            <div className="space-y-2">
              <h3 className="text-2xl font-black text-slate-100">Apakah Data Anda Sudah Benar?</h3>
              <p className="text-sm text-slate-400">Tolong pastikan data identitas di bawah ini adalah milik Anda.</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <span className="text-xs text-slate-400 font-bold tracking-wider uppercase">Nama Pasien</span>
                <span className="text-lg font-black text-teal-300">{patientData.nm_pasien}</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <span className="text-xs text-slate-400 font-bold tracking-wider uppercase">Nomor Rekam Medis (RM)</span>
                <span className="text-sm font-extrabold text-slate-200 tracking-wider">{patientData.no_rkm_medis}</span>
              </div>
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <span className="text-xs text-slate-400 font-bold tracking-wider uppercase">NIK (KTP)</span>
                <span className="text-sm font-extrabold text-slate-200 tracking-wider">{patientData.no_ktp}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-400 font-bold tracking-wider uppercase">Alamat Rumah</span>
                <span className="text-sm font-extrabold text-slate-200 max-w-xs text-right truncate">{patientData.alamat}</span>
              </div>
            </div>

            <div className="flex gap-4">
              <button 
                onClick={resetKiosk}
                className="flex-1 bg-red-500/10 hover:bg-red-500/20 active:scale-95 text-red-400 font-extrabold py-4 rounded-xl text-sm border border-red-500/20 transition-all"
              >
                TIDAK, DATA SALAH
              </button>
              <button 
                onClick={() => setStep('SELECT_SERVICE')}
                className="flex-2 bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 active:scale-95 text-slate-950 font-black py-4 rounded-xl text-lg shadow-lg shadow-teal-500/10 transition-all flex items-center justify-center gap-2"
              >
                YA, DATA BENAR
                <ArrowRight className="w-5 h-5 stroke-[3]" />
              </button>
            </div>
          </div>
        )}

        {/* Step: SELECT_SERVICE */}
        {step === 'SELECT_SERVICE' && (
          <div className="w-full max-w-4xl bg-slate-950/40 border border-slate-800 rounded-3xl p-8 shadow-2xl animate-fade-in space-y-6">
            <div className="flex justify-between items-center">
              <button onClick={() => setStep('VERIFY')} className="flex items-center gap-2 text-sm text-slate-400 hover:text-white font-bold transition-colors">
                <ArrowLeft className="w-4 h-4" /> KEMBALI
              </button>
              <div className="text-xs font-bold text-teal-400 tracking-wider">LANGKAH 3 DARI 4</div>
            </div>

            <div className="space-y-1">
              <h3 className="text-2xl font-black text-slate-100">Pilih Poliklinik & Dokter Spesialis</h3>
              <p className="text-sm text-slate-400">Silakan pilih unit pelayanan medis yang Anda tuju hari ini.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              {/* Poliklinik selection list */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                  <Building className="w-4 h-4 text-teal-400" /> Poliklinik Tujuan
                </h4>
                <div className="grid grid-cols-2 gap-3 max-h-[300px] overflow-y-auto pr-1">
                  {schedules.poliklinik.map(p => {
                    const isSelected = selectedPoli?.kd_poli === p.kd_poli;
                    return (
                      <div 
                        key={p.kd_poli}
                        onClick={() => setSelectedPoli(p)}
                        className={`p-4 rounded-2xl border text-center cursor-pointer transition-all active:scale-95 ${isSelected ? 'border-teal-500 bg-teal-500/10 text-teal-300 shadow-md' : 'border-slate-800 hover:border-slate-700 bg-slate-900/50 text-slate-300'}`}
                      >
                        <div className="text-sm font-bold truncate">{p.nm_poli}</div>
                        <div className="text-[10px] text-slate-500 mt-1 uppercase font-semibold">Aktif Hari Ini</div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Dokter selection list */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                  <UserCheck className="w-4 h-4 text-teal-400" /> Dokter Spesialis
                </h4>
                <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1">
                  {schedules.dokter.map(d => {
                    const isSelected = selectedDokter?.kd_dokter === d.kd_dokter;
                    return (
                      <div 
                        key={d.kd_dokter}
                        onClick={() => setSelectedDokter(d)}
                        className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-center justify-between active:scale-95 ${isSelected ? 'border-teal-500 bg-teal-500/10 text-teal-300 shadow-md' : 'border-slate-800 hover:border-slate-700 bg-slate-900/50 text-slate-300'}`}
                      >
                        <div>
                          <div className="text-sm font-extrabold">{d.nm_dokter}</div>
                          <div className="text-[10px] text-slate-500 uppercase mt-0.5 font-semibold">Spesialis Dokter</div>
                        </div>
                        {isSelected && <div className="w-3.5 h-3.5 rounded-full bg-teal-400 border-2 border-slate-900 shadow shadow-teal-500/20" />}
                      </div>
                    );
                  })}
                </div>
              </div>

            </div>

            <div className="pt-4 border-t border-slate-800/60 flex items-center justify-between">
              <div className="text-sm font-bold text-slate-400">
                Poli: <span className="text-teal-400">{selectedPoli?.nm_poli || '-'}</span> • Dokter: <span className="text-teal-400">{selectedDokter?.nm_dokter || '-'}</span>
              </div>
              <button 
                onClick={() => setStep('SELECT_PAYMENT')}
                disabled={!selectedPoli || !selectedDokter}
                className="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 active:scale-95 disabled:opacity-50 text-slate-950 font-black py-4 px-8 rounded-xl text-lg shadow-lg shadow-teal-500/10 transition-all flex items-center justify-center gap-2"
              >
                SELANJUTNYA
                <ArrowRight className="w-5 h-5 stroke-[3]" />
              </button>
            </div>
          </div>
        )}

        {/* Step: SELECT_PAYMENT */}
        {step === 'SELECT_PAYMENT' && (
          <div className="w-full max-w-2xl bg-slate-950/40 border border-slate-800 rounded-3xl p-8 shadow-2xl animate-fade-in space-y-6">
            <div className="flex justify-between items-center">
              <button onClick={() => setStep('SELECT_SERVICE')} className="flex items-center gap-2 text-sm text-slate-400 hover:text-white font-bold transition-colors">
                <ArrowLeft className="w-4 h-4" /> KEMBALI
              </button>
              <div className="text-xs font-bold text-teal-400 tracking-wider">LANGKAH 4 DARI 4</div>
            </div>

            <div className="space-y-1">
              <h3 className="text-2xl font-black text-slate-100">Pilih Cara Pembayaran</h3>
              <p className="text-sm text-slate-400">Silakan tentukan metode pembiayaan perawatan Anda.</p>
            </div>

            <div className="grid grid-cols-2 gap-4">
              {/* Option: UMUM / MANDIRI */}
              <div 
                onClick={() => setSelectedPj('A01')}
                className={`p-6 rounded-2xl border cursor-pointer text-center space-y-3 transition-all active:scale-95 ${selectedPj === 'A01' ? 'border-teal-500 bg-teal-500/10 text-teal-300' : 'border-slate-800 bg-slate-900/50 text-slate-400 hover:border-slate-700'}`}
              >
                <div className="w-12 h-12 rounded-full bg-teal-500/20 text-teal-400 flex items-center justify-center mx-auto">
                  <CreditCard className="w-6 h-6" />
                </div>
                <div>
                  <div className="font-extrabold text-base text-slate-200">UMUM (MANDIRI)</div>
                  <div className="text-[10px] text-slate-500 mt-1 uppercase font-semibold">Pembayaran Tunai / QRIS</div>
                </div>
              </div>

              {/* Option: BPJS KESEHATAN */}
              <div 
                onClick={() => setSelectedPj('BPJ')}
                className={`p-6 rounded-2xl border cursor-pointer text-center space-y-3 transition-all active:scale-95 ${selectedPj === 'BPJ' ? 'border-teal-500 bg-teal-500/10 text-teal-300' : 'border-slate-800 bg-slate-900/50 text-slate-400 hover:border-slate-700'}`}
              >
                <div className="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto">
                  <User className="w-6 h-6" />
                </div>
                <div>
                  <div className="font-extrabold text-base text-slate-200">BPJS KESEHATAN</div>
                  <div className="text-[10px] text-slate-500 mt-1 uppercase font-semibold">Bridging SEP Otonom</div>
                </div>
              </div>
            </div>

            {errorMsg && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl text-sm font-bold text-center">
                {errorMsg}
              </div>
            )}

            <button 
              onClick={handleRegistration}
              disabled={loading}
              className="w-full bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 active:scale-95 disabled:opacity-50 text-slate-950 font-black py-4 rounded-xl text-lg shadow-lg shadow-teal-500/20 transition-all flex items-center justify-center gap-2"
            >
              {loading ? <RefreshCw className="w-5 h-5 animate-spin" /> : (
                <>
                  <Printer className="w-5 h-5 stroke-[2.5]" />
                  KONFIRMASI & CETAK ANTRIAN
                </>
              )}
            </button>
          </div>
        )}

        {/* Step: SUCCESS */}
        {step === 'SUCCESS' && successReg && (
          <div className="w-full max-w-lg bg-slate-950/60 border border-teal-500/40 rounded-3xl p-8 shadow-2xl animate-fade-in text-center space-y-6">
            <div className="w-16 h-16 bg-teal-500/10 border-2 border-teal-500 text-teal-400 rounded-full flex items-center justify-center mx-auto shadow shadow-teal-500/20">
              <CheckCircle className="w-10 h-10" />
            </div>

            <div className="space-y-1">
              <h3 className="text-2xl font-black text-slate-100">Pendaftaran Selesai!</h3>
              <p className="text-sm text-slate-400">Silakan ambil karcis antrean dan bukti register di printer APM.</p>
            </div>

            {/* Receipt Mockup */}
            <div className="bg-white text-slate-900 rounded-2xl p-6 text-left border border-slate-200 shadow-lg space-y-4 font-mono">
              <div className="text-center border-b-2 border-dashed border-slate-300 pb-3">
                <h4 className="font-extrabold text-sm tracking-wide">RS MEDIKA UTAMA MANDIRI</h4>
                <p className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Karcis Antrean Kiosk Mandiri (APM)</p>
              </div>

              <div className="text-center space-y-1 py-2">
                <div className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">Nomor Antrean Poli</div>
                <div className="text-5xl font-black text-teal-800 tracking-tight">{successReg.no_reg}</div>
              </div>

              <div className="text-xs space-y-2 border-t border-slate-200 pt-4 font-sans font-medium text-slate-700">
                <div className="flex justify-between">
                  <span>Nama:</span>
                  <span className="font-bold text-slate-900 uppercase">{patientData?.nm_pasien}</span>
                </div>
                <div className="flex justify-between">
                  <span>No. Rawat:</span>
                  <span className="font-bold text-slate-900">{successReg.no_rawat}</span>
                </div>
                <div className="flex justify-between">
                  <span>Poliklinik:</span>
                  <span className="font-bold text-slate-900">{selectedPoli?.nm_poli}</span>
                </div>
                <div className="flex justify-between">
                  <span>Dokter:</span>
                  <span className="font-bold text-slate-900">{selectedDokter?.nm_dokter}</span>
                </div>
                <div className="flex justify-between">
                  <span>Cara Bayar:</span>
                  <span className="font-bold text-teal-800 uppercase">{selectedPj === 'A01' ? 'UMUM' : 'BPJS'}</span>
                </div>
              </div>

              <div className="text-center border-t-2 border-dashed border-slate-300 pt-4 text-[9px] text-slate-400 font-sans font-bold uppercase tracking-widest">
                Terima kasih atas kepercayaan Anda
              </div>
            </div>

            <button 
              onClick={resetKiosk}
              className="w-full bg-slate-800 hover:bg-slate-750 active:scale-95 text-teal-400 font-black py-4 rounded-xl text-lg tracking-wide transition-all"
            >
              SELESAI (KEMBALI KE BERANDA)
            </button>
          </div>
        )}

      </main>

      {/* Footer bar */}
      <footer className="bg-slate-950/40 border-t border-slate-800/40 py-4 px-8 text-center text-xs text-slate-500 font-medium shrink-0">
        &copy; {new Date().getFullYear()} RS Medika Utama Mandiri. Integrasi SIMRS Web Client Versi 2.0
      </footer>
    </div>
  );
}
