<template>
  <div class="app-container">
      <div class="filter-container">
        <el-input v-model="filters.name" placeholder="名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleSearch"></el-input>
        <el-select v-model="filters.businessline" placeholder="业务板块" clearable style="width: 200px" class="filter-item">
          <el-option v-for="(item,index) in businesslinelist" :key="index+''" :label="item.name" :value="item.name">
          </el-option>
        </el-select>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">查询</el-button>
        <el-button type="primary" icon="el-icon-edit" @click="handleAdd">新增</el-button>
      </div>
      <el-table :data="project" stripe border highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
          <el-table-column type="selection" min-width="5%">
          </el-table-column>
          <el-table-column prop="name" label="项目名称" min-width="20%" show-overflow-tooltip>
              <template slot-scope="scope">
                  <el-icon name="name"></el-icon>
                  <router-link v-if="scope.row.status" :to="{ name: '项目面板', params: {project_id: scope.row.id}}" style='text-decoration: none;color: #000000;'>
                      {{ scope.row.name }}
                  </router-link>
                  {{ !scope.row.status?scope.row.name:""}}
              </template>
          </el-table-column>
          <el-table-column prop="businessline" label="业务板块" min-width="10%">
          </el-table-column>
          <el-table-column prop="type" label="类型" min-width="10%">
          </el-table-column>
          <el-table-column prop="LastUpdateTime" label="最后修改时间" min-width="15%">
          </el-table-column>
          <el-table-column prop="status" label="状态" min-width="10%">
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
      <el-dialog width="60%" :title="form.title" :visible.sync="form.visible" :close-on-click-modal="false" style="width: 75%; left: 12.5%">
          <el-form :model="form.data" label-width="80px"  :rules="form.rules" ref="form">
              <el-form-item label="项目名称" prop="name">
                  <el-input v-model="form.data.name" auto-complete="off"></el-input>
              </el-form-item>
              <el-form-item label="业务板块" prop="businessLine">
                  <el-select style="width:100%" v-model="form.data.businessline" placeholder="请选择">
                    <el-option v-for="(item,index) in businesslinelist" :key="index+''" :label="item.name" :value="item.name">
                    </el-option>
                  </el-select>
              </el-form-item>
              <el-row :gutter="24">
                  <el-col :span="12">
                      <el-form-item label="类型" prop='type'>
                          <el-select v-model="form.data.type" placeholder="请选择">
                              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                              </el-option>
                          </el-select>
                      </el-form-item>
                  </el-col>
                  <el-col :span="12">
                      <el-form-item label="版本号" prop='version'>
                          <el-input v-model="form.data.version" auto-complete="off"></el-input>
                      </el-form-item>
                  </el-col>
              </el-row>
              <el-form-item label="描述" prop='description'>
                  <el-input type="textarea" :rows="6" v-model="form.data.description"></el-input>
              </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
              <el-button @click.native="form.visible = false">取消</el-button>
              <el-button type="primary" @click.native="editSubmit" :loading="form.loading">提交</el-button>
          </div>
      </el-dialog>
  </div>
</template>

<script>
  //import NProgress from 'nprogress'
    import { test} from '../../api/api';
    import axios from "axios";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    name: '',
                    businessline: ''
                },
                project: [],
                total: 0,
                page: 1,
                pages: 0,
                listLoading: false,
                sels: [],//列表选中列
                form: {
                    data: {
                        id: '',
                        name: '',
                        version: '',
                        type: '',
                        description: '',
                        businessline: ''
                    },
                    visible: false,
                    loading: false,
                    rules: {
                        name: [
                            { required: true, message: '请输入名称', trigger: 'blur' },
                            { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                        ],
                        type: [
                            { required: true, message: '请选择类型', trigger: 'blur' }
                        ],
                        version: [
                            { required: true, message: '请输入版本号', trigger: 'blur' },
                            { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
                        ],
                        description: [
                            { required: false, message: '请输入描述', trigger: 'blur' },
                            { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                        ]
                    },
                },
                options: [{ label: "Web", value: "Web"}, { label: "App", value: "App"}],
                businesslinelist: [{name: "集团科技"},{name: "加油宝科技"},{name: "物流科技"},{name: "金融科技"},{name: "其他"}]
            }
        },
        methods: {
            // 获取项目列表
            getProjectList() {
                this.listLoading = true;
                let self = this;
                sessionStorage.setItem("businessline",self.filters.businessline);
                let params = { page: self.page, name: self.filters.name, businessline: self.filters.businessline};
                let headers = {Authorization: 'Token '+sessionStorage.getItem('token')};
                axios.get(`${test}/api/project/project_list`, { params: params, headers:headers}).then((res) => {
                    self.listLoading = false;
                    let { msg, code, data } = res.data;
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
                })
            },
            handleSearch(){
                this.page=1;
                this.getProjectList();
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除项目[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: [row.id, ]};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(`${test}/api/project/del_project`, params, {header}).then(res => {
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
                        self.getProjectList()
                    });
                }).catch(() => {
                });
            },
            // 改变项目状态
            handleChangeStatus: function(index, row) {
                let self = this;
                this.listLoading = true;
                let params = { project_id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                if (row.status) {
                    axios.post(`${test}/api/project/disable_project`, params, {headers}).then(res => {
                        let { msg, code, data } = res.data;
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
                    axios.post(`${test}/api/project/enable_project`, params, {headers}).then(res => {
                        let { msg, code, data } = res.data;
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
                this.getProjectList()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.form.title="编辑";
                this.form.visible = true;
                this.form.data = Object.assign({}, row);
            },
            //显示新增界面
            handleAdd: function () {
                this.form.title="新增";
                this.form.visible = true;
                this.form.data={
                        id: '',
                        name: '',
                        version: '',
                        type: '',
                        description: '',
                        businessline: ''
                    };
            },
            //编辑
            editSubmit: function () {
                let self = this;
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.form.loading = true;
                            //NProgress.start();
                            let params = {
                                name: self.form.data.name,
                                type: self.form.data.type,
                                version: self.form.data.version,
                                description: self.form.data.description,
                                businessline: self.form.data.businessline
                            };
                            let url=`${test}/api/project/add_project`;
                            if(self.form.data.id!=''){
                                url=`${test}/api/project/update_project`;
                                params["project_id"]=self.form.data.id;
                            }
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+sessionStorage.getItem('token')
                            };
                            axios.post(url, params,{headers:header}).then(response => {
                                let {msg, code, data} = response.data;
                                self.form.loading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '执行成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['form'].resetFields();
                                    self.form.visible = false;
                                    self.getProjectList()
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
                            }).catch(error=>{

                            });
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
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: ids};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + sessionStorage.getItem('token')
                    };
                    axios.post(`${test}/api/project/del_project`, params, {header}).then(res => {
                        let {msg, code, data} = res.data;
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
                        self.getProjectList()
                    });
                }).catch(() => {});
            }
        },
        mounted() {
            if(sessionStorage.getItem("businessline")!=null){
                this.filters.businessline=sessionStorage.getItem("businessline");
                this.form.data.businessline=sessionStorage.getItem("businessline");
            }
            this.getProjectList();
        }
    }
</script>
