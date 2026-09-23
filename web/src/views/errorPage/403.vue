<template>
  <div class="permission-container">
    <div class="permission-card">
      <!-- 禁止图标区域 -->
      <div class="permission-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,20a9,9,0,1,1,9-9A9,9,0,0,1,12,21Z" fill="#ff4d4f"/>
          <path d="M17,7.05,7.05,17a1,1,0,0,0,0,1.41,1,1,0,0,0,1.41,0L17,8.46a1,1,0,0,0,0-1.41A1,1,0,0,0,17,7.05Z" fill="#ff4d4f"/>
          <path d="M17,16.95,7.05,7A1,1,0,0,0,5.64,8.46L15.54,18.36a1,1,0,0,0,1.41,0A1,1,0,0,0,17,16.95Z" fill="#ff4d4f"/>
        </svg>
      </div>

      <!-- 错误信息区域 -->
      <div class="error-content">
        <h1 class="error-title">403 禁止访问</h1>
        <p class="error-message">{{ message }}</p>
        <p class="error-detail">您的账号权限不足或访问请求被拒绝，如有需要请联系管理员</p>

        <!-- 分隔线 -->
        <div class="divider"></div>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <router-link to="/dashboard" class="home-btn">
            返回首页
          </router-link>

        </div>

      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Page403',
  computed: {
    message() {
      return '抱歉，您无权访问此页面'
    }
  },
  methods: {

  },
  mounted() {
    // 添加入场动画效果
    const elements = document.querySelectorAll('.permission-icon, .error-title, .error-message, .error-detail, .action-buttons, .admin-hint');
    elements.forEach((el, index) => {
      setTimeout(() => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, 100 + index * 150);
    });
  }
}
</script>

<style lang="scss" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.permission-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #2c3e50 0%, #1a1a2e 100%);
  padding: 20px;
  font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.permission-card {
  width: 100%;
  max-width: 500px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: card-enter 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
}

.permission-icon {
  background: linear-gradient(to right, #ff4d4f, #d9363e);
  padding: 45px 0;
  display: flex;
  justify-content: center;
  align-items: center;

  svg {
    width: 90px;
    height: 90px;
    opacity: 0;
    transform: scale(0.8);
    animation: icon-pulse 1.8s ease-out 0.5s forwards;
    filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2));
  }
}

.error-content {
  padding: 35px 40px;
  text-align: center;
}

.error-title {
  font-size: 32px;
  font-weight: 800;
  color: #333;
  margin-bottom: 15px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;
}

.error-message {
  font-size: 20px;
  line-height: 1.6;
  color: #ff4d4f;
  margin-bottom: 12px;
  font-weight: 600;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;
}

.error-detail {
  font-size: 16px;
  color: #666;
  line-height: 1.7;
  max-width: 380px;
  margin: 0 auto 25px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;
}

.divider {
  height: 1px;
  background: linear-gradient(to right, transparent, #eee, transparent);
  margin: 28px 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 25px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;
}

.home-btn {
  padding: 12px 36px;
  background: linear-gradient(to right, #1677ff, #0958d9);
  color: white !important;
  text-decoration: none;
  font-weight: 600;
  border-radius: 50px;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(22, 119, 255, 0.25);
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  display: inline-block;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(22, 119, 255, 0.35);
  }
}

.contact-btn {
  padding: 12px 32px;
  background: white;
  color: #1677ff !important;
  text-decoration: none;
  font-weight: 600;
  border-radius: 50px;
  font-size: 16px;
  border: 1px solid #1677ff;
  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    background: #e6f4ff;
  }
}

.admin-hint {
  font-size: 14px;
  color: #1677ff;
  background: #e6f4ff;
  padding: 12px 16px;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;

  svg {
    flex-shrink: 0;
  }
}

/* 动画效果 */
@keyframes card-enter {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes icon-pulse {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  80% {
    transform: scale(0.98);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* 响应式设计 */
@media (max-width: 600px) {
  .permission-card {
    max-width: 95%;
  }

  .permission-icon svg {
    width: 70px;
    height: 70px;
  }

  .error-content {
    padding: 30px 20px;
  }

  .error-title {
    font-size: 28px;
  }

  .error-message {
    font-size: 18px;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .home-btn, .contact-btn {
    width: 100%;
    max-width: 260px;
  }
}

@media (max-width: 400px) {
  .admin-hint {
    font-size: 13px;
  }
}
</style>
