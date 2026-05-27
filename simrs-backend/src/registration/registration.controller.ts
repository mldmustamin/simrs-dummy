import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { Controller, UseGuards, Post, Body, Req } from '@nestjs/common';
import { RegistrationService } from './registration.service';
import { PermissionGuard } from '../auth/permission.guard';
import { RequirePermission } from '../auth/require-permission.decorator';
import { CurrentUser, AuthenticatedUser } from '../auth/current-user.decorator';

@UseGuards(JwtAuthGuard, PermissionGuard)
@Controller('api/registrations')
export class RegistrationController {
  constructor(private readonly registrationService: RegistrationService) {}

  @Post()
  @RequirePermission('registrasi')
  async register(@Body() data: any, @Req() req: any) {
    // Escape hatch check: user role dari token JWT
    const userRole = req.user?.role || 'user';
    const isAdminBypass = userRole === 'admin' || userRole === 'superadmin' || userRole === 'management';
    
    return this.registrationService.createRegistration({
      no_rkm_medis: data.no_rkm_medis,
      kd_dokter: data.kd_dokter,
      kd_poli: data.kd_poli,
      kd_pj: data.kd_pj,
      bypassNoSep: data.bypassNoSep,
      isAdminBypass: isAdminBypass
    });
  }

  @Post('aps')
  @RequirePermission('registrasi')
  async registerAps(
    @Req() req: any,
    @CurrentUser() user: AuthenticatedUser,
    @Body()
    body: {
      no_rkm_medis: string;
      kd_dokter?: string;
      kd_poli?: string;
      kd_pj?: string;
      jenis_layanan: 'Lab' | 'Radiologi';
      p_jawab?: string;
      almt_pj?: string;
      hubunganpj?: string;
    },
  ) {
    return this.registrationService.createApsRegistration({
      ...body,
      actor: { id: user.username, name: user.name },
      ipAddress: req.ip,
      userAgent: req.headers['user-agent'],
    });
  }
}

