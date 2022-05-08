<script setup lang="ts">
import { ref } from "vue"
import hljs from 'highlight.js';

const result = ref(0)
const exp = ref("")
const vexp= ref("")

function calc(exp: string): number {
  
  type idxResult = { i: number, ret : string }

  const exec_calc = (exp: string): number => {
    var nums: number[] = []
    var ops: string[] = []
    var ret = 0
    var start = 0
    for (var i = 0; i < exp.length; i++) {
      var e = exp[i]
      if ("012345689".indexOf(e) < 0) {
        nums.push(Number(exp.slice(start, i)))
        ops.push(e)
        start = i + 1
      }
    }
    nums.push(Number(exp.slice(start)))
    
    var vst: number[] = []
    var ost: ((x: number, y: number) => number)[] = []
      
    const calcst = () => {
      if (ost.length > 0) {
        var opf = ost.pop()!
        var v2 = vst.pop()!
        var v1 = vst.pop()!
        vst.push(opf(v1, v2))
      }
    }
    //it = iter(nums)
    var it = 0
    vst.push(nums[it++])

    // for op in ops[1:]:
    for (var i = 0; i < ops.length; i++) {
        var op = ops[i]
        if (op == '+') {
            calcst()
            vst.push(nums[it++])
            ost.push((x, y) => x + y)
        } else if (op == '-') {
            calcst()
            vst.push(nums[it++])
            ost.push((x, y) => x - y)          
        } else if (op == '*') {
            vst.push(nums[it++])
            ost.push((x, y) => x * y)
            calcst()
        }
    }
    calcst()
    ret = vst[0]
    return ret
  }
  const parentheses = (exp: string): idxResult => {
    var buf = ''
    var i = 0
    for (i = 0; i < exp.length; i++) {
      if (exp[i] == '(') {
        var { i: i2, ret: v } = parentheses(exp.slice(i+1))
        i = i + 1 + i2
        buf += v 
      } else if (exp[i] == ')') {
        break
      } else {
        buf += exp[i]
      }
    }
    return { i: i, ret: String(exec_calc(buf))};
  }
  var { i: _, ret: ret} = parentheses(exp)
  return Number(ret)
}

function onInput(e: any) {
  exp.value = e.target.value
  vexp.value = hljs.highlight(e.target.value, {language: 'javascript'}).value

  result.value = calc(e.target.value)

  //var code = document.getElementById("calcexp")!
  //hljs.highlightAll()
  //hljs.highlightElement(code)
}
</script>

<template>
  <div class="input">
    <input :value="exp" @input="onInput" placeholder="Type here">
    <p v-html="vexp" /><p>={{ result }}</p>
  </div>
</template>

<style scoped>

</style>
