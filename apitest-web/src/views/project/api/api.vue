<template>
    <section>
        <el-row :span="24" class="row-title">
            <el-col :span="5">
                <el-button class="addGroup" @click="handleAddGroup(0)">新增分组</el-button>
                <router-link :to="{ name: '快速测试', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>
                    <el-button class="addGroup">快速测试</el-button>
                </router-link>
                <div class="api-title"><strong>接口分组</strong></div>
                <div class="api-title" style="cursor:pointer;">
                    <router-link :to="{ name: '接口列表', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>
                        所有接口
                    </router-link>
                </div>
                <aside>
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
            <!--新增-->
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
    import axios from 'axios';
    import NavMenu from "@/components/navMenu.vue";
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
            // 获取api分组
            getApiGroup() {
                let self = this;
                let params = {
                    project_id: this.$route.params.project_id
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                axios.get(`${test}/api/api/group`, { params: params, headers:headers}).then(res => {
                    let {msg, code, data} = res.data;
                    if (code === '999999') {
                        self.groupData = data;
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
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
                if(groupId){
                    this.GroupForm.data.parentId=groupId;
                }
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
                    axios.post(`${test}/api/api/del_group`, params, {headers}).then(res => {
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
                        self.getApiGroup()
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
                                url=`${test}/api/api/update_name_group`;
                                params["id"]=self.GroupForm.data.id;
                            }else{
                                url=`${test}/api/api/add_group`;
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
                                    self.getApiGroup();
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
                                    self.getApiGroup();
                                }
                            })
                        }).catch(() => {});
                    }
                });
            },
        },
        mounted() {
            this.getApiGroup();
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
