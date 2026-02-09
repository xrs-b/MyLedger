/**
 * 项目状态管理
 */

import { defineStore } from 'pinia'
import projectApi from '@/api/project'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    currentProject: null,
    loading: false,
    error: null
  }),

  getters: {
    ongoingProjects: (state) => state.projects.filter(p => p.status === 'ongoing'),
    completedProjects: (state) => state.projects.filter(p => p.status === 'completed')
  },

  actions: {
    async fetchProjects(status = null) {
      this.loading = true
      this.error = null
      
      try {
        const response = await projectApi.getList(status)
        this.projects = response.data?.projects || []
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取项目列表失败'
        console.error('获取项目列表错误:', error)
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchProject(id) {
      this.loading = true
      
      try {
        const response = await projectApi.getById(id)
        this.currentProject = response.data
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.data?.detail || '获取项目详情失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async create(data) {
      this.loading = true
      
      try {
        await projectApi.create(data)
        await this.fetchProjects()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '创建失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async update(id, data) {
      this.loading = true
      
      try {
        await projectApi.update(id, data)
        await this.fetchProjects()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '更新失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    async delete(id) {
      this.loading = true
      
      try {
        await projectApi.delete(id)
        await this.fetchProjects()
        return { success: true }
      } catch (error) {
        this.error = error.data?.detail || '删除失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})
