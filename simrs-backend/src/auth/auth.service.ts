import { Injectable, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { PrismaService } from '../prisma/prisma.service';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly jwtService: JwtService,
    private readonly configService: ConfigService,
  ) {}

  async login(username: string, password: string) {
    const usernameKey = this.configService.getOrThrow<string>('SIMRS_ADMIN_USERNAME_KEY');
    const passwordKey = this.configService.getOrThrow<string>('SIMRS_ADMIN_PASSWORD_KEY');
    
    // 1. Coba cari di tabel admin terlebih dahulu
    const adminResult = await this.prisma.$queryRaw<any[]>`
      SELECT 
        CAST(AES_DECRYPT(usere, ${usernameKey}) AS CHAR) as username,
        CAST(AES_DECRYPT(passworde, ${passwordKey}) AS CHAR) as decoded_password
      FROM admin
      WHERE AES_DECRYPT(usere, ${usernameKey}) = ${username}
    `;

    if (adminResult && adminResult.length > 0) {
      const adminUser = adminResult[0];
      if (adminUser.decoded_password === password) {
        const payload = { sub: adminUser.username, role: 'admin', name: 'Super Admin' };
        return {
          access_token: await this.jwtService.signAsync(payload),
          user: {
            username: adminUser.username,
            role: 'admin',
            name: 'Super Admin'
          }
        };
      } else {
        throw new UnauthorizedException('Kata sandi salah');
      }
    }

    // 2. Jika tidak ditemukan di admin, cari di tabel user (pegawai)
    const userResult = await this.prisma.$queryRaw<any[]>`
      SELECT 
        CAST(AES_DECRYPT(u.id_user, ${usernameKey}) AS CHAR) as username,
        CAST(AES_DECRYPT(u.password, ${passwordKey}) AS CHAR) as decoded_password,
        p.nama as nama
      FROM user u
      JOIN pegawai p ON CAST(AES_DECRYPT(u.id_user, ${usernameKey}) AS CHAR) = p.nik
      WHERE CAST(AES_DECRYPT(u.id_user, ${usernameKey}) AS CHAR) = ${username}
    `;

    if (userResult && userResult.length > 0) {
      const dbUser = userResult[0];
      if (dbUser.decoded_password === password) {
        const payload = { sub: dbUser.username, role: 'user', name: dbUser.nama };
        return {
          access_token: await this.jwtService.signAsync(payload),
          user: {
            username: dbUser.username,
            role: 'user',
            name: dbUser.nama
          }
        };
      } else {
        throw new UnauthorizedException('Kata sandi salah');
      }
    }

    throw new UnauthorizedException('Username tidak ditemukan');
  }

}
