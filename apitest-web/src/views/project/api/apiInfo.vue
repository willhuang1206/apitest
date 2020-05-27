<template>
    <section>
        <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px">
            <el-row :span="24">
                <el-col :span="2" style="padding-left: 6px; padding-right: 6px;">
                    <div class="httpStyle" v-model="type">{{type}}</div>
                </el-col>
                <el-col :span="2" style="padding-left: 6px;">
                    <div class="httpStyle" v-model="requestType">{{requestType}}</div>
                </el-col>
                <el-col :span="20" class="apiInfo">
                    <div>{{addr}}</div>
                    <div>{{apiName}}</div>
                </el-col>
                <!--<el-col :span="5">-->
                    <!--<i v-show="status" class="el-icon-check statusIcon"></i>-->
                    <!--<i v-show="!status" class="el-icon-close statusIcon"></i>-->
                    <!--<div class="apiDate" v-model="updateTime">{{updateTime}}</div>-->
                <!--</el-col>-->
            </el-row>
        </div>
        <el-collapse v-model="activeNames">
            <el-collapse-item title="请求头部" name="1">
                <el-table :data="head" highlight-current-row style="width: 100%;" v-loading="listLoadingHead">
                    <el-table-column type="index" label="#" min-width="5%">
                    </el-table-column>
                    <el-table-column prop="name" label="参数名" min-width="20%">
                    </el-table-column>
                    <el-table-column prop="value" label="参数值" min-width="60%" show-overflow-tooltip>
                    </el-table-column>
                </el-table>
            </el-collapse-item>
            <el-collapse-item title="请求参数" name="2">
                <template>
                    <div v-show="parameterRaw" :class="ParameterType? 'parameter-b': 'parameter-a'"
                         style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px;word-break: break-all" v-model="parameterRaw">{{parameterRaw}}</div>
                </template>
                <div v-show="!parameter.length&&!parameterRaw" class="raw">暂无数据</div>
                <el-table :data="parameter" highlight-current-row style="width: 100%;" v-loading="listLoadingParameter"
                          :class="ParameterType? 'parameter-a': 'parameter-b'">
                    <el-table-column type="index" label="#" min-width="5%">
                    </el-table-column>
                    <el-table-column prop="name" label="参数名" min-width="20%" show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column prop="value" label="参数值" min-width="40%" show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column prop="_type" label="参数类型" min-width="10%" show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column label="必填?" min-width="10%">
                        <template slot-scope="scope">
                            <img v-show="scope.row.required" src="@/assets/icon-yes.svg"/>
                            <img v-show="!scope.row.required" src="@/assets/icon-no.svg"/>
                        </template>
                    </el-table-column>
                    <el-table-column label="详情" min-width="10%">
                        <template slot-scope="scope">
                            <el-button size="small" @click="lookParameterInfo(scope.$index)">查看</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-collapse-item>
            <el-dialog title="请求参数详情" :visible.sync="parameterInfoVisible" :close-on-click-modal="false">
                <div v-model="parameterInfo" style="font-size: 15px">
                    <el-row :gutter="20" style="margin: 10px">
                        <div>
                            <el-col :span="7">参数名</el-col>
                            <el-col :span="7">参数类型</el-col>
                            <el-col :span="3">必填?</el-col>
                        </div>
                        <div style="margin-top: 30px">
                            <el-col :span="7">{{parameterInfo.name}}</el-col>
                            <el-col :span="7">{{parameterInfo._type}}</el-col>
                            <el-col :span="3">
                                <img v-show="parameterInfo.required" src="@/assets/icon-yes.svg"/>
                                <img v-show="!parameterInfo.required" src="@/assets/icon-no.svg"/>
                            </el-col>
                        </div>
                        <div style="margin-top: 70px"><el-col>参数值:</el-col></div>
                        <div style="margin-top: 100px">
                            <el-col>{{parameterInfo.value}}</el-col>
                        </div>
                        <div style="margin-top: 70px"><el-col>输入限制:</el-col></div>
                        <div style="margin-top: 100px">
                            <el-col v-show="parameterInfo.restrict">{{parameterInfo.restrict}}</el-col>
                            <el-col v-show="!parameterInfo.restrict">无限制要求</el-col>
                        </div>
                        <div style="margin-top: 140px"><el-col>说明:</el-col></div>
                        <div style="margin-top: 170px"><el-col v-show="parameterInfo.description">{{parameterInfo.description}}</el-col>
                            <el-col v-show="!parameterInfo.description">无详细说明</el-col>
                        </div>
                    </el-row>
                </div>
            </el-dialog>
            <el-collapse-item title="返回参数" name="3">
                <el-table :data="response" highlight-current-row style="width: 100%;" v-loading="listLoadingResponse">
                    <el-table-column type="index" label="#" min-width="5%">
                    </el-table-column>
                    <el-table-column prop="name" label="参数名" min-width="20%">
                    </el-table-column>
                    <el-table-column prop="value" label="预期值" min-width="40%">
                    </el-table-column>
                    <el-table-column prop="_type" label="参数类型" min-width="10%" show-overflow-tooltip>
                    </el-table-column>
                    <el-table-column label="必含?" min-width="10%">
                        <template slot-scope="scope">
                            <img v-show="scope.row.required" src="@/assets/icon-yes.svg"/>
                            <img v-show="!scope.row.required" src="@/assets/icon-no.svg"/>
                        </template>
                    </el-table-column>
                    <el-table-column label="详情" min-width="10%">
                        <template slot-scope="scope">
                            <el-button size="small" @click="lookResponseInfo(scope.$index)">查看</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-collapse-item>
            <el-dialog title="返回参数详情" :visible.sync="responseInfoVisible" :close-on-click-modal="false">
                <div v-model="responseInfo" style="font-size: 15px">
                    <el-row :gutter="20" style="margin: 10px">
                        <div>
                            <el-col :span="7">参数名</el-col>
                            <el-col :span="7">参数类型</el-col>
                            <el-col :span="3">必含?</el-col>
                        </div>
                        <div style="margin-top: 30px">
                            <el-col :span="7">{{responseInfo.name}}</el-col>
                            <el-col :span="7">{{responseInfo._type}}</el-col>
                            <el-col :span="3">
                                <img v-show="responseInfo.required" src="@/assets/icon-yes.svg"/>
                                <img v-show="!responseInfo.required" src="@/assets/icon-no.svg"/>
                            </el-col>
                        </div>
                        <div style="margin-top: 70px"><el-col>预期值:</el-col></div>
                        <div style="margin-top: 100px"><el-col v-show="responseInfo.value">{{responseInfo.value}}</el-col>
                            <el-col v-show="!responseInfo.value">无</el-col>
                        </div>
                        <div style="margin-top: 70px"><el-col>说明:</el-col></div>
                        <div style="margin-top: 100px"><el-col v-show="responseInfo.description">{{responseInfo.description}}</el-col>
                            <el-col v-show="!responseInfo.description">无详细说明</el-col>
                        </div>
                    </el-row>
                </div>
            </el-dialog>
            <el-collapse-item title="返回样例" name="4">
                  <div style="margin-bottom: 10px">
                      <el-button type="primary" size="mini" @click="format = !format">格式转换</el-button>
                  </div>
                  <el-card class="box-card">
                      <!--<div slot="header" class="clearfix">-->
                          <!--<span v-model="form.statusCode" style="font-size: 25px">{{form.statusCode}}</span>-->
                      <!--</div>-->
                      <div v-model="mockData" v-show="!format">
                          <!--<el-input v-model="form.data" :value="form.data" type="textarea" :rows="5" placeholder="返回样例"></el-input>-->
                          <div style="word-break: break-all;overflow:auto;overflow-x:hidden">{{mockData}}</div>
                      </div>
                      <div v-show="format">
                          <!--<pre id="formResult" style="border: 1px solid #e6e6e6;word-break: break-all;overflow:auto;overflow-x:hidden">{{form.resultData}}</pre>-->
                          <json-viewer :value="mockJsonData" :expand-depth=5 copyable></json-viewer>
                      </div>
                      <div v-show="!mockData" class="raw">暂无数据</div>
                  </el-card>
              </el-collapse-item>
            <!--<el-collapse-item title="普通Mock" name="4">-->
                <!--<el-card class="box-card">-->
                    <!--<div slot="header" class="clearfix">-->
                        <!--<el-select v-model="mockCode" placeholder="HTTP状态">-->
                            <!--<el-option v-for="(item,index) in httpCode" :key="index+''" :label="item.label" :value="item.value"></el-option>-->
                        <!--</el-select>-->
                        <!--<el-button type="primary" @click="changFormat">格式转换</el-button>-->
                    <!--</div >-->
                    <!--<div v-show="mockData" v-model="mockData" :class="resultShow? 'parameter-a': 'parameter-b'"-->
                         <!--style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px;word-break: break-all;line-height:25px">{{mockData}}</div>-->
                    <!--<div v-show="!mockData&&!mockJsonData" class="raw">暂无数据</div>-->
                    <!--<div v-show="mockJsonData" :class="!resultShow? 'parameter-a': 'parameter-b'"-->
                         <!--style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px;word-break: break-all;height:300px;overflow:auto;overflow-x:hidden">-->
                        <!--<pre>{{mockJsonData}}</pre>-->
                    <!--</div>-->
                <!--</el-card>-->
            <!--</el-collapse-item>-->
        </el-collapse>
    </section>
</template>

<script>
    import { test } from '@/api/api'
    import $ from 'jquery'
    import axios from 'axios'
    export default {
        data() {
            return {
                activeNames: ['2', '3', '4'],
                id: "",
                httpType: "",
                requestType: "",
                type: "",
                addr: "",
                apiName: "",
                updateTime: "",
                head: [],
                ParameterType: true,
                requestParameterType: "",
                parameter: [],
                parameterRaw: "",
                response: [],
                mockCode: "",
                mockData: "",
                mockJsonData: "",
                httpCode: [{value: '200', label: '200'},
                    {value: '404', label: '404'},
                    {value: '400', label: '400'},
                    {value: '500', label: '500'},
                    {value: '502', label: '502'},
                    {value: '302', label: '302'}],
                resultShow: true,
                status: true,
                listLoadingHead: false,
                listLoadingParameter: false,
                listLoadingResponse: false,
                parameterInfoVisible: false,
                parameterInfo: [],
                responseInfoVisible: false,
                responseInfo: [],
                format: false,
            }
        },
        methods: {
            getApiInfo() {
                let self = this;
                self.listLoadingHead = true;
                self.listLoadingParameter = true;
                self.listLoadingResponse = true;
                let param = {project_id: self.$route.params.project_id, api_id: self.$route.params.api_id};
                axios.get(test+"/api/api/api_info", {params:param}).then(response => {
                    self.listLoadingHead = false;
                    self.listLoadingParameter = false;
                    self.listLoadingResponse = false;
                    if (response.data.code === '999999') {
                        let data = response.data.data;
                        self.id = data.id;
                        self.httpType = data.httpType;
                        self.type = data.type;
                        self.requestType = data.requestType;
                        self.addr = data.apiAddress;
                        self.apiName = data.name;
                        self.updateTime = data.lastUpdateTime;
                        self.status = data.status;
                        self.head = data.headers;
                        self.requestParameterType = data.requestParameterType;
                        self.parameter = data.requestParameter;
                        try {
                            self.parameterRaw = data.requestParameterRaw.data;
                        } catch (e){

                        }
                        self.response = data.response;
                        self.mockCode = data.mockCode;
                        self.mockData = data.data;
                        if (data.data) {
                            self.mockJsonData = JSON.parse(data.data)
                        }
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
            formatChange() {
            },
            changFormat() {
                let demo = document.getElementsByTagName('pre')[0];
                console.log(demo)
                hljs.highlightBlock(demo);
                this.resultShow = !this.resultShow
            },
            lookParameterInfo(index) {
                this.parameterInfoVisible = true;
                this.parameterInfo = this.parameter[index]
            },
            lookResponseInfo(index) {
                this.responseInfoVisible = true;
                this.responseInfo = this.response[index]
            },
            parameterTypeChange() {
                if (this.requestParameterType === 'application/x-www-form-urlencoded'||this.requestParameterType === 'application/json'||this.requestParameterType === 'text/plain') {
                    this.ParameterType = true
                } else {
                    this.ParameterType = false
                }
            }
        },
        watch: {
            parameterType() {
                this.parameterTypeChange()
            }
        },
        mounted() {
            this.getApiInfo();
            this.formatChange()
        }
    }
</script>

<style lang="scss" scoped>
    .httpStyle {
        border-radius: 5px;
        padding-top: 20px;
        padding-right: 10px;
        padding-left: 10px;
        height: 74px;
        box-sizing: border-box;
        color: #fff;
        font-size: 160%;
        background-color: #409eff;
        text-align: center;
    }
    .apiInfo {
        padding-left: 25px;
        padding-right: 6px;
        font-size: 25px;
        padding-top: 7px
    }
    .statusIcon {
        padding-left: 25px;
        padding-right: 6px;
        padding-top: 7px;
        font-size: 30px;
    }
    .apiDate {
        margin-top: 18px;
        font-size: 20px;
    }
    .parameter-a {
        display: block;
    }
    .parameter-b {
        display: none;
    }
    .raw {
        border: 1px solid #e6e6e6;
        margin-bottom: 10px;
        padding:15px;
        text-align: center;
        z-index: 10000;
    }
</style>
