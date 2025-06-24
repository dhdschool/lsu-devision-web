import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/account',
      name: 'account',
      component: () => import('../views/AccountPage.vue'),
    },
    {
      path: '/base',
      name: 'base',
      component: () => import('../views/BasePage.vue'),
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactPage.vue'),
    },
    {
      path: '/createAccount',
      name: 'createAccount',
      component: () => import('../views/CreateAccountPage.vue'),
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('../views/HelpPage.vue'),
    },
    {
      path: '/home',
      name: 'homePage',
      component: () => import('../views/HomePage.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginPage.vue'),
    },
    {
      path: '/predictions',
      name: 'predictions',
      component: () => import('../views/PredictionPage.vue'),
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('../views/SettingsPage.vue'),
    }
  ],
})

export default router
