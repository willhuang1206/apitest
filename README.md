本接口测试平台使用vue.js和python开发, 访问地址:http://106.53.246.180, 主要功能包括接口管理,接口自动化和自动化测试任务等模块.

使用文档: 
接口测试平台使用文档.docx

后端apitest部署:
1. 初始化数据库: 创建mysql数据库,名称为apitest,新建用户名apitest,密码123456,然后从apitest.sql导入数据
2. 安装依赖: pip3 install -r requirements.txt
3. 启动服务: ./start.sh

前端apitest-web部署步骤:
1. 安装依赖包: npm install
2. 配置axios指向后端服务接口: 路径src/api/api.js,参数export const test = 'http://106.53.246.180:8092'
3. 构建前端代码: npm run build
4. 添加nginx配置访问dist目录下构建生成的代码