# BUPT GUIDING SYSTEM!
### version==1.0.0
### APP NAME: (None)

##### 项目架构
personalized-tourism-system/
│
├── backend/                    # 后端项目
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── com/tourism/
│   │   │   │       ├── controller/   # 控制器层
│   │   │   │       ├── service/      # 服务层 
│   │   │   │       ├── dao/          # 数据访问层
│   │   │   │       ├── model/        # 数据模型
│   │   │   │       ├── config/       # 配置类
│   │   │   │       └── utils/        # 工具类
│   │   │   └── resources/
│   │   │       ├── application.yml   # Spring Boot配置
│   │   │       └── mybatis/          # MyBatis映射文件
│   │   └── test/                     # 测试目录
│   ├── pom.xml                       # Maven依赖配置
│   └── README.md
│
├── frontend/                   # 前端项目
│   ├── public/
│   ├── src/
│   │   ├── assets/             # 静态资源
│   │   ├── components/         # 公共组件
│   │   ├── views/              # 页面组件
│   │   ├── router/             # 路由配置
│   │   ├── store/              # 状态管理
│   │   ├── services/           # 接口服务
│   │   ├── utils/              # 工具函数
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── README.md
│
├── algorithms/                 # 算法模块
│   ├── path_planning/          # 路径规划算法
│   ├── recommendation/         # 推荐算法
│   ├── search/                 # 搜索算法
│   └── README.md
│
├── data/                       # 数据处理
│   ├── osm_processing/         # OpenStreetMap数据处理
│   ├── scripts/                # 数据导入脚本
│   └── README.md
│
├── docs/                       # 项目文档
│   ├── design/                 # 系统设计文档
│   ├── requirements/           # 需求文档
│   └── api/                    # API文档
│
├── scripts/                    # 部署脚本
│   ├── docker-compose.yml
│   ├── nginx.conf
│   └── deploy.sh
│
├── .gitignore
└── README.md
##### 进展
对geojson数据处理并进行路径规划