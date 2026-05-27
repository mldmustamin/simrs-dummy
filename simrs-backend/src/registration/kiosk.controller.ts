import { Controller, Get, Post, Query, Body, HttpCode, HttpStatus } from '@nestjs/common';
import { Throttle } from '@nestjs/throttler';
import { KioskService } from './kiosk.service';
import { Public } from '../auth/public.decorator';
import { CheckPatientQueryDto, RegisterKioskDto } from './dto/kiosk.dto';

@Public()
@Controller('api/kiosk')
export class KioskController {
  constructor(private readonly kioskService: KioskService) {}

  @Get('check-patient')
  @Throttle({ default: { limit: 20, ttl: 60000 } })
  async checkPatient(@Query() query: CheckPatientQueryDto) {
    return this.kioskService.checkPatient(query.q);
  }

  @Get('active-schedules')
  async getActiveSchedules() {
    return this.kioskService.getActiveSchedules();
  }

  @Post('register')
  @HttpCode(HttpStatus.CREATED)
  @Throttle({ default: { limit: 5, ttl: 60000 } })
  async registerKiosk(@Body() body: RegisterKioskDto) {
    return this.kioskService.registerKiosk(body);
  }
}
