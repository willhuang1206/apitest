本接口测试平台使用vue.js和python开发, 访问地址:http://106.53.246.180, 主要功能包括接口管理,接口自动化和自动化测试任务等模块.

使用文档: 
接口测试平台使用文档.docx

前端apitest-web部署步骤:
1. 安装依赖包: npm install
2. 构建前端代码: npm run build
3. 添加nginx配置访问dist目录下构建生成的代码

后端apitest部署:
1. pip3 install -r requirements.txt
2. 启动apitest服务: ./start.sh