<template>
    <section>
        <el-form :model="form" ref="form" :rules="formRules">
            <el-row :span="24">
                <el-collapse v-model="activeNames">
                    <el-collapse-item title="请求头部" name="1">
                        <el-table :data="head" highlight-current-row @selection-change="selsChangeHead" ref="multipleHeadTable">
                            <el-table-column type="selection" min-width="5%" label="头部">
                            </el-table-column>
                            <el-table-column prop="name" label="参数名" min-width="20%">
                                <template slot-scope="scope">
                                    <el-select placeholder="head标签" filterable v-model="scope.row.name">
                                        <el-option v-for="(item,index) in header" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                    <el-input class="selectInput" v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="value" label="参数值" min-width="40%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="15%">
                                <template slot-scope="scope">
                                    <el-button class="el-icon-delete" size="mini" @click="delHead(scope.$index)"></el-button>
                                    <el-button v-if="scope.$index===(head.length-1)" size="mini" class="el-icon-plus" @click="addEmptyHead"></el-button>
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
                                <!--<el-col v-if="request3" :span="4"><el-radio v-model="requestParameterType" label="text/plain">Text</el-radio></el-col>-->
                                <!--<el-col v-if="request3" :span="8"><el-checkbox v-model="radioType" label="3" v-show="ParameterType">表单转源数据</el-checkbox></el-col>-->
                            </el-row>
                        </div>
                        <el-table :data="parameter" highlight-current-row :class="ParameterType? 'parameter-a': 'parameter-b'" @selection-change="selsChangeParameter" ref="multipleParameterTable">
                            <el-table-column type="selection" min-width="5%" label="头部">
                            </el-table-column>
                            <el-table-column prop="name" label="参数名" min-width="20%">
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="value" label="参数值" min-width="40%">
                                <template slot-scope="scope">
                                    <el-input type="textarea" :rows="1" v-model.trim="scope.row.value" :value="scope.row.value" placeholder="请输入参数值"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="15%">
                                <template slot-scope="scope">
                                    <el-button class="el-icon-delete" size="mini" @click="delParameter(scope.$index)"></el-button>
                                    <el-button v-if="scope.$index===(parameter.length-1)" size="mini" class="el-icon-plus" @click="addEmptyParameter"></el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                        <template>
                            <el-input :class="ParameterType? 'parameter-b': 'parameter-a'" type="textarea" :rows="5" placeholder="请输入内容" v-model.trim="parameterRaw"></el-input>
                        </template>
                    </el-collapse-item>
                </el-collapse>
            </el-row>
        </el-form>
    </section>
</template>
<script>
    import $ from 'jquery';
    import { test } from '@/api/api'
    import axios from 'axios';
    export default {
        name: 'ApiRequest',
        data() {
            return {
                paramType: [{value: 'Int', label: 'Int'},
                    {value: 'String', label: 'String'},
                    {value: 'Object', label: 'Object'},
                    {value: 'Array', label: 'Array'}],
                loadingSend: false,
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
                requestParameterType: "application/json",
                ParameterType: true,
                radioType: "",
                result: true,
                activeNames: ['2', '3', '4', '5'],
                id: "",
                head: [],
                parameter: [],
                parameterRaw: "",
                formRules: {
                },
                listLoading: false,
                headers: "",
                parameters: "",
                format: false,
                form: {
                    type: "http",
                    addr: ""
                }
            }
        },
        methods: {
            toggleHeadSelection(rows) {
                rows.forEach(row => {
                    this.$refs.multipleHeadTable.toggleRowSelection(row, true);
                });
            },
            toggleParameterSelection(rows) {
                rows.forEach(row => {
                    this.$refs.multipleParameterTable.toggleRowSelection(row, true);
                });
            },
            selsChangeParameter: function (sels) {
                this.parameters = sels;
            },
            selsChangeHead: function (sels) {
                this.headers = sels;
            },
            addEmptyHead() {
                let head = {name: "", value: ""};
                this.addHead(head);
            },
            addHead(head) {
                this.head.push(head);
                let rows = [this.head[this.head.length-1]];
                this.toggleHeadSelection(rows)
            },
            delHead(index) {
                if (this.head.length !== 1) {
                    this.head.splice(index, 1)
                }
            },
            addEmptyParameter(){
                let parameter = {name: "", value: "", required:"True", restrict: "", description: ""};
                this.addParameter(parameter);
            },
            addParameter(parameter) {
                this.parameter.push(parameter);
                let rows = [this.parameter[this.parameter.length-1]];
                this.toggleParameterSelection(rows)
            },
            delParameter(index) {
                if (this.parameter.length !== 1) {
                    this.parameter.splice(index, 1)
                }
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
            getParameters(){
                let parameters={}
                if ( this.requestParameterType === 'application/x-www-form-urlencoded'||this.requestParameterType === 'application/json'||this.requestParameterType === 'text/plain') {
                    for (let i = 0; i < this.parameters.length; i++) {
                        var a = this.parameters[i]["name"];
                        if (a) {
                            let parameterType=this.getDataType(this.parameters[i]["value"]);
                            if(parameterType=="Object"||parameterType=="Array"){
                                parameters[a] = JSON.parse(this.parameters[i]["value"]);
                            }else{
                                parameters[a] = this.parameters[i]["value"];
                            }
                        }
                    }
                } else {
                    parameters = this.parameterRaw;
                }
                return parameters;
            },
            changeParameterType() {
                if (this.requestParameterType === 'application/json') {
                    this.ParameterType = true;
                    if(this.parameterRaw!=""&&(this.parameters==""||(this.parameters.length==1&&this.parameters[0]["name"]==""))){
                        try{
                            let self=this;
                            this.parameter.splice(0);
                            let json=JSON.parse(this.parameterRaw);
                            $.each(json, function (name, value) {
                                if(typeof(value)!='string'){
                                    value=JSON.stringify(value);
                                }
                                let parameter = {name: name, value: value, required:"True", restrict: "", description: ""};
                                self.addParameter(parameter);
                            });
                        }catch(e){
                            console.log(e);
                        }
                    }
                } else if (this.requestParameterType === 'application/x-www-form-urlencoded'||this.requestParameterType === 'text/plain') {
                    this.ParameterType = true;
                } else if (this.requestParameterType === 'raw'){
                    this.ParameterType = false;
                    if(this.parameters!=""&&this.parameterRaw==""){
                        try{
                            let parameters={};
                            for (let i = 0; i < this.parameters.length; i++) {
                                var a = this.parameters[i]["name"];
                                if (a) {
                                    let parameterType=this.getDataType(this.parameters[i]["value"]);
                                    if(parameterType=="Object"||parameterType=="Array"){
                                        parameters[a] = JSON.parse(this.parameters[i]["value"]);
                                    }else{
                                        parameters[a] = this.parameters[i]["value"];
                                    }
                                }
                            }
                            this.parameterRaw=JSON.stringify(parameters);
                        }catch(e){
                            console.log(e);
                        }
                    }
                }
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
            this.toggleHeadSelection(this.head);
            this.toggleParameterSelection(this.parameter);
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
