<template>
    <section>
        <router-link :to="{ name: '基础信息', params: {project_id: this.$route.params.project_id,api_id:this.$route.params.api_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>接口详情</el-button>
        </router-link>
        <router-link :to="{ name: '基础信息', params: {project_id: this.$route.params.project_id,api_id:this.$route.params.api_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list" style="float: right">取消</el-button>
        </router-link>
        <el-button class="return-list" type="primary" style="float: right; margin-right: 15px" @click.native="updateApiInfo">保存</el-button>
        <el-form :model="form" ref="form" :rules="FormRules">
            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px">
                <el-row :gutter="10">
                    <el-col :span='8'>
                        <el-form-item label="接口分组:" label-width="83px" prop="firstGroup">
                            <treeselect v-model="form.firstGroup" :options="group" placeholder="请选择"/>
                            <!--<SelectTree :options="group" :filter="false" :value="form.firstGroup"/>-->
                            <!--<el-select v-model="form.firstGroup" placeholder="请选择分组">-->
                                <!--<el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id"></el-option>-->
                            <!--</el-select>-->
                        </el-form-item>
                    </el-col>
                    <el-col :span='10'>
                        <el-form-item label="接口类型:" label-width="83px" prop="type">
                            <el-select v-model="form.type" placeholder="请选择类型">
                                <el-option v-for="(item,index) in type" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span='8'>
                        <el-form-item label="接口名称:" label-width="83px" prop="name">
                            <el-input v-model.trim="form.name" placeholder="名称" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="10">
                        <el-form-item label="状态:" label-width="72px">
                            <el-select v-model="form.status" placeholder="接口状态">
                                <el-option v-for="(item,index) in status" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span="6">
                        <el-form-item label="URL:" label-width="83px">
                            <el-select v-model="form.method"  placeholder="请求方式">
                                <el-option v-for="(item,index) in request" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <!--<el-col :span="2">-->
                        <!--<el-form-item>-->
                            <!--<el-select v-model="form.http" placeholder="HTTP协议">-->
                                <!--<el-option v-for="(item,index) in Http" :key="index+''" :label="item.label" :value="item.value"></el-option>-->
                            <!--</el-select>-->
                        <!--</el-form-item>-->
                    <!--</el-col>-->
                    <el-col :span='18'>
                        <el-form-item prop="addr">
                            <el-input v-model.trim="form.addr" placeholder="地址" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-col :span="18">
                        <el-form-item label="接口描述:" label-width="83px">
                            <el-input v-model.trim="form.description" type="textarea" :rows="3" placeholder="接口描述"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </div>
            <el-row :span="24">
                <el-collapse v-model="activeNames" @change="handleChange">
                    <el-collapse-item title="请求头部" name="1">
                        <el-table :data="form.head" highlight-current-row>
                            <el-table-column prop="name" label="参数名" min-width="20%">
                                <template slot-scope="scope">
                                    <el-select placeholder="head标签" filterable v-model="scope.row.name">
                                        <el-option v-for="(item,index) in header" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                    <el-input class="selectInput" v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="value" label="参数值" min-width="30%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="20%">
                                <template slot-scope="scope">
                                    <el-button class="el-icon-delete" size="mini" @click="delHead(scope.$index)"></el-button>
                                    <el-button v-if="scope.$index===(form.head.length-1)" size="mini" class="el-icon-plus" @click="addHead"></el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-collapse-item>
                    <el-collapse-item title="请求参数" name="2">
                        <div style="margin: 5px">
                            <el-row :span="24">
                                <el-col :span="4"><el-radio v-model="requestParameterType" label="application/x-www-form-urlencoded">表单</el-radio></el-col>
                                <el-col :span="4"><el-radio v-model="requestParameterType" label="application/json">JSON</el-radio></el-col>
                                <el-col :span="4"><el-radio v-model="requestParameterType" label="raw">JSON源数据</el-radio><el-button v-show="form.type==='jyb'" type="primary" size="mini" @click="jybDecodePost">解密</el-button></el-col>
                            </el-row>
                        </div>
                        <el-table :data="form.parameter" highlight-current-row :class="ParameterType? 'parameter-a': 'parameter-b'">
                            <el-table-column prop="name" label="参数名" min-width="20%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="value" label="参数值" min-width="25%">
                                <template slot-scope="scope">
                                    <el-input type="textarea" :rows="1" v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="_type" label="参数类型" min-width="15%">
                                <template slot-scope="scope">
                                    <el-select v-model="scope.row._type"  placeholder="请求方式">
                                        <el-option v-for="(item,index) in paramType" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column label="必填?" min-width="10%" prop="required">
                                <template slot-scope="scope">
                                    <el-select v-model.trim="scope.row.required" placeholder="必填？">
                                        <el-option v-for="(item,index) in required4" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column prop="description" label="参数说明" min-width="20%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.description" :value="scope.row.desc" placeholder="请输入参数说明"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="15%">
                                <template slot-scope="scope">
                                    <el-button class="el-icon-delete" size="mini" @click="delParameter(scope.$index)"></el-button>
                                    <el-button v-if="scope.$index===(form.parameter.length-1)" size="mini" class="el-icon-plus" @click="addParameter"></el-button>
                                    <!--<el-button type="primary" size="mini" style="margin-bottom: 5px" @click="handleParameterEdit(scope.$index, scope.row)">更多设置</el-button>-->
                                </template>
                            </el-table-column>
                        </el-table>
                        <template>
                            <el-input :class="ParameterType? 'parameter-b': 'parameter-a'" type="textarea" :rows="5" placeholder="请输入内容" v-model.trim="parameterRaw"></el-input>
                        </template>
                    </el-collapse-item>
                    <el-collapse-item title="返回参数" name="3">
                        <el-table :data="form.response" highlight-current-row>
                            <el-table-column prop="name" label="参数名" min-width="20%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="value" label="预期值" min-width="25%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="_type" label="参数类型" min-width="15%">
                                <template slot-scope="scope">
                                    <el-select v-model.trim="scope.row._type"  placeholder="请求方式">
                                        <el-option v-for="(item,index) in paramType" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column label="必含?" min-width="10%" prop="required">
                                <template slot-scope="scope">
                                    <el-select v-model.trim="scope.row.required" placeholder="必填？">
                                        <el-option v-for="(item,index) in required4" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column prop="description" label="参数说明" min-width="20%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.description" :value="scope.row.desc" placeholder="请输入参数说明"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="15%">
                                <template slot-scope="scope">
                                    <el-button class="el-icon-delete" size="mini" @click="delResponse(scope.$index)"></el-button>
                                    <el-button v-if="scope.$index===(form.response.length-1)" size="mini" class="el-icon-plus" @click="addResponse"></el-button>
                                    <!--<el-button type="primary" size="mini" style="margin-bottom: 5px" @click="handleResponseEdit(scope.$index, scope.row)">更多设置</el-button>-->
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-collapse-item>
                    <el-collapse-item title="返回样例" name="4">
                        <div style="margin-bottom: 10px">
                            <el-button type="primary" size="mini" @click="formatResponse">格式转换</el-button>
                            <el-button type="primary" size="mini" @click="updateResponse">生成返回参数</el-button>
                        </div>
                        <el-card class="box-card">
                            <!--<div slot="header" class="clearfix">-->
                                <!--<span v-model="form.statusCode" style="font-size: 25px">{{form.statusCode}}</span>-->
                            <!--</div>-->
                            <div v-model="form.mockData" v-show="!format">
                                <el-input v-model="form.mockData" :value="form.mockData" type="textarea" :rows="5" placeholder="返回样例"></el-input>
                                <!--<div style="word-break: break-all;overflow:auto;overflow-x:hidden">{{form.mockData}}</div>-->
                            </div>
                            <div v-show="format">
                                <!--<pre id="formResult" style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden">{{form.resultData}}</pre>-->
                                <json-viewer :value="form.mockJsonData" :expand-depth=5 copyable></json-viewer>
                            </div>
                            <div v-show="!form.mockData" class="raw">暂无数据</div>
                        </el-card>
                    </el-collapse-item>
                    <!--<el-collapse-item title="普通mock" name="4">-->
                        <!--<el-card class="box-card">-->
                            <!--<div slot="header" class="clearfix">-->
                                <!--<el-select v-model="form.mockCode" placeholder="HTTP状态">-->
                                    <!--<el-option v-for="(item,index) in httpCode" :key="index+''" :label="item.label" :value="item.value"></el-option>-->
                                <!--</el-select>-->
                            <!--</div >-->
                            <!--<el-input v-model.trim="form.mockData" type="textarea" :rows="8" placeholder="请输入mock内容"></el-input>-->
                        <!--</el-card>-->
                    <!--</el-collapse-item>-->
                </el-collapse>
            </el-row>
        </el-form>
    </section>
</template>
<script>
    import Treeselect from '@riophae/vue-treeselect'
    // import the styles
    import '@riophae/vue-treeselect/dist/vue-treeselect.css'
    import { test } from '@/api/api'
//    import SelectTree from "../../../../components/treeSelect.vue";
    import $ from 'jquery'
    import axios from 'axios'
    export default {
        components: {
//          SelectTree,
          Treeselect,
        },
        data() {
            return {
                type: [{value: 'http', label: '普通http'},
                    {value: 'jyb', label: '加油宝app'},
                    {value: 'service', label: '微服务'}],
                request: [{value: 'GET', label: 'GET'},
                    {value: 'POST', label: 'POST'},
                    {value: 'PUT', label: 'PUT'},
                    {value: 'DELETE', label: 'DELETE'}],
                Http: [{value: 'HTTP', label: 'HTTP'},
                    {value: 'HTTPS', label: 'HTTPS'}],
                paramType: [{value: 'Int', label: 'Int'},
                    {value: 'String', label: 'String'},
                    {value: 'Object', label: 'Object'},
                    {value: 'Array', label: 'Array'}],
                checkHeadList: [],
                checkParameterList: [],
                ParameterType: true,
                group: [],
                requestParameterType: "application/x-www-form-urlencoded",
                status: [{value: true, label: '启用'},
                    {value: false, label: '禁用'}],
                header: [{value: 'Accept', label: 'Accept'},
                    {value: 'Accept-Charset', label: 'Accept-Charset'},
                    {value: 'Accept-Encoding', label: 'Accept-Encoding'},
                    {value: 'Accept-Language', label: 'Accept-Language'},
                    {value: 'Accept-Ranges', label: 'Accept-Ranges'},
                    {value: 'Authorization', label: 'Authorization'},
                    {value: 'Cache-Control', label: 'Cache-Control'},
                    {value: 'Connection', label: 'Connection'},
                    {value: 'Cookie', label: 'Cookie'},
                    {value: 'Content-Length', label: 'Content-Length'},
                    {value: 'Content-Type', label: 'Content-Type'},
                    {value: 'Content-MD5', label: 'Content-MD5'},
                    {value: 'Date', label: 'Date'},
                    {value: 'Expect', label: 'Expect'},
                    {value: 'From', label: 'From'},
                    {value: 'Host', label: 'Host'},
                    {value: 'If-Match', label: 'If-Match'},
                    {value: 'If-Modified-Since', label: 'If-Modified-Since'},
                    {value: 'If-None-Match', label: 'If-None-Match'},
                    {value: 'If-Range', label: 'If-Range'},
                    {value: 'If-Unmodified-Since', label: 'If-Unmodified-Since'},
                    {value: 'Max-Forwards', label: 'Max-Forwards'},
                    {value: 'Origin', label: 'Origin'},
                    {value: 'Pragma', label: 'Pragma'},
                    {value: 'Proxy-Authorization', label: 'Proxy-Authorization'},
                    {value: 'Range', label: 'Range'},
                    {value: 'Referer', label: 'Referer'},
                    {value: 'TE', label: 'TE'},
                    {value: 'Upgrade', label: 'Upgrade'},
                    {value: 'User-Agent', label: 'User-Agent'},
                    {value: 'Via', label: 'Via'},
                    {value: 'Warning', label: 'Warning'}],
                header4: "",
                addParameterFormVisible: false,
                addResponseFormVisible: false,
                required4:[{value: true, label: '是'},
                    {value: false, label: '否'}],
                httpCode:[{value: '', label: ''},
                    {value: '200', label: '200'},
                    {value: '404', label: '404'},
                    {value: '400', label: '400'},
                    {value: '500', label: '500'},
                    {value: '502', label: '502'},
                    {value: '302', label: '302'}],
                radioType: "",
                result: true,
                activeNames: ['2', '3', '4'],
                id: "",
                parameterRaw: "",
                form: {
                    firstGroup: null,
                    name: '',
                    type: 'http',
                    status: 'True',
                    method: 'GET',
                    http: 'HTTP',
                    addr: '',
                    head: [{name: "", value: ""}],
                    parameter: [{name: "", value: "", _type:"String", required:true, restrict: "", description: ""}],
                    parameterType: "",
                    response: [{name: "", value: "", _type:"String",required:true, description: ""}],
                    mockCode: '',
                    mockData: '',
                    mockJsonData: '',
                    description: '',
                },
                FormRules: {
                    name : [{ required: true, message: '请输入名称', trigger: 'blur' },
                        { max: 50, message: '不能超过50个字', trigger: 'blur' }],
                    type : [{ required: true, message: '请选择类型', trigger: 'blur'}],
                    addr : [{ required: true, message: '请输入地址', trigger: 'blur' }],
                    required : [{ required: true, message: '是否必须', trigger: 'blur' }],
                    firstGroup : [{ required: true, message: '请选择分组', trigger: 'blur'},],
                },
                editForm: {
                    name: "",
                    value: "",
                    required: "",
                    restrict: "",
                    description: "",
                },
                format: false,
                // editLoading: false
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
                axios.get(test+"/api/api/api_info", { params: {project_id: self.$route.params.project_id, api_id: self.$route.params.api_id}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        data = data.data;
                        self.id = data.id;
                        self.form.name = data.name;
                        self.form.type = data.type;
                        if (data.status) {
                            self.form.status = true;
                        } else {
                            self.form.status = false
                        }
                        self.form.method = data.requestType;
                        self.form.http = data.httpType;
                        self.form.addr = data.apiAddress;
                        if (data.headers.length) {
                            self.form.head = data.headers;
                        }
                        try {
                            self.parameterRaw = data.requestParameterRaw.data.replace(/'/g, "\"").replace(/None/g, "null").replace(/True/g, "true").replace(/False/g, "false");
                        } catch (e){

                        }
                        if (data.requestParameter.length) {
                            self.form.parameter = data.requestParameter;
                        }
                        self.form.parameterType = data.requestParameterType;
                        self.requestParameterType = self.form.parameterType;
                        if (data.response.length) {
                            self.form.response = data.response;
                        }
                        self.form.mockCode = data.mockCode;
                        self.form.mockData = data.data;
                        if (data.data) {
                            self.form.mockJsonData = JSON.parse(data.data)
                        }
                        self.form.description=data.description;
                        self.form.firstGroup = data.apiGroupLevelFirst;
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
            updateApiInfo(){
                if (this.form.mockData&&this.form.mockCode) {
                    if (!this.isJsonString(this.form.mockData)) {
                        this.$message({
                            message: 'mock格式错误',
                            center: true,
                            type: 'error'
                        })
                    } else {
                        this.updateApi()
                    }
                } else {
                    this.updateApi()
                }
            },
            updateApi: function () {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.form.parameterType = self.requestParameterType;
                            let _type = self.form.parameterType;
                            let _parameter = {};
                            let params={};

                            if ( _type === 'application/x-www-form-urlencoded'||_type === 'application/json'||_type === 'text/plain') {
                                if ( self.radioType === true) {
                                    _type = 'raw';
                                    self.form.parameter.forEach((item) => {
                                        if (item.name) {
                                            _parameter[item.name] = item.value
                                        }
                                        if (item.required) {
                                            if(item._type=="Object"||item._type=="Array"){
                                                params[item.name] = JSON.parse(item.value);
                                            }else{
                                                params[item.name] = item.value;
                                            }
                                        }
                                    });
                                    _parameter = JSON.stringify(_parameter)
                                } else {
                                    _parameter = self.form.parameter;
                                    self.form.parameter.forEach((item) => {
                                        if (item.required) {
                                            if(item._type=="Object"||item._type=="Array"){
                                                params[item.name] = JSON.parse(item.value);
                                            }else{
                                                params[item.name] = item.value;
                                            }
                                        }
                                    });
                                }
                            } else {
                                _parameter = self.parameterRaw
                            }
                            let param = JSON.stringify({
                                project_id: Number(self.$route.params.project_id),
                                id: Number(self.$route.params.api_id),
                                apiGroupLevelFirst_id: Number(self.form.firstGroup),
                                name: self.form.name,
                                type: self.form.type,
                                httpType: self.form.http,
                                requestType: self.form.method,
                                apiAddress: self.form.addr,
                                status: self.form.status,
                                headDict: self.form.head,
                                requestParameterType: _type,
                                requestList: _parameter,
                                responseList: self.form.response,
                                mockCode: self.form.mockCode,
                                data: self.form.mockData,
                                description: self.form.description,
                                params: JSON.stringify(params)
                            });
                            if (self.parameterRaw&&_type==="raw") {
                                if (!self.isJsonString(self.parameterRaw)) {
                                    self.$message({
                                        message: '源数据格式错误',
                                        center: true,
                                        type: 'error'
                                    })
                                } else {
                                    // console.log(_parameter)
                                    // console.log(typeof _parameter)
                                    axios.post(test + "/api/api/update_api", param, {headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                                        let data=response.data;
                                        if (data.code === '999999') {
                                            self.$router.push({
                                                name: '基础信息', params: {
                                                    project_id: self.$route.params.project_id,
                                                    api_id: self.$route.params.api_id
                                                }
                                            });
                                            self.$message({
                                                message: '修改成功',
                                                center: true,
                                                type: 'success'
                                            })
                                        }
                                        else {
                                            self.$message.error({
                                                message: data.msg,
                                                center: true,
                                            })
                                        }
                                    }).catch(error=>{

                                    });
                                }
                            } else {
                                axios.post(test + "/api/api/update_api", param, {headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                                    let data=response.data;
                                    if (data.code === '999999') {
                                        self.$router.push({
                                            name: '基础信息', params: {
                                                project_id: self.$route.params.project_id,
                                                api_id: self.$route.params.api_id
                                            }
                                        });
                                        self.$message({
                                            message: '修改成功',
                                            center: true,
                                            type: 'success'
                                        })
                                    }
                                    else {
                                        self.$message.error({
                                            message: data.msg,
                                            center: true,
                                        })
                                    }
                                }).catch(error=>{

                                });
                            }
                        }).catch(() => {});
                    }
                })
            },
            editParameterSubmit: function () {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.form.parameter[this.id] = this.editForm;
                        this.addParameterFormVisible = false
                    }
                })
            },
            handleParameterEdit: function (index, row) {
                this.addParameterFormVisible = true;
                this.id = index;
                this.editForm = Object.assign({}, row);
            },
            editResponseSubmit: function () {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.form.response[this.id] = this.editForm;
                        this.addResponseFormVisible = false
                    }
                })
            },
            handleResponseEdit: function (index, row) {
                this.addResponseFormVisible = true;
                this.id = index;
                this.editForm = Object.assign({}, row);
            },
            back(){
                this.$router.go(-1); // 返回上一层

            },
            // 获取api分组
            getApiGroupAndInfo() {
                let self = this;
                axios.get(test+"/api/api/group", {params:{project_id: this.$route.params.project_id},headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        self.group = data.data;
                    }else {
                        self.$message.error({
                            message: data.msg,
                            center: true,
                        })
                    }
                    this.getApiInfo();
                }).catch(error=>{

                });
            },
            addHead() {
                let headers = {name: "", value: ""};
                this.form.head.push(headers)
            },
            delHead(index) {
                this.form.head.splice(index, 1);
                if (this.form.head.length === 0) {
                    this.form.head.push({name: "", value: ""})
                }
            },
            addParameter() {
                let headers = {name: "", value: "", _type:"String", required:true, restrict: "", description: ""};
                this.form.parameter.push(headers)
            },
            delParameter(index) {
                this.form.parameter.splice(index, 1);
                if (this.form.parameter.length === 0) {
                    this.form.parameter.push({name: "", value: "", _type:"String", required:true, restrict: "", description: ""})
                }
            },
            addResponse() {
                let headers = {name: "", value: "", _type:"String", required:true, description: ""};
                this.form.response.push(headers)
            },
            delResponse(index) {
                this.form.response.splice(index, 1);
                if (this.form.response.length === 0) {
                    this.form.response.push({name: "", value: "", _type:"String", required:true, description: ""})
                }
            },
            changeParameterType() {
                if (this.requestParameterType === 'application/json') {
                    this.ParameterType = true;
                    if(this.parameterRaw!=""&&(this.form.parameter.length==0||this.form.parameter[0]["name"]=="")){
                        try{
                            let self=this;
                            this.form.parameter=[];
                            let json=JSON.parse(this.parameterRaw);
                            $.each(json, function (name, value) {
                                let type="String";
                                if(typeof(value)=='object'){
                                    if(value instanceof Array){
                                        type= 'Array'
                                    }else if( value instanceof Object ){
                                        type= 'Object';
                                    }
                                    value=JSON.stringify(value);
                                }else if(typeof(value)=='number'){
                                    type= 'Int';
                                }
                                let parameter = {name: name, value: value, _type:type,required:"True", restrict: "", description: ""};
                                self.form.parameter.push(parameter);
                            });
                        }catch(e){
                          alert(e);
                        }
                    }
                } else if (this.requestParameterType === 'application/x-www-form-urlencoded'||this.requestParameterType === 'text/plain') {
                    this.ParameterType = true;
                } else {
                    this.ParameterType = false;
                }
            },
            showData() {
                this.result = true
            },
            showHead(){
                this.result = false
            },
            handleChange(val) {
            },
            onSubmit() {
                console.log('submit!');
            },
            formatResponse(){
                if(!this.format&&this.form.mockData!=""){
                    try{
                        this.form.mockJsonData=JSON.parse(this.form.mockData);
                    }catch(e){}
                }
                this.format = !this.format;
            },
            getDataType(value){
                let type="String";
                try{
                    if(value instanceof Array){
                        type = 'Array';
                    }else if(value instanceof Object){
                        type = 'Object';
                    }else if(typeof(value)=='number'){
                        type = 'Int';
                    }
                }catch(Exception){}
                return type;
            },
            updateResponse(){
                this.$confirm('确认根据返回样例生成返回参数吗？', '提示', {}).then(() => {
                    this.form.response=[];
                    try{
                        let data=JSON.parse(this.form.mockData);
                        if(typeof(data)!='number'){
                            this.convertResponse('',data,2);
                        }
                    }catch(err){
                        alert(err);
                    }
                }).catch(() => {});
            },
            convertResponse(parent,data,depth){
                let self=this;
                $.each(data,function(name,value){
                    let item={required:true, description: ""};
                    try{
                        if(parent!=''){
                            item['name']=parent + '.' + name;
                        }else{
                            item['name']=name;
                        }
                        let type=self.getDataType(value);
                        if(type=='String'||type=='Int'){
                            item['_type']=type;
                            item['value']=value;
                            self.form.response.push(item);
                        }else if(type=='Array'){
                            item['_type']=type;
                            let childType=self.getDataType(value[0]);
                            if(childType=='String'||childType=='Int'){
                                item['value']=JSON.stringify(value);
                                self.form.response.push(item);
                            }else if(childType=='Object'){
                                item['value']='[]';
                                self.form.response.push(item);
                                if(depth>0){
                                    self.convertResponse(item['name']+"[*]",value[0],depth-1);
                                }
                            }
                        }else if(type=='Object'){
                            item['_type']=type;
                            item['value']='{}';
                            self.form.response.push(item);
                            if(depth>0){
                                self.convertResponse(item['name'],value,depth-1);
                            }
                        }
                    }catch(err){
                        alert(err.message);
                    }
                })
            },
            getValue(value) {
                this.form.firstGroup = value;
            },
            jybDecodePost() {
                var encodePost=this.parameterRaw.trim();
                if(encodePost=="")return;
                var apiUrl=this.form.addr.trim();
                var pos=0;
                var reg = new RegExp("(^|&)_pos=([^&]*)(&|$)", "i");
                var r = apiUrl.match(reg);
                if (r != null) {
                    pos=unescape(r[2]);
                }
                var version="";
                reg = new RegExp("(^|&)ver=([^&]*)(&|$)", "i");
                r = apiUrl.match(reg);
                if (r != null) {
                    version=unescape(r[2]);
                }
                let params = {
                    pos: pos,
                    post:encodePost,
                    version:version
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                let self=this;
                axios.post(test + '/api/api/jybdecode', params,{headers:headers}).then(res => {
                    let {msg, code, data} = res.data;
                    if (code === '999999') {
                        self.parameterRaw=JSON.stringify(data);
                    }else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
        },
        watch: {
            requestParameterType() {
                this.changeParameterType()
            }
        },
        mounted() {
            this.getApiGroupAndInfo();
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
</style>
<style lang="scss">
    .selectInput{
        input{
            border-right: 0px;
            border-radius: 4px 0px 0px 4px;
        }
    }
</style>
