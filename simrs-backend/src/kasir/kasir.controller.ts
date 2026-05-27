import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { Controller, UseGuards, Get, Param, Post, Body, Req } from '@nestjs/common';
import { KasirService } from './kasir.service';
import { PermissionGuard } from '../auth/permission.guard';
import { RequirePermission } from '../auth/require-permission.decorator';
import { CurrentUser, AuthenticatedUser } from '../auth/current-user.decorator';

@UseGuards(JwtAuthGuard, PermissionGuard)
@Controller('kasir')
export class KasirController {
  constructor(private readonly kasirService: KasirService) {}

  @Get('tagihan/:no_rawat')
  async getTagihan(@Param('no_rawat') no_rawat: string) {
    // Reconstruct slashes from no_rawat (e.g. 2026-02-25-000005 -> 2026/02/25/000005)
    const formattedNoRawat = no_rawat.replace(/-/g, '/');
    return this.kasirService.getTagihan(formattedNoRawat);
  }

  @Post('bayar')
  @RequirePermission('kasir_ralan')
  async prosesPembayaran(
    @Req() req: any,
    @CurrentUser() user: AuthenticatedUser,
    @Body()
    body: {
      no_rawat: string;
      nominal_bayar: number;
    },
  ) {
    const formattedNoRawat = body.no_rawat.replace(/-/g, '/');
    return this.kasirService.bayar(
      formattedNoRawat,
      body.nominal_bayar,
      { id: user.username, name: user.name },
      req.ip,
      req.headers['user-agent'],
    );
  }
}

