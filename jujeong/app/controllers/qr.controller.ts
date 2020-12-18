import { Router, Request, Response } from 'express';
import { getQrCode } from '../src/qrCode';

const router: Router = Router();

router.get('/', (request: Request, response: Response) => {
  getQrCode({
    id: 'dd1360',
    password: 'dnflwlq!2'
  }).then((qrCodeResult) => {
    if (qrCodeResult?.isSuccess) {
      const imageBuffer = Buffer.from(qrCodeResult.result, 'base64');
      response.writeHead(200, {
        'Content-Type': 'image/png',
        'Content-Length': imageBuffer.length
      });
      response.end(imageBuffer);
    } else {
      response.json(qrCodeResult);
      response.end();
    }
  })
});

export const QrController: Router = router;
