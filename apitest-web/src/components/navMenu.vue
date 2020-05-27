<template>
 <div class="navMenu">

  <template v-for="navMenu in navMenus">
   <el-menu-item v-if="!navMenu.children"
          :key="navMenu.id" :data="navMenu" :index="navMenu.id" :route="navMenu.value">
    <!--<i :class="navMenu.entity.icon"></i>-->
    <!--<span slot="title">{{navMenu.entity.alias}}</span>-->
     <template slot="title">{{navMenu.label}}
          <el-dropdown trigger="hover" class="editGroup" style="margin-right:10%">
              <i class="el-icon-more"></i>
              <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click.native="handleAdd(navMenu.id)">新增</el-dropdown-item>
                  <el-dropdown-item @click.native="handleEdit(navMenu.id, navMenu.label)">修改</el-dropdown-item>
                  <el-dropdown-item @click.native="handleDel(navMenu.id)">删除</el-dropdown-item>
              </el-dropdown-menu>
          </el-dropdown>
      </template>
   </el-menu-item>

   <el-submenu v-if="navMenu.children"
         :key="navMenu.id" :data="navMenu" :index="navMenu.id" :route="navMenu.value">
    <template slot="title">
      <router-link :to="navMenu.value" style="text-decoration:none;">
      <span>{{navMenu.label}}</span>
      </router-link>
     <!--<i :class="navMenu.entity.icon"></i>-->
      <el-dropdown trigger="hover" class="editGroup" style="margin-right:10%">
              <i class="el-icon-more"></i>
              <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click.native="handleAdd(navMenu.id)">新增</el-dropdown-item>
                  <el-dropdown-item @click.native="handleEdit(navMenu.id, navMenu.label)">修改</el-dropdown-item>
                  <el-dropdown-item @click.native="handleDel(navMenu.id)">删除</el-dropdown-item>
              </el-dropdown-menu>
          </el-dropdown>
    </template>
    <NavMenu :navMenus="navMenu.children" @handleAdd="handleAdd" @handleEdit="handleEdit" @handleDel="handleDel"></NavMenu>
   </el-submenu>
  </template>

 </div>
</template>

<script>
 export default {
  name: 'NavMenu',
  props: ['navMenus'],
  data() {
   return {}
  },
  methods: {
      handleAdd(id){
          this.$emit('handleAdd',id);
      },
      handleEdit(id,name){
          this.$emit('handleEdit',id,name);
      },
      handleDel(id){
          this.$emit('handleDel',id);
      }
  }
 }
</script>

<style scoped>

</style>
