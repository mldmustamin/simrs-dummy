import { Test, TestingModule } from '@nestjs/testing';
import { BpjsService } from './bpjs.service';
import { PrismaService } from '../prisma/prisma.service';

describe('BpjsService', () => {
  let service: BpjsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [BpjsService, { provide: PrismaService, useValue: {} }],
    }).compile();

    service = module.get<BpjsService>(BpjsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
