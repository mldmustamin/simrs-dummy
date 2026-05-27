import { Test, TestingModule } from '@nestjs/testing';
import { FarmasiService } from './farmasi.service';
import { AuditService } from '../audit/audit.service';
import { PrismaService } from '../prisma/prisma.service';

describe('FarmasiService', () => {
  let service: FarmasiService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        FarmasiService,
        { provide: PrismaService, useValue: {} },
        { provide: AuditService, useValue: {} },
      ],
    }).compile();

    service = module.get<FarmasiService>(FarmasiService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
