import { Injectable, CanActivate, ExecutionContext, ForbiddenException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { PrismaService } from '../prisma/prisma.service';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class PermissionGuard implements CanActivate {
  constructor(
    private readonly reflector: Reflector,
    private readonly prisma: PrismaService,
    private readonly configService: ConfigService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const requiredPermission = this.reflector.get<string>('permission', context.getHandler());
    if (!requiredPermission) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    if (!user) {
      return false;
    }

    // Admin passes all permission checks automatically
    if (user.role === 'admin') {
      return true;
    }

    // Normal users must have the corresponding permission set to 'true' in the user table
    const usernameKey = this.configService.getOrThrow<string>('SIMRS_ADMIN_USERNAME_KEY');
    
    // Query user permissions
    const result = await this.prisma.$queryRaw<any[]>`
      SELECT *
      FROM user
      WHERE AES_DECRYPT(id_user, ${usernameKey}) = ${user.username}
    `;

    if (!result || result.length === 0) {
      throw new ForbiddenException('User tidak ditemukan di sistem otorisasi');
    }

    const dbUser = result[0];
    const hasPermission = dbUser[requiredPermission] === 'true';

    if (!hasPermission) {
      throw new ForbiddenException(`Anda tidak memiliki hak akses [${requiredPermission}]`);
    }

    return true;
  }
}
