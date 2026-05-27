import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { Controller, UseGuards, Get, Post, Query, Body, HttpException, Req } from '@nestjs/common';
import { FarmasiService } from './farmasi.service';
import { PermissionGuard } from '../auth/permission.guard';
import { RequirePermission } from '../auth/require-permission.decorator';
import { CurrentUser, AuthenticatedUser } from '../auth/current-user.decorator';

@UseGuards(JwtAuthGuard, PermissionGuard)
@Controller('farmasi')
export class FarmasiController {
  constructor(private readonly farmasiService: FarmasiService) {}

  @Get('depo')
  @RequirePermission('beri_obat')
  getDepo() {
    return this.farmasiService.getDepo();
  }

  @Get('obat')
  @RequirePermission('beri_obat')
  searchObat(@Query('keyword') keyword: string) {
    return this.farmasiService.searchObat(keyword || '');
  }

  @Get('stok')
  @RequirePermission('beri_obat')
  getStok(@Query('kode_brng') kode_brng: string) {
    return this.farmasiService.getStokGudang(kode_brng);
  }

  @Get('metode-racik')
  @RequirePermission('beri_obat')
  getMetodeRacik() {
    return this.farmasiService.getMetodeRacik();
  }

  @Post('resep')
  @RequirePermission('beri_obat')
  createResep(@Body() data: any) {
    return this.farmasiService.createResep(data);
  }

  @Get('antrean-resep')
  @RequirePermission('beri_obat')
  getAntrean() {
    return this.farmasiService.getAntreanResep();
  }

  @Post('validasi')
  @RequirePermission('beri_obat')
  async validasiResep(@Body() body: { no_resep: string; kd_bangsal_asal?: string }) {
    try {
      return await this.farmasiService.validasiResep(body.no_resep, body.kd_bangsal_asal);
    } catch (e: any) {
      throw new HttpException({ message: e.message }, 500);
    }
  }

  @Post('serahkan')
  @RequirePermission('beri_obat')
  async serahkanObat(
    @Req() req: any,
    @CurrentUser() user: AuthenticatedUser,
    @Body() body: { no_resep: string; kd_bangsal_asal?: string },
  ) {
    try {
      return await this.farmasiService.serahkanObat(
        body.no_resep,
        body.kd_bangsal_asal,
        { id: user.username, name: user.name },
        req.ip,
        req.headers['user-agent'],
      );
    } catch (e: any) {
      if (e.message.includes('Insufficient Stock')) {
        throw new HttpException({ message: e.message }, 400);
      }
      throw new HttpException({ message: e.message }, 500);
    }
  }

  @Post('resep-bebas')
  @RequirePermission('beri_obat')
  async createResepBebas(
    @Req() req: any,
    @CurrentUser() user: AuthenticatedUser,
    @Body()
    body: {
      nama_pembeli: string;
      kd_bangsal_asal: string;
      items: { kode_brng: string; jml: number }[];
    },
  ) {
    try {
      return await this.farmasiService.createResepBebas(
        body,
        { id: user.username, name: user.name },
        req.ip,
        req.headers['user-agent'],
      );
    } catch (e: any) {
      if (e.message.includes('Insufficient Stock')) {
        throw new HttpException({ message: e.message }, 400);
      }
      throw new HttpException({ message: e.message }, 500);
    }
  }
}


