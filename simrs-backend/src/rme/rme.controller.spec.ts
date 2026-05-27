import { Test, TestingModule } from '@nestjs/testing';
import { RmeController } from './rme.controller';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { RmeService } from './rme.service';

describe('RmeController', () => {
  let controller: RmeController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [RmeController],
      providers: [{ provide: RmeService, useValue: {} }],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<RmeController>(RmeController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
