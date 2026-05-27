import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export interface AuditPayload {
  module: string;
  action: string;
  entityName: string;
  entityId: string;
  actorId: string;
  actorName: string;
  ipAddress?: string;
  userAgent?: string;
  beforePayload?: any;
  afterPayload?: any;
}

@Injectable()
export class AuditService {
  constructor(private readonly prisma: PrismaService) {}

  /**
   * Mengembalikan operasi create Prisma untuk Audit Trail yang bisa disematkan
   * di dalam blok `$transaction`. Ini menjamin audit dan transaksi utama terikat (durable outbox/ACID).
   */
  createAuditTx(tx: any, payload: AuditPayload) {
    return tx.simrs_web_audit_trail.create({
      data: {
        module: payload.module,
        action: payload.action,
        entity_name: payload.entityName,
        entity_id: payload.entityId,
        actor_id: payload.actorId,
        actor_name: payload.actorName,
        ip_address: payload.ipAddress || null,
        user_agent: payload.userAgent || null,
        before_payload: payload.beforePayload || null,
        after_payload: payload.afterPayload || null,
      },
    });
  }

  /**
   * Eksekusi langsung ke database (Fire-and-forget / non-transactional)
   * Hanya untuk event non-kritis seperti login.
   */
  async logNonCritical(payload: AuditPayload) {
    try {
      await this.prisma.simrs_web_audit_trail.create({
        data: {
          module: payload.module,
          action: payload.action,
          entity_name: payload.entityName,
          entity_id: payload.entityId,
          actor_id: payload.actorId,
          actor_name: payload.actorName,
          ip_address: payload.ipAddress || null,
          user_agent: payload.userAgent || null,
          before_payload: payload.beforePayload || null,
          after_payload: payload.afterPayload || null,
        },
      });
    } catch (error) {
      // Fire-and-forget, jangan biarkan error membatalkan flow login
      console.error('Failed to write non-critical audit log:', error);
    }
  }
}
