<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters" @submit.native.prevent>
				<el-form-item>
					<el-input v-model.trim="filters.name" placeholder="名称" @keyup.enter.native="handleSearch"></el-input>
				</el-form-item>
				<el-form-item>
            <el-select v-model="filters.type"  placeholder="类型">
                <el-option v-for="(item,index) in type" :label="item.label" :value="item.value"></el-option>
            </el-select>
        </el-form-item>
				<el-form-item>
					<el-button size="medium" type="primary" @click="handleSearch">查询</el-button>
				</el-form-item>
				<el-form-item>
					<router-link :to="{ name: '新增接口', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>
						<el-button size="medium" type="primary">新增</el-button>
					</router-link>
				</el-form-item>
        <el-form-item>
					<el-button size="medium" type="primary" @click="handleImportApi">导入</el-button>
				</el-form-item>
				<el-form-item>
					<el-button size="medium" type="primary" :disabled="update" @click="changeGroup">修改分组</el-button>
				</el-form-item>
			</el-form>
		</el-col>
		<el-dialog width="40%" title="修改所属分组" :visible.sync="updateGroupFormVisible" :close-on-click-modal="false">
			<el-form :model="updateGroupForm" label-width="80px" :rules="updateGroupFormRules" ref="updateGroupForm">
				<el-form-item label="分组名称" prop="firstGroup">
            <treeselect v-model="updateGroupForm.firstGroup" :options="group" placeholder="请选择"/>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="updateGroupFormVisible = false">取消</el-button>
				<el-button type="primary" @click.native="updateGroupSubmit" :loading="updateGroupLoading">提交</el-button>
			</div>
		</el-dialog>
    <el-dialog width="40%" title="设置发布项目" :visible.sync="updatePublishForm.visible" :close-on-click-modal="false">
			<el-form :model="updatePublishForm" label-width="80px" :rules="updatePublishForm.rules" ref="updatePublishForm">
				<el-form-item label="发布项目" prop="publish">
					<el-select v-model="updatePublishForm.publish" placeholder="请选择">
						<el-option v-for="(item,index) in updatePublishForm.publishlist" :key="index+''" :label="item" :value="item">
						</el-option>
					</el-select>
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="updatePublishForm.visible = false">取消</el-button>
				<el-button type="primary" @click.native="updatePublishSubmit" :loading="updatePublishForm.loading">提交</el-button>
			</div>
		</el-dialog>
    <el-dialog width="40%" title="导入接口" :visible.sync="importApi.visible" :close-on-click-modal="false">
			<el-form label-width="80px" :rules="importApi.rules">
        <el-form-item label="文件名:" prop='importApi.fileName'>
              <el-input v-model.trim="importApi.fileName"></el-input>
            </el-form-item>
        <el-form-item label="导入分组:" prop="importApi.toGroup">
          <treeselect v-model="importApi.toGroup" :options="group" placeholder="请选择"/>
				</el-form-item>
        <el-upload
              class="upload-demo"
              :action="uploadActionUrl"
              :on-success="handleUploadSuccess"
              :limit="1"
              accept=".json"
              :file-list="fileList">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传并导入json文件</div>
            </el-upload>
        </el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click.native="importApi.visible = false">取消</el-button>
				<el-button type="primary" @click.native="importApiSubmit" :loading="importApi.loading">提交</el-button>
			</div>
		</el-dialog>
		<!--列表-->
		<el-table :data="api" stripe border element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
			<el-table-column type="selection" min-width="4%">
			</el-table-column>
      <el-table-column prop="id" label="ID" sortable min-width="8%"></el-table-column>
			<el-table-column prop="name" label="名称" sortable min-width="14%" show-overflow-tooltip>
				<template slot-scope="scope">
					<!--<el-icon name="name"></el-icon>-->
					<router-link :to="{ name: '基础信息', params: {api_id: scope.row.id}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
				</template>
			</el-table-column>
			<el-table-column prop="type" label="类型" min-width="6%" show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="apiAddress" label="地址" min-width="20%" show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="userUpdate" label="更新人" min-width="8%" show-overflow-tooltip>
			</el-table-column>
			<el-table-column prop="lastUpdateTime" label="更新日期" min-width="15%" show-overflow-tooltip>
			</el-table-column>
			<!--<el-table-column label="Mock" min-width="7%">-->
				<!--<template slot-scope="scope">-->
					<!--<el-button v-if="scope.row.mockStatus" type="success" size="small" @click="checkMockStatus(scope.row)">关闭</el-button>-->
					<!--<el-button v-if="!scope.row.mockStatus" type="info" size="small"  @click="checkMockStatus(scope.row)">启动</el-button>-->
				<!--</template>-->
			<!--</el-table-column>-->
			<el-table-column label="操作" min-width="15%">
				<template slot-scope="scope">
          <!--<el-button-group>-->
            <!--<router-link :to="{ name: '修改接口', params: {api_id: scope.row.id}}" style='text-decoration: none;color: aliceblue;'>-->
              <!--<el-button type="primary" size="mini">修改</el-button>-->
            <!--</router-link>-->
					  <!--<el-button type="danger" size="mini" @click="handleDel(scope.$index, scope.row)">删除</el-button>-->
          <!--</el-button-group>-->
          <el-dropdown>
            <router-link :to="{ name: '修改接口', params: {api_id: scope.row.id}}" style='text-decoration: none;color: aliceblue;'>
              <el-button type="primary" size="small" plain>修改<i class="el-icon-arrow-down el-icon--right"></i></el-button>
            </router-link>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item><el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)" plain>删除</el-button></el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
			<el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChange" :current-page.sync="page" :total="total" :page-size="page_size" :page-count="pages" style="float:right;">
			</el-pagination>
		</el-col>
	</section>
</template>

<script>
//    import SelectTree from "../../../components/treeSelect.vue";
    import Treeselect from '@riophae/vue-treeselect'
    import '@riophae/vue-treeselect/dist/vue-treeselect.css'
    import { test } from '../../../api/api'
    import axios from 'axios'
    export default {
        components: {
//          SelectTree,
          Treeselect,
        },
        data() {
            return {
                filters: {
                    name: '',
                    type: '',
                },
                type: [{value: '', label: ''},
                    {value: 'http', label: '普通http'},
                    {value: 'jyb', label: '加油宝app'},
                    {value: 'service', label: '微服务'}],
                api: [],
                total: 0,
                page: 1,
                pages: 0,
                page_size:20,
                listLoading: false,
                sels: [],//列表选中列
                updateGroupFormVisible: false,
                updateGroupForm: {
                    firstGroup: null,
                },
                updateGroupFormRules: {
                    firstGroup : [{ type: 'number', required: true, message: '请选择分组', trigger: 'blur'}],
                },
                group: [],
                updateGroupLoading: false,
                update: true,
                loadSwaggerApi: false,
                addLoading: false,
                //新增界面数据
                swaggerUrl: "",
                updatePublishForm: {
                    visible: false,
                    loading: false,
                    publish: "",
                    publishlist: ["加油宝","资产系统"],
                    rules: {
                        publish : [{ type: 'string', required: true, message: '请选择发布项目', trigger: 'blur'}],
                    },
                },
                importApi:{
                    type: "auto",
                    types: [{value: 'auto', label: 'auto'},
                      {value: 'mock.fe', label: 'mock.fe'}],
                    visible: false,
                    loading: false,
                    rules: {
                        fromGroup : [{ type: 'string', required: true, message: '请选择源分组', trigger: 'blur'}],
                        toGroup : [{ type: 'string', required: true, message: '请选择导入分组', trigger: 'blur'}],
                    },
                    value: null,
                    fromGroup: null,
                    toGroup: null,
                    fromDate: "",
                    toDate: "",
                    groups: [],
                    fileName: "",
                },
                uploadActionUrl: test + "/api/imports/uploadfile",
                fileList: []
            }
        },
        methods: {
            handleUploadSuccess(res, file) {
              this.importApi.fileName=file.name;
            },
            // 修改mock状态
            checkMockStatus(row){
                let self = this;
                let param = JSON.stringify({
                    project_id:Number(this.$route.params.project_id),
                    id:Number(row.id)
                });
                axios.post(test+"/api/api/updateMock", param, {headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.listLoading = false;
                    if (data.code === '999999') {
                        self.$message.success({
                            message: data.msg,
                            center: true,
                        });
                        self.getApiList();
                    }
                    else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
			      },
            handleSearch(){
                this.page=1;
                this.getApiList();
            },
            // 获取接口列表
            getApiList() {
                this.listLoading = true;
                let self = this;
                sessionStorage.setItem("api_name",self.filters.name);
                sessionStorage.setItem("api_type",self.filters.type);
                let param = { project_id: this.$route.params.project_id, page: self.page, name: self.filters.name,type: self.filters.type};
                if (this.$route.params.firstGroup) {
                    param['apiGroupLevelFirst_id'] = this.$route.params.firstGroup;
                }
                axios.get(test+"/api/api/api_list", {params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.listLoading = false;
                    if (data.code === '999999') {
                        self.total = data.data.total;
                        self.pages=data.data.pages;
                        self.page_size=data.data.page_size;
                        self.api = data.data.data
                    }
                    else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
            // 获取接口列表
            getDevApiGroupList() {
                this.importApi.loading = true;
                let self = this;
                let param = {};
                let url=test+"/api/imports/apidomainlist";
                if(self.importApi.type=="mock.fe"){
                    url=test+"/api/imports/devapi_grouplist";
                }
                axios.get(url, {params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.importApi.loading = false;
                    if (data.code === '999999') {
                        self.importApi.groups = data.data;
                    }
                    else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
            // 修改接口所属分组
            importApiSubmit() {
                let self = this;
                this.$confirm('确认导入接口吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.importApi.loading = true;
                    //NProgress.start();
                    let params = JSON.stringify({
                        project_id:Number(this.$route.params.project_id),
                        group_id: this.importApi.toGroup,
                        fileName: this.importApi.fileName,
                    });
                    let url=test+"/api/imports/api_importfrompostman";
                    axios.post(url, params,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let data=response.data;
                        self.importApi.loading = false;
                        if (data.code === '999999') {
                            self.$message({
                                message: data.msg,
                                center: true,
                                type: 'success'
                            });
                        }
                        else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                        self.importApi.visible = false;
                        self.getApiList();
                    }).catch(error=>{

                    });
                }).catch(() => {

                });
            },
            // 修改接口所属分组
            updateGroupSubmit() {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认修改所属分组吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.updateGroupLoading = true;
                    //NProgress.start();
                    let params = JSON.stringify({
                        project_id:Number(this.$route.params.project_id),
                        apiGroupLevelFirst_id: Number(self.updateGroupForm.firstGroup),
                        ids: ids,
                    });
                    axios.post(test+"/api/api/update_group", params,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let data=response.data;
                        self.updateGroupLoading = false;
                        if (data.code === '999999') {
                            self.$message({
                                message: '修改成功',
                                center: true,
                                type: 'success'
                            });
                            self.$router.push({ name: '分组接口列表', params: { project_id: self.$route.params.project_id, firstGroup: self.updateGroupForm.firstGroup}});
                        }
                        else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                        self.updateGroupFormVisible = false;
                        self.getApiList();
                    }).catch(error=>{

                    });
                }).catch(() => {

                });
            },
            // 修改接口所属发布项目
            updatePublishSubmit() {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认修改发布项目吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.updatePublishForm.loading = true;
                    //NProgress.start();
                    let params = JSON.stringify({
                        project_id:Number(this.$route.params.project_id),
                        publish: self.updatePublishForm.publish,
                        ids: ids,
                    });
                    axios.post(test+"/api/api/update_publish", params,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let data=response.data;
                        self.updatePublishForm.loading = false;
                        if (data.code === '999999') {
                            self.$message({
                                message: '修改成功',
                                center: true,
                                type: 'success'
                            });
//								                self.$router.push({ name: '分组接口列表', params: { project_id: self.$route.params.project_id, firstGroup: self.updateGroupForm.firstGroup}});
                        }
                        else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                        self.updatePublishForm.visible = false;
                        self.getApiList();
                    }).catch(error=>{

                    });
                }).catch(() => {

                });
            },
            // 获取api分组
            getApiGroup() {
                let self = this;
                axios.get(test+"/api/api/group", {params:{ project_id: this.$route.params.project_id},headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        self.group = data.data;
                    }
                    else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
			// 修改分组弹窗
            changeGroup() {
                this.getApiGroup();
                this.updateGroupFormVisible = true;
            },
            changePublish() {
                this.updatePublishForm.visible = true;
            },
            handleImportApi() {
                this.getApiGroup();
                this.getDevApiGroupList();
                this.importApi.visible = true;
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除接口[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    axios.post(test+"/api/api/del_api", JSON.stringify({ project_id: Number(this.$route.params.project_id), ids: [row.id] }),{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let data=response.data;
                        if (data.code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                        self.getApiList();
                    }).catch(error=>{

                    });
                }).catch(() => {
                });
            },
			// 下载接口文档
            DownloadApi() {
                axios.get(test+"/api/api/Download", {params:{ project_id: this.$route.params.project_id},headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === "999999") {
                        window.open(test+"/api/api/download_doc?url="+data.data)
                    }
                }).catch(error=>{

                });
            },
			// 翻页
            handleCurrentChange(val) {
                this.page = val;
                this.getApiList()
            },
            selsChange: function (sels) {
                if (sels.length>0) {
                    this.sels = sels;
                    this.update = false
                } else {
                    this.update = true
                }
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    axios.post(test+"/api/api/del_api", JSON.stringify({ project_id: Number(this.$route.params.project_id), ids: ids}),{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let data=response.data;
                        self.listLoading = false;
                        if (data.code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        }
                        else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                        self.getApiList();
                    }).catch(error=>{

                    });
                }).catch(() => {
                });
            },
            addSubmit(){
                let self = this;
                this.addLoading = true;
                console.log(this.swaggerUrl);
                if (this.swaggerUrl){
                    axios.post(test+"/api/api/lead_swagger", JSON.stringify({ project_id: Number(this.$route.params.project_id), url: this.swaggerUrl}),{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let data=response.data;
                        if (data.code === '999999') {
                            self.$message({
                                message: '添加成功',
                                center: true,
                                type: 'success'
                            });
                            self.listLoading = true;
                            self.addLoading = false;
                            self.loadSwaggerApi = false;
                            self.getApiList()
                        }
                        else {
                            self.addLoading = false;
                            self.$message.error({
                                message: "导入失败，请检查地址是否正确",
                                center: true,
                            })
                        }
                        self.getApiList();
                    }).catch(error=>{

                    });
                } else {
                    this.addLoading = false
                }
            },
            load(){
                if(sessionStorage.getItem("api_name")!=null){
                    this.filters.name=sessionStorage.getItem("api_name");
                }
                if(sessionStorage.getItem("api_type")!=null){
                    this.filters.type=sessionStorage.getItem("api_type");
                }
                this.getApiList();
                if (this.$route.params.firstGroup) {
                    this.updateGroupForm.firstGroup = Number(this.$route.params.firstGroup);
                    this.importApi.toGroup=Number(this.$route.params.firstGroup);
                    sessionStorage.setItem("api_group",this.$route.params.firstGroup);
                }
            },
        },
        mounted() {
            this.load();
        },
        watch: {
            '$route' (to, from) { //监听路由是否变化
              if(to.query!= from.query){
                this.load();
              }
            }
        },
    }
</script>

<style lang="scss" scoped>
	.api-title {
		padding: 15px;
		margin: 0px;
		text-align: center;
		border-radius:5px;
		font-size: 15px;
		color: aliceblue;
		background-color: rgb(32, 160, 255);
		font-family: PingFang SC;
	}
	.group .editGroup {
		float:right;
	}
	.row-title {
		margin: 35px;
	}
	.addGroup {
		margin-top: 0px;
		margin-bottom: 10px;
		border-radius: 25px;
	}
	.api-view-a {
		margin-left: 15px;
		margin-right: 15px;
		display: block;
	}
	.api-view-b {
		margin-left: 15px;
		margin-right: 15px;
		display: none;
	}
</style>
