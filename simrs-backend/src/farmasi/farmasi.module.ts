import { Module } from '@nestjs/common';
import { FarmasiService } from './farmasi.service';
import { FarmasiController } from './farmasi.controller';
import { PrismaModule } from '../prisma/prisma.module';
import { AuditModule } from '../audit/audit.module';

@Module({
  imports: [PrismaModule, AuditModule],
  providers: [FarmasiService],
  controllers: [FarmasiController]
})
export class FarmasiModule {}

