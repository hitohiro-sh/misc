<script setup lang="ts">
import { ref } from "vue"
import hljs from 'highlight.js';

const vexp= ref("")

function onFileSelectionChanged(e: any) {
  const fr=new FileReader();

  fr.onload=function(){
      vexp.value = '<pre><code>'+
        hljs.highlight(fr.result!.toString(), {language: 'python'}).value
        +'</code></pre>'
  }
    
  fr.readAsText(e.target.files[0]);
}
</script>

<template>
  <div class="input">
    <input type="file"  @change="onFileSelectionChanged">
    <p v-html="vexp" />
  </div>
</template>

<style scoped>

</style>
