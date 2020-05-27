<template>
    <section>
        <el-row :span="24" class="row-title">
            <el-col :span="5">
                <el-button class="addGroup" @click="handleAddGroup(0)">新增分组</el-button>
                <div class="api-title"><strong>自动化分组</strong></div>
                <div class="api-title" style="cursor:pointer;">
                    <router-link :to="{ name: '自动化列表', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>
                        所有自动化
                    </router-link>
                </div>
                <aside>
                    <!--&lt;!&ndash;导航菜单&ndash;&gt;-->
                    <!--<el-menu default-active="2" class="el-menu-vertical-demo" active-text-color="rgb(32, 160, 255)" :unique-opened="true">-->
                        <!--<template v-for="(item,index) in groupData">-->
                            <!--<router-link :to="{ name: '分组自动化列表', params: {project_id: project, firstGroup: item.id}}" style="text-decoration:none;">-->
                            <!--<el-menu-item :index="index+''" :key="item.id" class="group">-->
                                <!--<template slot="title">{{item.name}}-->
                                    <!--<el-dropdown trigger="hover" class="editGroup" style="margin-right:10%">-->
                                        <!--<i class="el-icon-more"></i>-->
                                        <!--<el-dropdown-menu slot="dropdown">-->
                                            <!--<el-dropdown-item @click.native="handleDelFirst(item.id)">删除</el-dropdown-item>-->
                                            <!--<el-dropdown-item @click.native="handleEditFirstGroup(item.id, item.name)">修改</el-dropdown-item>-->
                                        <!--</el-dropdown-menu>-->
                                    <!--</el-dropdown>-->
                                <!--</template>-->
                            <!--</el-menu-item>-->
                            <!--</router-link>-->
                        <!--</template>-->
                    <!--</el-menu>-->
                    <el-menu
                     default-active="0"
                     class="el-menu-vertical-demo" router>
                     <!--background-color="#F0F6F6"-->
                     <!--text-color="#3C3F41"-->
                     <!--active-text-color="black">-->
                     <NavMenu :navMenus="groupData" @handleAdd="handleAddGroup" @handleEdit="handleEditGroup" @handleDel="handleDelGroup"></NavMenu>
                    </el-menu>
                </aside>
            </el-col>
            <el-dialog :title="GroupForm.title" :visible.sync="GroupForm.visible" :close-on-click-modal="false" style="width: 60%; left: 20%">
                <el-form :model="GroupForm.data" label-width="80px"  :rules="GroupForm.rules" ref="GroupForm">
                    <el-form-item label="分组名称" prop='name'>
                        <el-input v-model.trim="GroupForm.data.name" auto-complete="off" style="width: 90%"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click.native="GroupForm.visible = false">取消</el-button>
                    <el-button type="primary" @click.native="GroupFormSubmit" :loading="GroupForm.loading">提交</el-button>
                </div>
            </el-dialog>
            <el-col :span="19">
                <div style="margin-left: 10px;margin-right: 20px">
                    <router-view></router-view>
                </div>
            </el-col>
        </el-row>
    </section>
</template>

<script>
    import { test } from '@/api/api'
    import NavMenu from "@/components/navMenu.vue";
    import $ from 'jquery'
    import axios from 'axios'
    export default {
        components: {
          NavMenu
        },
        data() {
            return {
                project: "",
                groupData: [],
                GroupForm:{
                    title: '',
                    visible: false,
                    loading: false,
                    rules: {
                        name: [
                            { required: true, message: '请输入分组名称', trigger: 'blur' },
                        ]
                    },
                    //新增界面数据
                    data: {
                        name: '',
                        id: '',
                        parentId: '',
                    },
                },
                filters: {
                    name: ''
                },
                api: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列
                apiView: true,
            }
        },
        methods: {
            // 获取自动化分组
            getAutomationGroup() {
                let self = this;
                axios.get(test+"/api/automation/group", {params:{ project_id: Number(this.$route.params.project_id)},headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        self.groupData = data.data;
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
            // 添加分组弹窗显示
            handleAddGroup(groupId) {
                this.GroupForm.visible = true;
                this.GroupForm.title="新增分组";
                this.GroupForm.data={
                        name: '',
                        id: '',
                        parentId: groupId,
                    };
            },
            // 修改分组弹窗显示
            handleEditGroup(groupId, name) {
                this.GroupForm.visible = true;
                this.GroupForm.title="修改分组";
                this.GroupForm.data.id = groupId;
                this.GroupForm.data={
                        name: name,
                        id: groupId,
                        parentId: '',
                    };
            },
            //删除分组
            handleDelGroup: function (id) {
                this.$confirm('确认删除该分组吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    //NProgress.start();
                    let self = this;
                    let params = {
                        id: Number(id),
                        project_id: Number(this.$route.params.project_id)
                    };
                    let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + sessionStorage.getItem('token')
                    };
                    axios.post(`${test}/api/automation/del_group`, params, {headers}).then(res => {
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
                        self.getAutomationGroup()
                    })
                }).catch(() => {});
            },
            // 添加分组
            GroupFormSubmit() {
                this.$refs.GroupForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.GroupForm.loading = true;
                            //NProgress.start();
                            let params = {
                                project_id: Number(this.$route.params.project_id),
                                name: self.GroupForm.data.name
                            };
                            let url='';
                            if(self.GroupForm.data.id!=''){
                                url=`${test}/api/automation/update_name_group`;
                                params["id"]=self.GroupForm.data.id;
                            }else{
                                url=`${test}/api/automation/add_group`;
                                params["parent_id"]=self.GroupForm.data.parentId;
                            }
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+sessionStorage.getItem('token')
                            };
                            axios.post(url, params, {headers}).then(res => {
                                let {msg, code, data} = res.data;
                                self.GroupForm.loading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '执行成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['GroupForm'].resetFields();
                                    self.GroupForm.visible = false;
                                    self.getAutomationGroup();
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    });
                                    self.$refs['GroupForm'].resetFields();
                                    self.GroupForm.visible = false;
                                    self.getAutomationGroup();
                                }
                            })
                        }).catch(() => {});;
                    }
                });
            },
        },
        mounted() {
            this.getAutomationGroup();
            this.project = this.$route.params.project_id

        }
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
</style>
