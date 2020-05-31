<template>
  <div class="app-container documentation-container">
    <a class="document-btn" target="_blank" href="https://github.com/willhuang1206/apitest/wiki">文档</a>
    <a class="document-btn" target="_blank" href="https://github.com/willhuang1206/apitest">Github</a>
  </div>
</template>

<script>
export default {
  name: 'Documentation',
}
</script>

<style lang="scss" scoped>
.documentation-container {
  margin: 50px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;

  .document-btn {
    flex-shrink: 0;
    display: block;
    cursor: pointer;
    background: black;
    color: white;
    height: 60px;
    width: 200px;
    margin-bottom: 16px;
    line-height: 60px;
    font-size: 20px;
    text-align: center;
  }
}
</style>
