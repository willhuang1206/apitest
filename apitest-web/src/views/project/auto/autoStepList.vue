<template>
    <section>
        <!--<router-link :to="{ name: '自动化列表', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>-->
            <!--<el-button class="return-list"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>自动化列表</el-button>-->
        <!--</router-link>-->
        <el-button v-show="(currentType==='case'||currentType==='reuse')&&pageType==='update'" type="primary" @click.native="handleAdd">添加步骤</el-button>
        <el-button v-show="(currentType==='case'||currentType==='reuse')&&pageType==='update'" type="primary" @click.native="handleAddReuse">添加可重用步骤</el-button>
        <el-button v-show="currentType==='monitor'&&pageType==='update'" type="primary" @click="handleLinkApi">关联接口</el-button>
        <el-button v-show="currentType==='list'&&pageType==='update'" type="primary" @click="handleLinkAutomation">关联自动化</el-button>
        <!--<router-link :to="{ name: '添加新接口'}" style='text-decoration: none;color: #000000;'>-->
            <!--<el-button type="primary"><i class="el-icon-plus" style="margin-right: 5px"></i>新建接口</el-button>-->
        <!--</router-link>-->
        <el-button type="primary" v-show="pageType!=='update'" :disabled="running" @click="RunAutomation(ids)">
            <div v-show="!running">执行</div>
            <div v-show="running">执行中</div>
        </el-button>
        <el-button type="primary" v-show="pageType!=='update' && (currentType==='list'||currentType==='monitor') && failRerunShow" :disabled="running" @click="RunAutomation(failIds)">
          <div v-show="!running">失败重跑</div>
          <div v-show="running">执行中</div>
        </el-button>
        <!--<el-input type="textarea" :rows="1" v-model.trim="automation.params"></el-input>-->
        <el-select v-model="env"  v-show="pageType!=='update'" placeholder="执行环境">
            <el-option v-for="(item,index) in EnvList" :key="index+''" :label="item.name" :value="item.name"></el-option>
        </el-select>
        <el-select v-model="data"  multiple v-show="pageType!=='update'" placeholder="测试数据">
            <el-option v-for="(item,index) in DataList" :key="index+''" :label="item.name" :value="item.name"></el-option>
        </el-select>
        <el-select v-model="result.resulttrace"  v-show="pageType!=='update'" placeholder="执行结果" @change="getResult(result.resulttrace)">
            <el-option v-for="(item,index) in result.ResultList" :style="result_color[item.result]" :key="index+''" :label="item.testTime" :value="item.trace"></el-option>
        </el-select>
        <router-link :to="{ name: '更新自动化步骤', params: {automation_id: this.$route.params.automation_id,type: 'update'}}" style='text-decoration: none;'><el-button v-show="pageType!=='update'" class="return-list" type="primary" style="float: right; margin-right: 15px">修改</el-button></router-link>
        <router-link :to="{ name: '自动化步骤列表', params: {automation_id: this.$route.params.automation_id}}" style='text-decoration: none;'><el-button v-show="pageType==='update'" class="return-list" type="primary" style="float: right; margin-right: 15px">执行</el-button></router-link>
        <el-button v-show="pageType==='update'" class="return-list" type="primary" style="float: right; margin-right: 15px" @click.native="updateAutomation">保存</el-button>
        <el-dialog title="选择可重用步骤" :visible.sync="reuseSteps.visible" :close-on-click-modal="false" >
            <el-row :gutter="10">
                <el-col :span="18">
                    <el-table :data="reuseSteps.list" highlight-current-row v-loading="reuseSteps.loading"
                              style="width: 100%;" :show-header="true" max-height="400" @selection-change="selStepsChange">
                        <el-table-column type="selection" width="55">
                        </el-table-column>
                        <el-table-column prop="name" label="名称" min-width="20%" sortable>
                        </el-table-column>
                        <el-table-column prop="params" label="参数" min-width="50%" sortable>
                        </el-table-column>
                        <el-table-column prop="description" label="描述" min-width="30%" sortable>
                        </el-table-column>
                    </el-table>
                </el-col>
            </el-row>
            <el-col :span="24" class="toolbar">
                <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChangeStep" :current-page.sync="reuseSteps.page" :total="reuseSteps.total" :page-size="20" :page-count="reuseSteps.pages" style="float:right;">
                </el-pagination>
            </el-col>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="reuseSteps.visible = false">取消</el-button>
                <el-button type="primary" @click.native="addReuseSteps">提交</el-button>
            </div>
        </el-dialog>
        <el-dialog title="关联接口" :visible.sync="linkApi.visible" :close-on-click-modal="false" >
            <el-row>
              <el-input v-model.trim="linkApi.name" placeholder="名称,分组" @keyup.enter.native="getApiList"></el-input>
              <!--<el-button type="primary" @click="getAutomationList">查询</el-button>-->
            </el-row>
            <el-row :gutter="10">
                <el-col :span="24">
                    <el-table :data="linkApi.list" highlight-current-row v-loading="linkApi.loading"
                              style="width: 100%;" :show-header="true" max-height="400" @selection-change="selApisChange">
                        <el-table-column type="selection" width="55">
                        </el-table-column>
                        <el-table-column prop="name" label="名称" min-width="20%" sortable>
                        </el-table-column>
                        <el-table-column prop="params" label="参数" min-width="50%" sortable>
                        </el-table-column>
                        <el-table-column prop="description" label="描述" min-width="30%" sortable>
                        </el-table-column>
                    </el-table>
                </el-col>
            </el-row>
            <el-col :span="24" class="toolbar">
                <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChangeApi" :current-page.sync="linkApi.page" :total="linkApi.total" :page-size="20" :page-count="linkApi.pages" style="float:right;">
                </el-pagination>
            </el-col>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="linkApi.visible = false">取消</el-button>
                <el-button type="primary" @click.native="linkApiSubmit" :loading="linkApi.loading">提交</el-button>
            </div>
        </el-dialog>
        <el-dialog title="关联用例" :visible.sync="linkAutomation.visible" :close-on-click-modal="false" >
            <!--<el-col :span="24" style="padding-bottom: 0px;">-->
            <el-row>
              <el-input v-model.trim="linkAutomation.name" placeholder="名称,分组" @keyup.enter.native="getAutomationList"></el-input>
              <!--<el-button type="primary" @click="getAutomationList">查询</el-button>-->
            </el-row>
            <el-row :gutter="10">
                <el-col :span="24">
                    <el-table :data="linkAutomation.list" highlight-current-row v-loading="linkAutomation.loading"
                              style="width: 100%;" :show-header="true" max-height="400" @selection-change="selAutomationsChange">
                        <el-table-column type="selection" width="55">
                        </el-table-column>
                        <el-table-column prop="name" label="名称" min-width="20%" sortable>
                        </el-table-column>
                        <el-table-column prop="description" label="描述" min-width="30%" sortable>
                        </el-table-column>
                    </el-table>
                </el-col>
            </el-row>
            <el-col :span="24" class="toolbar">
                <el-pagination layout="total, prev, pager, next" @current-change="handleCurrentChangeAutomation" :current-page.sync="linkAutomation.page" :total="linkAutomation.total" :page-size="20" :page-count="linkAutomation.pages" style="float:right;">
                </el-pagination>
            </el-col>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="linkAutomation.visible = false">取消</el-button>
                <el-button type="primary" @click.native="linkAutomationSubmit" :loading="linkAutomation.loading">提交</el-button>
            </div>
        </el-dialog>
        <el-form :model="automationForm"  :rules="editFormRules" ref="automationForm" label-width="80px">
            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px">
                <el-row :gutter="10">
                    <el-col :span='8'>
                        <el-form-item label="名称" prop="name">
                            <el-input :disabled="pageType!=='update'" v-model.trim="automationForm.name" auto-complete="off"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span='5'>
                        <el-form-item label="类型" label-width="83px" prop="type">
                            <el-select :disabled="pageType!=='update'" v-model="automationForm.type" placeholder="类型">
                                <el-option v-for="(item,index) in automationType" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span='8'>
                        <el-form-item label="分组" label-width="83px" prop="group">
                            <treeselect :disabled="pageType!=='update'" v-model="automationForm.group" :options="group" placeholder="请选择"/>
                            <!--<SelectTree :options="group" :filter="false" :value="automationForm.group"/>-->
                            <!--<el-select v-model="automationForm.group" placeholder="分组">-->
                                <!--<el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id"></el-option>-->
                            <!--</el-select>-->
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="10">
                    <el-form-item label="参数" prop='params'>
                        <el-input type="textarea" :rows="2" v-model="automationForm.params"></el-input>
                    </el-form-item>
                </el-row>
                <el-row :gutter="10">
                    <el-form-item label="描述" prop='description'>
                        <el-input :disabled="pageType!=='update'" type="textarea" :rows="2" v-model="automationForm.description"></el-input>
                    </el-form-item>
                </el-row>
            </div>
        </el-form>
        <el-table class="steptable" row-key="index" :data="StepList" :row-class-name="getStepRowClass" @selection-change="selsChange" highlight-current-row v-loading="listLoading" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
            </el-table-column>
            <el-table-column type="index" min-width="5%">
            </el-table-column>
            <el-table-column prop="name" label="名称" min-width="30%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <span v-show="automationForm.type!=='monitor'&&scope.row.type!=='case'&&scope.row.type!=='reuse'" @click="handleEdit(scope.$index, scope.row)" style="font-size: 16px">{{scope.row.name}}</span>
                    <router-link v-show="scope.row.type==='case'||scope.row.type==='reuse'" :to="{ name: '自动化步骤列表', params: {automation_id: scope.row.stepId}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
                    <router-link v-show="automationForm.type==='monitor'" :to="{ name: '基础信息', params: {api_id: scope.row.id}}" style='text-decoration: none;'>{{ scope.row.name }}</router-link>
                </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="30%" show-overflow-tooltip>
                <template slot-scope="scope">
                    <span style="font-size: 16px">{{scope.row.description}}</span>
                </template>
            </el-table-column>
            <!--<el-table-column prop="testtime" label="执行时间" min-width="15%" show-overflow-tooltip>-->
                <!--<template slot-scope="scope">-->
                    <!--<span style="font-size: 16px">{{scope.row.testtime}}</span>-->
                <!--</template>-->
            <!--</el-table-column>-->
            <el-table-column prop="result" label="结果" min-width="10%">
                <template slot-scope="scope">
                    <span v-show="!scope.row.result||scope.row.result==='RUNNING'">未执行</span>
                    <router-link v-if="(scope.row.type==='case'||scope.row.type==='reuse')&&scope.row.result" :to="{ name: '自动化执行详情', params: {project_id: project_id,automation_id: scope.row.stepId,trace:scope.row.trace}}" style='text-decoration: none;'>
                      <span v-show="scope.row.result==='PASS'" style="color: #11b95c;cursor:pointer;">通过</span>
                      <span v-show="scope.row.result==='FAIL'" style="color: #cc0000;cursor:pointer;">失败</span>
                    </router-link>
                    <span v-show="(scope.row.type!=='case'&&scope.row.type!=='reuse')&&scope.row.result==='PASS'" style="color: #11b95c;cursor:pointer;" @click="resultShow(scope.row)">通过</span>
                    <span v-show="(scope.row.type!=='case'&&scope.row.type!=='reuse')&&scope.row.result==='FAIL'" style="color: #cc0000;cursor:pointer;" @click="resultShow(scope.row)">失败</span>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="启用" min-width="10%">
                <template slot-scope="scope">
                    <img v-show="scope.row.status" src="@/assets/icon-yes.svg"/>
                    <img v-show="!scope.row.status" src="@/assets/icon-no.svg"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="30%">
                <template slot-scope="scope">
                  <el-dropdown v-show="pageType==='update'&&(automationForm.type==='case'||automationForm.type==='reuse')">
                    <el-button type="primary" size="small" @click="handleEdit(scope.$index, scope.row)" plain>修改<i class="el-icon-arrow-down el-icon--right"></i></el-button>
                    <el-dropdown-menu slot="dropdown">
                      <el-dropdown-item><el-button type="primary" size="small" @click="handleCopy(scope.$index, scope.row)" plain>复制</el-button></el-dropdown-item>
                      <el-dropdown-item><el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)" plain>{{scope.row.status===false?'启用':'禁用'}}</el-button></el-dropdown-item>
                      <el-dropdown-item><el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)" plain>删除</el-button></el-dropdown-item>
                    </el-dropdown-menu>
                  </el-dropdown>
                  <el-button-group v-show="pageType==='update'">
                    <el-button v-show="automationForm.type==='list'" type="info" size="mini" @click="handleChangeStatus(scope.$index, scope.row)">{{scope.row.status===false?'启用':'禁用'}}</el-button>
                    <el-button v-show="automationForm.type==='monitor'" type="primary" size="mini" @click="handleUnlinkApi(scope.$index, scope.row)">取消关联</el-button>
                    <el-button v-show="automationForm.type==='list'" type="primary" size="mini" @click="handleUnlinkAutomation(scope.$index, scope.row)">取消关联</el-button>
                  </el-button-group>
                </template>
            </el-table-column>
        </el-table>
        <el-button v-show="pageType==='update'" class="return-list" type="primary" style="float: right; margin-right: 15px" :disabled="updateOrderStatus" @click="updateOrder()">
            编辑步骤顺序
        </el-button>
        <el-dialog width="80%" :title="editFormTitle" :visible.sync="editFormVisible" :close-on-click-modal="false" @open="actiontableshow" style="width: 100%;">
            <el-form :model="editForm"  :rules="editFormRules" ref="editForm" label-width="80px">
                <el-form-item label="名称" prop="name">
                    <el-input v-model.trim="editForm.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="类型:" label-width="83px" prop="type">
                    <el-select v-model="editForm.type" placeholder="类型">
                        <el-option v-for="(item,index) in stepType" :key="index+''" :label="item.label" :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="参数" prop='params'>
                    <el-input type="textarea" :rows="3" v-model="editForm.params"></el-input>
                </el-form-item>
                <el-form-item label="描述" prop='description'>
                    <el-input type="textarea" :rows="4" v-model="editForm.description"></el-input>
                </el-form-item>
                <el-form-item label="操作" prop='steps'><el-button size="mini" title="添加" class="el-icon-plus" @click="addCommand(0)"></el-button>
                    <!--<el-input type="textarea" :rows="4" v-model.trim="editForm.steps"></el-input>-->
                    <el-table id="actiontable" class="actiontable" row-key="name" :data="editForm.steps" highlight-current-row>
                            <el-table-column type="index" min-width="5%">
                            </el-table-column>
                            <el-table-column prop="name" label="名称" min-width="30%">
                                <template slot-scope="scope">
                                    <el-select style="width:100%" placeholder="步骤名称" filterable v-model="scope.row.name" @change="changeCommand(scope.$index)">
                                        <el-option v-for="(item,key) in commands" :key="key+''" :label="item.alias" :value="item.name"></el-option>
                                    </el-select>
                                    <!--<el-input class="selectInput" v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入内容"></el-input>-->
                                </template>
                            </el-table-column>
                            <el-table-column prop="params" label="参数" min-width="35%">
                                <template slot-scope="scope">
                                    <el-input type="textarea" :rows="2" v-model.trim="scope.row.params" :value="scope.row.params" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="描述" min-width="20%">
                                <template slot-scope="scope">
                                    <el-input type="textarea" :rows="2" v-model.trim="scope.row.description" :value="scope.row.description" placeholder="请输入内容"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="20%">
                                <template slot-scope="scope">
                                      <el-button-group>
                                        <el-button size="mini" title="删除" class="el-icon-minus" @click="delCommand(scope.$index)"></el-button>
                                        <el-button size="mini" title="添加" class="el-icon-plus" @click="addCommand(scope.$index)"></el-button>
                                        <router-link v-show="scope.row.type==='api'" :to="{ name: '基础信息', params: {api_id: scope.row.actionId}}" style='text-decoration: none;'><el-button title="查看接口" size="mini" class="el-icon-view"></el-button></router-link>
                                        <router-link v-show="scope.row.type==='automation'" :to="{ name: '自动化步骤列表', params: {automation_id: scope.row.actionId}}" style='text-decoration: none;'><el-button title="查看用例" size="mini" class="el-icon-view"></el-button></router-link>
                                      </el-button-group>
                                    <!--<el-button size="mini" class="el-icon-plus" @click="addCommand(scope.$index)"></el-button>-->
                                </template>
                            </el-table-column>
                        </el-table>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button v-show="pageType==='update'" type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
        </el-dialog>

        <el-dialog width="60%" :title="StepResultName" :visible.sync="AutomationResult" :close-on-click-modal="false">
            <el-table :data="StepResultDetails" max-height="400" highlight-current-row v-loading="listLoading" style="width: 100%;">
                <el-table-column type="expand">
                    <template slot-scope="props">
                        <el-form label-position="left" inline class="demo-table-expand">

                            <el-table v-show="props.row.type==='automation'" :data="props.row.details" highlight-current-row v-loading="listLoading" style="width: 100%;">
                                <!--<el-table-column type="expand">-->
                                    <!--<template slot-scope="props">-->
                                        <!--<el-form label-position="left" inline class="demo-table-expand">-->
                                            <!--<el-row v-show="props.row.type==='api'" :gutter="10">-->
                                                <!--<el-form-item label="接口地址： ">-->
                                                    <!--<span>{{ props.row.url }}</span>-->
                                                <!--</el-form-item>-->
                                            <!--</el-row>-->
                                            <!--<el-row v-show="props.row.type==='api'" :gutter="10">-->
                                                <!--<el-form-item label="请求方式： ">-->
                                                    <!--<span>{{ props.row.method }}</span>-->
                                                <!--</el-form-item>-->
                                            <!--</el-row>-->
                                            <!--<el-row v-show="props.row.type==='api'" :gutter="10">-->
                                                <!--<el-form-item label="请求参数： ">-->
                                                    <!--<span style="word-break: break-all;overflow:auto;overflow-x:hidden">{{ props.row.data }}</span>-->
                                                <!--</el-form-item>-->
                                            <!--</el-row>-->
                                            <!--<el-row :gutter="10">-->
                                                <!--<el-form-item label="返回结果： ">-->
                                                    <!--<span>-->
                                                        <!--&lt;!&ndash;<pre style="word-break: break-all;overflow:auto;overflow-x:hidden">&ndash;&gt;-->
                                                          <!--<code v-show="props.row.type!=='api'" >{{ props.row.result }}</code>-->
                                                        <!--&lt;!&ndash;</pre>&ndash;&gt;-->
                                                        <!--<json-viewer v-show="props.row.type==='api'" :value="props.row.result" :expand-depth=5 boxed copyable></json-viewer>-->
                                                    <!--</span>-->
                                                <!--</el-form-item>-->
                                            <!--</el-row>-->
                                        <!--</el-form>-->
                                    <!--</template>-->
                                <!--</el-table-column>-->
                                <el-table-column type="index" width="55">
                                </el-table-column>
                                <el-table-column prop="name" label="名称" min-width="20%" show-overflow-tooltip>
                                    <template slot-scope="scope">
                                        <span style="font-size: 16px">{{scope.row.name}}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="result" label="结果" min-width="40%" show-overflow-tooltip>
                                    <template slot-scope="scope">
                                        <span style="font-size: 16px">{{scope.row.result}}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="status" label="状态" min-width="10%" show-overflow-tooltip>
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
                            <el-row v-show="props.row.type!=='automation'" :gutter="10">
                                <el-form-item label="返回结果： ">
                                    <span>
                                        <!--<pre style="word-break: break-all;overflow:auto;overflow-x:hidden">-->
                                          <code v-show="props.row.type!=='api'" >{{ props.row.result }}</code>
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
                <el-table-column prop="result" label="结果" min-width="40%" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <span style="font-size: 16px">{{scope.row.result}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="status" label="状态" min-width="10%" show-overflow-tooltip>
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
        </el-dialog>
    </section>
</template>

<script>
    import Treeselect from '@riophae/vue-treeselect'
    // import the styles
    import '@riophae/vue-treeselect/dist/vue-treeselect.css'
    import { test,getProjectConfig,runAutomation } from '../../../api/api'
//    import SelectTree from "../../../components/treeSelect.vue";
    import Sortable from 'sortablejs'
    import $ from 'jquery'
    import moment from "moment"
    import axios from "axios"
    export default {
        components: {
          Treeselect
        },
//        inject: ["reload"],
        data() {
            return{
                automationType: [{value: 'case', label: '普通用例'},
                     {value: 'reuse', label: '可复用用例'},
                    {value: 'list', label: '用例集'},
                    {value: 'data', label: '数据用例'},
                    {value: 'monitor', label: '接口监控'},
                ],
                currentType: "",
                result_color: {"PASS":"color:green","FAIL":"color:red"},
                stepType: [{value: 'normal', label: '普通'},
                    {value: 'project', label: '项目'},
                    {value: 'global', label: '全局'}],
                project: "",
                automation: "",
                StepList: [],
                stepIds: [],
                failIds: [],
                failRerunShow: false,
                ids: [],
                listLoading: false,
                running: false,
                updateOrderStatus: false,
                searchName: "",
                total: 0,
                page: 1,
                env: '',
                data: '',
                group: [],
                EnvList: [],
                DataList: [],
                commands: {},
                groupData: [],
                sels: [],//列表选中列
                AutomationResult: false,
                StepResultDetails: [],
                StepResultName: "",
                result: {},
                StepListLen: "",
                StepListIndex: 0,
                activeIndex: "",

                editFormVisible: false,//编辑界面是否显示
                editFormTitle: "",
                editLoading: false,
                editFormRules: {
                    name: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 1024, message: '长度在 1 到 1024 个字符', trigger: 'blur' }
                    ],
                    type: [
                        { required: true, message: '请选择类型', trigger: 'blur'}
                    ],
                    description: [
                        { required: false, message: '请输入描述', trigger: 'blur' },
                        { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
                    ]
                },
                //编辑界面数据
                editForm: {
                    name: '',
                    params: '{}',
                    steps: [],
                    description: '',
                    type: 'normal',
                    order: ''
                },
                //新增界面数据
                addForm: {
                    name: '',
                    params: '{}',
                    steps: [{"type":"","name":"","actionId":0,"params":"{}","description":"","disable":"False"}],
                    description: '',
                    type: 'normal',
                    order: ''
                },
                automationForm: {
                    name: '',
                    type: '',
                    group: null,
                    params: '{}',
                    description: '',
                    id: ''
                },
                linkAutomation: {
                    visible: false,
                    loading: false,
                    list: [],
                    page: 1,
                    pages: 0,
                    total: 0,
                    selAutomations: []
                },
                linkApi: {
                    visible: false,
                    loading: false,
                    list: [],
                    page: 1,
                    pages: 0,
                    total: 0,
                    selApis: []
                },
                reuseSteps: {
                    visible: false,
                    loading: false,
                    list: [],
                    total: 0,
                    page: 1,
                    pages: 0,
                    selSteps: []
                },
                result: {
                    resulttrace: '',
                    ResultList: []
                },
                getResultTimer: '',
                getResultTimes: 0,
                project_id: this.$route.params.project_id,
                pageType: '',
            }
        },
        methods: {
            selsChange: function (sels) {
                if(this.automationForm.type=="monitor"){
                    this.ids = sels.map(item => item.id);
                }else{
                    this.ids = sels.map(item => item.stepId);
                }
            },
            getStepRowClass({ row }) {
              if (!row.status) {
                return 'disable-step';
              }
              return '';
            },
            handleSelect(key, keyPath) {
                this.activeIndex = key;
                console.log(this.activeIndex)
            },
            // 获取用例分组
            getAutomationGroupAndInfo() {
                let self = this;
                axios.get(test+"/api/automation/group", {params:{project_id:this.$route.params.project_id}}).then(response => {
                    if (response.data.code === '999999') {
                        self.group = response.data.data;
                    }else{
                        self.$message.error({
                            message: response.data.msg,
                            center: true,
                        })
                    }
                    self.getAutomationStepList();
                }).catch(error=>{

                });
            },
            getAutomationStepList() {
                this.listLoading = true;
                let self = this;
                let params={ project_id: this.$route.params.project_id,
                    page: self.page,
                    name: self.searchName,
                    automation_id: this.$route.params.automation_id
                };
                axios.get(test+"/api/automation/step_list", {params:params}).then(response => {
                    self.listLoading = false;
                    self.stepIds=[];
                    if (response.data.code === '999999') {
                        self.currentType=response.data.data.automation.type;
                        self.StepList = [];
                        self.result.ResultList = [];
                        self.automationForm=response.data.data.automation;
                        self.automationForm.group=response.data.data.automation.group;
                        response.data.data.steps.forEach((item) =>{
                            item.result = false;
                            self.StepList.push(item);
                            if(response.data.data.automation.type=='list'){
                                self.stepIds.push(item.stepId);
                            }else if(response.data.data.automation.type=='monitor'){
                                self.stepIds.push(item.id);
                            }
                        });
                        response.data.data.results.forEach((item) =>{
                            self.result.ResultList.push(item);
                        });
                        // self.ApiList = data.data.data
                    }else {
                        self.$message.error({
                            message: response.data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{
                });
            },
            getCommandList() {
                this.listLoading = true;
                let self = this;
                axios.get(test+"/api/automation/command_list", {params:{project_id:this.$route.params.project_id,automation_id: this.$route.params.automation_id}}).then(response => {
                    self.listLoading = false;
                    if (response.data.code === '999999') {
                        self.commands = {};
                        response.data.data.data.forEach((item) =>{
                            self.commands[item.name]=item;
                        });
                        // self.ApiList = data.data.data
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
            getResult(trace) {
                let self = this;
                let params={ project_id: this.$route.params.project_id,
                    automation_id: this.$route.params.automation_id,
                    trace: trace
                };
                if(!self.running) {
                  self.StepList.forEach((item, index) => {
                    item.testtime = "";
                    item.result = null;
                    item.details = [];
                  });
                };
                axios.get(test+"/api/automation/getresult", {params:params}).then(response => {
                    self.getResultTimes++;
                    if (response.data.code === '999999') {
                        self.failIds=[]
                        response.data.data.details.forEach((item,index) =>{
                            self.StepList.forEach((step,stepIndex)=>{
                                if(((item.type=="step"||item.type=="automation")&&item["id"]==step["stepId"])||((item.type=="api")&&item["id"]==step["id"])){
                                  step.result=item.status;
                                  step.testtime=item.testtime;
                                  step.details=item.details;
                                  step.trace=item.trace;
                                  if(item.status=="FAIL"&&(item["type"]=="api"||item["type"]=="automation")){
                                      self.failIds.push(item["id"]);
                                  }
                                }
                            })
                        });
                        if(response.data.data.status!="RUNNING"||self.getResultTimes>100){
                            self.getResultTimes=0;
                            clearInterval(self.getResultTimer);
                            self.running=false;
                            if(self.failIds.length>0){
                                self.failRerunShow=true;
                            }else{
                                self.failRerunShow=false;
                            }
                        }
                    }else{
                        self.$message.error({
                            message: '获取失败',
                            center: true,
                        })
                    }
                }).catch(error=>{

                });
            },
            StepTotal() {
                this.StepListLen = this.StepList.length;
            },
            handleLinkApi: function () {
                this.linkApi.visible = true;
                this.linkApi.page=1;
                this.getApiList();
            },
            getApiList(){
                let self=this;
                self.linkApi.loading = true;
                let params={
                    project_id: this.$route.params.project_id,
                    page: self.linkApi.page,
                    name: self.linkApi.name,
                    exclude: JSON.stringify(self.stepIds),
                };
                axios.get(test+"/api/api/api_list", {params:params}).then(response => {
                    self.linkApi.loading = false;
                    if (response.data.code === '999999') {
                        self.linkApi.list = response.data.data.data;
                        self.linkApi.total = response.data.data.total;
                        self.linkApi.pages = response.data.data.pages;
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
            //取消关联
            handleUnlinkApi: function (index, row) {
                this.$confirm('确认取消关联接口[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    let self = this;
                    let params=JSON.stringify({ project_id: Number(this.$route.params.project_id), automation_id: Number(this.$route.params.automation_id),ids: [row.id] });
                    let headers={
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/automation/unlink_api", params,{headers:headers}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '取消关联成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        self.getAutomationStepList();
                    }).catch(error=>{

                    });
                }).catch(() => {
                });
            },
            //取消关联
            handleUnlinkAutomation: function (index, row) {
                this.$confirm('确认取消关联用例[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params=JSON.stringify({ project_id: Number(this.$route.params.project_id), automation_id: Number(this.$route.params.automation_id),ids: [row.stepId] });
                    let headers={
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/automation/unlink_automation", params,{headers:headers}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '取消关联成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        self.getAutomationStepList();
                    }).catch(error=>{

                    });
                }).catch(() => {
                });
            },
            handleChangeStatus: function(index, row) {
                let self = this;
                this.listLoading = true;
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                let params = {project_id: Number(this.$route.params.project_id),id: row.id,status:!row.status,type:row.type};
                let successMsg='禁用成功';
                if(!row.status){
                    successMsg='启用成功';
                }
                axios.post(test+"/api/automation/stepstatus_update", params,{headers:headers}).then(response => {
                    self.listLoading = false;
                    if (response.data.code === '999999') {
                        self.$message({
                            message: successMsg,
                            center: true,
                            type: 'success'
                        })
                        row.status = !row.status;
                    }else {
                        self.$message.error({
                            message: response.data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{
                });
            },
            linkApiSubmit: function () {
                let ids = this.linkApi.selApis.map(item => item.id);
                let self = this;
                this.$confirm('确认关联选中的接口吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    let params=JSON.stringify({
                        project_id: Number(this.$route.params.project_id),
                        automation_id: Number(this.$route.params.automation_id),
                        ids: ids
                    });
                    let headers={
                        "Content-Type": "application/json",
                        Authorization: 'Token '+sessionStorage.getItem('token')
                    };
                    axios.post(test+"/api/automation/link_api", params,{headers:headers}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '关联成功',
                                center: true,
                                type: 'success'
                            })
                        }else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        self.linkApi.visible = false;
                        self.getAutomationStepList()
                    }).catch(error=>{
                    });
                }).catch(() => {

                });
            },
            getAutomationList(){
                let self=this;
                self.linkAutomation.loading = true;
                let params={
                    project_id: this.$route.params.project_id,
                    type: "case",
                    page: self.linkAutomation.page,
                    exclude: JSON.stringify(self.stepIds),
                };
                if(this.linkAutomation.name!=""){
                    params["name"]=this.linkAutomation.name;
                }
                let headers={Authorization: 'Token '+sessionStorage.getItem('token')};
                axios.get(test+"/api/automation/automation_list", {params:params,headers:headers}).then(response => {
                    self.linkAutomation.loading = false;
                    if (response.data.code === '999999') {
                        self.linkAutomation.list = response.data.data.data;
                        self.linkAutomation.total = response.data.data.total;
                        self.linkAutomation.pages = response.data.data.pages;
                    }else{
                        self.$message.error({
                            message: response.data.msg,
                            center: true,
                        })
                    }
                }).catch(error=>{
                });
            },
            //显示新增界面
            handleLinkAutomation: function () {
                this.linkAutomation.visible = true;
                this.linkAutomation.page = 1;
                this.getAutomationList();
            },
            linkAutomationSubmit: function () {
                let ids = this.linkAutomation.selAutomations.map(item => item.id);
                let self = this;
                this.$confirm('确认关联选中的用例吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    //NProgress.start();
                    let params=JSON.stringify({
                        project_id: Number(this.$route.params.project_id),
                        automation_id: Number(this.$route.params.automation_id),
                        ids: ids
                    });
                    let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                    axios.post(test+"/api/automation/link_automation", params,{headers:headers}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '关联成功',
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
                        self.linkAutomation.visible = false;
                        self.getAutomationStepList()
                    }).catch(error=>{
                    });
                }).catch(() => {

                });
            },
            RunAutomation(ids) {
                if (this.env) {
                    let self = this;
                    let data={
                            project_id: Number(this.$route.params.project_id),
                            automation_id: Number(this.$route.params.automation_id),
                            params: this.automationForm.params,
                            env: this.env,
                            data: this.data,
                    };
                    if(ids&&ids.length>0){
                        data["ids"]=ids;
                    }
                    let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+sessionStorage.getItem('token')
                            };
                    runAutomation(header,data).then(data => {
                        if (data.code === '999999') {
                            self.$message({
                                message: '开始执行',
                                center: true,
                                type: "success",
                            }),
                            self.StepList.forEach((item,index) =>{
                                item.testtime="";
                                item.result=null;
                                item.details=[];
                            });
                            self.result.ResultList.splice(0,0,{"testTime":data.data.testtime,"trace":data.data.trace,"result":data.data.status});
                            if(data.data.status=="RUNNING"){
                                self.running=true;
                                self.getResultTimes=0;
                                self.getResultTimer = setInterval(() =>{
//                                        self.getAutomationStepList();
                                    self.getResult(data.data.trace);
                                }, 3000);
                            }
                        }else {
                            self.$message.error({
                                message: data.msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    this.$message({
                        message: '请选择测试环境',
                        center: true,
                        type: 'warning'
                    })
                }
            },
            handleDel(index, row){
                this.$confirm('确认删除步骤[' + row.name + ']吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    let self = this;
                    let params=JSON.stringify({
                            project_id: Number(this.$route.params.project_id),
                            automation_id: Number(this.$route.params.automation_id),
                            ids: [{"order":index+1,"id":row.stepId}] });
                    let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                    axios.post(test+"/api/automation/del_step", params,{headers:headers}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: response.data.msg,
                                center: true,
                            })
                        }
                        self.getAutomationStepList();
                    }).catch(error=>{
                    });
                }).catch(() => {
                });
            },
            resultShow(row) {
                this.AutomationResult=true;
                this.StepResultDetails=row.details;
                this.StepResultName=row.name;
            },
            handleCurrentChangeStep(val) {
                this.reuseSteps.page = val;
                this.getReuseStepList();
            },
            handleCurrentChangeAutomation(val) {
                this.linkAutomation.page = val;
                this.getAutomationList();
            },
            handleCurrentChangeApi(val) {
                this.linkApi.page = val;
                this.getApiList();
            },
            selStepsChange(sels){
                this.reuseSteps.selSteps = sels;
            },
            selApisChange(sels){
                this.linkApi.selApis = sels;
            },
            selAutomationsChange(sels){
                this.linkAutomation.selAutomations = sels;
            },
            addReuseSteps: function () {
                let ids = this.reuseSteps.selSteps.map(item => item.id);
                let self = this;
                this.$confirm('确认添加选中的步骤吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    self.listLoading = true;
                    let params=JSON.stringify({
                        project_id: Number(this.$route.params.project_id),
                        automation_id: Number(this.$route.params.automation_id),
                        ids: ids
                    });
                    let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                    axios.post(test+"/api/automation/add_reuse_steps", params,{headers:headers}).then(response => {
                        self.listLoading = false;
                        if (response.data.code === '999999') {
                            self.$message({
                                message: '添加成功',
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
                        self.reuseSteps.visible = false;
                        self.getAutomationStepList();
                    }).catch(error=>{
                    });
                }).catch(() => {

                });
            },
            getEnv() {
                let self = this;
                let headers = {
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                getProjectConfig(headers, {project_id: self.$route.params.project_id,page: self.page, name: "", type: "env"}).then(data => {
                    if (data.code === '999999') {
                        self.EnvList=[];
                        data.data.data.forEach((item) => {
                            if (item.status) {
                                self.EnvList.push(item);
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
            getData() {
                let self = this;
                let headers = {
                    Authorization: 'Token '+sessionStorage.getItem('token')
                };
                getProjectConfig(headers, {project_id: this.$route.params.project_id,page: self.page, name: "", type: "data"}).then(data => {
                    if (data.code === '999999') {
                        self.DataList=[];
                        data.data.data.forEach((item) => {
                            if (item.status) {
                                self.DataList.push(item);
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
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                if(this.pageType=='update'){
                    this.editFormTitle = "修改步骤";
                }else{
                    this.editFormTitle = "查看步骤";
                }
                this.editForm = {"id":row.stepId,"name":row.name,"type":row.type,"params":row.params,"steps":JSON.parse(row.steps),"description":row.description};
                this.editForm.order = index+1;
            },
            actiontableshow: function(){
                const _this = this;
                let tbody = document.querySelector('.actiontable .el-table__body-wrapper tbody');
                if(tbody!=null){
                    Sortable.create(tbody, {
                      onEnd({ newIndex, oldIndex }) {
                        const currRow = _this.editForm.steps.splice(oldIndex, 1)[0];
                        _this.editForm.steps.splice(newIndex, 0, currRow);
                      }
                    });
                }
            },
            handleCopy: function (index, row) {
                this.editFormVisible = true;
                this.editFormTitle = "复制步骤";
                this.editForm = {"name":row.name,"type":row.type,"params":row.params,"steps":JSON.parse(row.steps),"description":row.description};
                this.editForm.order = this.StepList.length+1;
            },
            //显示新增界面
            handleAdd: function () {
                this.editFormVisible = true;
                this.editFormTitle = "添加步骤";
                this.editForm=this.addForm;
                this.editForm.order=this.StepList.length+1;
            },
            //显示新增界面
            handleAddReuse: function () {
                this.reuseSteps.visible = true;
                this.reuseSteps.page=1;
                this.getReuseStepList();
            },
            getReuseStepList() {
                let self=this;
                let params={project_id: this.$route.params.project_id,page: self.reuseSteps.page};
                let headers={Authorization:'Token '+sessionStorage.getItem('token')};
                self.reuseSteps.loading = true;
                axios.get(test+"/api/automation/step_list", {params:params,headers:headers}).then(response => {
                    self.reuseSteps.loading = false;
                    if (response.data.code === '999999') {
                        self.reuseSteps.list = response.data.data.data;
                        self.reuseSteps.total = response.data.data.total;
                        self.reuseSteps.pages = response.data.data.pages;
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
            // 修改用例
            editSubmit: function () {
                if(this.editForm.id==null){
                    this.addSubmit();
                }else{
                    let self = this;
                    let steps=this.editForm.steps;
                    if(steps.length==1&&steps[0]["name"]==""){
                        steps=[];
                    }
                    this.$refs.editForm.validate((valid) => {
                        if (valid) {
                            this.$confirm('确认提交吗？', '提示', {}).then(() => {
                                self.editLoading = true;
                                //NProgress.start();
                                let params = JSON.stringify({
                                    project_id: Number(this.$route.params.project_id),
                                    automation_id: Number(this.$route.params.automation_id),
                                    id: Number(self.editForm.id),
                                    type: self.editForm.type,
                                    name: self.editForm.name,
                                    params: self.editForm.params,
                                    steps: JSON.stringify(steps),
                                    description: self.editForm.description,
                                    order: self.editForm.order
                                });
                                let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                                axios.post(test+"/api/automation/update_step", params,{headers:headers}).then(response => {
                                    self.editLoading = false;
                                    if (response.data.code === '999999') {
                                        self.$message({
                                            message: '修改成功',
                                            center: true,
                                            type: 'success'
                                        });
                                        self.$refs['editForm'].resetFields();
                                        self.editFormVisible = false;
                                        self.getAutomationStepList()
                                    } else if (response.data.code === '999997'){
                                        self.$message.error({
                                            message: response.data.msg,
                                            center: true,
                                        })
                                    } else {
                                        self.$message.error({
                                            message: response.data.msg,
                                            center: true,
                                        })
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
                        let steps=this.editForm.steps;
                        if(steps.length==1&&steps[0]["name"]==""){
                            steps=[];
                        }
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = JSON.stringify({
                                project_id: Number(this.$route.params.project_id),
                                type: this.editForm.type,
                                automation_id: Number(this.$route.params.automation_id),
                                name: self.editForm.name,
                                params: self.editForm.params,
                                steps: JSON.stringify(steps),
                                description: self.editForm.description,
                                order: self.editForm.order
                            });
                            let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                            axios.post(test+"/api/automation/add_step", params,{headers:headers}).then(response => {
                                self.editLoading = false;
                                if (response.data.code === '999999') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
                                    self.getAutomationStepList()
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
                                    self.getAutomationStepList()
                                }
                            }).catch(error=>{
                            });
                        }).catch(() => {});
                    }
                });
            },
            // 修改用例
            updateAutomation: function () {
                let self = this;
                this.$refs.automationForm.validate((valid) => {
                    if (valid) {
//                        this.$confirm('确认保存吗？', '提示', {}).then(() => {
                            let orders=[];
                            this.StepList.forEach((item) => {
                                orders.push(item["id"]);
                            })
                            let params = JSON.stringify({
                                project_id: Number(this.$route.params.project_id),
                                id: Number(self.automationForm.id),
                                type: self.automationForm.type,
                                name: self.automationForm.name,
                                params: self.automationForm.params,
                                group_id: Number(this.automationForm.group),
                                description: self.automationForm.description,
                                orders:orders
                            });
                            let headers={"Content-Type": "application/json",Authorization: 'Token '+sessionStorage.getItem('token')};
                            axios.post(test+"/api/automation/update_automation", params,{headers:headers}).then(response => {
                                if (response.data.code === '999999') {
                                    self.$message({
                                        message: '保存成功',
                                        center: true,
                                        type: 'success'
                                    });
                                } else {
                                    self.$message.error({
                                        message: response.data.msg,
                                        center: true,
                                    })
                                }
                            }).catch(error=>{
                            });
//                        }).catch(() => {});
                    }
                });
            },
            addCommand(index) {
                this.editForm.steps.splice(index+1,0,{"type":"","name":"","actionId":0,"params":"{}","description":"","disable":"False"})
            },
            delCommand(index) {
                this.editForm.steps.splice(index, 1);
            },
            changeCommand(index) {
                let command=this.commands[this.editForm.steps[index].name];
                this.editForm.steps[index].name=command.name;
                this.editForm.steps[index].type=command.type;
                this.editForm.steps[index].actionId=command.actionId;
                this.editForm.steps[index].params=command.value;
                this.editForm.steps[index].description=command.desc;
            },
            rowDrop() {
                try{
                    const tbody = document.querySelector('.steptable .el-table__body-wrapper tbody');
                    const _this = this;
                    Sortable.create(tbody, {
                      onEnd({ newIndex, oldIndex }) {
                        const currRow = _this.StepList.splice(oldIndex, 1)[0];
                        _this.StepList.splice(newIndex, 0, currRow);
                      }
                    });
                }catch(err){
                    alert(err);
                }
            },
            updateOrder(){
                if(this.pageType=='update')this.rowDrop();
                this.updateOrderStatus=true;
            },
            init(){
                this.pageType=this.$route.params.type;
                this.getAutomationGroupAndInfo();
                if(this.pageType=='update'){
                    this.getCommandList();
                }else{
                    this.getEnv();
                    this.getData();
                }
            },
        },
        mounted() {
            this.init();
        },
        watch: {
            '$route' (to, from) { //监听路由是否变化
              if(to.query!= from.query){
                  this.reload();
                  if(this.pageType=='update')this.rowDrop();
//                 this.$router.go(0)
              }
            }
        },
    }
</script>

<style lang="scss" scoped>
    .return-list {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }
    .HttpStatus {
        border-radius: 25px;
        padding: 10px;
        box-sizing: border-box;
        color: #fff;
        font-size: 15px;
        background-color: #409eff;
        text-align: center;
        margin-right: 10px;
    }
    .resultStyle{
        margin-left: 2%;
        margin-top: 10px;
    }
    .lin{
        left: 2%;
        border: 1px solid #e6e6e6;
        width: 90%;
        position: relative
    }
    .disable-step{
        opacity:0.5;
    }
</style>
