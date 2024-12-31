const routes = [
  // 預設Layout
  {
    path: '/default',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },

  // 自定義 Layout
  {
    path: '/',
    component: () => import('layouts/customLayout1.vue'),
    children: [
      { path: '', component: () => import('pages/SendJobPage.vue') },
      /* ... 新增子路由...
      { path: 'other_page', component: () => import('pages/其他Page.vue') },
      */
    ]
  },

  // ... 新增 Layout ...
  /*
  {
    path: '/new_route',
    component: () => import('layouts/新增Layout.vue'),
    children: [
      { path: '', component: () => import('pages/新增Page.vue') },        // 網址: /new_route
      { path: 'page1', component: () => import('pages/新增Page1.vue') },  // 網址: /new_route/page1
      { path: 'page2', component: () => import('pages/新增Page2.vue') },  // 網址: /new_route/page2
    ]
  },
  */

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
