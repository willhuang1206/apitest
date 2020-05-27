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
            </el-form>
        </el-col>
        <!--列表-->
        <el-table :data="project" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column prop="name" label="名称" min-width="15%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="type" label="类型" min-width="5%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="value" label="值" min-width="25%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="25%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="5%">
                <template slot-scope="scope">
                    <img v-show="scope.row.status" src="@/assets/icon-yes.svg"/>
                    <img v-show="!scope.row.status" src="@/assets/icon-no.svg"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="20%">
                <template slot-scope="scope">
                  <!--<el-button-group>-->
                    <!--<el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>-->
                    <!--<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>-->
                    <!--<el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">{{scope.row.status===false?'启用':'禁用'}}</el-button>-->
                  <!--</el-button-group>-->
                  <el-dropdown>
                    <el-button size="small" type="primary" @click="handleEdit(scope.$index, scope.row)" plain>编辑<i class="el-icon-arrow-down el-icon--right"></i></el-button>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item><el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)" plain>删除</el-button></el-dropdown-item>
                      <el-dropdown-item><el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)" plain>{{scope.row.status===false?'启用':'禁用'}}</el-button></el-dropdown-item>
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

        <!--编辑界面-->
        <el-dialog width="40%" :title="editForm.title" :visible.sync="editForm.visible" :close-on-click-modal="false">
            <el-form :model="editForm.data"  :rules="editForm.rules" ref="editForm" label-width="80px">
                <el-form-item label="名称" prop="name">
                    <el-input v-model.trim="editForm.data.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="类型" prop="type">
                    <el-select v-model="editForm.data.type"  placeholder="类型">
                        <el-option v-for="(item,index) in type" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="值" prop='value'>
                    <el-input type="textarea" :rows="5" v-model.trim="editForm.data.value"></el-input>
                </el-form-item>
                <el-form-item label="描述" prop='description'>
                    <el-input type="textarea" :rows="5" v-model.trim="editForm.data.description"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editForm.visible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editForm.loading">提交</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    //import NProgress from 'nprogress'
    import { test } from '../../api/api';
    import axios from 'axios';
    export default {
        data() {
            return {
                type: [{value: 'env', label: '环境'},
                    {value: 'data', label: '数据'},
                    {value: 'config', label: '配置'}],
                filters: {
                    name: ''
                },
                project: [],
                total: 0,
                page: 1,
                pages: 0,
                listLoading: false,
                sels: [],//列表选中列
                editForm:{
                    //编辑界面数据
                    data: {
                        id: '',
                        name: '',
                        type: 'env',
                        value: '',
                        description: ''
                    },
                    title: "",
                    visible: false,//编辑界面是否显示
                    loading: false,
                    rules: {
                        name: [
                            { required: true, message: '请输入名称', trigger: 'blur' },
                            { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                        ],
                        type : [
                            { required: true, message: '请选择类型', trigger: 'blur'}
                        ],
                        value: [
                            { required: true, message: '请输入值', trigger: 'blur' },
                        ],
                        description: [
                            { required: false, message: '请输入描述', trigger: 'blur' },
                            { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                        ]
                    },
                },
            }
        },
        methods: {
            // IP格式验证
            isValidIP(ip) {
                var reg = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
                var regPort = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5]):([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$$/;

                return regPort.test(ip) || reg.test(ip);
            },
            handleSearch(){
                this.page=1;
                this.getProjectConfig();
            },
            // 获取HOST列表
            getProjectConfig() {
                this.listLoading = true;
                let self = this;
                let params = {
                    project_id: this.$route.params.project_id,
                    page: self.page,
                    name: self.filters.name,
                    type: self.filters.type,
                };
                let headers = {
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                axios.get(`${test}/api/project/config_list`, { params: params, headers:headers}).then(res => {
                    let { msg, code, data } = res.data;
                    self.listLoading = false;
                    if (code === '999999') {
                        self.total = data.total;
                        self.project = data.data;
                        self.pages=data.pages;
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                });
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除配置[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {
                        project_id: Number(this.$route.params.project_id),
                        ids: [row.id, ]
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(`${test}/api/project/del_config`, params, {headers}).then(res => {
                        self.listLoading = false;
                        let { msg, code, data } = res.data;
                        if (code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getProjectConfig();
                    });
                }).catch(() => {
                });
            },
            handleChangeStatus: function(index, row) {
                let self = this;
                this.listLoading = true;
                let params = {
                    project_id: Number(this.$route.params.project_id),
                    config_id: Number(row.id)
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                if (row.status) {
                    axios.post(`${test}/api/project/disable_config`, params, {headers}).then(res => {
                        let {msg, code, data} = res.data;
                        self.listLoading = false;
                        if (code === '999999') {
                            self.$message({
                                message: '禁用成功',
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
                    });
                } else {
                    axios.post(`${test}/api/project/enable_config`, params, {headers}).then(res => {
                        let {msg, code, data} = res.data;
                        self.listLoading = false;
                        if (code === '999999') {
                            self.$message({
                                message: '启用成功',
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
                    });
                }
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getProjectConfig()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editForm.title="编辑";
                this.editForm.visible = true;
                this.editForm.data = Object.assign({}, row);
            },
            //显示新增界面
            handleAdd: function () {
                this.editForm.title="新增";
                this.editForm.visible = true;
                this.editForm.data = {
                        id: '',
                        name: '',
                        type: 'env',
                        value: '',
                        description: ''
                    };
            },
            //编辑
            editSubmit: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editForm.loading = true;
                            //NProgress.start();
                            let params = {
                                project_id: Number(this.$route.params.project_id),
                                name: self.editForm.data.name,
                                type: self.editForm.data.type,
                                value: self.editForm.data.value,
                                description: self.editForm.data.description
                            };
                            let url=`${test}/api/project/add_config`;
                            if(self.editForm.data.id!=""){
                                url=`${test}/api/project/update_config`;
                                params["id"]=Number(self.editForm.data.id);
                            }
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+sessionStorage.getItem('token')
                            };
                            axios.post(url, params, {headers}).then(res => {
                                let {msg, code, data} = res.data;
                                self.editForm.loading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '执行成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editForm.visible = false;
                                    self.getProjectConfig();
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                }
                            })
                        }).catch(() => {});
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
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
                    let params = {
                        project_id: Number(this.$route.params.project_id),
                        ids: ids
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + sessionStorage.getItem('token')
                    };
                    axios.post(`${test}/api/project/del_config`, params, {headers}).then(res => {
                        let {msg, code, data} = res.data;
                        self.listLoading = false;
                        if (code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getProjectConfig();
                    })
                }).catch(() => {});
            }
        },
        mounted() {
            this.getProjectConfig();
        }
    }

</script>
<style>
</style>
