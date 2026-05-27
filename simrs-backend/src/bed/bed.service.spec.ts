import { Test, TestingModule } from '@nestjs/testing';
import { BedService } from './bed.service';
import { PrismaService } from '../prisma/prisma.service';

describe('BedService', () => {
  let service: BedService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [BedService, { provide: PrismaService, useValue: {} }],
    }).compile();

    service = module.get<BedService>(BedService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
