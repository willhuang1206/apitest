<template>
    <!--列表-->
    <el-row class="member-manage">
        <p style="color:#999"><strong>项目成员</strong></p>

        <el-dialog width="50%" title="更新成员权限" :visible.sync="users.visible" :close-on-click-modal="false" >
            <el-select filterable v-model="users.group" placeholder="请选择权限">
                <el-option v-for="(item,index) in groups" :key="index+''" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
            <el-row :gutter="10">
                <el-col :span="18">
                    <el-table :data="users.list" highlight-current-row v-loading="users.loading"
                              style="width: 100%;" :show-header="true" max-height="400" @selection-change="selUsersChange">
                        <el-table-column type="selection" width="55">
                        </el-table-column>
                        <el-table-column prop="id" label="ID" min-width="10%">
                        </el-table-column>
                        <el-table-column prop="username" label="用户名" min-width="20%">
                        </el-table-column>
                        <el-table-column prop="name" label="姓名" min-width="20%">
                        </el-table-column>
                    </el-table>
                </el-col>
            </el-row>
            <el-col :span="24" class="toolbar">
                <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChangeUser" :current-page.sync="users.page" :total="users.total" :page-size="20" :page-count="users.pages" style="float:right;">
                </el-pagination>
            </el-col>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="users.visible = false">取消</el-button>
                <el-button type="primary" @click.native="updateUsersSubmit" :loading="users.loading">提交</el-button>
            </div>
        </el-dialog>

        <el-col :span="24">
            <el-table :data="memberData" highlight-current-row v-loading="listLoading" style="width: 100%;">
                <el-table-column prop="username" label="姓名" min-width="30%">
                </el-table-column>
                <el-table-column prop="group" label="权限" min-width="30%">
                </el-table-column>
                <el-table-column prop="userPhone" label="手机号" min-width="20%">
                </el-table-column>
                <el-table-column prop="userEmail" label="邮箱地址" min-width="20%">
                </el-table-column>
            </el-table>
            <!--工具条-->
            <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChange" :current-page.sync="page" :total="total" :page-size="20" :page-count="pages" style="float:right;">
            </el-pagination>
        </el-col>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" @submit.native.prevent>
                <el-form-item>
                    <el-button type="primary" @click="handleUpdate">更新</el-button>
                </el-form-item>
            </el-form>
        </el-col>
    </el-row>
</template>

<script>
    import { test} from "../../api/api";
    import axios from 'axios';
    export default {
        data() {
            return {
                groups: [{value: '1', label: '管理员'},
                    {value: '2', label: '测试经理'},
                    {value: '3', label: '测试成员'},
                    {value: '4', label: '项目成员'},
                    {value: '0', label: '无权限'}],
                memberData: [],
                total: 0,
                page: 1,
                pages: 0,
                listLoading: false,
                reportFrom: "",
                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                editFormRules: {
                    reportFrom: [
                        { required: true, message: '请输入发送人', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ],
                    mailUser: [
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ],
                    mailPass: [
                        { required: true, message: '请输入口令', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ],
                    mailSmtp: [
                        { required: false, message: '请输入邮件服务器', trigger: 'blur' },
                        { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
                    ]
                },
                //编辑界面数据
                editForm: {
                },
                users: {
                    visible: false,
                    loading: false,
                    list: [],
                    total: 0,
                    selUsers: [],
                    page: 1,
                    pages: 0
                },
            }
        },
        methods: {
            handleCurrentChange(val) {
                this.page = val;
                this.getProjectMember();
            },
            // 获取成员列表
            getProjectMember() {
                this.listLoading = true;
                let self = this;
                let params = {
                    project_id: this.$route.params.project_id,
                    page: self.page
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                axios.get(`${test}/api/member/project_member`, { params: params, headers:headers}).then(res => {
                    let {msg, code, data} = res.data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.total = data.total;
                        self.pages=data.pages;
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
            handleCurrentChangeUser(val) {
                this.users.page = val;
                this.getGlobalUser();
            },
            getGlobalUser() {
                this.users.loading = true;
                let self = this;
                let params = {
                    page: self.users.page,
                };
                let headers = {
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                axios.get(test+"/api/global/user_list", { params: params}).then(response => {
                    self.users.loading = false;
                    if (response.data.code === '999999') {
                        self.users.total = response.data.data.total;
                        self.users.pages = response.data.data.pages;
                        self.users.list=[];
                        response.data.data.data.forEach((item) =>{
                            self.users.list.push(item);
                        });
                    }
                    else {
                        self.$message.error({
                            message: response.data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
            //显示新增界面
            handleUpdate: function () {
                this.users.visible = true;
            },
            selUsersChange(sels){
                this.users.selUsers = sels;
            },
            updateUsersSubmit: function () {
                let ids = this.users.selUsers.map(item => item.id);
                let self = this;
                this.$confirm('确认更新选中的用户吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.users.loading = true;
                    //NProgress.start();
                    let params=JSON.stringify({
                        project_id: this.$route.params.project_id,
                        group: self.users.group,
                        ids: ids
                    });
                    let headers={
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/member/update", params,{headers:headers}).then(response => {
                        self.users.loading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '更新成功',
                                center: true,
                                type: 'success'
                            })
                        }else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        self.users.visible = false;
                        self.getProjectMember();
                    }).catch(error=>{
                    });
                }).catch(() => {

                });
            }
        },
        mounted() {
            this.getProjectMember();
            this.getGlobalUser();
        }
    }
</script>

<style lang="scss" scoped>
    .member-manage {
        margin: 35px;
    }
</style>
