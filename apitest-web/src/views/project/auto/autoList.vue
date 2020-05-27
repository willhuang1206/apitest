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
                        <el-option v-for="(item,index) in automationType" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button size="medium" type="primary" @click="handleSearch">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button size="medium" type="primary" @click="handleAdd">新增</el-button>
                </el-form-item>
                <el-form-item>
                  <el-button size="medium" type="primary" @click="handleImportAutomation">导入</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button size="medium" type="primary" :disabled="update" @click="changeGroup">修改分组</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <el-dialog width="40%" :title="editFormTitle" :visible.sync="editFormVisible" :close-on-click-modal="false">
            <el-form :model="editForm"  :rules="editFormRules" ref="editForm" label-width="80px">
                <el-form-item label="名称" prop="name">
                    <el-input v-model.trim="editForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="类型" label-width="83px" prop="type">
                    <el-select v-model="editForm.type" placeholder="类型">
                        <el-option v-for="(item,index) in automationType" :key="index+''" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="分组" label-width="83px" prop="group">
                    <treeselect v-model="editForm.group" :options="group" placeholder="请选择"/>
                    <!--<SelectTree :options="group" :filter="false" :value="editForm.group"/>-->
                    <!--<el-select v-model="editForm.group" placeholder="分组">-->
                        <!--<el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id"></el-option>-->
                    <!--</el-select>-->
                </el-form-item>
                <el-form-item label="参数" prop='params'>
                    <el-input type="textarea" :rows="4" v-model.trim="editForm.params"></el-input>
                </el-form-item>
                <el-form-item label="描述" prop='description'>
                    <el-input type="textarea" :rows="4" v-model.trim="editForm.description"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
        </el-dialog>

        <el-dialog width="40%" title="修改所属分组" :visible.sync="updateGroupFormVisible" :close-on-click-modal="false">
            <el-form :model="updateGroupForm" label-width="80px"  :rules="updateGroupFormRules" ref="updateGroupForm">
                <el-form-item label="分组" prop="firstGroup">
                    <treeselect v-model="updateGroupForm.firstGroup" :options="group" placeholder="请选择"/>
                    <!--<SelectTree :options="group" :filter="false" :value="updateGroupForm.firstGroup"/>-->
                    <!--<el-select v-model="updateGroupForm.firstGroup" placeholder="请选择分组">-->
                        <!--<el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id">-->
                        <!--</el-option>-->
                    <!--</el-select>-->
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="updateGroupFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="updateGroupSubmit" :loading="updateGroupLoading">提交</el-button>
            </div>
        </el-dialog>

        <el-dialog width="40%" title="导入用例" :visible.sync="importAutomation.visible" :close-on-click-modal="false">
          <el-form label-width="80px" :rules="importAutomation.rules">
            <!--<el-form-item label="导入分组" prop="importApi.importGroup">-->
              <!--<el-select v-model="updatePublishForm.publish" placeholder="请选择">-->
                <!--<el-option v-for="(item,index) in updatePublishForm.publishlist" :key="index+''" :label="item" :value="item">-->
                <!--</el-option>-->
              <!--</el-select>-->
              <!--<el-tree :data="importApi.data" show-checkbox></el-tree>-->
            <!--</el-form-item>-->
            <el-form-item label="文件名:" prop='importAutomation.fileName'>
              <el-input v-model.trim="importAutomation.fileName"></el-input>
            </el-form-item>
            <el-form-item label="导入分组:" prop="importAutomation.toGroup">
              <treeselect v-model="importAutomation.toGroup" :options="group" placeholder="请选择"/>
              <!--<SelectTree :options="group" :filter="false" :value="importAutomation.toGroup"/>-->
              <!--<el-select v-model="importAutomation.toGroup" placeholder="请选择">-->
                <!--<el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id">-->
                <!--</el-option>-->
              <!--</el-select>-->
            </el-form-item>
            <el-row>
              <a :href="downloadTemplateUrl">下载模板</a>
              <el-upload
                class="upload-demo"
                :action="uploadFileUrl"
                :on-success="handleUploadSuccess"
                :limit="1"
                accept=".xls,.xlsx"
                :file-list="fileList">
                <el-button size="small" type="primary">点击上传</el-button>
                <div slot="tip" class="el-upload__tip">只能上传并导入excel文件</div>
              </el-upload>
            </el-row>
            </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click.native="importAutomation.visible = false">取消</el-button>
            <el-button type="primary" @click.native="importAutomationSubmit" :loading="importAutomation.loading">提交</el-button>
          </div>
        </el-dialog>

        <!--列表-->
        <el-table :data="automationlist" stripe border element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="4%">
            </el-table-column>
            <el-table-column prop="id" label="ID" sortable min-width="8%">
            </el-table-column>
            <el-table-column prop="name" label="名称" sortable min-width="14%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link :to="{ name: '自动化步骤列表', params: {automation_id: scope.row.id}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
                </template>
            </el-table-column>
            <el-table-column prop="type" label="类型" min-width="6%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="20%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="userUpdate" label="更新人" min-width="8%" show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="updateTime" label="更新日期" min-width="15%" show-overflow-tooltip>
            </el-table-column>
            <!--<el-table-column v-show="listType==='list'" prop="result" label="执行结果" min-width="10%" sortable show-overflow-tooltip>-->
                <!--<template slot-scope="scope">-->
                    <!--<span v-show="!scope.row.result">尚无执行结果</span>-->
                    <!--<span v-show="scope.row.result==='PASS'" style="color: #11b95c;">成功</span>-->
                    <!--<span v-show="scope.row.result==='FAIL'" style="color: #cc0000;">失败</span>-->
                <!--</template>-->
            <!--</el-table-column>-->
            <el-table-column label="操作" min-width="15%">
                <template slot-scope="scope">
                  <!--<el-button-group>-->
                    <!--<router-link :to="{ name: '更新自动化步骤', params: {automation_id: scope.row.id,type: 'update'}}" style='text-decoration: none;'><el-button size="mini"">修改</el-button></router-link>-->
                    <!--<el-button type="primary" size="mini" @click="handleCopy(scope.$index, scope.row)">复制</el-button>-->
                    <!--<el-button type="danger" size="mini" @click="handleDel(scope.$index, scope.row)">删除</el-button>-->
                  <!--</el-button-group>-->
                  <el-dropdown>
                    <router-link :to="{ name: '更新自动化步骤', params: {automation_id: scope.row.id,type: 'update'}}" style='text-decoration: none;'>
                      <el-button type="primary" size="small" plain>修改<i class="el-icon-arrow-down el-icon--right"></i></el-button>
                    </router-link>
                    <el-dropdown-menu slot="dropdown">
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
            <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChange" :current-page.sync="page" :total="total" :page-size="page_size" :page-count="pages" style="float:right;">
            </el-pagination>
        </el-col>
    </section>
</template>

<script>
    import Treeselect from '@riophae/vue-treeselect'
    import Cookies from 'js-cookie'
    import '@riophae/vue-treeselect/dist/vue-treeselect.css'
//    import SelectTree from "../../../components/treeSelect.vue";
    import { test,getProjectConfig,runAutomation } from '../../../api/api'
    import $ from 'jquery'
    import moment from "moment"
    import axios from 'axios'
    export default {
        components: {
//          SelectTree,
          Treeselect,
        },
        data() {
            return {
                automationType: [
                    {value: '', label: ''},
                    {value: 'case', label: '普通用例'},
                    {value: 'reuse', label: '可复用用例'},
                    {value: 'list', label: '用例集'},
                    {value: 'data', label: '数据用例'},
                    {value: 'monitor', label: '接口监控'},
                ],
                listType: "",
                filters: {
                    name: '',
                    type: '',
                },
                env: '',
                automationlist: [],
                total: 0,
                pages: 0,
                page: 1,
                page_size: 20,
                listLoading: false,
                sels: [],//列表选中列
                delLoading: false,
                disDel: true,
                TestStatus: false,
                updateGroupFormVisible: false,
                updateGroupForm: {
                    firstGroup: null,
                },
                updateGroupFormRules: {
                    firstGroup : [{ type: 'number', required: true, message: '请选择父分组', trigger: 'blur'}],
                },
                group: [],
                updateGroupLoading: false,
                update: true,

                editFormVisible: false,//编辑界面是否显示
                editFormTitle: "",
                editLoading: false,
                editFormRules: {
                    name: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 1024, message: '长度在 1 到 1024 个字符', trigger: 'blur' }
                    ],
                    group: [
                        { type: 'number', required: true, message: '请选择分组', trigger: 'blur'}
                    ],
                    description: [
                        { required: false, message: '请输入描述', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                    ]
                },
                //编辑界面数据
                editForm: {
                    name: '',
                    group: null,
                    description: '',
                    params: '{}',
                    type: 'case',
                },
                getResultTimer: '',
                importAutomation:{
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
                fileList: [],
                formData: [],
                role: Cookies.get('role'),
                uploadFileUrl: test + "/api/imports/uploadfile",
                downloadTemplateUrl: test + "/api/imports/downloadtemplate"
            }
        },
        methods: {
            handleUploadSuccess(res, file) {
              this.importAutomation.fileName=file.name;
            },
            handleSearch(){
                this.page=1;
                this.getAutomationList();
            },
            // 获取用例列表
            getAutomationList() {
                this.listLoading = true;
                let self = this;
                sessionStorage.setItem("auto_name",self.filters.name);
                sessionStorage.setItem("auto_type",self.filters.type);
                let param = { project_id: this.$route.params.project_id, page: self.page, name: self.filters.name, type: self.filters.type};
                if (this.$route.params.firstGroup) {
                    param['first_group_id'] = this.$route.params.firstGroup;
                }
                axios.get(test+"/api/automation/automation_list", { params: param}).then(response => {
                    self.listLoading = false;
                    if (response.data.code === '999999') {
                        self.total = response.data.data.total;
                        self.pages = response.data.data.pages;
                        self.page_size=response.data.data.page_size;
                        self.automationlist=[];
                        response.data.data.data.forEach((item) =>{
                            item.result = false;
                            self.automationlist.push(item)
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
            // 获取接口列表
            getAutomationDomainList() {
                this.importAutomation.loading = true;
                let self = this;
                let param = {};
                axios.get(test+"/api/imports/autodomainlist", {params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.importAutomation.loading = false;
                    if (data.code === '999999') {
//                        alert(JSON.stringify(data.data));
                        self.importAutomation.groups = data.data;
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
            // 修改用例所属分组
            updateGroupSubmit() {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认修改所属分组吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.updateGroupLoading = true;
                    //NProgress.start();
                    let params = JSON.stringify({
                        project_id: Number(this.$route.params.project_id),
                        group_id: self.updateGroupForm.firstGroup,
                        ids:ids
                    });
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/automation/update_automation_group", params,{headers:header}).then(response => {
                        self.updateGroupLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '修改成功',
                                center: true,
                                type: 'success'
                            });
                            self.$router.push({ name: '分组自动化列表', params: { project_id: self.$route.params.project_id, firstGroup: self.updateGroupForm.firstGroup}});
                        }
                        else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        self.updateGroupFormVisible = false;
                        self.getAutomationList();
                    }).catch(error=>{

                    });
                }).catch(() => {

                });
            },
            importAutomationSubmit() {
                let self = this;
                this.$confirm('确认导入用例吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.importAutomation.loading = true;
                    //NProgress.start();
                    let params = JSON.stringify({
                        project_id:Number(this.$route.params.project_id),
                        group_id: this.importAutomation.toGroup,
                        fileName: this.importAutomation.fileName,
                    });
                    axios.post(test+"/api/imports/automation_importfromexcel", params,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                        let data=response.data;
                        self.importAutomation.loading = false;
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
                        self.importAutomation.visible = false;
                        self.getAutomationList();
                    }).catch(error=>{

                    });
                }).catch(() => {

                });
            },
            // 获取用例分组
            getAutomationGroup() {
                let self = this;
                axios.get(test+"/api/automation/group", {params:{project_id: this.$route.params.project_id}}).then(response => {
                    if (response.data.code === '999999') {
                        self.group = response.data.data;
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
            changeGroup() {
                this.getAutomationGroup();
                this.updateGroupFormVisible = true;
            },
            handleImportAutomation() {
                this.getAutomationGroup();
//                this.getAutomationDomainList();
                this.importAutomation.visible = true;
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除用例[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let param=JSON.stringify({
                                project_id: Number(this.$route.params.project_id),
                                ids: [row.id] });
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/automation/del_automation",param,{headers:header}).then(response => {
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        }else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        this.listLoading = true;
                        self.getAutomationList();
                    }).catch(error=>{
                        this.listLoading = true;
                    });
                }).catch(() => {
                });
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getAutomationList()
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
                    let param=JSON.stringify({ project_id: Number(this.$route.params.project_id), ids: ids});
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/automation/del_automation",param,{headers:header}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        }
                        else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        self.getAutomationList();
                    }).catch(error=>{

                    });
                }).catch(() => {

                });
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.getAutomationGroup();
                this.editFormTitle="编辑";
                this.editFormVisible = true;
                this.editForm = {"id":row.id,"name":row.name,"type":row.type,"params":row.params,"group":row.group,"description":row.description};
            },
            //显示新增页面,复制用例
            handleCopy: function (index, row) {
                this.getAutomationGroup();
                this.editFormTitle="复制";
                this.editForm={"copyId":row.id,"name":row.name,"type":row.type,"params":row.params,"group":row.group,"description":row.description};
                this.editFormVisible = true;
            },
            //显示新增界面
            handleAdd: function () {
                this.getAutomationGroup();
                this.editFormTitle="新增";
                this.editFormVisible = true;
            },
            // 修改用例
            editSubmit: function () {
                if(this.editForm.id==null){
                    this.addSubmit();
                }else{
                    let self = this;
                    this.$refs.editForm.validate((valid) => {
                        if (valid) {
                            this.$confirm('确认提交吗？', '提示', {}).then(() => {
                                self.editLoading = true;
                                //NProgress.start();
                                let params = JSON.stringify({
                                    project_id: Number(this.$route.params.project_id),
                                    id: Number(self.editForm.id),
                                    type: self.editForm.type,
                                    name: self.editForm.name,
                                    params: self.editForm.params,
                                    group_id: Number(this.editForm.group),
                                    description: self.editForm.description });
                                let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                                axios.post(test+"/api/automation/update_automation", params,{headers:headers}).then(response => {
                                    self.editLoading = false;
                                    if (response.data.code === '999999') {
                                        self.$message({
                                            message: '修改成功',
                                            center: true,
                                            type: 'success'
                                        });
                                        self.$refs['editForm'].resetFields();
                                        self.editFormVisible = false;
                                        self.getAutomationList();
                                    } else if (response.data.code === '999997'){
                                        self.$message.error({
                                            message: response.data.msg,
                                            center: true,
                                        });
                                    } else {
                                        self.$message.error({
                                            message: response.data.msg,
                                            center: true,
                                        });
                                    }
                                }).catch(error=>{

                                });
                            }).catch(() => {});
                        }
                    });
                }
            },
            //新增用例
            addSubmit: function () {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let param = {
                                project_id: Number(this.$route.params.project_id),
                                type: this.editForm.type,
                                group_id: this.editForm.group,
                                name: self.editForm.name,
                                params: self.editForm.params,
                                description: self.editForm.description };
                            if(this.editFormTitle=="复制"){
                                param["copyId"]=self.editForm.copyId;
                            }
                            param=JSON.stringify(param);
                            let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                            axios.post(test+"/api/automation/add_automation", param,{headers:headers}).then(response => {
                                self.editLoading = false;
                                if (response.data.code === '999999') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
                                    self.getAutomationList()
                                } else if (response.data.code === '999997'){
                                    self.$message.error({
                                        message: response.data.msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: response.data.msg,
                                        center: true,
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
                                    self.getAutomationList()
                                }
                            }).catch(error=>{

                            });
                        }).catch(() => {});
                    }
                });
            },
            init(){
                if(sessionStorage.getItem("auto_name")!=null){
                    this.filters.name=sessionStorage.getItem("auto_name");
                }
                if(sessionStorage.getItem("auto_type")!=null){
                    this.filters.type=sessionStorage.getItem("auto_type");
                }
//                this.getAutomationGroup();
                this.getAutomationList();
                if (this.$route.params.firstGroup) {
                    this.updateGroupForm.firstGroup = Number(this.$route.params.firstGroup);
                    this.editForm.group=Number(this.$route.params.firstGroup);
                }
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
    a{
    text-decoration:none;
    }
</style>
