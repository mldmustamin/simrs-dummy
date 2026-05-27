import { Module } from '@nestjs/common';
import { RegistrationService } from './registration.service';
import { RegistrationController } from './registration.controller';
import { KioskService } from './kiosk.service';
import { KioskController } from './kiosk.controller';
import { PrismaModule } from '../prisma/prisma.module';
import { BpjsModule } from '../bpjs/bpjs.module';
import { AuditModule } from '../audit/audit.module';

@Module({
  imports: [PrismaModule, BpjsModule, AuditModule],
  providers: [RegistrationService, KioskService],
  controllers: [RegistrationController, KioskController]
})
export class RegistrationModule {}


