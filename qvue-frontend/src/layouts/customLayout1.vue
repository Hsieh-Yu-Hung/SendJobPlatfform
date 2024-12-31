<template>
  <q-layout view="hHh lpR lFf">

    <q-header elevated class="bg-indigo-4 text-white">
      <q-toolbar>

        <!-- 可調整： 左上角選單按鈕 -->
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <!-- 可調整： 標題 -->
        <q-toolbar-title>

          <!--標題內容-->
          <q-chip color="indigo-5" text-color="white">
            <q-avatar>
              <img src="~assets/tool_icon.png">
            </q-avatar>
            <span class="text-h6 text-uppercase">Sent Job Platform</span>
          </q-chip>

        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" overlay behavior="desktop" elevated>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    const leftDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
}
</script>
