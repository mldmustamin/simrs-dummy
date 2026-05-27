import { Test, TestingModule } from '@nestjs/testing';
import { RegistrationService } from './registration.service';
import { AuditService } from '../audit/audit.service';
import { BpjsService } from '../bpjs/bpjs.service';
import { PrismaService } from '../prisma/prisma.service';

describe('RegistrationService', () => {
  let service: RegistrationService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        RegistrationService,
        { provide: PrismaService, useValue: {} },
        { provide: BpjsService, useValue: {} },
        { provide: AuditService, useValue: {} },
      ],
    }).compile();

    service = module.get<RegistrationService>(RegistrationService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
