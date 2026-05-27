import { Test, TestingModule } from '@nestjs/testing';
import { RmeService } from './rme.service';
import { PrismaService } from '../prisma/prisma.service';

describe('RmeService', () => {
  let service: RmeService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [RmeService, { provide: PrismaService, useValue: {} }],
    }).compile();

    service = module.get<RmeService>(RmeService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
