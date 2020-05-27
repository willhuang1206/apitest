<template>
    <div class="main">
        <el-row>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h2><i class=""/>{{name}} {{version}}</h2>
                    <div>项目名称和版本</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '成员管理'}" style='text-decoration: none;color: #000000;'><h2><i class=""/>{{memberCount}}人</h2></router-link>
                    <div>项目组成员</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '项目配置'}" style='text-decoration: none;color: #000000;'><h2><i class=""/>{{configCount}}个项目配置</h2></router-link>
                    <div>测试环境和数据配置</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '项目动态'}" style='text-decoration: none;color: #000000;'><h2><i class=""/>{{dynamicCount}}条项目动态</h2></router-link>
                    <div>项目动态</div>
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '接口列表'}" style='text-decoration: none;color: #000000;'><h2>{{apiCount}}个接口</h2></router-link>
                    <div>接口数量</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '自动化列表'}" style='text-decoration: none;color: #000000;'><h2>{{automationCount}}个自动化用例</h2></router-link>
                    <div>自动化数量</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '接口列表'}" style='text-decoration: none;color: #000000;'><h2>{{apiAutomatedCount}}个接口已自动化</h2></router-link>
                    <div>接口自动化覆盖{{apiAutomatedCoverage}}%</div>
                </el-card>
            </el-col>
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <router-link :to="{name: '自动化统计'}" style='text-decoration: none;color: #000000;'><h2>{{resultCount}}次执行自动化</h2></router-link>
                    <div>自动化用例执行</div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    import { test } from '../../api/api';
    import axios from "axios";
    export default {
        props: ['project_id'],
        data() {
            return {
                name: '',
                type: '',
                version: '',
                updateDate: '',
                apiCount: 0,
                apiAutomatedCount: 0,
                apiAutomatedCoverage: 0,
                automationCount: 0,
                resultCount: 0,
                statusCount: 0,
                dynamicCount: 0,
                memberCount: 0,
                configCount: 0,
                createDate: '',
            }
        },
        methods: {
            getProjectInfo() {
                var self = this;
                let params = { project_id: this.project_id};
                let headers = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                axios.get(`${test}/api/title/project_info`, { params: params, headers:headers}).then(res => {
                   let { msg, code, data } = res.data;
                   self.listLoading = false;
                        if (code === '999999') {
                            self.name = data.name;
                            self.type = data.type;
                            self.version = data.version;
                            self.updateDate = data.LastUpdateTime;
                            self.apiCount = data.apiCount;
                            self.automationCount = data.automationCount;
                            self.apiAutomatedCount = data.apiAutomatedCount;
                            self.apiAutomatedCoverage=parseFloat((self.apiAutomatedCount*100/self.apiCount).toFixed(1));
                            self.resultCount=data.resultCount;
                            self.dynamicCount = data.dynamicCount;
                            self.memberCount = data.memberCount;
                            self.configCount = data.configCount;
                            self.createDate = data.createTime;
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
        mounted() {
            this.getProjectInfo()
        }
    }
</script>

<style lang="scss" scoped>
    .box-card {
        width: 100%;
        height: 100%;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .member {
        width: 7%;
    }
    .main {
        margin: 35px;
        margin-top: 10px;
    }
    .inline {
        margin: 10px;
        margin-left: 0px;
        margin-right: 20px;
    }
</style>
