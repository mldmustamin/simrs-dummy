import { Injectable, Logger } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { BpjsService } from '../bpjs/bpjs.service';
import { AuditService } from '../audit/audit.service';

@Injectable()
export class RegistrationService {
  private readonly logger = new Logger(RegistrationService.name);

  constructor(
    private prisma: PrismaService,
    private bpjsService: BpjsService,
    private readonly auditService: AuditService,
  ) {}

  async createRegistration(data: {
    no_rkm_medis: string;
    kd_dokter: string;
    kd_poli: string;
    kd_pj: string;
    bypassNoSep?: string;
    isAdminBypass?: boolean;
  }) {
    const today = new Date();
    
    // Format YYYY/MM/DD
    const dateStr = today.toISOString().split('T')[0].replace(/-/g, '/');
    
    // Cari no rawat terakhir hari ini
    const lastReg = await this.prisma.reg_periksa.findFirst({
      where: {
        no_rawat: { startsWith: dateStr }
      },
      orderBy: { no_rawat: 'desc' }
    });

    let no_urut = "000001";
    if (lastReg) {
      const lastNo = parseInt(lastReg.no_rawat.split('/').pop() || "0");
      no_urut = (lastNo + 1).toString().padStart(6, '0');
    }
    const no_rawat = `${dateStr}/${no_urut}`;

    // Cari no antrean
    const lastAntrean = await this.prisma.reg_periksa.findFirst({
      where: {
        kd_poli: data.kd_poli,
        kd_dokter: data.kd_dokter,
        tgl_registrasi: today
      },
      orderBy: { no_reg: 'desc' }
    });

    let no_reg = "001";
    if (lastAntrean && lastAntrean.no_reg) {
      const lastRegNo = parseInt(lastAntrean.no_reg);
      no_reg = (lastRegNo + 1).toString().padStart(3, '0');
    }

    // Insert to database
    const reg = await this.prisma.reg_periksa.create({
      data: {
        no_rawat,
        no_reg,
        tgl_registrasi: today,
        jam_reg: today,
        kd_dokter: data.kd_dokter,
        no_rkm_medis: data.no_rkm_medis,
        kd_poli: data.kd_poli,
        kd_pj: data.kd_pj,
        p_jawab: 'Mandiri', // Default
        almt_pj: 'Alamat',
        hubunganpj: 'Sendiri',
        stts: 'Belum',
        stts_daftar: 'Lama',
        status_lanjut: 'Ralan',
        status_bayar: 'Belum_Bayar',
        status_poli: 'Lama',
        sttsumur: 'Th',
      }
    });

    // BPJS Bridging Logic (100% Otonom Default + Escape Hatch)
    if (data.kd_pj === 'BPJ') {
      try {
        const pasien = await this.prisma.pasien.findUnique({
          where: { no_rkm_medis: data.no_rkm_medis }
        });
        const noKartu = pasien?.no_peserta || '';
        
        await this.bpjsService.createSEP(
          noKartu,
          reg.no_rawat,
          data.kd_poli,
          data.kd_dokter,
          data.isAdminBypass,
          data.bypassNoSep
        );
      } catch (error) {
        this.logger.error(`Gagal membuat SEP: ${error.message}`);
        throw new Error(`Pendaftaran sukses, namun Bridging V-Claim gagal: ${error.message}`);
      }
    }

    return reg;
  }

  async createApsRegistration(data: {
    no_rkm_medis: string;
    kd_dokter?: string;
    kd_poli?: string;
    kd_pj?: string;
    jenis_layanan: 'Lab' | 'Radiologi';
    p_jawab?: string;
    almt_pj?: string;
    hubunganpj?: string;
    actor?: { id: string; name: string };
    ipAddress?: string;
    userAgent?: string;
  }) {
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0].replace(/-/g, '/');

    // 1. Resolve Poli and Dokter if not supplied
    const targetPoli = data.kd_poli || (data.jenis_layanan === 'Lab' ? 'U0026' : 'U0008'); // Unit Laborat / Poliklinik Radiologi
    const targetDokter = data.kd_dokter || '-';

    // 2. Fetch patient to get default kd_pj if not provided
    const pasien = await this.prisma.pasien.findUnique({
      where: { no_rkm_medis: data.no_rkm_medis }
    });

    if (!pasien) {
      throw new Error(`Pasien dengan No RM ${data.no_rkm_medis} tidak ditemukan.`);
    }

    const targetPj = data.kd_pj || pasien.kd_pj || 'A01'; // Default to A01 (Umum) if null

    // 3. Generate no_rawat
    const lastReg = await this.prisma.reg_periksa.findFirst({
      where: {
        no_rawat: { startsWith: dateStr }
      },
      orderBy: { no_rawat: 'desc' }
    });

    let no_urut = "000001";
    if (lastReg) {
      const lastNo = parseInt(lastReg.no_rawat.split('/').pop() || "0");
      no_urut = (lastNo + 1).toString().padStart(6, '0');
    }
    const no_rawat = `${dateStr}/${no_urut}`;

    // 4. Generate no_reg (queue number)
    const lastAntrean = await this.prisma.reg_periksa.findFirst({
      where: {
        kd_poli: targetPoli,
        kd_dokter: targetDokter,
        tgl_registrasi: today
      },
      orderBy: { no_reg: 'desc' }
    });

    let no_reg = "001";
    if (lastAntrean && lastAntrean.no_reg) {
      const lastRegNo = parseInt(lastAntrean.no_reg);
      no_reg = (lastRegNo + 1).toString().padStart(3, '0');
    }

    // 5. Save to reg_periksa and write audit trail in a single Prisma transaction
    const reg = await this.prisma.$transaction(async (tx) => {
      const createdReg = await tx.reg_periksa.create({
        data: {
          no_rawat,
          no_reg,
          tgl_registrasi: today,
          jam_reg: today,
          kd_dokter: targetDokter,
          no_rkm_medis: data.no_rkm_medis,
          kd_poli: targetPoli,
          kd_pj: targetPj,
          p_jawab: data.p_jawab || pasien.nm_pasien || 'Mandiri',
          almt_pj: data.almt_pj || pasien.alamat || 'Alamat',
          hubunganpj: data.hubunganpj || 'Sendiri',
          stts: 'Belum',
          stts_daftar: 'Lama',
          status_lanjut: 'Ralan',
          status_bayar: 'Belum_Bayar',
          status_poli: 'Lama',
          sttsumur: 'Th',
          sumber_daftar: 'APS', // Flag khusus Layanan Mandiri APS
        }
      });

      // Jika layanan mandiri adalah Laboratorium, otomatis masukkan tindakan lab dasar
      if (data.jenis_layanan === 'Lab') {
        const labTest = await tx.jns_perawatan_lab.findFirst({
          where: { status: '1' }
        });

        if (labTest) {
          const docCode = targetDokter === '-' ? 'D0000004' : targetDokter;
          await tx.periksa_lab.create({
            data: {
              no_rawat,
              nip: '-', // Default
              kd_jenis_prw: labTest.kd_jenis_prw,
              tgl_periksa: today,
              jam: today,
              dokter_perujuk: docCode,
              bagian_rs: labTest.bagian_rs || 0,
              bhp: labTest.bhp,
              tarif_perujuk: labTest.tarif_perujuk,
              tarif_tindakan_dokter: labTest.tarif_tindakan_dokter,
              tarif_tindakan_petugas: labTest.tarif_tindakan_petugas || 0,
              kso: labTest.kso || 0,
              menejemen: labTest.menejemen || 0,
              biaya: labTest.total_byr || 0,
              kd_dokter: docCode,
              status: 'Belum',
              kategori: labTest.kategori || 'PK',
            }
          });
        }
      }

      // Audit Trail
      await this.auditService.createAuditTx(tx, {
        module: 'Registration',
        action: 'CreateAPS',
        entityName: 'reg_periksa',
        entityId: no_rawat,
        actorId: data.actor?.id || 'system',
        actorName: data.actor?.name || 'System',
        ipAddress: data.ipAddress,
        userAgent: data.userAgent,
        beforePayload: null,
        afterPayload: {
          no_rawat,
          no_reg,
          kd_poli: targetPoli,
          jenis_layanan: data.jenis_layanan,
        },
      });

      return createdReg;
    });

    return reg;
  }
}

