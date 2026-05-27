import { Module } from '@nestjs/common';
import { KasirController } from './kasir.controller';
import { KasirService } from './kasir.service';
import { AuditModule } from '../audit/audit.module';

@Module({
  imports: [AuditModule],
  controllers: [KasirController],
  providers: [KasirService]
})
export class KasirModule {}

