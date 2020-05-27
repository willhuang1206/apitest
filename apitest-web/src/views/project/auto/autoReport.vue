<template>
    <section>
    <div class="main">
        <!--工具条-->
      <el-container>
      <el-header>
        <el-col v-show="!report.visible" :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <!--<el-button v-show="!summaryTable.visible" class="return-list" @click="back"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>返回</el-button>-->
                <!--<el-form-item v-show="summaryTable.visible">-->
                    <!--<el-input v-model.trim="filters.name" placeholder="名称" @keyup.enter.native="viewAutomationSummary"></el-input>-->
                <!--</el-form-item>-->
                <el-form-item v-if="global">
                    <el-select v-model="project_id"  placeholder="项目">
                        <el-option label="所有项目" value=""></el-option>
                        <el-option v-for="(item,index) in projectlist" :key="index+''" :label="item.name" :value="item.id"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-select v-model="type"  placeholder="类型">
                        <el-option v-for="(item,index) in listType" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item prop="timeArray">
                    <el-date-picker  v-model="filters.testtime" format="yyyy-MM-dd" value-format="yyyy-MM-dd" type="daterange" :picker-options="pickerOptions"
                                     range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" align="right" ></el-date-picker>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleSearch(type)">查询</el-button>
                </el-form-item>
            </el-form>
        </el-col>
        <el-row v-show="report.visible">
            <el-col :span="5" class='inline'>
                <el-card class="box-card">
                    <h3><i class=""/>{{report.data.name}}</h3>
                </el-card>
            </el-col>
            <el-col :span="3" class='inline'>
                <el-card class="box-card">
                    <h3><i class=""/>{{report.data.env}}</h3>
                </el-card>
            </el-col>
            <el-col :span="4" class='inline'>
                <el-card class="box-card">
                    <h3><i class=""/>{{report.data.testTime}}</h3>
                </el-card>
            </el-col>
            <el-col :span="3" class='inline'>
                <el-card class="box-card">
                    <h3>
                      <span v-show="report.data.status==='PASS'" style="color: #11b95c;">测试通过</span>
                      <span v-show="report.data.status==='FAIL'" style="color: #cc0000;">测试失败</span>
                    </h3>
                </el-card>
            </el-col>
            <el-col :span="3" class='inline'>
                <el-card class="box-card">
                    <h3><i class=""/>执行用例{{report.data.totalCount}}个</h3>
                </el-card>
            </el-col>
            <el-col v-show="report.data.status==='FAIL'" :span="2" class='inline'>
                <el-card class="box-card">
                    <h3><i class=""/>失败{{report.data.failCount}}个</h3>
                </el-card>
            </el-col>
            <el-col :span="3" class='inline'>
                <el-card class="box-card">
                    <h3><i class=""/>耗时{{report.data.duration}}秒</h3>
                </el-card>
            </el-col>
        </el-row>
        </el-header>
      <el-main>
        <el-row v-show="!report.visible">
          <el-card v-show="autoChart.visible" class="box-card">
            <div id="autoChart" style="height:376px"></div>
          </el-card>
        </el-row>
        <el-row v-show="!report.visible">
          <el-card v-show="publishChart.visible" class="box-card">
            <div id="publishChart" style="height:376px"></div>
          </el-card>
        </el-row>
        <el-row v-show="!report.visible">
          <el-col :span="12">
        <el-card v-show="failChart.visible" class="box-card">
          <div id="failTypeChart" style="height:376px"></div>
        </el-card>
            </el-col>
          <el-col :span="12">
        <el-card v-show="failChart.visible" class="box-card">
          <div id="failSeverityChart" style="height:376px"></div>
        </el-card>
            </el-col>
        </el-row>
        <el-row>
        <el-table :data="detailTable.list" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" v-loading="detailTable.loading" v-show="detailTable.visible" :row-style="tableRowStyle">
            <el-table-column type="expand">
                <template slot-scope="scope">
                    <el-table :data="scope.row.details" highlight-current-row style="width: 100%;">
                        <el-table-column type="expand">
                            <template slot-scope="props">
                                <el-form label-position="left" inline class="demo-table-expand">
                                    <el-row v-show="props.row.type==='api'" :gutter="10">
                                        <el-form-item label="接口地址： ">
                                            <span>{{ props.row.url }}</span>
                                        </el-form-item>
                                    </el-row>
                                    <el-row v-show="props.row.type==='api'" :gutter="10">
                                        <el-form-item label="请求方式： ">
                                            <span>{{ props.row.method }}</span>
                                        </el-form-item>
                                    </el-row>
                                    <el-row v-show="props.row.type==='api'" :gutter="10">
                                        <el-form-item label="请求参数： ">
                                            <span style="word-break: break-all;overflow:auto;overflow-x:hidden">{{ props.row.data }}</span>
                                        </el-form-item>
                                    </el-row>
                                    <el-row :gutter="10">
                                        <el-form-item label="返回结果： ">
                                            <span>
                                                <!--<pre style="word-break: break-all;overflow:auto;overflow-x:hidden">-->
                                                  <code v-show="props.row.type!=='api'">{{ props.row.result }}</code>
                                                <!--</pre>-->
                                                  <json-viewer v-show="props.row.type==='api'" :value="props.row.result" :expand-depth=5 boxed copyable></json-viewer>
                                            </span>
                                        </el-form-item>
                                    </el-row>
                                </el-form>
                            </template>
                        </el-table-column>
                        <el-table-column type="index" width="55">
                        </el-table-column>
                        <el-table-column prop="name" label="名称" min-width="20%" show-overflow-tooltip>
                            <template slot-scope="scope">
                                <span style="font-size: 16px">{{scope.row.name}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="result" label="返回结果" min-width="40%" show-overflow-tooltip>
                            <template slot-scope="scope">
                                <span style="font-size: 16px">{{scope.row.result}}</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="status" label="执行状态" min-width="10%" show-overflow-tooltip>
                            <template slot-scope="scope">
                                <span v-show="scope.row.status==='PASS'" style="color: #11b95c;cursor:pointer;">成功</span>
                                <span v-show="scope.row.status==='FAIL'" style="color: #cc0000;cursor:pointer;">失败</span>
                            </template>
                        </el-table-column>
                        <el-table-column prop="description" label="描述" min-width="30%" show-overflow-tooltip>
                            <template slot-scope="scope">
                                <span style="font-size: 16px">{{scope.row.description}}</span>
                            </template>
                        </el-table-column>
                    </el-table>
                </template>
            </el-table-column>
            <el-table-column type="index" label="#" width="100">
            </el-table-column>
            <el-table-column prop="name" label="步骤名称" min-width="20%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <span>{{scope.row.name}}</span>
                </template>
            </el-table-column>
            <el-table-column prop="testTime" label="测试时间" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="duration" label="执行时间(毫秒)" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="result" label="执行结果" min-width="15%" sortable show-overflow-tooltip>
              <template slot-scope="scope">
                    <span v-show="scope.row.result==='PASS'" style="color: #11b95c;">PASS</span>
                    <span v-show="scope.row.result==='FAIL'" @click="handleUpdateFail(detailTable.parentResult)" style="color: #cc0000;cursor:pointer;">FAIL</span>
                </template>
            </el-table-column>
        </el-table>
        <el-table :data="resultTable.list" stripe border element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" v-loading="resultTable.loading" v-show="resultTable.visible" :row-style="tableRowStyle">
            <el-table-column type="index" label="#" width="100">
            </el-table-column>
            <el-table-column  prop="name" label="名称" min-width="20%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link v-if="type==='case'" :to="{ name: '自动化执行详情', params: {project_id: project_id,automation_id: scope.row.automation_id,trace:scope.row.trace}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
                    <router-link v-if="type!=='case'" :to="{ name: '自动化任务执行结果', params: {project_id: project_id,trace:scope.row.trace}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
                </template>
            </el-table-column>
            <el-table-column prop="testTime" label="测试时间" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="env" label="环境" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="duration" label="执行时间(毫秒)" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="result" label="测试结果" min-width="15%" sortable show-overflow-tooltip>
              <template slot-scope="scope">
                    <span v-show="scope.row.result==='PASS'" style="color: #11b95c;">PASS</span>
                    <span v-show="scope.row.result==='FAIL'" :title="scope.row.failDetail" @click="handleUpdateFail(scope.row)" style="color: #cc0000;cursor:pointer;">FAIL<span v-if="scope.row.failType">({{failType[scope.row.failType]}}原因)</span></span>
                </template>
            </el-table-column>
            <el-table-column v-if="type==='case'" label="操作" min-width="20%">
                <template slot-scope="scope">
                    <router-link :to="{ name: '自动化步骤列表', params: {automation_id: scope.row.automation_id}}" style='text-decoration: none;'><el-button type="primary" size="small">查看用例</el-button></router-link>
                </template>
            </el-table-column>
        </el-table>
        <!--工具条-->
        <el-col v-show="resultTable.visible" :span="24" class="toolbar">
          <el-pagination layout="total, prev, pager, next" @current-change="handleResultPage" :current-page.sync="resultTable.page" :page-size="resultTable.pageSize" :page-count="resultTable.pages" :total="resultTable.total" style="float:right;">
          </el-pagination>
        </el-col>
        <el-table :data="summaryTable.list" stripe border element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" v-show="summaryTable.visible" highlight-current-row v-loading="summaryTable.loading" style="width: 100%;">
            <!--<el-table-column type="selection" min-width="5%">-->
            <!--</el-table-column>-->
            <el-table-column prop="automation_id" label="ID" min-width="5%" sortable>
            </el-table-column>
            <el-table-column prop="name" label="自动化名称" min-width="20%" sortable show-overflow-tooltip>
                <template slot-scope="scope">
                    <el-icon name="name"></el-icon>
                    <router-link :to="{ name: '自动化执行结果', params: {project_id: project_id,automation_id: scope.row.automation_id}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
                </template>
            </el-table-column>
            <el-table-column prop="total" label="执行总数" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="passed" label="执行成功" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="passRate" label="通过率(%)" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="duration" label="执行总时间(毫秒)" min-width="10%" sortable show-overflow-tooltip>
            </el-table-column>
            <!--<el-table-column label="操作" min-width="20%">-->
                <!--<template slot-scope="scope">-->
                    <!--<el-button type="primary" size="small" @click="viewAutomationResult('case',scope.row.automation_id)">查看</el-button>-->
                <!--</template>-->
            <!--</el-table-column>-->
        </el-table>
        <!--工具条-->
        <el-col v-show="summaryTable.visible" :span="24" class="toolbar">
          <el-pagination layout="total, prev, pager, next" @current-change="handleSummaryPage" :page-size="summaryTable.pageSize" :current-page.sync="summaryTable.page" :page-count="summaryTable.pages" :total="summaryTable.total" style="float:right;">
          </el-pagination>
        </el-col>
          <el-table :data="apiAutomatedTable.list" stripe border element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" v-loading="apiAutomatedTable.loading" v-show="apiAutomatedTable.visible" :row-style="tableRowStyle">
            <el-table-column type="index" label="#" width="100">
            </el-table-column>
            <el-table-column  prop="name" label="名称" min-width="20%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="num" label="关联自动化数" min-width="15%" sortable show-overflow-tooltip>
            </el-table-column>
            <el-table-column prop="automationName" label="关联自动化用例" min-width="30%" sortable show-overflow-tooltip>
            </el-table-column>
        </el-table>
        <!--工具条-->
        <el-col v-show="apiAutomatedTable.visible" :span="24" class="toolbar">
          <el-pagination layout="total, prev, pager, next" @current-change="handleApiAutomatedTablePage" :current-page.sync="apiAutomatedTable.page" :page-size="20" :page-count="apiAutomatedTable.pages" :total="apiAutomatedTable.total" style="float:right;">
          </el-pagination>
        </el-col>
          </el-row>
      </el-main>
      </el-container>
      <el-dialog width="40%" title="错误详情" :visible.sync="failForm.visible" :close-on-click-modal="false">
            <el-form :model="failForm.data"  :rules="failForm.rules" ref="failForm" label-width="80px">
                <el-form-item label="类型" label-width="83px" prop="type">
                    <el-select v-model="failForm.data.type" placeholder="类型">
                        <el-option v-for="(item,key) in failType" :label="item" :value="key"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="严重等级" label-width="83px" prop="severity">
                    <el-select v-model="failForm.data.severity" placeholder="严重等级">
                        <el-option v-for="(item,index) in severity" :key="index+''" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="根源" prop='cause'>
                    <el-input type="textarea" :rows="2" v-model.trim="failForm.data.cause"></el-input>
                </el-form-item>
                <el-form-item label="详情" prop='detail'>
                    <el-input type="textarea" :rows="2" v-model.trim="failForm.data.detail"></el-input>
                </el-form-item>
                <el-form-item label="关联缺陷" prop='bug'>
                    <el-input type="input" v-model.trim="failForm.data.bug"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="failForm.visible = false">取消</el-button>
                <el-button type="primary" @click.native="updateFailSubmit" :loading="failForm.loading">提交</el-button>
            </div>
        </el-dialog>
    </div>
    </section>
</template>

<script>
    import { test } from '../../../api/api'
    import $ from 'jquery'
    import axios from 'axios'
    export default {
        name: "automation-report",
        data(){
            return {
                project_id: this.$route.params.project_id,
                automation_id: this.$route.params.automation_id,
                type: "autoChart",
                global: false,
                report: {
                    visible: false,
                    data: {},
                },
                filters: {
                    name: "",
                    testtime: this.defaultDate(),
                    start_time: "",
                    end_time: "",
                    project: "",
                },
                projectlist: [],
                listType: [{value: 'autoChart', label: '用例执行统计'},
                    {value: 'apiChart', label: '接口执行统计'},
                    {value: 'publish', label: '发布项目统计'},
                    {value: 'case', label: '用例执行情况'},
                    {value: 'task', label: '任务执行情况'},
                    {value: 'apiAutomated', label: '接口覆盖统计'},
                    {value: 'dynamicChart', label: '项目动态统计'},
                ],
                summaryTable:{
                    loading: false,
                    visible: false,
                    list: [],
                    page: 1,
                    pages: 0,
                    total: 0,
                    pageSize: 20,
                },
                resultTable:{
                    loading: false,
                    visible: false,
                    list: [],
                    page: 1,
                    pages: 0,
                    total: 0,
                    pageSize:20,
                },
                detailTable:{
                    loading: false,
                    visible: false,
                    list: [],
                    parentResult: null,
                },
                apiAutomatedTable:{
                    loading: false,
                    visible: false,
                    list: [],
                    page: 1,
                    pages: 0,
                    total: 0,
                },
                stepTable:{
                    visible: false,
                    list: [],
                    name: ""
                },
                autoChart:{
                    visible: false,
                },
                publishChart:{
                    visible: false,
                },
                failChart:{
                    visible: false,
                },
                failType: {'code':'编码','env':'环境','data':'数据','other':'其他'},
                severity: [{value: 'fatal', label: '致命的'},
                     {value: 'critical', label: '严重的'},
                    {value: 'major', label: '一般的'},
                    {value: 'minor', label: '微小的'},
                ],
                failForm: {
                    visible: false,
                    loading: false,
                    data:{
                        id: "",
                        type: "code",
                        severity: "major",
                        cause: "",
                        detail: "",
                        bug: "",
                    },
                    row: null,
                    rules: {
                        type: [
                            { required: true, message: '请选择类型', trigger: 'blur'}
                        ],
                        severity: [
                            { required: true, message: '请选择严重等级', trigger: 'blur'}
                        ],
                        cause: [
                            { required: true, message: '请输入根源', trigger: 'blur' },
                            { max: 256, message: '不能超过256个字符', trigger: 'blur' }
                        ],
                        detail: [
                            { required: true, message: '请输入详情', trigger: 'blur' },
                            { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                        ],
                        bug: [
                            { max: 50, message: '不能超过50个字符', trigger: 'blur' }
                        ],
                    },
                },
                pickerOptions: {
                  shortcuts: [{
                    text: '今天',
                    onClick(picker) {
                      const end = new Date();
                      const start = new Date();
                      picker.$emit('pick', [start, end])
                    }
                  },{
                    text: '昨天',
                    onClick(picker) {
                      const end=new Date();
                      end.setDate(end.getDate() - 1);
                      const start=new Date();
                      start.setDate(start.getDate() - 1);
                      picker.$emit('pick', [start, end])
                    }
                  },{
                    text: '本周',
                    onClick(picker) {
                      const end = new Date();
                      const weekday = end.getDay() || 7;
                      const start = new Date();
                      start.setDate(start.getDate() - weekday + 1);
                      picker.$emit('pick', [start, end]);
                    }
                  },{
                    text: '上周',
                    onClick(picker) {
                      const end = new Date();
                      const weekday = end.getDay() || 7;
                      end.setDate(end.getDate() - weekday);
                      const start = new Date();
                      start.setDate(end.getDate() - 6);
                      picker.$emit('pick', [start, end])
                    }
                  },{
                    text: '最近一周',
                    onClick(picker) {
                      const end = new Date();
                      const start = new Date();
                      start.setDate(start.getDate() - 6);
                      picker.$emit('pick', [start, end]);
                    }
                  },{
                    text: '本月',
                    onClick(picker) {
                      const end = new Date();
                      const start = new Date();
                      start.setDate(1);
                      picker.$emit('pick', [start, end])
                    }
                  },{
                    text: '最近一个月',
                    onClick(picker) {
                      const end = new Date();
                      const start = new Date();
                      start.setTime(start.getTime() - 3600 * 1000 * 24 * 29);
                      picker.$emit('pick', [start, end]);
                    }
                  }, {
                    text: '最近三个月',
                    onClick(picker) {
                      const end = new Date();
                      const start = new Date();
                      start.setTime(start.getTime() - 3600 * 1000 * 24 * 89);
                      picker.$emit('pick', [start, end]);
                    }
                  },{
                    text: '今年',
                    onClick(picker) {
                      const end = new Date();
                      const start = new Date();
                      start.setMonth(0);
                      start.setDate(1);
                      picker.$emit('pick', [start, end]);
                    }
                  }]
                },
            }
        },
        methods: {
            tableRowStyle(row) {
                if (row.result === 'ERROR' || row.result === 'FAIL') {
                    return "background-color: #DC143C;"
                } else if(row.result === 'TimeOut'){
                    return "background-color: #FFE4C4;"
                }
              },
            filterHandler(value, row, column) {
                return row.result === value;
            },
            handleSearch(type){
                this.apiAutomatedTable.visible=false;
                this.publishChart.visible=false;
                if(type=="case"){
                    this.summaryTable.page=1;
                    this.autoChart.visible=false;
                    this.failChart.visible=false;
                    this.viewAutomationSummary();
                }else if(type=="autoChart"){
                    this.autoChart.visible=true;
                    this.failChart.visible=true;
                    this.viewAutomationChart();
                    this.viewAutomationSummary();
                }else if(type=="apiChart"){
                    this.autoChart.visible=true;
                    this.failChart.visible=false;
                    this.viewApiChart();
                }else if(type=="dynamicChart"){
                    this.autoChart.visible=true;
                    this.failChart.visible=false;
                    this.viewDynamicChart();
                }else if(type=="publish"){
                    this.resultTable.page=1;
                    this.autoChart.visible=true;
                    this.publishChart.visible=true;
                    this.failChart.visible=false;
                    this.viewPublishChart();
                    this.viewAutomationResult(type,"");
                }else if(type=="task"){
                    this.resultTable.page=1;
                    this.autoChart.visible=false;
                    this.failChart.visible=false;
                    this.viewAutomationResult(type,"");
                }else if(type=="apiAutomated"){
                    this.apiAutomatedTable.page=1;
                    this.autoChart.visible=false;
                    this.failChart.visible=false;
                    this.viewApiAutomated();
                }
            },
            viewAutomationSummary() {
                if(this.filters.testtime!=""&&this.filters.testtime!=null){
                    this.filters.start_time=this.filters.testtime[0];
                    this.filters.end_time=this.filters.testtime[1];
                }else{
                    this.filters.start_time="";
                    this.filters.end_time="";
                }
                this.summaryTable.visible=true;
                this.resultTable.visible=false;
                this.detailTable.visible=false;
                this.summaryTable.loading = true;
                let self = this;
                let param={
                        project_id: this.project_id,
                        name: this.filters.name,
                        start_time: this.filters.start_time,
                        end_time: this.filters.end_time,
                        page: self.summaryTable.page
                    };
                if(this.filters.start_time!=""&&this.filters.end_time!=""){
                    self.summaryTable.pageSize=500;
                    param["page_size"]=self.summaryTable.pageSize;
                }else{
                    self.summaryTable.pageSize=20;
                    param["page_size"]=self.summaryTable.pageSize;
                }
                axios.get(test + "/api/report/automation_summary",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.summaryTable.loading = false;
                    if (data.code === '999999') {
//                            alert(data.data.data);
                        self.summaryTable.total = data.data.total;
                        self.summaryTable.pages = data.data.pages;
                        self.summaryTable.list = [];
//                            alert(data.data.data);
                        data.data.data.forEach((item) =>{
                            item["passRate"]=parseFloat((item["passed"]*100/item["total"]).toFixed(1));
                            self.summaryTable.list.push(item);
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
            },
            viewAutomationChart() {
                if(this.filters.testtime!=""&&this.filters.testtime!=null){
                    this.filters.start_time=this.filters.testtime[0];
                    this.filters.end_time=this.filters.testtime[1];
                }else{
                    this.filters.start_time="";
                    this.filters.end_time="";
                }
                let self = this;
                let param={
                        project_id: this.project_id,
                        start_time: this.filters.start_time,
                        end_time: this.filters.end_time
                    };
                axios.get(test + "/api/report/automation_chart",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        this.autoChart.visible=true;
                        this.drawbar(data.data.autoChart, "autoChart","用例执行统计","bar");
                        if(data.data.failTypeChart.line_name.length>0){
                            this.failChart.visible=true;
                            this.drawpie(data.data.failTypeChart, "failTypeChart","失败类型");
                            this.drawpie(data.data.failSeverityChart, "failSeverityChart","失败严重等级");
                        }else{
                            this.failChart.visible=false;
                        }
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
            viewPublishChart() {
                if(this.filters.testtime!=""&&this.filters.testtime!=null){
                    this.filters.start_time=this.filters.testtime[0];
                    this.filters.end_time=this.filters.testtime[1];
                }else{
                    this.filters.start_time="";
                    this.filters.end_time="";
                }
                this.summaryTable.visible=false;
                this.resultTable.visible=false;
                this.detailTable.visible=false;
                this.summaryTable.loading = true;
                let self = this;
                let param={
                        project_id: this.project_id,
                        start_time: this.filters.start_time,
                        end_time: this.filters.end_time
                    };
                axios.get(test + "/api/report/publish_chart",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        this.autoChart.visible=true;
                        this.drawbar(data.data.publish_chart, "autoChart","发布项目统计-按日期","bar");
                        this.publishChart.visible=true;
                        this.drawpie(data.data.publish_pie, "publishChart","发布项目");
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
            viewApiChart() {
                if(this.filters.testtime!=""&&this.filters.testtime!=null){
                    this.filters.start_time=this.filters.testtime[0];
                    this.filters.end_time=this.filters.testtime[1];
                }else{
                    this.filters.start_time="";
                    this.filters.end_time="";
                }
                this.summaryTable.visible=false;
                this.resultTable.visible=false;
                this.detailTable.visible=false;
                this.summaryTable.loading = true;
                let self = this;
                let param={
                        project_id: this.project_id,
                        start_time: this.filters.start_time,
                        end_time: this.filters.end_time
                    };
                axios.get(test + "/api/report/api_chart",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        this.autoChart.visible=true;
                        this.drawbar1(data.data, "autoChart","接口执行统计","bar");
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
            viewDynamicChart() {
                if(this.filters.testtime!=""&&this.filters.testtime!=null){
                    this.filters.start_time=this.filters.testtime[0];
                    this.filters.end_time=this.filters.testtime[1];
                }else{
                    this.filters.start_time="";
                    this.filters.end_time="";
                }
                this.summaryTable.visible=false;
                this.resultTable.visible=false;
                this.detailTable.visible=false;
                this.summaryTable.loading = true;
                let self = this;
                let param={
                        project_id: this.project_id,
                        start_time: this.filters.start_time,
                        end_time: this.filters.end_time
                    };
                axios.get(test + "/api/report/dynamic_chart",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    if (data.code === '999999') {
                        this.autoChart.visible=true;
                        this.drawbar1(data.data, "autoChart","项目动态统计","bar");
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
            drawbar(test_bar_data, chartid,title,type) {
                let echartBar = this.$echarts.init(document.getElementById(chartid));
                echartBar.clear();
                var option = {
                    title: {
                        text: title
                    },
                    tooltip : {
                        trigger: 'axis'
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    legend: {
                        data:['执行数','通过率']
                    },
                    xAxis : [
                        {
                            type : 'category',
                            data: test_bar_data.line_name,
                            axisLabel: {
                                interval: 0,
                                rotate: 30,
                            },
                            axisPointer: {
                                type: 'shadow'
                            }
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
                            name : '执行数'
                        },
                        {
                            type : 'value',
                            name : '通过率',
                            min: 0,
                            max: 100,
                            interval: 20,
                            axisLabel: {
                                formatter: '{value}%'
                            }
                        }
                    ],
                    series : [
                        {
                            name: '执行数',
                            type: type,
                            itemStyle: {
                                normal: {
//                                    color:'#7cb5ec',
                                    label : {
                                        show: true, position: 'top'
                                    }
                                }
                            },
                            data: test_bar_data.line_x
                        },
                        {
                            name: '通过率',
                            type: 'line',
                            smooth: true,
                            yAxisIndex: 1,
                            itemStyle: {
                                normal: {
                                    color:'#26B99A',
                                    label : {
                                        show: true, position: 'top'
                                    }
                                }
                            },
                            data: test_bar_data.line_x1
                        }
                    ]
                };
                echartBar.setOption(option);
            },
            drawbar1(test_bar_data, chartid,title,type) {
                let echartBar = this.$echarts.init(document.getElementById(chartid));
                echartBar.clear();
                var option = {
                    title: {
                        text: title
                    },
                    tooltip : {
                        trigger: 'axis'
                    },
                    toolbox: {
                        show : true,
                        feature : {
                            mark : {show: true},
                            dataView : {show: true, readOnly: false},
                            magicType : {show: true, type: ['line', 'bar']},
                            restore : {show: true},
                            saveAsImage : {show: true}
                        }
                    },
                    calculable : true,
                    legend: {
                        data:['执行数']
                    },
                    xAxis : [
                        {
                            type : 'category',
                            data: test_bar_data.line_name,
                            axisLabel: {
                                interval: 0,
                                rotate: 30,
                            },
                            axisPointer: {
                                type: 'shadow'
                            }
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
                            name : '执行数'
                        }
                    ],
                    series : [
                        {
                            name: '执行数',
                            type: type,
                            itemStyle: {
                                normal: {
                                    color:'#7cb5ec',
                                    label : {
                                        show: true, position: 'top'
                                    }
                                }
                            },
                            data: test_bar_data.line_x
                        }
                    ]
                };
                echartBar.setOption(option);
            },
            drawpie(data, chartid,title) {
                let echartBar = this.$echarts.init(document.getElementById(chartid));
                echartBar.clear();
                var option = {
                    title: {
                        text: title + "统计",
                    },
                    tooltip: {
                        trigger: 'item',
                        formatter: '{a} <br/>{b} : {c} ({d}%)'
                    },
                    legend: {
                        left: 'center',
                        data: data.line_name,
                    },
                    series: [
                        {
                            name: title,
                            type: 'pie',
                            radius: '55%',
                            center: ['50%', '60%'],
                            data: data.line_data,
                            label: {
                                formatter: '{b} : {c} ({d}%)'
                            },
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                };
                echartBar.setOption(option);
            },
            viewApiAutomated() {
                this.summaryTable.visible=false;
                this.resultTable.visible=false;
                this.detailTable.visible=false;
                this.apiAutomatedTable.visible=true;
                this.apiAutomatedTable.loading=true;
                let param={
                    project_id: this.project_id,
                    page: this.apiAutomatedTable.page,
                };
                let url=test + "/api/report/apiautomatedcoverage";
                let self=this;
                axios.get(url,{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.apiAutomatedTable.loading = false;
                    if (data.code === '999999') {
                        self.apiAutomatedTable.list = data.data.data;
                        self.apiAutomatedTable.pages=data.data.pages;
                        self.apiAutomatedTable.total=data.data.total;
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
            viewAutomationResult(type,automationId) {
                this.type=type;
                if(this.filters.testtime!=""&&this.filters.testtime!=null){
                    this.filters.start_time=this.filters.testtime[0];
                    this.filters.end_time=this.filters.testtime[1];
                }else{
                    this.filters.start_time="";
                    this.filters.end_time="";
                }
                this.summaryTable.visible=false;
                this.resultTable.visible=true;
                this.detailTable.visible=false;
                this.resultTable.loading=true;
                let param={
                    project_id: this.project_id,
                    start_time: this.filters.start_time,
                    end_time: this.filters.end_time,
                    page: this.resultTable.page,
                    type: this.type,
                };
                let url=test + "/api/report/automation_result";
                if(this.type=="case"){
                    if(automationId!=""){
                        param["automation_id"]=automationId;
                        this.automation_id=automationId;
                    }else if(this.$route.params.trace){
                        param["trace"]=this.$route.params.trace;
                    }else{
                        param["automation_id"]=automationId;
                        this.automation_id=param["automation_id"]
                    }
                }else{
                    url=test + "/api/report/automations_result";
                }
                let self=this;
                axios.get(url,{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.resultTable.loading = false;
                    if (data.code === '999999') {
                        self.resultTable.list = data.data.data;
                        self.resultTable.pages=data.data.pages;
                        self.resultTable.total=data.data.total;
                        self.resultTable.pageSize=data.data.page_size;
                        if(data.data.report){
                            self.report.visible=true;
                            self.report.data=data.data.report;
                        }
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
            viewAutomationDetail(id,trace) {
                this.summaryTable.visible=false;
                this.resultTable.visible=false;
                this.detailTable.visible=true;
                this.detailTable.loading=true;
                let self=this;
                let param={
                        automation_id: id,
                        trace: trace
                    };
                axios.get(test + "/api/report/automation_detail",{params:param,headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                    let data=response.data;
                    self.detailTable.loading = false;
                    if (data.code === '999999') {
                        self.detailTable.list = data.data.results;
                        self.detailTable.parentResult=data.data.parentResult;
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
            // 翻页
            handleSummaryPage(val) {
                this.summaryTable.page = val;
                this.viewAutomationSummary();
            },
            // 翻页
            handleApiAutomatedTablePage(val) {
                this.apiAutomatedTable.page = val;
                this.viewApiAutomated();
            },
            handleResultPage(val) {
                this.resultTable.page = val;
                if(this.$route.params.automation_id){
                    this.viewAutomationResult(this.type,this.$route.params.automation_id);
                }else{
                    this.viewAutomationResult(this.type,"");
                }
            },
            defaultDate(){
                //获取新的时间(2019.4.12）
                let date = new Date();
                //获取当前时间的年份转为字符串
                let year = date.getFullYear().toString();   //'2019'
                //获取月份，由于月份从0开始，此处要加1，判断是否小于10，如果是在字符串前面拼接'0'
                let month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1).toString() : (date.getMonth() + 1).toString();  //'04'
                //获取天，判断是否小于10，如果是在字符串前面拼接'0'
                let da = date.getDate() < 10 ? '0' + date.getDate().toString() : date.getDate().toString();  //'12'
                //字符串拼接，开始时间，结束时间
                let end = year + '-' + month + '-' + da;  //当天'2019-04-12'
                let beg = year + '-' + month + '-01';    //当月第一天'2019-04-01'
                return [beg, end]; //将值设置给插件绑定的数据
            },
            handleUpdateFail(row){
                this.failForm.visible=true;
                this.failForm.data={id:row.id,type:row.failType,severity:row.failSeverity,cause:row.failCause,detail:row.failDetail,bug:row.failBug};
                this.failForm.row=row;
            },
            updateFailSubmit() {
                this.$refs.failForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            let self = this;
                            let param=JSON.stringify({
                                    project_id: this.$route.params.project_id,
                                    result_id: this.failForm.data.id,
                                    type: this.failForm.data.type,
                                    severity: this.failForm.data.severity,
                                    cause: this.failForm.data.cause,
                                    detail: this.failForm.data.detail,
                                    bug: this.failForm.data.bug,
                                });
                            axios.post(test + "/api/report/updateresultfaildetail",param,{headers:{"Content-Type": "application/json", Authorization: 'Token ' + sessionStorage.getItem('token')}}).then(response => {
                                let data=response.data;
                                if (response.data.code === '999999') {
                                    self.failForm.visible=false;
                                    self.failForm.row.failType=this.failForm.data.type;
                                    self.failForm.row.failSeverity=this.failForm.data.severity;
                                    self.failForm.row.failCause=this.failForm.data.cause;
                                    self.failForm.row.failDetail=this.failForm.data.detail;
                                    self.failForm.row.failBug=this.failForm.data.bug;
                                    self.$message({
                                        message: '更新成功',
                                        center: true,
                                        type: 'success'
                                    })
                                } else {
                                    self.$message.error({
                                        message: response.data.msg,
                                        center: true,
                                    })
                                }
                            }).catch(error=>{});
                        }).catch(() => {});
                    }
                });
            },
            // 获取项目列表
            getProjectList() {
                this.listLoading = true;
                let self = this;
                let params = { page: 1, page_size: 100, status: true};
                let headers = {Authorization: 'Token '+sessionStorage.getItem('token')};
                axios.get(`${test}/api/project/project_list`, { params: params, headers:headers}).then((res) => {
                    let { msg, code, data } = res.data;
                    if (code === '999999') {
                        self.projectlist = data.data;
                    }else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },
            init(){
                this.autoChart.visible=false;
                this.failChart.visible=false;
                if(this.$route.params.project_id){
                    this.project_id=this.$route.params.project_id;
                    this.global=false;
                }else{
                    this.global=true;
                    this.getProjectList();
                }
                if(this.$route.params.automation_id){
                    this.automation_id=this.$route.params.automation_id;
                    if(!this.$route.params.trace){
                        this.viewAutomationResult('case',this.automation_id);
                    }else{
                        this.viewAutomationDetail(this.$route.params.automation_id,this.$route.params.trace);
                    }
                }else if(this.$route.params.trace){
                    this.viewAutomationResult('case',"");
                }
            }
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

<style scoped>
    .number-pass {
        border-radius: 25px;
        position: absolute;
        height: 100px;
        box-sizing: border-box;
        color: #fff;
        font-size: 25px;
        text-align: center;
        width: 100px;
        top: -70px;
        right: 350px;
    }
    .number-fail {
        border-radius: 25px;
        border: 1px solid #C4C4C4;
        position: absolute;
        height: 100px;
        box-sizing: border-box;
        /*color: #fff;*/
        font-size: 25px;
        text-align: center;
        width: 100px;
        top: -70px;
        right: 240px;
    }
    .number-error {
        border-radius: 25px;
        position: absolute;
        height: 100px;
        box-sizing: border-box;
        color: #fff;
        font-size: 25px;
        text-align: center;
        width: 100px;
        top: -70px;
        right: 130px;
    }
    .number-total {
        border-radius: 25px;
        border: 1px solid #C4C4C4;
        position: absolute;
        height: 100px;
        box-sizing: border-box;
        /*color: #fff;*/
        font-size: 25px;
        text-align: center;
        width: 100px;
        top: -70px;
        right: 20px;
    }
    .demo-table-expand {
        font-size: 0;
      }
      .demo-table-expand label {
          width: 90px;
          color: #99a9bf;
      }
      .demo-table-expand .el-form-item {
          margin-right: 0;
          margin-bottom: 0;
          width: 50%;
      }
    .return-list {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }
</style>
