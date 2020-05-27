<template>
    <section>
        <router-link :to="{ name: '新增接口', params: {project_id: this.$route.params.project_id, addForm: this.form}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list">快速新建API</el-button>
        </router-link>
        <el-form :model="form" ref="form" :rules="formRules">
            <el-col :span="3" class="HOST">
                <el-form-item prop="env">
                    <el-select v-model="form.env"  placeholder="测试环境">
                        <el-option v-for="(item,index) in Host" :key="index+''" :label="item.name" :value="item.host"></el-option>
                    </el-select>
                </el-form-item>
            </el-col>
            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px;padding-bottom: 0px">
                <el-row :gutter="10">
                    <el-col :span='3'>
                        <el-form-item>
                            <el-select v-model="form.type" @change="typeChanged" placeholder="请选择类型">
                                <el-option v-for="(item,index) in type" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="3">
                        <el-form-item>
                            <el-select v-model="form.method" placeholder="请求方式">
                                <el-option v-for="(item,index) in request" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <!--<el-col :span="3">-->
                        <!--<el-form-item>-->
                            <!--<el-select v-model="form.http" placeholder="HTTP协议">-->
                                <!--<el-option v-for="(item,index) in Http" :key="index+''" :label="item.label" :value="item.value"></el-option>-->
                            <!--</el-select>-->
                        <!--</el-form-item>-->
                    <!--</el-col>-->
                    <el-col :span='15'>
                        <el-form-item prop="addr">
                            <el-input v-model.trim="form.addr" @change="addrChanged" placeholder="地址" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span='2'>
                        <el-button type="primary" @click="fastTest" :loading="loadingSend">执行</el-button>
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
                                <div style="word-break: break-all;overflow:auto;overflow-x:hidden">{{form.resultData}}</div>
                            </div>
                            <div v-model="form.resultHead" :class="resultShow? 'parameter-b': 'parameter-a'">{{form.resultHead}}</div>
                            <div :class="resultShow? 'parameter-a': 'parameter-b'" v-show="format && form.resultData">
                                <!--<pre id="formResult" style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden">{{form.resultData}}</pre>-->
                                <json-viewer :value="form.resultData" :expand-depth=5 copyable></json-viewer>
                            </div>
                            <div v-show="!form.resultData&&!form.resultHead" class="raw">暂无数据</div>
                        </el-card>
                    </el-collapse-item>
                </el-collapse>
            </el-row>
        </el-form>
    </section>
</template>
<script>
    import $ from 'jquery'
    import VuePopper from "element-ui/src/utils/vue-popper";
    import { test } from '@/api/api'
    import ApiRequest from './apiRequest.vue'
    import axios from 'axios'
    export default {
        components: {VuePopper,ApiRequest},
        data() {
            return {
                type: [{value: 'http', label: '普通http'},
                    {value: 'jyb', label: '加油宝app'},
                    {value: 'service', label: '微服务'}],
                request: [{value: 'get', label: 'GET'},
                    {value: 'post', label: 'POST'},
                    {value: 'put', label: 'PUT'},
                    {value: 'delete', label: 'DELETE'}],
                Http: [{value: 'http', label: 'HTTP'},
                    {value: 'https', label: 'HTTPS'}],
                loadingSend: false,
                result: true,
                activeNames: ['2', '3', '4'],
                Host: [{name: "", host: ""}],
                id: "",
                form: {
                    url:"",
                    method: 'POST',
                    http: 'HTTP',
                    type: 'http',
                    addr: '',
                    contentType: "",
                    statusCode: "",
                    resultData: "",
                    resultHead: "",
                    parameters: [],
                    parameter: {},
                    headDic: {},
                    headers: [],
                },
                formRules: {
                    env: [
                        { required: false, message: '请选择测试环境', trigger: 'blur'}
                    ],
                    addr: [
                        { required: true, message: '请输入地址', trigger: 'blur' },
                    ]
                },
                resultShow: true,
                format: false,
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
            getHost() {
                let self = this;
                axios.get(test+"/api/project/config_list", {params:{ project_id: this.$route.params.project_id, page: this.page, type:'env'},headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
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
                }).catch(error=>{

                });
            },
            fastTest: function() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        this.loadingSend = true;
                        let self = this;
                        let head=this.$refs.apiRequest.head;
                        self.form.statusCode = '';
                        self.form.resultData = '';
                        self.form.resultHead = '';
                        self.form.headDic={};
                        self.form.headers=[];
                        for (let i = 0; i < head.length; i++) {
                            var a = head[i]["name"];
                            if (a) {
                                self.form.headDic[a] = head[i]["value"];
                                self.form.headers.push({"name":a,"value":head[i]["value"]});
                            }
                        }
                        let address = self.form.addr;
                        let url="";
                        let env="";
                        if (address.indexOf("http://") ===0||address.indexOf("https://") ===0){
                            url=address;
                            if(self.form.env!="")env=self.form.env;
                        }else{
                            url = self.form.http + "://" + self.form.env + address;
                        }
                        self.form.contentType = self.$refs.apiRequest.requestParameterType;
                        self.form.parameter=self.$refs.apiRequest.getParameters();
                        self.form.parameters=self.$refs.apiRequest.parameters;
                        let param = {project_id:self.$route.params.project_id,type:self.form.type,method:self.form.method,contentType:self.form.contentType,url:url,headers:self.form.headDic,data:self.form.parameter};
                        axios.post(test+"/api/api/run_api", param,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                            let data=response.data;
                            self.loadingSend = false;
                            self.form.statusCode = data["data"]["result"][0];
                            self.form.resultData = data["data"]["result"][1];
                            self.form.resultHead = data["data"]["result"][2];
//                            $("#formResult").text(JSON.stringify(self.form.resultData));
                        }).catch(error=>{
                            self.loadingSend = false;
                            self.$message.error({
                                message: "执行失败,请重试.",
                                center: true,
                            })
                        });
                    }
                })
            },
            showBody() {
                this.resultShow = true
            },
            showHeader() {
                this.resultShow = false
            },
            handleChange(val) {
            },
            typeChanged(){
                this.$refs.apiRequest.form.type=this.form.type;
            },
            addrChanged(){
                this.$refs.apiRequest.form.addr=this.form.addr;
            }
        },
        mounted() {
            this.$refs.apiRequest.addEmptyHead();
            this.$refs.apiRequest.addEmptyParameter();
            this.getHost();
        },
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
        /*position:absolute;*/
        /*margin-left:7px;*/
        /*padding-left:10px;*/
        /*width: 63%;*/
        /*height:25px;*/
        /*left:1px;*/
        /*top:1px;*/
        /*border-bottom:0px;*/
        /*border-right:0px;*/
        /*border-left:0px;*/
        /*border-top:0px;*/
        position: absolute;
        /*margin-left: 7px;*/
        padding-left: 9px;
        width: 180px;
        /*border-radius:0px;*/
        /*height: 38px;*/
        left: 1px;
        border-right: 0px;
    }
    .raw {
        border: 1px solid #e6e6e6;
        margin-bottom: 10px;
        padding:15px;
        text-align: center
    }
    .HOST {
        position: absolute;
        right: 10px;
        top: 0px;
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
