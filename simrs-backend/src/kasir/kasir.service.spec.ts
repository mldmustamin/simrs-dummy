import { Test, TestingModule } from '@nestjs/testing';
import { KasirService } from './kasir.service';
import { AuditService } from '../audit/audit.service';
import { PrismaService } from '../prisma/prisma.service';

describe('KasirService', () => {
  let service: KasirService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        KasirService,
        { provide: PrismaService, useValue: {} },
        { provide: AuditService, useValue: {} },
      ],
    }).compile();

    service = module.get<KasirService>(KasirService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
