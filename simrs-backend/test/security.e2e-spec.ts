import { INestApplication, ValidationPipe } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import request from 'supertest';
import { App } from 'supertest/types';
import { AppModule } from '../src/app.module';
import { PrismaService } from '../src/prisma/prisma.service';

describe('Global authentication guard (e2e)', () => {
  let app: INestApplication<App>;

  beforeAll(async () => {
    process.env.JWT_SECRET = 'test-only-secret-for-global-auth-guard';
    process.env.SIMRS_ADMIN_USERNAME_KEY = 'test-username-key';
    process.env.SIMRS_ADMIN_PASSWORD_KEY = 'test-password-key';

    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    })
      .overrideProvider(PrismaService)
      .useValue({
        onModuleInit: jest.fn(),
        onModuleDestroy: jest.fn(),
      })
      .compile();

    app = moduleFixture.createNestApplication();
    app.useGlobalPipes(new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }));
    await app.init();
  });

  it('allows an explicitly public route without a token', () => {
    return request(app.getHttpServer()).get('/').expect(200).expect('Hello World!');
  });

  it.each(['/lab/request', '/ranap/admisi', '/operasi/input'])(
    'rejects anonymous writes to %s',
    (path) => request(app.getHttpServer()).post(path).send({}).expect(401),
  );

  it('validates and rate limits invalid login attempts', async () => {
    for (let attempt = 0; attempt < 5; attempt += 1) {
      await request(app.getHttpServer()).post('/api/auth/login').send({ username: '' }).expect(400);
    }

    await request(app.getHttpServer()).post('/api/auth/login').send({ username: '' }).expect(429);
  });

  it('rejects unknown fields on public kiosk registration payloads', () => {
    return request(app.getHttpServer())
      .post('/api/kiosk/register')
      .send({
        no_rkm_medis: '000001',
        kd_poli: 'INT',
        kd_dokter: 'D001',
        kd_pj: 'A01',
        unexpected: true,
      })
      .expect(400);
  });

  afterAll(async () => {
    await app.close();
  });
});
