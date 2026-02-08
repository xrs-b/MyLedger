/**
 * 项目状态管理
 */

import { defineStore } from 'pinia'
import projectApi from '@/api/project'

export const useProjectStore = defineStore('project', {
  // ============ 状态 ============
  state: () => ({
    projects: [],
    currentProject: null,
    loading: false,
    error: null
  }),

  // ============ Getter ============
  getters: {
    // 进行中的项目
    ongoingProjects: (state) => state.projects.filter(p => p.status === 'ongoing'),
    
    // 已完成的项目
    completedProjects: (state) => state.projects.filter(p => p.status === 'completed'),
    
    // 全部项目
    allProjects: (state) => state.projects
  },

  // ============ 动作 ============
  actions: {
    /**
     * 获取项目列表
     */
    async fetchProjects(status = null) {
      this.loading = true
      this.error = null
      
      try {
        const params = status ? { status } : {}
        const response = await projectApi.getList(params)
        this.projects = response.data.projects
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || '获取项目列表失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 获取项目详情
     * @param {number} id - 项目ID
     */
    async fetchProject(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await projectApi.getById(id)
        this.currentProject = response.data
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || '获取项目详情失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 创建项目
     * @param {Object} data - 项目数据
     */
    async create(data) {
      this.loading = true
      
      try {
        await projectApi.create(data)
        await this.fetchProjects()
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || '创建失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 更新项目
     * @param {number} id - 项目ID
     * @param {Object} data - 更新数据
     */
    async update(id, data) {
      this.loading = true
      
      try {
        await projectApi.update(id, data)
        await this.fetchProjects()
        if (this.currentProject?.id === id) {
          await this.fetchProject(id)
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || '更新失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 删除项目
     * @param {number} id - 项目ID
     */
    async delete(id) {
      this.loading = true
      
      try {
        await projectApi.delete(id)
        this.projects = this.projects.filter(p => p.id !== id)
        if (this.currentProject?.id === id) {
          this.currentProject = null
        }
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || '删除失败'
        return { success: false, message: this.error }
      } finally {
        this.loading = false
      }
    },

    /**
     * 完成项目
     * @param {number} id - 项目ID
     */
    async complete(id) {
      try {
        await projectApi.complete(id)
        await this.fetchProjects()
        if (this.currentProject?.id === id) {
          await this.fetchProject(id)
        }
        return { success: true }
      } catch (error) {
        return { success: false, message: error.response?.data?.detail }
      }
    },

    /**
     * 重新打开项目
     * @param {number} id - 项目ID
     */
    async reopen(id) {
      try {
        await projectApi.reopen(id)
        await this.fetchProjects()
        if (this.currentProject?.id === id) {
          await this.fetchProject(id)
        }
        return { success: true }
      } catch (error) {
        return { success: false, message: error.response?.data?.detail }
      }
    },

    /**
     * 清除当前项目
     */
    clearCurrent() {
      this.currentProject = null
    },

    /**
     * 清除错误
     */
    clearError() {
      this.error = null
    }
  }
})
