import { Test, TestingModule } from '@nestjs/testing';
import { CasemixController } from './casemix.controller';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { CasemixService } from './casemix.service';

describe('CasemixController', () => {
  let controller: CasemixController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [CasemixController],
      providers: [{ provide: CasemixService, useValue: {} }],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<CasemixController>(CasemixController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
