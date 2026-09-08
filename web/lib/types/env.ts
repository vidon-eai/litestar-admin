import { z } from 'zod';
const clientSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url({ message: 'NEXT_PUBLIC_API_URL 必須是有效的 URL' }),
});

const processEnv = {
  NODE_ENV: process.env.NODE_ENV,
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
};

const _clientEnv = clientSchema.safeParse(processEnv);

if (!_clientEnv.success) {
  console.error('❌ 無效或缺失的 Client 環境變數：', _clientEnv.error.flatten().fieldErrors);
  throw new Error('Client 環境變數驗證失敗！');
}

// 5. 導出類型安全的 env 物件
export const env = {
  ..._clientEnv.data,
};