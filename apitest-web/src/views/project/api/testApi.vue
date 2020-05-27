<template>
    <section>
        <el-form :model="form" ref="form" :rules="formRules">
            <el-col :span="3" class="HOST">
                <el-form-item prop="env">
                    <el-select v-model="form.env"  placeholder="测试环境">
                        <el-option v-for="(item,index) in Host" :key="index+''" :label="item.name" :value="item.name"></el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px; padding:15px; padding-bottom: 0px">
                <el-row :gutter="10">
                    <el-col :span="3">
                        <el-form-item >
                            <el-select v-model="form.method"  placeholder="请求方式">
                                <el-option v-for="(item,index) in request" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span='18'>
                        <el-form-item prop="addr">
                            <el-input v-model.trim="form.addr" placeholder="地址" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span='2'>
                        <el-button type="primary" @click="Test" :loading="loadingSend">执行</el-button>
                    </el-col>
                </el-row>
            </div>
            <el-row :span="24">
                <el-collapse v-model="activeNames" @change="handleChange">
                    <ApiRequest ref="apiRequest"/>
                    <el-collapse-item title="响应结果" name="4">
                        <div style="margin-bottom: 10px">
                            <el-button @click="showBody">Body</el-button>
                            <el-button @click="showHeader">Head</el-button>
                            <el-button type="primary" @click="format = !format">格式转换</el-button>
                        </div>
                        <el-card class="box-card">
                            <!--<div slot="header" class="clearfix">-->
                                <!--<span v-model="form.statusCode" style="font-size: 25px">{{form.statusCode}}</span>-->
                            <!--</div>-->
                            <div v-model="form.resultData" :class="resultShow? 'parameter-a': 'parameter-b'" v-show="!format">
                                <div style="word-break: break-all;overflow:auto;overflow-x:hidden">
                                    {{form.resultData}}
                                </div>
                            </div>
                            <div v-model="form.resultHead" :class="resultShow? 'parameter-b': 'parameter-a'">{{form.resultHead}}</div>
                            <div :class="resultShow? 'parameter-a': 'parameter-b'" v-show="format">
                              <json-viewer :value="form.resultData" :expand-depth=5 copyable></json-viewer>
                            </div>
                            <div v-show="!form.resultData&&!form.resultHead" class="raw">暂无数据</div>
                        </el-card>
                    </el-collapse-item>
                    <el-collapse-item title="请求历史" name="5" v-show="false">
                        <el-table :data="requestHistory" stripe style="width: 100%" v-loading="listLoading">
                            <el-table-column prop="requestTime" label="操作时间" min-width="20%">
                            </el-table-column>
                            <el-table-column prop="requestType" label="请求方式" min-width="10%">
                            </el-table-column>
                            <el-table-column prop="requestAddress" label="请求地址" min-width="49%">
                            </el-table-column>
                            <el-table-column prop="httpCode" label="HTTP状态" min-width="11%">
                            </el-table-column>
                            <el-table-column min-width="10%" label="操作">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delHistory(scope.row)"></i>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-collapse-item>
                </el-collapse>
            </el-row>
        </el-form>
    </section>
</template>
<script>
    import { test } from '@/api/api'
    import ApiRequest from './apiRequest.vue'
    import $ from 'jquery'
    import axios from 'axios'
    export default {
        components: {ApiRequest},
        data() {
            return {
                request: [{value: 'GET', label: 'GET'},
                    {value: 'POST', label: 'POST'},
                    {value: 'PUT', label: 'PUT'},
                    {value: 'DELETE', label: 'DELETE'}],
                Http: [{value: 'http', label: 'HTTP'},
                    {value: 'https', label: 'HTTPS'}],
                loadingSend: false,
                result: true,
                activeNames: ['2', '3', '4', '5'],
                id: "",
                Host: [],
                form: {
                    url: "",
                    method: 'POST',
                    http: 'http',
                    addr: '',
                    statusCode: "",
                    resultData: "",
                    resultHead: "",
                },
                formRules: {
                    env: [
                        { required: true, message: '请选择测试环境', trigger: 'blur'}
                    ],
                    addr: [
                        { required: true, message: '请输入地址', trigger: 'blur' },
                    ]
                },
                requestHistory: [],
                listLoading: false,
                headers: "",
                parameters: "",
                resultShow: true,
                format: false,
                type:""
            }
        },
        methods: {
            isJsonString(str) {
                try {
                    if (typeof JSON.parse(str) === "object") {
                        return true;
                    }
                } catch(e) {
                }
                return false;
            },
            getApiInfo() {
                let self = this;
                let param = {project_id: self.$route.params.project_id, api_id: self.$route.params.api_id};
                axios.get(test+"/api/api/api_info", {params:param}).then(response => {
                    let data=response.data;
                    if (response.data.code === '999999') {
                        self.form.method = data.data.requestType;
                        self.form.http = data.data.httpType.toLowerCase();
                        self.form.addr = data.data.apiAddress;
                        if (data.data.headers.length) {
                            data.data.headers.forEach((item) => {
                                this.$refs.apiRequest.addHead(item);
                            });
                        } else {
                            this.$refs.apiRequest.addEmptyHead();
                        }
                        if (data.data.requestParameter.length) {
                            data.data.requestParameter.forEach((item) => {
                                this.$refs.apiRequest.addParameter(item);
                            });
                        } else {
                            this.$refs.apiRequest.addEmptyParameter();
                        }
                        try {
                            this.$refs.apiRequest.requestParameter.parameterRaw = data.data.requestParameterRaw[0].data;
                        } catch (e) {

                        }
                        this.$refs.apiRequest.requestParameterType = data.data.requestParameterType;
                        self.type=data.data.type;
                        self.getHost();
                    }else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
            getHistory() {
                let self = this;
                this.listLoading = true;
                let params={project_id: this.$route.params.project_id, api_id: self.$route.params.api_id};
                axios.get(test+"/api/api/history_list", { params: params}).then(response => {
                    self.listLoading = false;
                    if (response.data.code === '999999') {
                        self.requestHistory = response.data.data
                        // data.data.data.forEach((item) => {
                        //     self.requestHistory.push(item)
                        // })
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
            AddHistroy(code) {
                let self = this;
                this.listLoading = true;
                let params = JSON.stringify({ project_id: Number(this.$route.params.project_id),
                    api_id: Number(self.$route.params.api_id),
                    requestType :self.form.method,
                    requestAddress: self.form.http + "://" + self.form.env + self.form.addr,
                    httpCode: code
                });
                let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                axios.post(test+"/api/api/add_history", params,{ headers: headers}).then(response => {
                    self.listLoading = false;
                    if (response.data.code === '999999') {
                        self.getHistory()
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
            delHistory(row) {
                let self = this;
                let params = JSON.stringify({
                    project_id: Number(self.$route.params.project_id),
                    api_id: Number(self.$route.params.api_id),
                    id: Number(row.id)
                });
                let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                axios.post(test+"/api/api/del_history", params,{ headers: headers}).then(response => {
                    if (response.data.code === '999999') {
                        this.getHistory();
                        self.$message.success({
                            message: "删除成功！",
                            center: true,
                        })
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
            getHost() {
                let self = this;
                let headers = {
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                let params={project_id: self.$route.params.project_id,page: self.page, name: "", type: "env"};
                axios.get(`${test}/api/project/config_list`, { params: params, headers:headers}).then(res => {
                    let data=res.data;
                    if (data.code === '999999') {
                        data.data.data.forEach((item) => {
                            if (item.status) {
                                self.Host.push(item)
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
            Test: function() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.loadingSend = true;
                        let self = this;
                        let _parameter = new Object();
                        let headers = new Object();
                        self.form.statusCode = '';
                        self.form.resultData = '';
                        self.form.resultHead = '';
                        let head=this.$refs.apiRequest.head;
                        for (let i = 0; i < head.length; i++) {
                            var a = head[i]["name"];
                            if (a) {
                                headers[a] = head[i]["value"]
                            }
                        }
                        let address = this.form.addr;
                        let url="";
                        let env="";
                        if (address.indexOf("http://") ===0||address.indexOf("https://") ===0){
                            url=address;
                            if(self.form.env!="")env=self.form.env;
                        }else{
                            url = self.form.http + "://" + self.form.env + address;
                        }
                        let contentType = this.$refs.apiRequest.requestParameterType;
                        let parameters=this.$refs.apiRequest.parameters;
                        if ( contentType === 'application/x-www-form-urlencoded'||contentType === 'application/json'||contentType === 'text/plain') {
                            for (let i = 0; i < parameters.length; i++) {
                                var a = parameters[i]["name"];
                                if (a) {
                                    if(parameters[i]["_type"]=="Object"||parameters[i]["_type"]=="Array"){
                                        _parameter[a] = JSON.parse(parameters[i]["value"]);
                                    }else{
                                        _parameter[a] = parameters[i]["value"];
                                    }
                                }
                            }
                        } else {
                            // POST(url, self.form.parameterRaw, headers)
                            _parameter = this.$refs.apiRequest.parameterRaw;
                        }
                        let params = JSON.stringify({project_id:self.$route.params.project_id,api_id: self.$route.params.api_id,url:url,headers:headers,data:_parameter,env:env});
                        axios.post(test+"/api/api/run_api", params,{ headers:{"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')} }).then(response => {
                            self.loadingSend = false;
                            self.form.statusCode = response.data["data"]["result"][0];
                            self.form.resultData = response.data["data"]["result"][1];
                            self.form.resultHead = response.data["data"]["result"][2];
//                                self.AddHistroy(jqXHR.status)
                        }).catch(error=>{
                        });
                    }
                })
            },
            neatenFormat() {
                this.format = !this.format;
            },
            showBody() {
                this.resultShow = true
            },
            showHeader() {
                this.resultShow = false
            },
            handleChange(val) {
            },
            onSubmit() {
                console.log('submit!');
            },
        },
        mounted() {
            this.getApiInfo();
            this.getHistory()
        }
    }
</script>

<style lang="scss" scoped>
    .return-list {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }
    .head-class {
        font-size: 17px
    }
    .parameter-a {
        display: block;
    }
    .parameter-b {
        display: none;
    }
    .selectInput {
        position: absolute;
        /*margin-left: 7px;*/
        padding-left: 9px;
        width: 180px;
        /*border-radius:0px;*/
        /*height: 38px;*/
        left: 1px;
        border-right: 0px;
    }
    .HOST {
        position: absolute;
        right: 30px;
        top: 0px;
    }
    .raw {
        border: 1px solid #e6e6e6;
        margin-bottom: 10px;
        padding:15px;
        text-align: center
    }
</style>
<style lang="scss">
    .selectInput{
        input{
            border-right: 0px;
            border-radius: 4px 0px 0px 4px;
        }
    }
</style>
