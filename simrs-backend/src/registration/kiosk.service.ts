import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { AuditService } from '../audit/audit.service';

@Injectable()
export class KioskService {
  private readonly logger = new Logger(KioskService.name);

  constructor(
    private readonly prisma: PrismaService,
    private readonly auditService: AuditService,
  ) {}

  async checkPatient(q: string) {
    if (!q || q.trim() === '') {
      throw new Error('Kata kunci pencarian tidak boleh kosong');
    }

    const patient = await this.prisma.pasien.findFirst({
      where: {
        OR: [
          { no_rkm_medis: q.trim() },
          { no_ktp: q.trim() },
        ],
      },
      include: {
        penjab: true,
      },
    });

    if (!patient) {
      return { exists: false, data: null };
    }

    return {
      exists: true,
      data: {
        no_rkm_medis: patient.no_rkm_medis,
        nm_pasien: patient.nm_pasien,
        no_ktp: patient.no_ktp,
        alamat: patient.alamat || '-',
        kd_pj: patient.kd_pj || 'A01',
        cara_bayar: patient.penjab?.png_jawab || 'UMUM',
      },
    };
  }

  async getActiveSchedules() {
    // Mengambil semua poliklinik dan dokter yang tersedia untuk pendaftaran
    const [poliklinik, dokter] = await Promise.all([
      this.prisma.poliklinik.findMany({
        select: { kd_poli: true, nm_poli: true },
      }),
      this.prisma.dokter.findMany({
        select: { kd_dokter: true, nm_dokter: true },
      }),
    ]);

    return { poliklinik, dokter };
  }

  async registerKiosk(data: {
    no_rkm_medis: string;
    kd_poli: string;
    kd_dokter: string;
    kd_pj: string;
  }) {
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0].replace(/-/g, '/');

    // 1. Verifikasi Pasien
    const patient = await this.prisma.pasien.findUnique({
      where: { no_rkm_medis: data.no_rkm_medis },
    });

    if (!patient) {
      throw new Error(`Pasien dengan No RM ${data.no_rkm_medis} tidak ditemukan.`);
    }

    const MAX_RETRIES = 5;
    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
      try {
        // 2. Jalankan pembuatan nomor rawat dan antrean di dalam transaksi database yang aman
        const reg = await this.prisma.$transaction(async (tx) => {
          // Cari nomor rawat terakhir hari ini
          const lastReg = await tx.reg_periksa.findFirst({
            where: {
              no_rawat: { startsWith: dateStr },
            },
            orderBy: { no_rawat: 'desc' },
          });

          let no_urut = '000001';
          if (lastReg) {
            const lastNo = parseInt(lastReg.no_rawat.split('/').pop() || '0');
            no_urut = (lastNo + 1).toString().padStart(6, '0');
          }
          const no_rawat = `${dateStr}/${no_urut}`;

          const queryDate = new Date(today.toISOString().split('T')[0] + 'T00:00:00.000Z');

          // Cari nomor antrean terakhir untuk poli dan dokter ini hari ini
          const lastAntrean = await tx.reg_periksa.findFirst({
            where: {
              kd_poli: data.kd_poli,
              kd_dokter: data.kd_dokter,
              tgl_registrasi: queryDate,
            },
            orderBy: { no_reg: 'desc' },
          });

          let no_reg = '001';
          if (lastAntrean && lastAntrean.no_reg) {
            const lastRegNo = parseInt(lastAntrean.no_reg);
            no_reg = (lastRegNo + 1).toString().padStart(3, '0');
          }

          // Simpan data pendaftaran
          const createdReg = await tx.reg_periksa.create({
            data: {
              no_rawat,
              no_reg,
              tgl_registrasi: today,
              jam_reg: today,
              kd_dokter: data.kd_dokter,
              no_rkm_medis: data.no_rkm_medis,
              kd_poli: data.kd_poli,
              kd_pj: data.kd_pj,
              p_jawab: patient.nm_pasien || 'Mandiri',
              almt_pj: patient.alamat || 'Alamat',
              hubunganpj: 'Sendiri',
              stts: 'Belum',
              stts_daftar: 'Lama',
              status_lanjut: 'Ralan',
              status_bayar: 'Belum_Bayar',
              status_poli: 'Lama',
              sttsumur: 'Th',
              sumber_daftar: 'APM', // Flag khusus Kiosk Pendaftaran Mandiri
            },
            include: {
              poliklinik: true,
              dokter: true,
            },
          });

          // Simpan jejak audit secara aman terikat dalam transaksi
          await this.auditService.createAuditTx(tx, {
            module: 'KioskRegistration',
            action: 'CreateAPM',
            entityName: 'reg_periksa',
            entityId: no_rawat,
            actorId: 'Kiosk-APM',
            actorName: `Kios Mandiri - Pasien ${patient.nm_pasien}`,
            ipAddress: '127.0.0.1',
            userAgent: 'Kiosk Browser',
            beforePayload: null,
            afterPayload: {
              no_rawat,
              no_reg,
              kd_poli: data.kd_poli,
              nm_poli: createdReg.poliklinik.nm_poli,
              kd_dokter: data.kd_dokter,
              nm_dokter: createdReg.dokter.nm_dokter,
            },
          });

          return createdReg;
        });

        return reg;
      } catch (error: any) {
        // Jika error adalah unique constraint violation (P2002), lakukan retry
        if (error.code === 'P2002' && attempt < MAX_RETRIES) {
          const delay = Math.floor(Math.random() * 100) + 50; // Jeda acak 50ms - 150ms
          this.logger.warn(`Konflik nomor rawat terdeteksi (attempt ${attempt}/${MAX_RETRIES}). Mengulang dalam ${delay}ms...`);
          await new Promise((resolve) => setTimeout(resolve, delay));
          continue;
        }
        throw error;
      }
    }
  }
}
