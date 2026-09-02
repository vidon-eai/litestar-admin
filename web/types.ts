// 1. 通用 API 回應外殼 (Generic Response Envelope)
export interface ApiResponse<T = unknown> {
  code: number;          // 業務狀態碼 (0 代表成功)
  message: string;       // 提示訊息 (對應 detail 或 status_message)
  data: T;               // 實際業務數據
  timestamp: string;     // 回應時間戳記
}

// 2. 針對該 API 提煉出的業務 Data 模型 (以知識庫 Dataset 為例)
export interface Collection {
  id: string;
  datasetId: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

export interface DatasetDetail {
  id: string;
  createdBy: string;
  updatedBy: string | null;
  name: string;
  description: string;
  collections: Collection[];
  createdAt: string;
  updatedAt: string;
}