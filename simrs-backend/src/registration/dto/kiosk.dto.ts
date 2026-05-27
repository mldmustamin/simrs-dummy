import { IsNotEmpty, IsString, MaxLength } from 'class-validator';

export class CheckPatientQueryDto {
  @IsString()
  @IsNotEmpty()
  @MaxLength(30)
  q: string;
}

export class RegisterKioskDto {
  @IsString()
  @IsNotEmpty()
  @MaxLength(15)
  no_rkm_medis: string;

  @IsString()
  @IsNotEmpty()
  @MaxLength(5)
  kd_poli: string;

  @IsString()
  @IsNotEmpty()
  @MaxLength(20)
  kd_dokter: string;

  @IsString()
  @IsNotEmpty()
  @MaxLength(3)
  kd_pj: string;
}
