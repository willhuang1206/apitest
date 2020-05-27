<template>
    <div style="margin:35px">
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model.trim="filters.name" placeholder="名称" @keyup.enter.native="handleSearch"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">新增</el-button>
                </el-form-item>
                <!--<el-form-item v-show="listType!=='list'">-->
                    <!--<el-button type="primary" @click.native="Download">下载自动化</el-button>-->
                <!--</el-form-item>-->
                <!--<el-button v-show="listType!=='list'" type="primary" @click.native="getTask"><div>设置定时任务</div></el-button>-->
            </el-form>
        </el-col>
        <el-dialog width="40%" :title="formTitle" :visible.sync="publishVShow"  :close-on-click-modal="false">
            <el-form ref="form" :model="form" label-width="100px" :rules="formRules">
                <el-form-item label="发布项目：" prop="name">
                    <el-select style="width:100%" filterable :disabled="publishVType==='run'" v-model="form.name" placeholder="请选择">
                      <el-option v-for="(item,index) in publishlist" :key="index+''" :label="item" :value="item">
                      </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="用例：" prop="automations">
                    <el-select style="width:100%" filterable multiple :disabled="publishVType==='run'" v-model="form.automations" placeholder="请选择">
                        <el-option v-for="item in automationlist" :key="item.id" :label="item.name" :value="item.id"></el-option>
                    </el-select>
                </el-form-item>
                <!--<el-form-item label="参数" prop='params'>-->
                    <!--<el-input type="textarea" :rows="3" v-model.trim="form.params"></el-input>-->
                <!--</el-form-item>-->
                <el-form-item label="执行环境" prop='env'>
                    <el-select v-model="form.env"  :disabled="publishVType==='run'" placeholder="执行环境">
                        <el-option v-for="(item,index) in EnvList" :key="index+''" :label="item.name" :value="item.name"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="状态:" prop='status'>
                    <el-select v-model="form.status" :disabled="publishVType==='run'" placeholder="状态">
                        <el-option v-for="(item,index) in status" :key="index+''" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="结果反馈:" prop='sendEmail'>
                    <el-select v-model="form.sendEmail" placeholder="结果反馈">
                        <el-option v-for="(item,index) in sendEmail" :key="index+''" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="收件人" prop='emails'>
                    <!--<el-input type="textarea" :rows="3" v-model.trim="form.emails"></el-input>-->
                    <el-select style="width:100%" filterable multiple v-model="form.emails" placeholder="请选择">
                        <el-option v-for="item in memberData" :key="item.userEmail" :label="item.username" :value="item.userEmail"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item v-show="publishVType==='run'" label="上线单ID" prop="publishId">
                    <el-input v-model.trim="form.publishId" auto-complete="off"></el-input>
                </el-form-item>
                <!--<el-form-item label="执行时间：" prop="timeArray">-->
                    <!--<el-date-picker  v-model="form.timeArray" type="datetimerange" :picker-options="pickerOptions2"-->
                                     <!--range-separator="   至   " start-placeholder="开始日期" end-placeholder="结束日期" align="right" ></el-date-picker>-->
                <!--</el-form-item>-->
                <el-form-item>
                    <el-button @click.native="publishVShow = false">取消</el-button>
                    <el-button type="primary" v-show="publishVType!=='run'" :loading="editLoading" @click.native="editSubmit">保存</el-button>
                    <el-button type="primary" v-show="publishVType==='run'" :loading="editLoading" @click.native="runSubmit">执行</el-button>
                </el-form-item>
            </el-form>
        </el-dialog>

        <!--列表-->
        <el-table :data="publishConfigList" stripe border highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="id" sortable label="ID" min-width="5%">
            </el-table-column>
            <el-table-column prop="name" sortable label="发布项目名称" min-width="15%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="automationName" label="用例名称" min-width="15%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="env" sortable label="执行环境" min-width="10%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="5%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <img v-show="scope.row.status" src="@/assets/icon-yes.svg"/>
                    <img v-show="!scope.row.status" src="@/assets/icon-no.svg"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="25%">
                <template slot-scope="scope">
                  <!--<el-button-group>-->
                    <!--<el-button size="mini" @click="handleEdit(scope.$index, scope.row)">修改</el-button>-->
                    <!--<el-button type="primary" size="mini" @click="handleCopy(scope.$index, scope.row)">复制</el-button>-->
                    <!--<el-button type="danger" size="mini" @click="handleDel(scope.$index, scope.row)">删除</el-button>-->
                    <!--<el-button type="info" size="mini" @click="handleChangeStatus(scope.$index, scope.row)">{{scope.row.status===false?'启动':'停止'}}</el-button>-->
                    <!--<el-button type="success" size="mini" @click="handleRun(scope.$index, scope.row)">执行</el-button>-->
                  <!--</el-button-group>-->
                  <el-dropdown>
                    <el-button type="primary" size="small" @click="handleEdit(scope.$index, scope.row)" plain>修改<i class="el-icon-arrow-down el-icon--right"></i></el-button>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item><el-button type="success" size="small" @click="handleRun(scope.$index, scope.row)" plain>执行</el-button></el-dropdown-item>
                      <el-dropdown-item><el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)" plain>{{scope.row.status===false?'启用':'禁用'}}</el-button></el-dropdown-item>
                      <el-dropdown-item><el-button type="primary" size="small" @click="handleCopy(scope.$index, scope.row)" plain>复制</el-button></el-dropdown-item>
                      <el-dropdown-item><el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)" plain>删除</el-button></el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                </template>
            </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChange" :current-page.sync="page" :total="total" :page-size="20" :page-count="pages" style="float:right;">
            </el-pagination>
        </el-col>
    </div>
</template>

<script>
    import { test,getProjectConfig,getGlobalPublish} from '../../../api/api'
    import $ from 'jquery'
    import moment from "moment"
    import axios from "axios"
    export default {
        data() {
            return {
                status: [{value: true, label: '启动'},
                    {value: false, label: '停止'}],
                sendEmail: [{value: 0, label: '不发送'},
                    {value: 1, label: '发送'}],
                filters: {
                    name: ''
                },
                env: '',
                EnvList: [],
                automationlist: [],
                memberData: [],
                publishlist: [],
                publishConfigList: [],
                total: 0,
                page: 1,
                pages: 0,
                listLoading: false,
                editLoading: false,
                sels: [],//列表选中列
                publishVShow: false,
                publishVType: "add",
                formTitle: "发布项目配置",
                delLoading: false,
                disDel: true,
                form: {
                    id: "",
                    name: "",
                    env: "",
                    automations: [],
                    params: "{}",
                    status: "true",
                    sendEmail: 0,
                    emails: [],
                    publishId: "",
                },
                formRules: {
                    name: [
                        { required: true, message: '请选择发布项目'},
                    ],
                    env: [
                        { required: true, message: '请选择执行环境'},
                    ],
                    automation: [
                        { required: true, message: '请选择执行的用例'},
                    ]
                },
            }
        },
        methods: {
            getPublish() {
                if(this.publishlist.length==0){
                    let self = this;
                    let headers = {
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    getGlobalPublish(headers, {}).then(data => {
                        if (data.code === '999999') {
                            data.data.forEach((item) => {
                                self.publishlist.push(item);
                            })
                        }else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                    });
                }
            },
            // 获取用例列表
            getAutomationList() {
                let self = this;
                let param = { project_id: this.$route.params.project_id, page: self.page, page_size:1000};
                axios.get(test+"/api/automation/automation_list",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        self.automationlist=[];
                        data.data.data.forEach((item) =>{
                            self.automationlist.push(item)
                        });
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
            // 获取成员列表
            getProjectMember() {
                let self = this;
                let params = {
                    project_id: this.$route.params.project_id,
                    page: self.page,
                    page_size: 100
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                axios.get(`${test}/api/member/project_member`, { params: params, headers:headers}).then(res => {
                    let {msg, code, data} = res.data;
                    if (code === '999999') {
                        self.memberData = data.data
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            handleSearch(){
                this.page=1;
                this.getPublishList();
            },
            // 获取用例列表
            getPublishList() {
                let self = this;
                let param = { project_id: this.$route.params.project_id, page: self.page, name: self.filters.name};
                axios.get(test+"/api/automation/publish_list",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        self.total = data.data.total;
                        self.pages=data.data.pages;
                        self.publishConfigList=[];
                        data.data.data.forEach((item) =>{
                            self.publishConfigList.push(item)
                        });
                    }else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除发布项目配置[' + row.name + ',' + row.env + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let param=JSON.stringify({
                                project_id: Number(this.$route.params.project_id),
                                ids: [row.id] });
                    axios.post(test+"/api/automation/del_publish",param,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        this.listLoading = false;
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
                        self.getPublishList();
                    }).catch(error=>{

                    });
                }).catch(() => {
                });
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getPublishList()
            },
            selsChange: function (sels) {
                if (sels.length>0) {
                    this.sels = sels;
                }
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认删除选中发布项目配置吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    axios.post(test+"/api/automation/del_publish",JSON.stringify({ project_id: Number(this.$route.params.project_id), ids: ids}),{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
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
                        self.getPublishList();
                    }).catch(error=>{

                    });
                }).catch(() => {

                });
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.formTitle="编辑";
                this.publishVShow = true;
                this.publishVType="update";
                this.form=Object.assign({}, row);
//                this.form = {"id":row.id,"name":row.name,"type":row.type,"params":row.params,"group":row.group,"description":row.description};
            },
            //显示编辑界面
            handleRun: function (index, row) {
                this.formTitle="执行";
                this.publishVShow = true;
                this.publishVType="run";
                this.form=Object.assign({}, row);
//                this.form = {"id":row.id,"name":row.name,"type":row.type,"params":row.params,"group":row.group,"description":row.description};
            },
            //显示新增界面
            handleAdd: function () {
                this.formTitle="新增";
                this.publishVShow = true;
                this.publishVType="add";
                this.form={name: "", env: "", automations: [], params: "{}", status: true, sendEmail: 0, emails: []};
            },
            //显示新增页面,复制用例
            handleCopy: function (index, row) {
                this.formTitle="复制";
                this.publishVType="copy";
                //this.form={"name":row.name,"type":row.type,"params":row.params,"group":row.group,"description":row.description};
                let form=(Object.assign({}, row));
                delete form["id"];
                this.form=form;
                this.publishVShow = true;
            },
            // 修改任务
            editSubmit: function () {
                if(this.form.automations.length==0){
                    this.$message.error({
                        message: "请选择用例!",
                        center: true,
                    })
                    return;
                }
                let self = this;
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let param = {
                              project_id: Number(this.$route.params.project_id),
                              automations: JSON.stringify(self.form.automations),
                              name: self.form.name,
                              params: self.form.params,
                              env: self.form.env,
                              status: self.form.status,
                              sendEmail: self.form.sendEmail,
                              emails: JSON.stringify(self.form.emails)};
                            let url=test+"/api/automation/add_publish";
                            if(self.form.id!=null){
                                param["id"]=Number(self.form.id);
                                url=test+"/api/automation/update_publish";
                            }
                            axios.post(url,param,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                                let data=response.data;
                                self.editLoading = false;
                                if (data.code === '999999') {
                                    self.$message({
                                        message: '执行成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['form'].resetFields();
                                    self.publishVShow = false;
                                    self.getPublishList();
                                } else if (data.code === '999997'){
                                    self.$message.error({
                                        message: data.msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: data.msg,
                                        center: true,
                                    })
                                }
                            }).catch(error=>{});
                        }).catch(() => {});
                    }
                });
            },
            // 改变任务状态
            handleChangeStatus: function(index, row) {
                let self = this;
                let url="";
                let message="";
                this.listLoading = true;
                let param = JSON.stringify({ project_id: Number(this.$route.params.project_id),id: row.id});
                if (row.status) {
                    url=test+"/api/automation/disable_publish";
                    message='禁用成功';
                } else {
                    url=test+"/api/automation/enable_publish";
                    message='启用成功';
                }
                axios.post(url,param,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let { msg, code, data }=response.data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.$message({
                            message: message,
                            center: true,
                            type: 'success'
                        });
                        row.status = !row.status;
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
            runSubmit: function() {
                if(!this.form.publishId){
                    this.$message.error({
                        message: "请填写上线单ID!",
                        center: true,
                    })
                    return;
                }
                this.$confirm('确认测试发布项目' + this.form.name + ',' + this.form.env + '环境,上线单' + this.form.publishId + '吗?', '提示', {}).then(() => {
                    let self = this;
                    let url="";
                    let message="";
                    this.listLoading = true;
                    let param = { project_id: Number(this.$route.params.project_id),publish:self.form.id,id: self.form.publishId,sendEmail:self.form.sendEmail,emails:self.form.emails};
                    axios.post(test+"/api/automation/test_publish",param,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let { msg, code, data }=response.data;
                        self.listLoading = false;
                        self.publishVShow = false;
                        if (code === '999999') {
                            self.$message({
                                message: "开始执行",
                                center: true,
                                type: 'success'
                            });
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    }).catch(error=>{

                    });
                }).catch(() => {});
            },
            getEnv() {
                let self = this;
                let headers = {
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                getProjectConfig(headers, {project_id: self.$route.params.project_id,page: self.page, name: "", type: "env"}).then(data => {
                    if (data.code === '999999') {
                        data.data.data.forEach((item) => {
                            if (item.status) {
                                self.EnvList.push(item)
                            }
                        })
                    }else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                });
            },
            init(){
                this.getPublishList();
                this.getAutomationList();
                this.getProjectMember();
                this.getEnv();
                this.getPublish();
            },
        },
        mounted() {
            this.init();
        },
        watch: {
            '$route' (to, from) { //监听路由是否变化
              if(to.query!= from.query){
                this.init();//重新加载数据
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
