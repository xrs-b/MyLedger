<template>
  <div class="category-selector">
    <!-- 类型选择 -->
    <van-tabs v-model:active="activeType" @change="onTypeChange">
      <van-tab name="expense" title="支出" />
      <van-tab name="income" title="收入" />
    </van-tabs>

    <!-- 一级分类选择 -->
    <van-tabs v-model:active="activeCategory" @change="onCategoryChange" class="sub-tabs">
      <van-tab 
        v-for="category in categories" 
        :key="category.id" 
        :title="category.name"
        :name="category.id"
      />
    </van-tabs>

    <!-- 二级分类选择 -->
    <div class="category-items">
      <div 
        v-for="item in currentItems" 
        :key="item.id"
        class="category-item"
        :class="{ active: selectedItem?.id === item.id }"
        @click="selectItem(item)"
      >
        <span class="item-name">{{ item.name }}</span>
      </div>
    </div>

    <!-- 确认按钮 -->
    <div class="confirm-bar" v-if="showConfirm">
      <span>已选择: {{ selectedItem?.name }}</span>
      <van-button type="primary" size="small" @click="confirm">
        确定
      </van-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useCategoryStore } from '@/stores/category'
import { storeToRefs } from 'pinia'

const props = defineProps({
  modelValue: {
    type: Object,
    default: null
  },
  showConfirm: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const categoryStore = useCategoryStore()
const { categories } = storeToRefs(categoryStore)

const activeType = ref('expense')  // 当前类型: expense/income
const activeCategory = ref(null)   // 当前一级分类ID
const selectedItem = ref(null)     // 选中的二级分类

// 根据类型获取分类列表
const categoriesByType = computed(() => {
  return categories.value[activeType.value] || []
})

// 当前一级分类的二级分类列表
const currentItems = computed(() => {
  if (!activeCategory.value) return []
  const category = categoriesByType.value.find(c => c.id === activeCategory.value)
  return category?.items || []
})

// 初始化
onMounted(async () => {
  await categoryStore.fetchCategories()
  
  // 默认选中第一个分类
  if (categoriesByType.value.length > 0) {
    activeCategory.value = categoriesByType.value[0].id
  }
})

// 类型变化时，重置选中
const onTypeChange = () => {
  activeCategory.value = null
  selectedItem.value = null
  
  // 默认选中第一个分类
  if (categoriesByType.value.length > 0) {
    activeCategory.value = categoriesByType.value[0].id
  }
  
  emit('update:modelValue', null)
}

// 一级分类变化时，重置二级分类选中
const onCategoryChange = () => {
  selectedItem.value = null
  emit('update:modelValue', null)
}

// 选择二级分类
const selectItem = (item) => {
  selectedItem.value = item
  emit('update:modelValue', item)
}

// 确认选择
const confirm = () => {
  if (selectedItem.value) {
    emit('confirm', {
      type: activeType.value,
      categoryId: activeCategory.value,
      item: selectedItem.value
    })
  }
}

// 监听外部 v-model 变化
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    selectedItem.value = newVal
  }
}, { immediate: true })
</script>

<style scoped>
.category-selector {
  background-color: #fff;
}

.sub-tabs {
  margin-top: 8px;
  background-color: #f7f8fa;
}

.category-items {
  display: flex;
  flex-wrap: wrap;
  padding: 12px;
  gap: 8px;
}

.category-item {
  padding: 8px 16px;
  background-color: #f7f8fa;
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.category-item:active {
  background-color: #e8e8e8;
}

.category-item.active {
  background-color: #1989fa;
  color: #fff;
}

.confirm-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-top: 1px solid #ebedf0;
  background-color: #fff;
  position: sticky;
  bottom: 0;
}

.confirm-bar span {
  font-size: 14px;
  color: #323233;
}
</style>
