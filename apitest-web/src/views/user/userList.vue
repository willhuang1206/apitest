<template>
    <div class="app-container">
        <!--工具条-->
        <div class="filter-container">
            <el-input v-model.trim="filters.name" style="width: 200px;" placeholder="名称" @keyup.enter.native="handleSearch"></el-input>
            <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
            <el-button type="primary" icon="el-icon-edit" @click="handleAdd">新增</el-button>
            <!--<el-button type="primary" @click="handleLink">关联</el-button>-->
        </div>
        <!--列表-->
        <el-table :data="userlist" stripe border highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="username" label="用户名" min-width="15%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="name" label="姓名" min-width="10%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column v-if=false prop="password" label="密码" min-width="" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="email" label="邮箱" min-width="20%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="phone" label="手机号" min-width="20%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="type" label="类型" min-width="10%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column label="操作" min-width="20%">
                <template slot-scope="scope">
                    <el-button type="primary" v-show="scope.row.type==='local'" size="small" @click="handleEdit(scope.$index, scope.row)" plain>编辑</el-button>
                    <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)" plain>删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChange" :current-page.sync="page" :total="total" :page-size="20" :page-count="pages" style="float:right;">
            </el-pagination>
        </el-col>

        <!--编辑界面-->
        <el-dialog width="40%" :title="editForm.title" :visible.sync="editForm.visible" :close-on-click-modal="false">
            <el-form :model="editForm"  :rules="editForm.rules" ref="editForm" label-width="80px">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model.trim="editForm.username" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="姓名" prop='name'>
                    <el-input v-model.trim="editForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input type="password" v-model.trim="editForm.password" auto-complete="off" placeholder="密码"></el-input>
                </el-form-item>
                <el-form-item label="验证密码" prop="checkPass">
                    <el-input type="password" v-model.trim="editForm.checkPass" auto-complete="off" placeholder="密码"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop='email'>
                    <el-input v-model.trim="editForm.email" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="手机号" prop='phone'>
                    <el-input v-model.trim="editForm.phone" auto-complete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editForm.visible = false">取消</el-button>
                <el-button type="primary" @click.native="editFormSubmit" :loading="editForm.loading">提交</el-button>
            </div>
        </el-dialog>

        <el-dialog width="50%" title="关联用户" :visible.sync="users.visible" :close-on-click-modal="false" >
            <el-row :gutter="10">
                <el-col :span="24">
                    <el-table :data="users.list" highlight-current-row v-loading="users.loading"
                              style="width: 100%;" :show-header="true" max-height="400" @selection-change="selUsersChange">
                        <el-table-column type="selection" min-width="5%">
                        </el-table-column>
                        <el-table-column prop="user_id" label="ID" min-width="10%">
                        </el-table-column>
                        <el-table-column prop="user_name" label="用户名" min-width="20%">
                        </el-table-column>
                        <el-table-column prop="name" label="姓名" min-width="20%">
                        </el-table-column>
                        <el-table-column prop="phone" label="手机" min-width="20%">
                        </el-table-column>
                        <el-table-column prop="email" label="邮箱" min-width="25%">
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
                <el-button type="primary" @click.native="linkUsersSubmit" :loading="users.loading">提交</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    //import NProgress from 'nprogress'
    import { test} from '../../api/api';
    import axios from 'axios'
    import md5 from 'js-md5'
    export default {
        data() {
            return {
                filters: {
                    name: ''
                },
                total: 0,
                page: 1,
                pages: 0,
                users: [],
                userlist: [],
                listLoading: false,
                sels: [],//列表选中列

                editForm:{
                    id: "",
                    visible: false,
                    loading: false,
                    title: "新增",
                    username: "",
                    name: "",
                    password: "",
                    checkPass: "",
                    email: "",
                    phone: "",
                    rules: {
                        username: [
                            { required: true, message: '请输入用户名', trigger: 'blur' },
                            { min: 4, max: 10, message: '长度在 4 到 10 个字符', trigger: 'blur' }
                        ],
                        name: [
                            { required: true, message: '请输入姓名', trigger: 'blur' },
                            { min: 2, max: 4, message: '长度在 2 到 4 个字符', trigger: 'blur' }
                        ],
                        password : [
                            { required: true, message: '请输入密码', trigger: 'blur'},
                            { min: 6, max: 50, message: '长度至少为6', trigger: 'blur' }
                        ],
                        checkPass : [
                            { required: true, message: '请再次输入密码', trigger: 'blur'},
                            { min: 6, max: 50, message: '长度至少为6', trigger: 'blur' }
                        ],
                        email: [
                            { required: true, message: '请输入邮箱', trigger: 'blur' },
                        ]
                    },
                },

                users: {
                    visible: false,
                    loading: false,
                    list: [],
                    total: 0,
                    page: 1,
                    pages: 0,
                    selUsers: []
                },

            }
        },
        methods: {
            handleSearch(){
                this.page=1;
                this.getGlobalUser();
            },
            getGlobalUser() {
                this.listLoading = true;
                let self = this;
                let params = {
                    page: self.page,
                    name: self.filters.name,
                };
                let headers = {
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                axios.get(test+"/api/global/user_list", { params: params}).then(response => {
                    self.listLoading = false;
                    if (response.data.code === '999999') {
                        self.total = response.data.data.total;
                        self.pages=response.data.data.pages;
                        self.userlist=[];
                        response.data.data.data.forEach((item) =>{
                            self.userlist.push(item)
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
            getUsers() {
                let self=this;
                self.users.loading = true;
                let params={
                    page: self.users.page
                };
                axios.get(test+"/api/global/get_users", {params:params}).then(response => {
                    self.users.loading = false;
                    if (response.data.code === '999999') {
                        self.users.list = response.data.data.data;
                        self.users.total = response.data.data.total;
                        self.users.pages = response.data.data.pages;
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
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除用户[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        ids: [row.id, ]
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/global/del_user", params,{headers:headers}).then(response => {
                        let data = response.data;
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
                        self.getGlobalUser()
                    }).catch(error=>{

                    });
                }).catch(() => {
                });
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getGlobalUser();
            },
            handleCurrentChangeUser(val) {
                this.users.page = val;
                this.getUsers();
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editForm.visible = true;
                this.editForm.title = "编辑";
                try{
                    this.editForm.id=row.id;
                    this.editForm.username=row.username;
                    this.editForm.name=row.name;
                    this.editForm.password=row.password;
                    this.editForm.checkPass=row.password;
                    this.editForm.email=row.email;
                    this.editForm.phone=row.phone;
//                    this.editForm = {"id":row.id,"username":row.username,"name":row.name,"password":row.password,"checkPass":row.password,"email":row.email,"phone":row.phone};
                }catch(err){
                    alert(err);
                }
            },
            //显示新增界面
            handleAdd: function () {
                this.editForm.id="";
                this.editForm.username="";
                this.editForm.name="";
                this.editForm.password="";
                this.editForm.checkPass="";
                this.editForm.email="";
                this.editForm.phone="";
                this.editForm.visible = true;
                this.editForm.title = "新增";
            },
            handleLink: function () {
                this.users.visible = true;
                this.users.page=1;
                this.getUsers();
            },
            linkUsersSubmit: function () {
                let ids = this.users.selUsers.map(item => item.user_id);
                let self = this;
                this.$confirm('确认关联选中的用户吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    let params=JSON.stringify({
                        ids: ids
                    });
                    let headers={
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/global/link_users", params,{headers:headers}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '关联成功',
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
                        self.getGlobalUser()
                    }).catch(error=>{
                    });
                }).catch(() => {

                });
            },
            //编辑
            editFormSubmit: function () {
                if(this.editForm.password!=this.editForm.checkPass){
                    this.$message.error({
                        message: "两次输入的密码不一致,请重新输入!",
                        center: true,
                    })
                    return;
                }
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editForm.loading = true;
                            //NProgress.start();
                            let params = {
                                id: Number(self.editForm.id),
                                username: self.editForm.username,
                                name: self.editForm.name,
                                password: md5(self.editForm.password),
                                email: self.editForm.email,
                                phone: self.editForm.phone
                            };
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+sessionStorage.getItem('token')
                            };
                            let url=test+"/api/global/add_user";
                            if(self.editForm.id!=""){
                                url=test+"/api/global/update_user";
                            }
                            axios.post(url, params,{headers:headers}).then(response => {
                                self.editForm.loading = false;
                                if (response.data.code === '999999') {
                                    self.$message({
                                        message: '成功',
                                        center: true,
                                        type: 'success'
                                    })
                                    self.editForm.visible = false;
                                    self.getGlobalUser();
                                }else {
                                    self.$message.error({
                                        message: response.data.msg,
                                        center: true,
                                    })
                                }
                            }).catch(error=>{
                            });
                        }).catch(() => {});
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            selUsersChange(sels){
                this.users.selUsers = sels;
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认删除选中的用户吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    let params = {
                        ids: ids
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/global/del_user", params,{headers:headers}).then(response => {
                        let data = response.data;
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
                        self.getGlobalUser()
                    }).catch(error=>{

                    });
                }).catch(() => {});
            }
        },
        mounted() {
            this.getGlobalUser();
        }
    }

</script>
<style>
</style>
