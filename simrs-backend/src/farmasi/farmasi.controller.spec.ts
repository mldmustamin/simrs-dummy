import { Test, TestingModule } from '@nestjs/testing';
import { FarmasiController } from './farmasi.controller';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { PermissionGuard } from '../auth/permission.guard';
import { FarmasiService } from './farmasi.service';

describe('FarmasiController', () => {
  let controller: FarmasiController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [FarmasiController],
      providers: [{ provide: FarmasiService, useValue: {} }],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .overrideGuard(PermissionGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<FarmasiController>(FarmasiController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
