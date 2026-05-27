import { Test, TestingModule } from '@nestjs/testing';
import { KasirController } from './kasir.controller';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { PermissionGuard } from '../auth/permission.guard';
import { KasirService } from './kasir.service';

describe('KasirController', () => {
  let controller: KasirController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [KasirController],
      providers: [{ provide: KasirService, useValue: {} }],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .overrideGuard(PermissionGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<KasirController>(KasirController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
