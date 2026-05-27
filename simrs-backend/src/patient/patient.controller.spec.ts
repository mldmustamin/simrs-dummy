import { Test, TestingModule } from '@nestjs/testing';
import { PatientController } from './patient.controller';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { PatientService } from './patient.service';

describe('PatientController', () => {
  let controller: PatientController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [PatientController],
      providers: [{ provide: PatientService, useValue: {} }],
    })
      .overrideGuard(JwtAuthGuard)
      .useValue({ canActivate: () => true })
      .compile();

    controller = module.get<PatientController>(PatientController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
