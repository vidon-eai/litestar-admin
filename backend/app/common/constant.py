from enum import Enum


class RET(Enum):
    """
    系统返回码枚举

    0~200: 成功状态码
    400~600: HTTP标准错误码
    4000+: 自定义业务错误码
    """

    # 成功状态码
    OK = (0, "成功")
    SUCCESS = (200, "操作成功")
    CREATED = (201, "创建成功")
    ACCEPTED = (202, "请求已接受")
    NO_CONTENT = (204, "操作成功,无返回数据")

    # HTTP标准错误码
    ERROR = (1, "请求错误")
    BAD_REQUEST = (400, "参数错误")
    UNAUTHORIZED = (401, "未授权")
    FORBIDDEN = (403, "访问受限")
    NOT_FOUND = (404, "资源不存在")
    BAD_METHOD = (405, "不支持的请求方法")
    NOT_ACCEPTABLE = (406, "不接受的请求")
    CONFLICT = (409, "资源冲突")
    GONE = (410, "资源已删除")
    PRECONDITION_FAILED = (412, "前提条件失败")
    UNSUPPORTED_MEDIA_TYPE = (415, "不支持的媒体类型")
    UNPROCESSABLE_ENTITY = (422, "无法处理的实体")
    TOO_MANY_REQUESTS = (429, "请求过于频繁")

    # 服务器错误码
    INTERNAL_SERVER_ERROR = (500, "服务器内部错误")
    NOT_IMPLEMENTED = (501, "功能未实现")
    BAD_GATEWAY = (502, "网关错误")
    SERVICE_UNAVAILABLE = (503, "服务不可用")
    GATEWAY_TIMEOUT = (504, "网关超时")
    HTTP_VERSION_NOT_SUPPORTED = (505, "HTTP版本不支持")

    # 數據庫操作相關錯誤碼 (4200+)
    DB_ERR = (4200, "數據庫操作失敗")
    DB_CONN_ERR = (4201, "數據庫連接超時")
    DB_DATA_NOT_FOUND = (4202, "查詢不到相關數據")
    DB_DUPLICATE_KEY = (4203, "主鍵或唯一索引衝突")
    DB_FOREIGN_KEY_VIOLATION = (4204, "外鍵約束限制")
    DB_DATA_TOO_LONG = (4205, "數據長度超出限制")
    DB_LOCK_WAIT_TIMEOUT = (4206, "數據庫鎖等待超時")
    DB_DEADLOCK = (4207, "數據庫死鎖")
    DB_TRANSACTION_ERR = (4208, "事務回滾失敗")
    DB_MAX_CONNECTIONS = (4209, "數據庫連接數已滿")

    # 自定义业务错误码
    EXCEPTION = (-1, "系统异常")
    DATAEXIST = (4003, "数据已存在")
    DATAERR = (4004, "数据错误")
    PARAMERR = (4103, "参数错误")
    IOERR = (4302, "IO错误")
    SERVERERR = (4500, "服务错误")
    UNKOWNERR = (4501, "未知错误")
    TIMEOUT = (4502, "请求超时")
    RATE_LIMIT_EXCEEDED = (4503, "访问频率超限")

    # Token相关错误码
    INVALID_TOKEN = (4504, "无效令牌")
    EXPIRED_TOKEN = (4505, "令牌过期")

    # 认证授权错误码
    INVALID_CREDENTIALS = (4506, "无效凭证")
    INVALID_REQUEST = (4507, "无效请求")
    INVALID_FORMAT = (4508, "格式错误")
    INVALID_INPUT = (4509, "输入错误")
    INVALID_STATE = (4510, "状态错误")
    INVALID_OPERATION = (4511, "操作错误")
    INVALID_PERMISSION = (4512, "权限错误")
    INVALID_RESOURCE = (4513, "资源错误")
    INVALID_CONFIGURATION = (4514, "配置错误")

    # 会话安全错误码
    INVALID_SESSION = (4515, "会话错误")
    INVALID_LICENSE = (4516, "许可证错误")
    INVALID_CERTIFICATE = (4517, "证书错误")
    INVALID_SIGNATURE = (4518, "签名错误")
    INVALID_ENCRYPTION = (4519, "加密错误")
    INVALID_DECRYPTION = (4520, "解密错误")
    INVALID_COMPRESSION = (4521, "压缩错误")
    INVALID_DECOMPRESSION = (4522, "解压错误")

    # 权限相关错误码
    INVALID_AUTHENTICATION = (4523, "认证错误")
    INVALID_AUTHORIZATION = (4524, "授权错误")
    INVALID_ACCESS = (4525, "访问错误")
    INVALID_SECURITY = (4526, "安全错误")

    # 系统组件错误码
    INVALID_NETWORK = (4527, "网络错误")
    INVALID_DATABASE = (4528, "数据库错误")
    INVALID_CACHE = (4529, "缓存错误")
    INVALID_QUEUE = (4530, "队列错误")
    INVALID_LOCK = (4531, "锁错误")
    INVALID_TRANSACTION = (4532, "事务错误")
    INVALID_LOG = (4533, "日志错误")
    INVALID_MONITORING = (4534, "监控错误")
    INVALID_NOTIFICATION = (4535, "通知错误")

    # 任务调度错误码
    INVALID_SCHEDULING = (4536, "调度错误")
    INVALID_TASK = (4537, "任务错误")
    INVALID_JOB = (4538, "作业错误")
    INVALID_WORKFLOW = (4539, "工作流错误")

    # 开发相关错误码
    INVALID_SCRIPT = (4540, "脚本错误")
    INVALID_PLUGIN = (4541, "插件错误")
    INVALID_MODULE = (4542, "模块错误")
    INVALID_PACKAGE = (4543, "包错误")
    INVALID_CLASS = (4544, "类错误")
    INVALID_FUNCTION = (4545, "函数错误")
    INVALID_METHOD = (4546, "方法错误")
    INVALID_PROPERTY = (4547, "属性错误")
    INVALID_VARIABLE = (4548, "变量错误")
    INVALID_CONSTANT = (4549, "常量错误")
    INVALID_ENUM = (4550, "枚举错误")
    INVALID_INTERFACE = (4551, "接口错误")
    INVALID_PROTOCOL = (4552, "协议错误")

    # 服务相关错误码
    INVALID_SERVICE = (4553, "服务错误")
    INVALID_CLIENT = (4554, "客户端错误")
    INVALID_SERVER = (4555, "服务器错误")
    INVALID_SYSTEM = (4556, "系统错误")

    # 用户权限错误码
    INVALID_USER = (4557, "用户错误")
    INVALID_GROUP = (4558, "用户组错误")
    INVALID_ROLE = (4559, "角色错误")
    INVALID_PERMISSION_GROUP = (4560, "权限组错误")
    INVALID_PERMISSION_ROLE = (4561, "权限角色错误")
    INVALID_PERMISSION_USER = (4562, "权限用户错误")
    INVALID_PERMISSION_RESOURCE = (4563, "权限资源错误")
    INVALID_PERMISSION_ACTION = (4564, "权限操作错误")
    INVALID_PERMISSION_SCOPE = (4565, "权限范围错误")
    INVALID_PERMISSION_LEVEL = (4566, "权限级别错误")
    INVALID_PERMISSION_TYPE = (4567, "权限类型错误")
    INVALID_PERMISSION_STATUS = (4568, "权限状态错误")
    INVALID_PERMISSION_TIME = (4569, "权限时间错误")
    INVALID_PERMISSION_CONDITION = (4570, "权限条件错误")
    INVALID_PERMISSION_POLICY = (4571, "权限策略错误")
    INVALID_PERMISSION_RULE = (4572, "权限规则错误")
    INVALID_PERMISSION_EXCEPTION = (4573, "权限异常错误")
    INVALID_PERMISSION_VALIDATION = (4574, "权限验证错误")
    INVALID_PERMISSION_AUTHENTICATION = (4575, "权限认证错误")
    INVALID_PERMISSION_AUTHORIZATION = (4576, "权限授权错误")
    INVALID_PERMISSION_ACCESS = (4577, "权限访问错误")
    INVALID_PERMISSION_SECURITY = (4578, "权限安全错误")
    INVALID_PERMISSION_NETWORK = (4579, "权限网络错误")
    INVALID_PERMISSION_DATABASE = (4580, "权限数据库错误")
    INVALID_PERMISSION_CACHE = (4581, "权限缓存错误")
    INVALID_PERMISSION_QUEUE = (4582, "权限队列错误")
    INVALID_PERMISSION_LOCK = (4583, "权限锁错误")
    INVALID_PERMISSION_TRANSACTION = (4584, "权限事务错误")
    INVALID_PERMISSION_LOG = (4585, "权限日志错误")
    INVALID_PERMISSION_MONITORING = (4586, "权限监控错误")
    INVALID_PERMISSION_NOTIFICATION = (4587, "权限通知错误")
    INVALID_PERMISSION_SCHEDULING = (4588, "权限调度错误")
    INVALID_PERMISSION_TASK = (4589, "权限任务错误")
    INVALID_PERMISSION_JOB = (4590, "权限作业错误")
    INVALID_PERMISSION_WORKFLOW = (4591, "权限工作流错误")
    INVALID_PERMISSION_SCRIPT = (4592, "权限脚本错误")
    INVALID_PERMISSION_PLUGIN = (4593, "权限插件错误")
    INVALID_PERMISSION_MODULE = (4594, "权限模块错误")
    INVALID_PERMISSION_PACKAGE = (4595, "权限包错误")
    INVALID_PERMISSION_CLASS = (4596, "权限类错误")
    INVALID_PERMISSION_FUNCTION = (4597, "权限函数错误")
    INVALID_PERMISSION_METHOD = (4598, "权限方法错误")
    INVALID_PERMISSION_PROPERTY = (4599, "权限属性错误")
    INVALID_PERMISSION_VARIABLE = (4600, "权限变量错误")
    INVALID_PERMISSION_CONSTANT = (4601, "权限常量错误")
    INVALID_PERMISSION_ENUM = (4602, "权限枚举错误")
    INVALID_PERMISSION_INTERFACE = (4603, "权限接口错误")
    INVALID_PERMISSION_PROTOCOL = (4604, "权限协议错误")
    INVALID_PERMISSION_SERVICE = (4605, "权限服务错误")
    INVALID_PERMISSION_CLIENT = (4606, "权限客户端错误")
    INVALID_PERMISSION_SERVER = (4607, "权限服务器错误")
    INVALID_PERMISSION_SYSTEM = (4608, "权限系统错误")

    def __init__(self, code: int, msg: str) -> None:
        """
        初始化返回码。

        参数:
        - code (int): 错误码。
        - msg (str): 错误信息。

        返回:
        - None
        """
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        """
        获取错误码。

        返回:
        - int: 错误码数值。
        """
        return self._code

    @property
    def msg(self) -> str:
        """
        获取错误信息。

        返回:
        - str: 错误信息文本。
        """
        return self._msg


class MySQLError(Enum):
    """
    MySQL 錯誤碼枚舉

    參考 MySQL 官方錯誤碼，統一封裝供業務層使用
    """

    # ==================== 連接與權限 ====================
    ER_ACCESS_DENIED_ERROR = (1045, "存取被拒：帳號、密碼或權限錯誤")
    ER_TOO_MANY_CONNECTIONS = (1040, "資料庫連線數已達上限")
    ER_DBACCESS_DENIED_ERROR = (1044, "無此資料庫的存取權限")
    ER_CANNOT_CONNECT = (2003, "無法連接到 MySQL 伺服器")
    ER_SERVER_GONE_AWAY = (2006, "MySQL 伺服器已斷線")
    ER_LOST_CONNECTION = (2013, "查詢過程中與伺服器連線遺失")

    # ==================== 語法與物件 ====================
    ER_PARSE_ERROR = (1064, "SQL 語法錯誤")
    ER_BAD_FIELD_ERROR = (1054, "未知的欄位名稱")
    ER_NO_SUCH_TABLE = (1146, "資料表不存在")
    ER_UNKNOWN_TABLE = (1051, "未知的資料表")

    # ==================== 資料完整性 ====================
    ER_DUP_ENTRY = (1062, "主鍵或唯一索引重複")
    ER_NO_REFERENCED_ROW_2 = (1452, "外鍵約束違反：找不到對應的父記錄")
    ER_ROW_IS_REFERENCED_2 = (1217, "外鍵約束違反：無法刪除或更新父記錄")
    ER_NO_DEFAULT_FOR_FIELD = (1364, "欄位沒有預設值且不可為空")
    ER_DATA_TOO_LONG = (1406, "資料長度超過欄位限制")
    ER_TRUNCATED_WRONG_VALUE = (1292, "資料截斷或格式錯誤")

    # ==================== 資源與鎖定 ====================
    ER_TABLE_FULL = (1114, "資料表已滿（磁碟空間不足）")
    ER_LOCK_WAIT_TIMEOUT = (1205, "鎖等待超時")
    ER_DEADLOCK = (1213, "發生死鎖")
    ER_CANT_CREATE_TABLE = (1005, "無法建立資料表（通常為外鍵定義錯誤）")
    ER_WRONG_KEY_FILE = (126, "索引檔案損壞")

    # ==================== 其他常見 ====================
    ER_QUERY_INTERRUPTED = (1317, "查詢被中斷")
    ER_UNKNOWN_ERROR = (1105, "未知的 MySQL 錯誤")

    def __init__(self, code: int, msg: str) -> None:
        """
        初始化 MySQL 錯誤碼

        參數:
        - code (int): MySQL 原始錯誤代碼
        - msg (str): 錯誤描述
        """
        self._code = code
        self._msg = msg

    @property
    def code(self) -> int:
        """MySQL 原始錯誤碼"""
        return self._code

    @property
    def msg(self) -> str:
        """錯誤描述訊息"""
        return self._msg

    @classmethod
    def get(cls, code: int) -> "MySQLError":
        """根據錯誤碼取得對應枚舉（推薦使用）"""
        for member in cls:
            if member.code == code:
                return member
        raise ValueError(f"未知的 MySQL 錯誤碼: {code}")

    @classmethod
    def get_msg(cls, code: int, default: str = "資料庫操作失敗") -> str:
        """快速取得錯誤訊息"""
        try:
            return cls.get(code).msg
        except ValueError:
            return default


class PostgreSQLError(Enum):
    """
    PostgreSQL 錯誤碼枚舉 (SQLSTATE)

    參考 PostgreSQL 官方附錄 A 錯誤碼定義
    """

    # ==================== 連接與權限 (Class 08 / 28) ====================
    ER_INVALID_AUTHORIZATION_SPECIFICATION = ("28000", "存取被拒：帳號或密碼錯誤")
    ER_CONNECTION_EXCEPTION = ("08000", "無法連接到 PostgreSQL 伺服器")
    ER_CONNECTION_DOES_NOT_EXIST = ("08003", "連線不存在或已斷線")
    ER_CONNECTION_FAILURE = ("08006", "與伺服器連線遺失")
    ER_TOO_MANY_CONNECTIONS = ("53300", "資料庫連線數已達上限")

    # ==================== 語法與物件 (Class 42) ====================
    ER_SYNTAX_ERROR = ("42601", "SQL 語法錯誤")
    ER_UNDEFINED_COLUMN = ("42703", "未知的欄位名稱")
    ER_UNDEFINED_TABLE = ("42P01", "資料表不存在")

    # ==================== 資料完整性 (Class 23) ====================
    ER_UNIQUE_VIOLATION = ("23505", "主鍵或唯一索引重複")
    ER_FOREIGN_KEY_VIOLATION = ("23503", "外鍵約束違反：找不到對應的父記錄或無法刪除")
    ER_NOT_NULL_VIOLATION = ("23502", "欄位不可為空（違反非空約束）")
    ER_STRING_DATA_RIGHT_TRUNCATION = ("22001", "資料長度超過欄位限制")
    ER_INVALID_TEXT_REPRESENTATION = ("22P02", "資料格式錯誤（資料截斷或類型不匹配）")

    # ==================== 資源與鎖定 (Class 40 / 55) ====================
    ER_DISK_FULL = ("53100", "資料庫磁碟空間不足")
    ER_LOCK_NOT_AVAILABLE = ("55P03", "鎖無法取得")
    ER_DEADLOCK_DETECTED = ("40P01", "發生死鎖")
    ER_QUERY_CANCELED = ("57014", "查詢被使用者或超時中斷")

    # ==================== 其他常見 ====================
    ER_UNKNOWN_ERROR = ("99999", "未知的 PostgreSQL 錯誤")

    def __init__(self, code: str, msg: str) -> None:
        self._code = code
        self._msg = msg

    @property
    def code(self) -> str:
        return self._code

    @property
    def msg(self) -> str:
        return self._msg

    @classmethod
    def get(cls, code: str) -> "PostgreSQLError":
        """根據 SQLSTATE 取得對應枚舉"""
        for member in cls:
            if member.code == code:
                return member
        raise ValueError(f"未知的 PostgreSQL 錯誤碼: {code}")

    @classmethod
    def get_msg(cls, code: str, default: str = "資料庫操作失敗") -> str:
        try:
            return cls.get(code).msg
        except ValueError:
            return default
