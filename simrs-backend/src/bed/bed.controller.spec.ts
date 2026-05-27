import { Test, TestingModule } from '@nestjs/testing';
import { BedController } from './bed.controller';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { BedService } from './bed.service';

describe('BedController', () => {
  let controller: BedController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [BedController],
      providers: [{ provide: BedService, useValue: {} }],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<BedController>(BedController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
